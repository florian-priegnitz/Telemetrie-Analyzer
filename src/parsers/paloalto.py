"""Parser für Palo Alto PAN-OS URL-Filtering Logs (Syslog-CSV).

Issue #27 (E3-2). PAN-OS URL-Filtering-Logs sind THREAT-Logs mit Subtype ``url``
und werden typischerweise via Syslog als CSV exportiert (PAN-OS 10.x / 11.x).
Dieser Parser liest das CSV-Body-Format mit folgenden Pflicht-Positionen
(0-indexiert nach optional entferntem Syslog-Prefix):

    Pos  0  version              (immer "1")
    Pos  3  type                 (nur "THREAT"-Zeilen werden gelesen)
    Pos  4  subtype              (nur "url" wird geparst)
    Pos  6  generated_time       → timestamp       ("YYYY/MM/DD HH:MM:SS")
    Pos  7  source_ip            → client          (pseudonymisiert)
    Pos 12  source_user          → user            (pseudonymisiert)
    Pos 14  application          → app
    Pos 30  action               → action          (alert/allow/block-url/...)
    Pos 31  url                  → domain + url_path
    Pos 33  url_category         → urlcategory
    Pos 44  user_agent           → useragent

Positions sind via ``DEFAULT_FIELDS`` konfigurierbar — Enterprise-Admins können
abweichende Layouts durch Override anpassen (siehe ``PanOSUrlParser(..., fields=...)``).

DSGVO-Hinweis (Art. 25): ``url_path`` wird auf erstes Segment reduziert
(konsistent mit ``zscaler.py``), um Chat-Titel/Workspace-Leaks zu vermeiden.

Syslog-Prefix (z.B. ``<14>Jun 23 10:00:00 PA-FW-01 ``) wird vor dem CSV-
Parsing erkannt und entfernt.

Referenz:
https://docs.paloaltonetworks.com/pan-os/10-2/pan-os-admin/monitoring/use-syslog-for-monitoring/syslog-field-descriptions/url-filtering-log-fields
"""

import csv
import io
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd

from src.parsers.base import BaseParser, coerce_timestamp_ns
from src.privacy.pseudonymizer import Pseudonymizer

DEFAULT_FIELDS: dict[str, int] = {
    "version": 0,
    "type": 3,
    "subtype": 4,
    "generated_time": 6,
    "src_ip": 7,
    "src_user": 12,
    "application": 14,
    "action": 30,
    "url": 31,
    "url_category": 33,
    "useragent": 44,
}

_TIMESTAMP_FMT = "%Y/%m/%d %H:%M:%S"

_COLUMNS = [
    "timestamp", "client", "domain", "source_file", "source_type",
    "user", "action", "method", "url_path", "status_code",
    "bytes_uploaded", "bytes_downloaded", "urlcategory", "useragent", "app",
]

# Matches optional "<PRI>Hostname MMM DD HH:MM:SS Hostname " before CSV body.
# CSV body starts with digit(s) + comma (the version field).
_SYSLOG_PREFIX = re.compile(r"^<\d+>.*?(?=\d+,\d{4}/\d{2}/\d{2} )", re.DOTALL)


def _strip_syslog_prefix(line: str) -> str:
    return _SYSLOG_PREFIX.sub("", line)


def _truncate_path(path: str | None) -> str | None:
    if not path or path == "/":
        return path or None
    segments = path.lstrip("/").split("/", 1)
    first = segments[0]
    return f"/{first}" if first else "/"


def _extract_domain_and_path(url: str) -> tuple[str | None, str | None]:
    url = (url or "").strip()
    if not url or url == "-":
        return None, None
    if "://" not in url:
        # PAN-OS log URL field ist oft host+path ohne scheme
        head, _, tail = url.partition("/")
        host = head.split(":")[0]
        path = f"/{tail}" if tail else None
        return (host.lower().rstrip(".") or None), _truncate_path(path)
    parsed = urlparse(url)
    if not parsed.hostname:
        return None, _truncate_path(parsed.path)
    return parsed.hostname.lower().rstrip("."), _truncate_path(parsed.path)


def parse_paloalto_log(
    source: Path | str,
    pseudonymizer: Pseudonymizer | None = None,
    fields: dict[str, int] = DEFAULT_FIELDS,
) -> pd.DataFrame:
    """Parst Palo Alto PAN-OS URL-Filtering-Logs (Syslog-CSV) in ein DataFrame.

    Args:
        source: Pfad zur Log-Datei. Darf Syslog-Header enthalten
            (``<14>Hostname …,1,YYYY/MM/DD HH:MM:SS,…``) oder nur den CSV-Body.
        pseudonymizer: Pseudonymizer für ``src_ip`` und ``src_user``.
        fields: Position-Mapping. Muss mindestens ``{"subtype", "generated_time",
            "src_ip", "url"}`` enthalten.

    Returns:
        DataFrame mit den Spalten aus ``_COLUMNS``. Nicht-URL-Subtypen
        (z.B. ``THREAT/virus``) und fehlerhafte Zeilen werden übersprungen.

    Raises:
        ValueError: Wenn ``fields`` Pflicht-Positionen nicht enthält.
    """
    required = {"subtype", "generated_time", "src_ip", "url"}
    missing = required - set(fields)
    if missing:
        raise ValueError(
            f"PAN-OS Parser benötigt mindestens Positionen für {sorted(required)}, "
            f"fehlen: {sorted(missing)}"
        )

    if pseudonymizer is None:
        pseudonymizer = Pseudonymizer()

    source = Path(source)
    records: list[dict] = []

    with open(source, encoding="utf-8", errors="replace") as f:
        raw = f.read()

    for raw_line in raw.splitlines():
        line = _strip_syslog_prefix(raw_line).strip()
        if not line or line.startswith("#"):
            continue

        try:
            parts = next(csv.reader(io.StringIO(line)))
        except (StopIteration, csv.Error):
            continue
        if len(parts) <= max(fields.values()):
            continue

        if parts[fields["subtype"]].strip() != "url":
            continue

        ts_raw = parts[fields["generated_time"]].strip()
        try:
            ts = datetime.strptime(ts_raw, _TIMESTAMP_FMT)
        except ValueError:
            continue

        src_ip = parts[fields["src_ip"]].strip()
        if not src_ip:
            continue
        domain, path = _extract_domain_and_path(parts[fields["url"]])
        if not domain:
            continue

        user_raw = parts[fields["src_user"]].strip() if "src_user" in fields else ""
        user = pseudonymizer.pseudonymize_user(user_raw) if user_raw else None

        def _get(name: str) -> str | None:
            if name not in fields:
                return None
            val = parts[fields[name]].strip()
            return val or None

        records.append({
            "timestamp": ts,
            "client": pseudonymizer.pseudonymize_ip(src_ip),
            "domain": domain,
            "source_file": source.name,
            "source_type": "paloalto",
            "user": user,
            "action": _get("action"),
            "method": None,  # PAN-OS URL-Logs enthalten HTTP-Method nicht zuverlässig
            "url_path": path,
            "status_code": None,
            "bytes_uploaded": None,  # URL-Filter-Logs führen keine Bytes
            "bytes_downloaded": None,
            "urlcategory": _get("url_category"),
            "useragent": _get("useragent"),
            "app": _get("application"),
        })

    if not records:
        df = pd.DataFrame(columns=_COLUMNS)
        return df.astype({
            "bytes_uploaded": "Int64",
            "bytes_downloaded": "Int64",
            "status_code": "Int16",
        })

    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["bytes_uploaded"] = df["bytes_uploaded"].astype("Int64")
    df["bytes_downloaded"] = df["bytes_downloaded"].astype("Int64")
    df["status_code"] = df["status_code"].astype("Int16")
    df = coerce_timestamp_ns(df)
    return df[_COLUMNS]


class PanOSUrlParser(BaseParser):
    """BaseParser-konformer Wrapper für PAN-OS URL-Filtering-Logs."""

    OPTIONAL_COLUMNS = {
        "source_file", "source_type",
        "user", "action", "method", "url_path", "status_code",
        "bytes_uploaded", "bytes_downloaded",
        "urlcategory", "useragent", "app",
    }

    def parse(
        self,
        path: str | Path,
        fields: dict[str, int] = DEFAULT_FIELDS,
    ) -> pd.DataFrame:
        df = parse_paloalto_log(path, self.pseudonymizer, fields=fields)
        return self._finalize(df)
