"""Parser für Azure Entra ID Sign-In Logs (JSONL aus Azure Monitor / Log Analytics).

Issue #31 (E3-6). Azure Entra (früher Azure AD) exportiert Sign-In-Events via
Diagnostic Settings → Log Analytics → Storage Account als **JSONL / NDJSON**
(eine JSON-Zeile pro Event).

Shadow-AI-Angle: Jede externe AI-App (Microsoft 365 Copilot, ChatGPT Enterprise,
Claude Enterprise, Notion AI, etc.) benötigt eine Entra-App-Registration. Der
App-Name steht in ``AppDisplayName`` — dieser wird als ``domain`` genutzt, um
AI-Zugriffe über SSO sichtbar zu machen. Ergänzt DNS/Proxy-Parser um die
**Authentifizierungs-Ebene**, speziell relevant für Cloud-First-Umgebungen.

Mapping auf unser Common-Schema:
- ``TimeGenerated`` (ISO-8601 UTC)          → ``timestamp`` (tz-naive)
- ``IPAddress`` (fallback ``UserId``)       → ``client`` (ip_* / user_* Pseudonym)
- ``UserPrincipalName``                     → ``user`` (user_* Pseudonym)
- ``AppDisplayName``                        → ``domain`` (lowercase — die „App" ist das Ziel)
- ``AppId``                                 → ``app`` (GUID-Referenz)
- ``ConditionalAccessStatus`` + ``Status``  → ``action``
  (``blocked`` wenn CA failure, ``failed`` wenn errorCode!=0, sonst ``success``)
- ``Status.errorCode``                      → ``status_code``

**action-Semantik:**
- ``blocked``   — ConditionalAccessStatus == "failure" (Policy hat geblockt)
- ``failed``    — Status.errorCode != 0 (Auth-Fehler, z.B. 50126 bad password)
- ``success``   — errorCode == 0 und CA in {success, notApplied}

**Hinweis zu ``status_code``:** das Common-Schema sieht ``status_code`` als
``Int16`` vor (HTTP-Status 0–32767). Azure-errorCodes sind 5–6-stellig
(z.B. 50126, 500121) — passen nicht rein. Wir mappen errorCode daher NICHT
auf ``status_code``; der semantische Kontext ist in ``action`` komplett
abgedeckt (``failed``/``blocked``/``success``).

DSGVO Art. 25: ``UserPrincipalName`` und ``IPAddress`` werden pseudonymisiert.
``LocationDetails.city`` / ``DeviceDetail.deviceId`` werden NICHT ins Output
übernommen (Datensparsamkeit — nicht nötig für Shadow-AI-Detection).

Referenz: https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/signinlogs
"""

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.parsers.base import BaseParser
from src.privacy.pseudonymizer import Pseudonymizer

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


def _parse_timestamp(raw: str | None) -> datetime | None:
    if not raw:
        return None
    # ISO-8601 UTC mit optionalem Z oder +00:00; pd.to_datetime ist robust.
    try:
        ts = pd.to_datetime(raw, utc=True)
    except (ValueError, TypeError):
        return None
    if pd.isna(ts):
        return None
    return ts.tz_convert("UTC").tz_localize(None).to_pydatetime()


def _derive_action(event: dict) -> str:
    ca_status = event.get("ConditionalAccessStatus")
    if ca_status == "failure":
        return "blocked"
    status = event.get("Status") or {}
    if isinstance(status, dict):
        error_code = status.get("errorCode")
        if error_code is not None and error_code != 0:
            return "failed"
    return "success"


def _parse_int(value) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def parse_entra_signin_log(
    source: Path | str,
    pseudonymizer: Pseudonymizer | None = None,
) -> pd.DataFrame:
    """Parst Azure Entra Sign-In Logs (JSONL) in ein DataFrame.

    Args:
        source: Pfad zur JSONL-Datei (Azure Log Analytics Export).
        pseudonymizer: Pseudonymizer für IP + UserPrincipalName. Wenn None,
            wird einer erzeugt.

    Returns:
        DataFrame mit ``_COLUMNS``. Leere Datei oder nur unparsebare Zeilen
        ergeben leeres DF (mit korrekten dtypes).
    """
    if pseudonymizer is None:
        pseudonymizer = Pseudonymizer()

    source = Path(source)
    records: list[dict] = []

    with open(source, encoding="utf-8", errors="replace") as f:
        for line_no, raw_line in enumerate(f, 1):
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
    df["bytes_uploaded"] = df["bytes_uploaded"].astype("Int64")
    df["bytes_downloaded"] = df["bytes_downloaded"].astype("Int64")
    df["status_code"] = df["status_code"].astype("Int16")
    return df[_COLUMNS]


def _build_record(
    event: dict,
    source_name: str,
    pseudonymizer: Pseudonymizer,
) -> dict | None:
    ts_raw = event.get("TimeGenerated") or event.get("CreatedDateTime")
    ts = _parse_timestamp(ts_raw)
    if ts is None:
        return None

    app_display = (event.get("AppDisplayName") or "").strip()
    if not app_display:
        return None
    domain = app_display.lower()

    ip_address = (event.get("IPAddress") or "").strip()
    user_principal = (event.get("UserPrincipalName") or "").strip()
    user_id = (event.get("UserId") or "").strip()

    # client: IP bevorzugt, sonst UserId als stable Identifier
    client_seed = ip_address or user_id
    if not client_seed:
        return None
    if ip_address:
        client = pseudonymizer.pseudonymize_ip(client_seed)
    else:
        # UserId (GUID) → pseudonymize als user-Pseudonym, damit keine IP-Kollision
        client = pseudonymizer.pseudonymize_user(client_seed)

    user = pseudonymizer.pseudonymize_user(user_principal) if user_principal else None

    return {
        "timestamp": ts,
        "client": client,
        "domain": domain,
        "source_file": source_name,
        "source_type": "azure_entra",
        "user": user,
        "action": _derive_action(event),
        "method": event.get("AuthenticationProtocol") or None,
        "url_path": None,  # Sign-In-Logs kennen keine URL
        "status_code": None,  # Azure errorCodes sprengen Int16 — Semantik in action
        "bytes_uploaded": None,  # Sign-In-Logs führen keine Bytes
        "bytes_downloaded": None,
        "urlcategory": None,
        "useragent": _extract_useragent(event.get("DeviceDetail")),
        "app": event.get("AppId") or None,
    }


def _extract_useragent(device_detail) -> str | None:
    """Baut einen User-Agent-Proxy aus DeviceDetail.

    Azure Sign-In hat kein Top-Level-UA-Feld; das Nächste ist
    ``DeviceDetail.browser`` + ``operatingSystem``, was für Audit-Zwecke
    ausreicht (z.B. ``Chrome on Windows``).
    """
    if not isinstance(device_detail, dict):
        return None
    browser = (device_detail.get("browser") or "").strip()
    os_name = (device_detail.get("operatingSystem") or "").strip()
    if browser and os_name:
        return f"{browser} on {os_name}"
    return browser or os_name or None


class EntraIDSignInParser(BaseParser):
    """BaseParser-konformer Wrapper für Entra ID Sign-In JSONL-Logs."""

    OPTIONAL_COLUMNS = {
        "source_file", "source_type",
        "user", "action", "method", "url_path", "status_code",
        "bytes_uploaded", "bytes_downloaded",
        "urlcategory", "useragent", "app",
    }

    def parse(self, path: str | Path) -> pd.DataFrame:
        df = parse_entra_signin_log(path, self.pseudonymizer)
        return self._finalize(df)
