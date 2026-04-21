"""Parser für Windows Sysmon Event ID 22 (DNS Query).

Issue #34 (E3-9). Sysmon Event 22 loggt jede DNS-Auflösung eines Prozesses auf
Windows-Clients — die aufschlussreichste Shadow-AI-Detection-Quelle für
Endpunkt-zentrische Umgebungen (kein Proxy, kein Gateway, aber Sysmon
flächendeckend ausgerollt).

**Unterstützte Formate:** JSONL (eine Zeile = ein Event). Abgedeckt werden:

1. **Flat-Shape** (z.B. evtx2json, nxlog2json) — Keys auf Top-Level:
   ``{"EventID": 22, "UtcTime": "...", "QueryName": "...", "Image": "...",
     "Computer": "...", "User": "CONTOSO\\alice"}``
2. **Winlogbeat/Elastic-Shape** — Keys unter ``winlog.event_data``:
   ``{"@timestamp": "...", "event": {"code": "22"}, "host": {"name": "..."},
     "winlog": {"event_data": {"QueryName": "...", "Image": "..."}}}``
3. **Azure-Sentinel-Shape** — Keys unter ``sysmon``:
   ``{"TimeCreated": "...", "sysmon": {"QueryName": "...", "Image": "..."}}``

XML-Format (Raw wevtutil-Export) wird absichtlich **nicht** unterstützt —
Konvertierung via ``evtx2json`` / ``winlogbeat`` / ``nxlog`` ist Standard
und schlägt dann auf NDJSON-Pfad ab.

**Event-Filter:** nur ``EventID == 22`` bzw. ``event.code == "22"``. Andere
Sysmon-Events (1/3/11/...) werden verworfen.

**Mapping auf Common-Schema:**
- ``UtcTime`` / ``@timestamp``      → ``timestamp`` (datetime64 tz-naive UTC)
- ``Computer`` / ``host.name``       → ``client`` (pseudonymisiert, ``ip_<hash>``)
- ``QueryName``                      → ``domain`` (lowercase, trailing dot entfernt)
- ``User``                           → ``user`` (pseudonymisiert, ``user_<hash>``)
- ``Image``                          → ``process`` (auf basename reduziert, DSGVO Art. 25)
- ``QueryStatus``                    → ``status_code`` (0 = success, NXDOMAIN = 9003, …)

DSGVO Art. 25: Pfade in ``Image`` werden auf basename reduziert (der volle
Pfad kann Benutzerverzeichnisse enthalten, ``C:\\Users\\alice\\AppData\\...``).
Hostnames werden als Client-Identifikator pseudonymisiert — Sysmon liefert
``Computer`` statt IP, deshalb wird das Präfix ``ip_`` beibehalten (konsistenter
Pseudonym-Raum mit anderen Parsern).

Referenz: https://learn.microsoft.com/de-de/sysinternals/downloads/sysmon
"""

from __future__ import annotations

import json
import ntpath
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

from src.parsers.base import BaseParser
from src.privacy.pseudonymizer import Pseudonymizer

_COLUMNS = [
    "timestamp", "client", "domain", "source_file", "source_type",
    "user", "process", "status_code",
]


def _empty_df() -> pd.DataFrame:
    df = pd.DataFrame(columns=_COLUMNS)
    return df.astype({"status_code": "Int32"})


def _event_id(event: dict) -> int | None:
    """Extrahiert EventID aus allen unterstützten Shapes."""
    sysmon_block = event.get("sysmon") if isinstance(event.get("sysmon"), dict) else {}
    for candidate in (
        event.get("EventID"),
        event.get("event_id"),
        (event.get("event") or {}).get("code") if isinstance(event.get("event"), dict) else None,
        (event.get("winlog") or {}).get("event_id") if isinstance(event.get("winlog"), dict) else None,
        sysmon_block.get("EventID"),
        sysmon_block.get("event_id"),
    ):
        if candidate is None:
            continue
        try:
            return int(candidate)
        except (ValueError, TypeError):
            continue
    return None


def _event_data(event: dict) -> dict:
    """Extrahiert das EventData-Dict (Feldnamen wie QueryName/Image/...).

    Je nach Exporter liegen die Sysmon-spezifischen Felder entweder flat auf
    Top-Level, unter ``winlog.event_data`` (Winlogbeat) oder unter ``sysmon``
    (Azure Sentinel). Wir merged die Scopes mit Flat-Shape als Vorrang.
    """
    data = dict(event)
    winlog = event.get("winlog") or {}
    if isinstance(winlog, dict):
        inner = winlog.get("event_data") or {}
        if isinstance(inner, dict):
            for k, v in inner.items():
                data.setdefault(k, v)
    sysmon = event.get("sysmon") or {}
    if isinstance(sysmon, dict):
        for k, v in sysmon.items():
            data.setdefault(k, v)
    return data


def _parse_timestamp(event: dict, data: dict) -> datetime | None:
    """Präferenz: UtcTime (Sysmon-nativ) > @timestamp > TimeCreated."""
    for candidate in (
        data.get("UtcTime"),
        event.get("@timestamp"),
        event.get("TimeCreated"),
        data.get("TimeCreated"),
    ):
        if not candidate:
            continue
        try:
            return pd.to_datetime(candidate, utc=True, errors="raise").to_pydatetime().replace(tzinfo=None)
        except (ValueError, TypeError):
            continue
    return None


def _hostname(event: dict, data: dict) -> str | None:
    """Computer-Name hat Vorrang, Winlogbeat nennt ihn host.name."""
    for candidate in (
        data.get("Computer"),
        event.get("Computer"),
        (event.get("host") or {}).get("name") if isinstance(event.get("host"), dict) else None,
    ):
        if candidate:
            return str(candidate).strip()
    return None


def _user(event: dict, data: dict) -> str | None:
    """Account-Name aus User (DOMAIN\\user) oder Winlogbeat user.name."""
    for candidate in (
        data.get("User"),
        (event.get("user") or {}).get("name") if isinstance(event.get("user"), dict) else None,
    ):
        if candidate:
            return str(candidate).strip()
    return None


def _process_basename(image: str | None) -> str | None:
    """DSGVO Art. 25: Image-Pfad auf Dateinamen reduzieren.

    ``C:\\Users\\alice\\AppData\\Local\\Programs\\cursor\\Cursor.exe`` → ``Cursor.exe``
    """
    if not image:
        return None
    return ntpath.basename(str(image)) or None


def _normalize_domain(name: str | None) -> str | None:
    if not name:
        return None
    domain = str(name).strip().rstrip(".").lower()
    return domain or None


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
    if _event_id(event) != 22:
        return None
    data = _event_data(event)

    ts = _parse_timestamp(event, data)
    if ts is None:
        return None

    host = _hostname(event, data)
    if not host:
        return None

    domain = _normalize_domain(data.get("QueryName"))
    if not domain:
        return None

    user_raw = _user(event, data)

    return {
        "timestamp": ts,
        "client": pseudonymizer.pseudonymize(host, prefix="ip_"),
        "domain": domain,
        "source_file": source_name,
        "source_type": "sysmon",
        "user": pseudonymizer.pseudonymize(user_raw, prefix="user_") if user_raw else None,
        "process": _process_basename(data.get("Image")),
        "status_code": _parse_int(data.get("QueryStatus")),
    }


def parse_sysmon_log(
    source: Path | str,
    pseudonymizer: Pseudonymizer | None = None,
) -> pd.DataFrame:
    """Parst eine Sysmon-Event-22-NDJSON-Datei in ein Common-Schema-DataFrame.

    Args:
        source: Pfad zur NDJSON-Datei.
        pseudonymizer: Pseudonymizer-Instanz. Wenn None, wird eine erzeugt.

    Returns:
        DataFrame mit Spalten aus ``_COLUMNS``. Leere Datei oder nur Events
        mit ``EventID != 22`` → leeres DataFrame.
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
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df[_COLUMNS]


class SysmonParser(BaseParser):
    """BaseParser-konforme Klasse für Sysmon-Event-22-Logs."""

    OPTIONAL_COLUMNS: set[str] = {
        "source_file", "source_type", "user", "process", "status_code",
    }

    def parse(self, path: str | Path) -> pd.DataFrame:
        df = parse_sysmon_log(path, self.pseudonymizer)
        return self._finalize(df)
