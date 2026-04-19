"""Parser für Zscaler Internet Access (ZIA) Web Proxy Logs via NSS.

Issue #26 (E3-1). Zscaler NSS (Nanolog Streaming Service) exportiert
Web-Proxy-Events in konfigurierbaren Feed-Formaten. Dieser Parser unterstützt
das tab-separierte LEEF-ähnliche Standard-Format mit folgender Default-
Feldreihenfolge (siehe `DEFAULT_FIELDS`):

    datetime \\t user \\t clientIP \\t url \\t action \\t urlcategory \\t app
    \\t respcode \\t reqsize \\t respsize \\t method \\t useragent

Timestamp-Format: ``%d-%b-%Y %H:%M:%S`` (z.B. ``23-Jun-2022 16:24:59``), UTC.
Leere Felder sind als ``-`` oder Leerstring zulässig.

Referenz: https://help.zscaler.com/zia/nss-feed-output-format-web-logs

DSGVO-Hinweis (Art. 25 Data Minimization): `url_path` wird bewusst auf das
**erste Path-Segment** reduziert (z.B. ``/g/g-abc/titel`` → ``/g``). Volle
Pfade können personenbezogene Inhalte tragen (Chat-Titel, Workspace-Namen,
User-spezifische Konfigurations-URLs). Query-Strings werden komplett
verworfen (``urlparse(...).path`` ignoriert ``?key=value``).
"""

from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd

from src.parsers.base import BaseParser
from src.privacy.pseudonymizer import Pseudonymizer

DEFAULT_FIELDS: tuple[str, ...] = (
    "datetime",
    "user",
    "clientIP",
    "url",
    "action",
    "urlcategory",
    "app",
    "respcode",
    "reqsize",
    "respsize",
    "method",
    "useragent",
)

_TIMESTAMP_FMT = "%d-%b-%Y %H:%M:%S"

_COLUMNS = [
    "timestamp", "client", "domain", "source_file", "source_type",
    "user", "action", "method", "url_path", "status_code",
    "bytes_uploaded", "bytes_downloaded", "urlcategory", "useragent", "app",
]


def _empty_df() -> pd.DataFrame:
    df = pd.DataFrame(columns=_COLUMNS)
    return df.astype({
        "bytes_uploaded": "Int64",
        "bytes_downloaded": "Int64",
        "status_code": "Int16",
    })


def _parse_int(value: str) -> int | None:
    value = (value or "").strip()
    if not value or value == "-":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _truncate_path(path: str | None) -> str | None:
    """Reduziert Path auf erstes Segment (DSGVO Art. 25).

    Beispiele:
        ``/g/g-abc/titel`` → ``/g``
        ``/`` → ``/``
        ``/api`` → ``/api``
        ``""`` / None → None
    """
    if not path or path == "/":
        return path or None
    segments = path.lstrip("/").split("/", 1)
    first = segments[0]
    if not first:
        return "/"
    return f"/{first}"


def _extract_domain_and_path(url: str) -> tuple[str | None, str | None]:
    url = (url or "").strip()
    if not url or url == "-":
        return None, None
    if "://" not in url:
        host = url.split("/", 1)[0].split(":")[0]
        return (host.lower().rstrip(".") or None), None
    parsed = urlparse(url)
    if not parsed.hostname:
        return None, _truncate_path(parsed.path)
    return parsed.hostname.lower().rstrip("."), _truncate_path(parsed.path)


def parse_zscaler_log(
    source: Path | str,
    pseudonymizer: Pseudonymizer | None = None,
    fields: tuple[str, ...] = DEFAULT_FIELDS,
) -> pd.DataFrame:
    """Parst Zscaler ZIA Web Proxy Logs (NSS tab-separated) in ein DataFrame.

    Args:
        source: Pfad zur NSS-Export-Datei.
        pseudonymizer: Pseudonymizer für ``clientIP`` und ``user``.
            Wenn None, wird einer erzeugt.
        fields: Feldreihenfolge im NSS-Feed. Default entspricht dem
            dokumentierten Zscaler Web-Logs-Standard.

    Returns:
        DataFrame mit den Spalten aus ``_COLUMNS``. Leere Datei oder nur
        unparsebare Zeilen ergeben ein leeres DataFrame (mit korrekten dtypes).
    """
    if pseudonymizer is None:
        pseudonymizer = Pseudonymizer()

    required_fields = {"datetime", "clientIP", "url"}
    missing_fields = required_fields - set(fields)
    if missing_fields:
        raise ValueError(
            f"Zscaler NSS-Feed benötigt mindestens {sorted(required_fields)}, "
            f"fehlen: {sorted(missing_fields)}"
        )

    source = Path(source)
    records: list[dict] = []

    idx = {name: i for i, name in enumerate(fields)}
    n_fields = len(fields)

    with open(source, encoding="utf-8", errors="replace") as f:
        for raw_line in f:
            line = raw_line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < n_fields:
                continue

            ts_raw = parts[idx["datetime"]].strip()
            try:
                ts = datetime.strptime(ts_raw, _TIMESTAMP_FMT)
            except ValueError:
                continue

            client_ip = parts[idx["clientIP"]].strip()
            if not client_ip or client_ip == "-":
                continue
            domain, path = _extract_domain_and_path(parts[idx["url"]])
            if not domain:
                continue

            user_raw = parts[idx["user"]].strip()
            user = (
                pseudonymizer.pseudonymize_user(user_raw)
                if user_raw and user_raw != "-"
                else None
            )

            records.append({
                "timestamp": ts,
                "client": pseudonymizer.pseudonymize_ip(client_ip),
                "domain": domain,
                "source_file": source.name,
                "source_type": "zscaler",
                "user": user,
                "action": (parts[idx["action"]].strip() or None) if "action" in idx else None,
                "method": (parts[idx["method"]].strip() or None) if "method" in idx else None,
                "url_path": path,
                "status_code": _parse_int(parts[idx["respcode"]]) if "respcode" in idx else None,
                "bytes_uploaded": _parse_int(parts[idx["reqsize"]]) if "reqsize" in idx else None,
                "bytes_downloaded": _parse_int(parts[idx["respsize"]]) if "respsize" in idx else None,
                "urlcategory": (parts[idx["urlcategory"]].strip() or None) if "urlcategory" in idx else None,
                "useragent": (parts[idx["useragent"]].strip() or None) if "useragent" in idx else None,
                "app": (parts[idx["app"]].strip() or None) if "app" in idx else None,
            })

    if not records:
        return _empty_df()

    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bytes_uploaded"] = df["bytes_uploaded"].astype("Int64")
    df["bytes_downloaded"] = df["bytes_downloaded"].astype("Int64")
    df["status_code"] = df["status_code"].astype("Int16")
    return df[_COLUMNS]


class ZscalerParser(BaseParser):
    """BaseParser-konformer Wrapper um ``parse_zscaler_log``."""

    OPTIONAL_COLUMNS = {
        "source_file", "source_type",
        "user", "action", "method", "url_path", "status_code",
        "bytes_uploaded", "bytes_downloaded",
        "urlcategory", "useragent", "app",
    }

    def parse(
        self,
        path: str | Path,
        fields: tuple[str, ...] = DEFAULT_FIELDS,
    ) -> pd.DataFrame:
        df = parse_zscaler_log(path, self.pseudonymizer, fields=fields)
        return self._finalize(df)
