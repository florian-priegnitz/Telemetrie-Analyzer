"""Parser für Elastic Common Schema (ECS) Events (NDJSON).

Issue #35 (E3-10). ECS ist Elastic's vendor-agnostisches Schema (v8.0+)
und wird von Beats, Logstash, Filebeat-Modulen und jedem modernen
SIEM-Connector produziert. Durch den Fokus auf ECS-Kernfelder erlaubt
dieser Parser, beliebige Quellen (Cloud Audit Logs, Endpoint-Agents,
Proxy-Appliances) zu normalisieren, sofern sie ECS-konform ausgeliefert
werden — unser **universeller Fallback-Parser** für alles, was kein
dedizierter Parser ist.

**Event-Filter:** Der Parser akzeptiert nur Events mit ``event.category``
oder ``event.type`` in der DNS/Network/Web-Domäne:

- ``event.category`` enthält eines von: ``network`` · ``dns`` · ``web``
- **oder** ``dns.question.name`` vorhanden
- **oder** ``url.domain`` vorhanden

Andere ECS-Events (``authentication``, ``process``, ``file``, …) werden
verworfen — sie liefern kein Shadow-AI-Signal.

**Mapping auf Common-Schema (ECS 8.x):**
- ``@timestamp``                                 → ``timestamp``
- ``source.ip`` (fallback ``client.ip``)         → ``client`` (ip_* pseudonym)
- ``dns.question.name`` (fallback ``url.domain``,
  dann ``destination.domain``)                   → ``domain`` (lowercase, no trailing dot)
- ``user.name`` (fallback ``user.email``)        → ``user`` (user_* pseudonym)
- ``http.request.method``                        → ``method``
- ``http.response.status_code``                  → ``status_code``
- ``url.path``                                   → ``url_path`` (DSGVO-Truncation)
- ``http.request.body.bytes`` /
  ``http.response.body.bytes``                   → ``bytes_uploaded`` / ``bytes_downloaded``
- ``user_agent.original``                        → ``useragent``
- ``event.action``                               → ``action``
- ``destination.as.organization.name``           → ``asn_org`` (optional)

DSGVO Art. 25: URL-Pfade werden auf erstes Segment reduziert (Query-String
wird verworfen). ``source.geo.*`` / ``device.*`` werden absichtlich
**nicht** übernommen.

Referenz: https://www.elastic.co/guide/en/ecs/current/ecs-reference.html
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import pandas as pd

from src.parsers.base import BaseParser
from src.privacy.pseudonymizer import Pseudonymizer

_COLUMNS = [
    "timestamp", "client", "domain", "source_file", "source_type",
    "user", "method", "status_code", "url_path",
    "bytes_uploaded", "bytes_downloaded", "useragent", "action", "asn_org",
]

_RELEVANT_CATEGORIES = {"network", "dns", "web"}


def _empty_df() -> pd.DataFrame:
    df = pd.DataFrame(columns=_COLUMNS)
    return df.astype({
        "status_code": "Int32",
        "bytes_uploaded": "Int64",
        "bytes_downloaded": "Int64",
    })


def _get(event: dict, dotted: str, default: Any = None) -> Any:
    """Extrahiert einen Wert via ECS-Dotted-Path (z.B. ``source.ip``).

    Unterstützt sowohl nested Dicts als auch bereits gedottete Top-Level-Keys
    (einige Exporter flatten ECS, andere nicht).
    """
    if dotted in event:
        return event[dotted]
    parts = dotted.split(".")
    cursor: Any = event
    for part in parts:
        if not isinstance(cursor, dict) or part not in cursor:
            return default
        cursor = cursor[part]
    return cursor


def _is_relevant_event(event: dict) -> bool:
    cat = _get(event, "event.category")
    if isinstance(cat, list):
        if _RELEVANT_CATEGORIES.intersection(cat):
            return True
    elif isinstance(cat, str) and cat in _RELEVANT_CATEGORIES:
        return True

    if _get(event, "dns.question.name"):
        return True
    if _get(event, "url.domain"):
        return True
    return False


def _parse_timestamp(event: dict) -> datetime | None:
    ts_raw = _get(event, "@timestamp") or _get(event, "timestamp")
    if not ts_raw:
        return None
    try:
        return pd.to_datetime(ts_raw, utc=True, errors="raise").to_pydatetime().replace(tzinfo=None)
    except (ValueError, TypeError):
        return None


def _domain(event: dict) -> str | None:
    for dotted in ("dns.question.name", "url.domain", "destination.domain",
                   "destination.address", "server.domain"):
        value = _get(event, dotted)
        if value:
            domain = str(value).strip().rstrip(".").lower()
            if domain:
                return domain
    return None


def _client_ip(event: dict) -> str | None:
    for dotted in ("source.ip", "client.ip", "host.ip"):
        value = _get(event, dotted)
        if isinstance(value, list) and value:
            value = value[0]
        if value:
            return str(value).strip()
    return None


def _user_name(event: dict) -> str | None:
    for dotted in ("user.name", "user.email", "user.id"):
        value = _get(event, dotted)
        if value:
            return str(value).strip()
    return None


def _truncate_path(path: str | None) -> str | None:
    """DSGVO Art. 25: Path auf erstes Segment, Query-String verwerfen."""
    if not path:
        return None
    path = str(path).split("?", 1)[0].split("#", 1)[0]
    if not path or path == "/":
        return path or None
    segments = path.lstrip("/").split("/", 1)
    first = segments[0]
    return f"/{first}" if first else "/"


def _url_path(event: dict) -> str | None:
    direct = _get(event, "url.path")
    if direct:
        return _truncate_path(direct)
    full = _get(event, "url.full") or _get(event, "url.original")
    if full and "://" in str(full):
        return _truncate_path(urlparse(str(full)).path)
    return None


def _parse_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _build_record(
    event: dict,
    source_name: str,
    pseudonymizer: Pseudonymizer,
) -> dict | None:
    if not _is_relevant_event(event):
        return None

    ts = _parse_timestamp(event)
    if ts is None:
        return None

    client_ip = _client_ip(event)
    if not client_ip:
        return None

    domain = _domain(event)
    if not domain:
        return None

    user_raw = _user_name(event)

    return {
        "timestamp": ts,
        "client": pseudonymizer.pseudonymize(client_ip, prefix="ip_"),
        "domain": domain,
        "source_file": source_name,
        "source_type": "elastic_ecs",
        "user": pseudonymizer.pseudonymize(user_raw, prefix="user_") if user_raw else None,
        "method": _get(event, "http.request.method"),
        "status_code": _parse_int(_get(event, "http.response.status_code")),
        "url_path": _url_path(event),
        "bytes_uploaded": _parse_int(_get(event, "http.request.body.bytes")),
        "bytes_downloaded": _parse_int(_get(event, "http.response.body.bytes")),
        "useragent": _get(event, "user_agent.original"),
        "action": _get(event, "event.action"),
        "asn_org": _get(event, "destination.as.organization.name"),
    }


def parse_elastic_ecs_log(
    source: Path | str,
    pseudonymizer: Pseudonymizer | None = None,
) -> pd.DataFrame:
    """Parst eine ECS-NDJSON-Datei in ein Common-Schema-DataFrame.

    Args:
        source: Pfad zur NDJSON-Datei (eine ECS-JSON pro Zeile).
        pseudonymizer: Pseudonymizer-Instanz. Wenn None, wird eine erzeugt.

    Returns:
        DataFrame mit Spalten aus ``_COLUMNS``. Events ohne DNS/Web/Network-
        Relevanz werden verworfen.
    """
    if pseudonymizer is None:
        pseudonymizer = Pseudonymizer()

    source = Path(source)
    records: list[dict] = []

    with open(source, encoding="utf-8", errors="replace") as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(event, dict):
                continue
            record = _build_record(event, source.name, pseudonymizer)
            if record is not None:
                records.append(record)

    if not records:
        return _empty_df()

    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["status_code"] = df["status_code"].astype("Int32")
    df["bytes_uploaded"] = df["bytes_uploaded"].astype("Int64")
    df["bytes_downloaded"] = df["bytes_downloaded"].astype("Int64")
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df[_COLUMNS]


class ElasticECSParser(BaseParser):
    """BaseParser-konforme Klasse für ECS-NDJSON-Logs."""

    OPTIONAL_COLUMNS: set[str] = {
        "source_file", "source_type", "user", "method", "status_code",
        "url_path", "bytes_uploaded", "bytes_downloaded", "useragent",
        "action", "asn_org",
    }

    def parse(self, path: str | Path) -> pd.DataFrame:
        df = parse_elastic_ecs_log(path, self.pseudonymizer)
        return self._finalize(df)
