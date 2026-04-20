"""Parser für Fortinet FortiGate webfilter.log (FortiOS 7.x key=value).

Issue #29 (E3-4). FortiGate loggt UTM-Web-Events im ``type=utm, subtype=webfilter``
Format als Space-separated key=value-Paare. Werte mit Leerzeichen sind
in ``"..."`` gequotet. Optional Syslog-Prefix (``<190>…``) vor dem key-value-Body.

Mapping auf unser Common-Schema:
- ``date`` + ``time``                 → ``timestamp`` (tz-naive UTC)
- ``srcip``                           → ``client`` (pseudonymisiert, ``ip_*``)
- ``user``                            → ``user`` (pseudonymisiert, ``user_*``)
- ``hostname``                        → ``domain`` (lowercase, ohne trailing ``.``)
- ``url``                             → ``url_path`` (auf erstes Segment reduziert, DSGVO)
- ``action``                          → ``action`` (``blocked``/``passthrough``/``monitor``)
- ``catdesc``                         → ``urlcategory``
- ``sentbyte`` / ``rcvdbyte``         → ``bytes_uploaded`` / ``bytes_downloaded``
- ``method``                          → ``method`` (FortiGate-spezifisch: domain/get/post/connect)
- ``service``                         → ``app`` (HTTP/HTTPS/FTP/...)

**Filter:** nur ``subtype=webfilter``-Zeilen werden geparst. Andere UTM-Subtypes
(ips, virus, appctrl, ...) werden übersprungen.

DSGVO Art. 25: ``srcip`` und ``user`` werden pseudonymisiert. ``url`` wird auf
das erste Pfad-Segment reduziert (konsistent mit zscaler/paloalto).

Referenz: https://docs.fortinet.com/document/fortigate/7.4.2/fortios-log-message-reference
"""

import re
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.parsers.base import BaseParser
from src.privacy.pseudonymizer import Pseudonymizer

# Matcht key=value mit optional gequoteten Werten.
# Gruppen: 1=key, 2=quoted_value, 3=bare_value (genau eine nicht-leer).
_KV_PATTERN = re.compile(r'(\w+)=(?:"([^"]*)"|(\S+))')

# Syslog-Prefix <PRI>... bis zum ersten "date=..." Schlüssel.
_SYSLOG_PREFIX = re.compile(r"^<\d+>.*?(?=date=)")

_TIMESTAMP_FMT = "%Y-%m-%d %H:%M:%S"

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


def _strip_syslog_prefix(line: str) -> str:
    return _SYSLOG_PREFIX.sub("", line)


def _parse_kv(line: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for match in _KV_PATTERN.finditer(line):
        key, quoted, bare = match.group(1), match.group(2), match.group(3)
        result[key] = quoted if quoted is not None else bare
    return result


def _truncate_path(path: str | None) -> str | None:
    if not path or path == "/":
        return path or None
    segments = path.lstrip("/").split("/", 1)
    first = segments[0]
    return f"/{first}" if first else "/"


def _parse_int(value: str | None) -> int | None:
    if not value or value == "-":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def parse_fortinet_log(
    source: Path | str,
    pseudonymizer: Pseudonymizer | None = None,
) -> pd.DataFrame:
    """Parst Fortinet FortiGate webfilter.log (key=value-Format) in ein DataFrame.

    Args:
        source: Pfad zur Log-Datei. Kann Syslog-Header enthalten.
        pseudonymizer: Pseudonymizer für ``srcip`` und ``user``. Wenn None, wird
            ein neuer erzeugt.

    Returns:
        DataFrame mit ``_COLUMNS``. Leere Datei oder nur nicht-webfilter-Zeilen
        ergeben ein leeres DF (mit korrekten dtypes).
    """
    if pseudonymizer is None:
        pseudonymizer = Pseudonymizer()

    source = Path(source)
    records: list[dict] = []

    with open(source, encoding="utf-8", errors="replace") as f:
        for raw_line in f:
            line = _strip_syslog_prefix(raw_line.rstrip("\n")).strip()
            if not line or line.startswith("#"):
                continue
            kv = _parse_kv(line)
            record = _build_record(kv, source.name, pseudonymizer)
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


def _build_record(
    kv: dict[str, str],
    source_name: str,
    pseudonymizer: Pseudonymizer,
) -> dict | None:
    # Subtype-Filter
    if kv.get("subtype") != "webfilter":
        return None

    date = kv.get("date")
    time = kv.get("time")
    if not date or not time:
        return None
    try:
        ts = datetime.strptime(f"{date} {time}", _TIMESTAMP_FMT)
    except ValueError:
        return None

    srcip = kv.get("srcip")
    if not srcip:
        return None

    hostname = kv.get("hostname", "").strip()
    if not hostname:
        return None
    domain = hostname.lower().rstrip(".")
    if not domain:
        return None

    user_raw = kv.get("user", "").strip()
    user = pseudonymizer.pseudonymize_user(user_raw) if user_raw else None

    return {
        "timestamp": ts,
        "client": pseudonymizer.pseudonymize_ip(srcip),
        "domain": domain,
        "source_file": source_name,
        "source_type": "fortinet",
        "user": user,
        "action": kv.get("action") or None,
        "method": kv.get("method") or None,
        "url_path": _truncate_path(kv.get("url")),
        "status_code": None,  # webfilter.log enthält keinen HTTP-Status
        "bytes_uploaded": _parse_int(kv.get("sentbyte")),
        "bytes_downloaded": _parse_int(kv.get("rcvdbyte")),
        "urlcategory": kv.get("catdesc") or None,
        "useragent": None,  # webfilter.log führt User-Agent nicht
        "app": kv.get("service") or None,
    }


class FortiGateWebfilterParser(BaseParser):
    """BaseParser-konformer Wrapper für FortiGate webfilter.log."""

    OPTIONAL_COLUMNS = {
        "source_file", "source_type",
        "user", "action", "method", "url_path", "status_code",
        "bytes_uploaded", "bytes_downloaded",
        "urlcategory", "useragent", "app",
    }

    def parse(self, path: str | Path) -> pd.DataFrame:
        df = parse_fortinet_log(path, self.pseudonymizer)
        return self._finalize(df)
