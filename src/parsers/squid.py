"""Parser für Squid Proxy Access Logs → pandas DataFrame.

Unterstützte Formate:
1. Squid Native Log (default `/var/log/squid/access.log`):
   1709971200.123 234 192.168.1.42 TCP_MISS/200 1547 POST https://api.openai.com/v1/chat - HIER_DIRECT/1.2.3.4 application/json

   Felder (whitespace-separated):
     time elapsed remotehost code/status bytes method url rfc931 peerstatus/peerhost type

2. Common Log Format mit URL statt Pfad:
   192.168.1.42 - - [09/Mar/2024:08:15:32 +0000] "POST https://api.openai.com/v1/chat HTTP/1.1" 200 1547

Volumen-Detection: für Upload-Tracking muss Squid mit erweitertem `logformat` laufen,
das `%>st` (read from client = upload bytes) anstelle der Default-Reply-Size enthält.
Beispiel-Konfiguration siehe `config/squid_logformat.conf`.
"""

import re
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd

from src.parsers.base import BaseParser
from src.privacy.pseudonymizer import Pseudonymizer

# Squid native: 10 whitespace-separated felder, time ist epoch.ms
_NATIVE_PATTERN = re.compile(
    r"^(?P<time>\d+\.\d+)\s+"
    r"(?P<elapsed>\d+)\s+"
    r"(?P<client>\S+)\s+"
    r"(?P<code_status>\S+)\s+"
    r"(?P<bytes>\d+)\s+"
    r"(?P<method>\S+)\s+"
    r"(?P<url>\S+)\s+"
    r"(?P<rfc931>\S+)\s+"
    r"(?P<peer>\S+)\s+"
    r"(?P<content_type>\S+)"
)

# Common log: client - - [date] "METHOD URL HTTP/x.y" status bytes
_COMMON_PATTERN = re.compile(
    r'^(?P<client>\S+)\s+\S+\s+\S+\s+'
    r'\[(?P<date>[^\]]+)\]\s+'
    r'"(?P<method>\S+)\s+(?P<url>\S+)\s+HTTP/[\d.]+"\s+'
    r'(?P<status>\d+)\s+(?P<bytes>\d+|-)'
)

_COMMON_DATE_FMT = "%d/%b/%Y:%H:%M:%S %z"

_COLUMNS = [
    "timestamp", "client", "domain", "source_file", "source_type",
    "query_type", "bytes_uploaded", "bytes_downloaded",
    "method", "url_path", "status_code",
]


def _empty_df() -> pd.DataFrame:
    df = pd.DataFrame(columns=_COLUMNS)
    df = df.astype({
        "bytes_uploaded": "Int64",
        "bytes_downloaded": "Int64",
        "status_code": "Int16",
    })
    return df


def _extract_domain(url: str) -> str | None:
    if "://" not in url:
        # Squid CONNECT method liefert "host:port" statt URL
        host = url.split(":")[0] if ":" in url else url
        return host.lower().rstrip(".") or None
    parsed = urlparse(url)
    if not parsed.hostname:
        return None
    return parsed.hostname.lower().rstrip(".")


def _extract_path(url: str) -> str | None:
    if "://" not in url:
        return None
    parsed = urlparse(url)
    return parsed.path or None


def _detect_format(first_line: str) -> str:
    """Heuristik: native beginnt mit Epoch-Float, common mit IP."""
    stripped = first_line.strip()
    if not stripped:
        return "native"
    head = stripped.split(maxsplit=1)[0]
    if "." in head:
        before, after = head.split(".", 1)
        if before.isdigit() and after.isdigit():
            return "native"
    return "common"


def parse_squid_log(
    source: Path | str,
    pseudonymizer: Pseudonymizer | None = None,
    format: str = "auto",
) -> pd.DataFrame:
    """Parst ein Squid Access Log und gibt ein DataFrame zurück.

    Args:
        source: Pfad zur Log-Datei
        pseudonymizer: Pseudonymizer-Instanz für DSGVO-konforme IP-Maskierung.
                       Wenn None, wird automatisch einer erzeugt.
        format: "native", "common" oder "auto" (Default: Heuristik anhand erster Zeile)

    Returns:
        DataFrame mit Spalten:
          timestamp, client, domain, source_file, source_type,
          query_type, bytes_uploaded (Int64), bytes_downloaded (Int64),
          method, url_path, status_code (Int16)
    """
    if pseudonymizer is None:
        pseudonymizer = Pseudonymizer()

    source = Path(source)
    records: list[dict] = []

    with open(source, encoding="utf-8", errors="replace") as f:
        first_line = f.readline()
        if not first_line:
            return _empty_df()

        active_format = format
        if active_format == "auto":
            active_format = _detect_format(first_line)

        all_lines = [first_line] + f.readlines()

    for line in all_lines:
        record = _parse_line(line.strip(), active_format, source.name, pseudonymizer)
        if record is not None:
            records.append(record)

    if not records:
        return _empty_df()

    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bytes_uploaded"] = df["bytes_uploaded"].astype("Int64")
    df["bytes_downloaded"] = df["bytes_downloaded"].astype("Int64")
    df["status_code"] = df["status_code"].astype("Int16")
    return df[_COLUMNS]


def _parse_line(
    line: str,
    fmt: str,
    source_name: str,
    pseudonymizer: Pseudonymizer,
) -> dict | None:
    if not line:
        return None

    if fmt == "native":
        m = _NATIVE_PATTERN.match(line)
        if not m:
            return None
        ts = datetime.fromtimestamp(float(m.group("time")), tz=UTC).replace(tzinfo=None)
        url = m.group("url")
        domain = _extract_domain(url)
        if not domain:
            return None
        code_status = m.group("code_status")
        status_part = code_status.split("/")[-1] if "/" in code_status else code_status
        try:
            status_code = int(status_part)
        except ValueError:
            status_code = None
        return {
            "timestamp": ts,
            "client": pseudonymizer.pseudonymize_ip(m.group("client")),
            "domain": domain,
            "source_file": source_name,
            "source_type": "squid",
            "query_type": None,
            "bytes_uploaded": int(m.group("bytes")),
            "bytes_downloaded": None,
            "method": m.group("method"),
            "url_path": _extract_path(url),
            "status_code": status_code,
        }

    if fmt == "common":
        m = _COMMON_PATTERN.match(line)
        if not m:
            return None
        try:
            ts = datetime.strptime(m.group("date"), _COMMON_DATE_FMT)
            ts = ts.astimezone(UTC).replace(tzinfo=None)
        except ValueError:
            return None
        url = m.group("url")
        domain = _extract_domain(url)
        if not domain:
            return None
        bytes_str = m.group("bytes")
        bytes_val = int(bytes_str) if bytes_str.isdigit() else None
        return {
            "timestamp": ts,
            "client": pseudonymizer.pseudonymize_ip(m.group("client")),
            "domain": domain,
            "source_file": source_name,
            "source_type": "squid",
            "query_type": None,
            "bytes_uploaded": bytes_val,
            "bytes_downloaded": None,
            "method": m.group("method"),
            "url_path": _extract_path(url),
            "status_code": int(m.group("status")),
        }

    return None


class SquidParser(BaseParser):
    """BaseParser-konformer Wrapper um `parse_squid_log`."""

    OPTIONAL_COLUMNS = {
        "bytes_uploaded",
        "bytes_downloaded",
        "method",
        "status_code",
        "url_path",
        "query_type",
        "source_file",
        "source_type",
    }

    def parse(self, path: str | Path, format: str = "auto") -> pd.DataFrame:
        df = parse_squid_log(path, self.pseudonymizer, format=format)
        return self._finalize(df)
