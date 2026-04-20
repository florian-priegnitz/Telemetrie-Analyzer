"""Parser für Netskope CASB / Secure Web Gateway Events (JSON NDJSON).

Issue #33 (E3-8). Netskope ist marktführender CASB. Exportiert Events via
REST API v2 oder Cloud Log Shipper als **NDJSON**. Dieser Parser liest den
Log-Shipper-Standard-Output (JSON-Lines).

**Shadow-AI-Fokus:** Netskope klassifiziert seit 2024 explizit
``appcategory = "Artificial Intelligence"`` mit 1.550+ getaggten AI-Apps
(OpenAI ChatGPT, Anthropic Claude, Google Gemini, Copilot, Perplexity,
Character.ai, Midjourney, ...). Zusätzlich spezifische Activities:
- ``"Prompt"`` = LLM-Eingabe
- ``"Completion"`` = LLM-Antwort
- ``"Upload File"`` = Doc-Upload zu AI

Beides sind erstrangige Detection-Vektoren.

Mapping auf unser Common-Schema:
- ``_insertion_epoch_timestamp`` / ``timestamp``  → ``timestamp``
  (Unix-Epoch-Sekunden → datetime tz-naive UTC)
- ``src_ip`` (fallback ``userip``)                → ``client`` (ip_* Pseudonym)
- ``user``                                        → ``user`` (user_* Pseudonym)
- ``hostname`` (fallback ``app``)                 → ``domain`` (lowercase)
- ``app``                                         → ``app`` (1:1, z.B. "OpenAI ChatGPT")
- ``appcategory``                                 → ``urlcategory``
- ``action``                                      → ``action`` (allow/block/alert)
- ``activity``                                    → ``activity`` (Netskope-Extra:
                                                     Login/Prompt/Completion/Upload File/...)
- ``method``                                      → ``method``
- ``uri_path`` (oder aus ``url``)                 → ``url_path`` (DSGVO-Truncation)
- ``bytes_uploaded`` / ``bytes_downloaded``       → ``bytes_*``
- ``useragent``                                   → ``useragent``

**CCL-Mapping (Cloud Confidence Level):** Netskope bewertet Apps mit
``ccl`` in ``{high, medium, low, poor}`` (je geringer, desto riskanter).
Nicht direkt im Schema mapbar — wird derzeit verworfen. Folge-Issue könnte
``ccl`` als optionale Zusatzspalte aufnehmen (analog zu activity).

DSGVO Art. 25: ``user`` und ``src_ip`` pseudonymisiert. ``src_country``/
``src_region``/``device``/``os`` werden NICHT übernommen (Datensparsamkeit).
``url_path`` auf erstes Segment reduziert (konsistent mit restlichen Parsern).

Referenz: https://docs.netskope.com/en/rest-api-v2-overview-312207/
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd

from src.parsers.base import BaseParser
from src.privacy.pseudonymizer import Pseudonymizer

_COLUMNS = [
    "timestamp", "client", "domain", "source_file", "source_type",
    "user", "action", "method", "url_path", "status_code",
    "bytes_uploaded", "bytes_downloaded", "urlcategory", "useragent", "app",
    "activity",
]


def _empty_df() -> pd.DataFrame:
    df = pd.DataFrame(columns=_COLUMNS)
    return df.astype({
        "bytes_uploaded": "Int64",
        "bytes_downloaded": "Int64",
        "status_code": "Int16",
    })


def _parse_timestamp(event: dict) -> datetime | None:
    """Netskope liefert Unix-Epoch (Sekunden) in mehreren Feldern.

    Präferenz: ``_insertion_epoch_timestamp`` > ``timestamp`` > ``event_time``.
    """
    for key in ("_insertion_epoch_timestamp", "timestamp", "event_time"):
        value = event.get(key)
        if value is None:
            continue
        try:
            epoch = int(value)
        except (ValueError, TypeError):
            continue
        try:
            return datetime.fromtimestamp(epoch, tz=timezone.utc).replace(tzinfo=None)
        except (ValueError, OSError, OverflowError):
            continue
    return None


def _parse_int(value) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _truncate_path(path: str | None) -> str | None:
    if not path or path == "/":
        return path or None
    segments = path.lstrip("/").split("/", 1)
    first = segments[0]
    return f"/{first}" if first else "/"


def _derive_url_path(event: dict) -> str | None:
    # Netskope hat oft uri_path direkt; fallback über url
    uri_path = event.get("uri_path")
    if uri_path:
        return _truncate_path(uri_path)
    url = event.get("url")
    if url and "://" in url:
        return _truncate_path(urlparse(url).path)
    return None


def parse_netskope_log(
    source: Path | str,
    pseudonymizer: Pseudonymizer | None = None,
) -> pd.DataFrame:
    """Parst Netskope CASB/SWG NDJSON-Events in ein DataFrame.

    Args:
        source: Pfad zur NDJSON-Datei.
        pseudonymizer: Pseudonymizer. Wenn None, wird einer erzeugt.

    Returns:
        DataFrame mit ``_COLUMNS``. Leere Datei oder nur unparsebare Zeilen
        → leeres DF mit korrekten dtypes.
    """
    if pseudonymizer is None:
        pseudonymizer = Pseudonymizer()

    source = Path(source)
    records: list[dict] = []

    with open(source, encoding="utf-8", errors="replace") as f:
        for raw_line in f:
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
    ts = _parse_timestamp(event)
    if ts is None:
        return None

    src_ip = (event.get("src_ip") or event.get("userip") or "").strip()
    if not src_ip:
        return None

    hostname = (event.get("hostname") or "").strip()
    app = (event.get("app") or "").strip()
    # domain: hostname bevorzugt (echter DNS-Name), Fallback app-Name (Schema-
    # Dehnung wie bei Entra/AWS VPC).
    domain_raw = hostname or app
    if not domain_raw:
        return None
    domain = domain_raw.lower().rstrip(".")

    user_raw = (event.get("user") or "").strip()
    user = pseudonymizer.pseudonymize_user(user_raw) if user_raw else None

    return {
        "timestamp": ts,
        "client": pseudonymizer.pseudonymize_ip(src_ip),
        "domain": domain,
        "source_file": source_name,
        "source_type": "netskope",
        "user": user,
        "action": event.get("action") or None,
        "method": event.get("method") or None,
        "url_path": _derive_url_path(event),
        "status_code": None,  # Netskope schreibt keinen stabilen HTTP-Status
        "bytes_uploaded": _parse_int(event.get("bytes_uploaded")),
        "bytes_downloaded": _parse_int(event.get("bytes_downloaded")),
        "urlcategory": event.get("appcategory") or None,
        "useragent": event.get("useragent") or None,
        "app": app or None,
        "activity": event.get("activity") or None,
    }


class NetskopeCASBParser(BaseParser):
    """BaseParser-konformer Wrapper für Netskope CASB NDJSON-Events."""

    OPTIONAL_COLUMNS = {
        "source_file", "source_type",
        "user", "action", "method", "url_path", "status_code",
        "bytes_uploaded", "bytes_downloaded",
        "urlcategory", "useragent", "app",
        "activity",
    }

    def parse(self, path: str | Path) -> pd.DataFrame:
        df = parse_netskope_log(path, self.pseudonymizer)
        return self._finalize(df)
