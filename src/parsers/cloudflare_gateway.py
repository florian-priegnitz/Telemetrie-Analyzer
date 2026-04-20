"""Parser für Cloudflare Gateway Logs (Zero Trust — DNS + HTTP).

Issue #32 (E3-7). Cloudflare Gateway exportiert Events via **Logpush** in zwei
getrennten Datasets (``gateway_dns`` und ``gateway_http``) als **NDJSON**
nach S3/R2/GCS/Splunk. Dieser Parser akzeptiert beide Typen in derselben
Datei — DNS- vs. HTTP-Events werden pro Zeile anhand der Feld-Präsenz
unterschieden (``QueryName`` → DNS, ``URL`` → HTTP).

**Shadow-AI-Angle (2024+):** Cloudflare kategorisiert AI-Dienste in
``QueryCategoryNames`` (DNS) bzw. ``CategoryNames`` (HTTP) mit Einträgen wie
``"Generative AI"``, ``"AI Chatbots"``, ``"Machine Learning"``. Dies ist der
primäre Detection-Vektor.

Mapping auf unser Common-Schema:
- ``Datetime``                        → ``timestamp`` (ISO-8601 UTC, tz-naive)
- ``SrcIP``                           → ``client`` (ip_* Pseudonym)
- ``Email``                           → ``user`` (user_* Pseudonym, wenn present)
- ``QueryName`` (DNS) / Host aus URL → ``domain``
- URL-Pfad (HTTP, erstes Segment)    → ``url_path`` (DSGVO-Truncation)
- ``ResolverDecision`` (DNS) / ``Action`` (HTTP) → ``action``
- ``QueryCategoryNames`` / ``CategoryNames`` (Liste → comma-join) → ``urlcategory``
- ``QueryType``                       → ``query_type`` (DNS only)
- ``HTTPMethod``                      → ``method`` (HTTP only)
- ``HTTPStatusCode``                  → ``status_code`` (HTTP only)
- ``UploadBytes`` / ``DownloadBytes`` → ``bytes_uploaded`` / ``bytes_downloaded``
- ``UserAgent``                       → ``useragent`` (HTTP only)
- ``ApplicationName``                 → ``app``

``source_type`` ist ``cloudflare_gateway_dns`` oder ``cloudflare_gateway_http``
je Event — erlaubt Downstream-Filterung.

DSGVO Art. 25: ``Email`` und ``SrcIP`` pseudonymisiert. ``DeviceID``/
``DeviceName``/``Location`` werden NICHT übernommen (Datensparsamkeit).

Referenzen:
- https://developers.cloudflare.com/logs/logpush/logpush-job/datasets/account/gateway_dns/
- https://developers.cloudflare.com/logs/logpush/logpush-job/datasets/account/gateway_http/
"""

import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd

from src.parsers.base import BaseParser
from src.privacy.pseudonymizer import Pseudonymizer

_COLUMNS = [
    "timestamp", "client", "domain", "source_file", "source_type",
    "user", "action", "method", "url_path", "status_code",
    "bytes_uploaded", "bytes_downloaded", "urlcategory", "useragent", "app",
    "query_type",
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
    try:
        ts = pd.to_datetime(raw, utc=True)
    except (ValueError, TypeError):
        return None
    if pd.isna(ts):
        return None
    return ts.tz_convert("UTC").tz_localize(None).to_pydatetime()


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


def _extract_domain_and_path(url: str) -> tuple[str | None, str | None]:
    url = (url or "").strip()
    if not url:
        return None, None
    if "://" not in url:
        head, _, tail = url.partition("/")
        host = head.split(":")[0]
        path = f"/{tail}" if tail else None
        return (host.lower().rstrip(".") or None), _truncate_path(path)
    parsed = urlparse(url)
    if not parsed.hostname:
        return None, _truncate_path(parsed.path)
    return parsed.hostname.lower().rstrip("."), _truncate_path(parsed.path)


def _normalize_categories(value) -> str | None:
    """Cloudflare kann Kategorien als Liste oder String senden."""
    if value is None:
        return None
    if isinstance(value, list):
        clean = [str(v).strip() for v in value if v]
        return ", ".join(clean) if clean else None
    s = str(value).strip()
    return s or None


def parse_cloudflare_gateway_log(
    source: Path | str,
    pseudonymizer: Pseudonymizer | None = None,
) -> pd.DataFrame:
    """Parst Cloudflare Gateway Logpush-NDJSON (DNS + HTTP gemischt) in DataFrame.

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
    ts = _parse_timestamp(event.get("Datetime"))
    if ts is None:
        return None

    src_ip = (event.get("SrcIP") or "").strip()
    if not src_ip:
        return None

    # Detection-Priorität: QueryName → DNS (autoritativstes DNS-Feld),
    # sonst URL/HTTPMethod → HTTP. Schützt gegen Schema-Drift, wenn ein DNS-
    # Event versehentlich HTTPStatusCode enthält.
    if "QueryName" in event:
        return _build_dns_record(event, ts, src_ip, source_name, pseudonymizer)
    if "URL" in event or "HTTPMethod" in event:
        return _build_http_record(event, ts, src_ip, source_name, pseudonymizer)
    return None


def _build_dns_record(
    event: dict,
    ts: datetime,
    src_ip: str,
    source_name: str,
    pseudonymizer: Pseudonymizer,
) -> dict | None:
    query_name = (event.get("QueryName") or "").strip()
    if not query_name:
        return None
    email = (event.get("Email") or "").strip()
    return {
        "timestamp": ts,
        "client": pseudonymizer.pseudonymize_ip(src_ip),
        "domain": query_name.lower().rstrip("."),
        "source_file": source_name,
        "source_type": "cloudflare_gateway_dns",
        "user": pseudonymizer.pseudonymize_user(email) if email else None,
        "action": event.get("ResolverDecision") or None,
        "method": None,
        "url_path": None,
        "status_code": None,
        "bytes_uploaded": None,
        "bytes_downloaded": None,
        "urlcategory": _normalize_categories(
            event.get("QueryCategoryNames") or event.get("MatchedCategoryNames")
        ),
        "useragent": None,
        "app": event.get("ApplicationName") or None,
        "query_type": event.get("QueryType") or None,
    }


def _build_http_record(
    event: dict,
    ts: datetime,
    src_ip: str,
    source_name: str,
    pseudonymizer: Pseudonymizer,
) -> dict | None:
    url = (event.get("URL") or "").strip()
    if not url:
        return None
    domain, path = _extract_domain_and_path(url)
    if not domain:
        return None
    email = (event.get("Email") or "").strip()
    return {
        "timestamp": ts,
        "client": pseudonymizer.pseudonymize_ip(src_ip),
        "domain": domain,
        "source_file": source_name,
        "source_type": "cloudflare_gateway_http",
        "user": pseudonymizer.pseudonymize_user(email) if email else None,
        "action": event.get("Action") or None,
        "method": event.get("HTTPMethod") or None,
        "url_path": path,
        "status_code": _parse_int(event.get("HTTPStatusCode")),
        "bytes_uploaded": _parse_int(event.get("UploadBytes")),
        "bytes_downloaded": _parse_int(event.get("DownloadBytes")),
        "urlcategory": _normalize_categories(event.get("CategoryNames")),
        "useragent": event.get("UserAgent") or None,
        "app": event.get("ApplicationName") or None,
        "query_type": None,
    }


class CloudflareGatewayParser(BaseParser):
    """BaseParser-konformer Wrapper für Cloudflare Gateway Logpush-NDJSON
    (DNS + HTTP gemischt akzeptiert).
    """

    OPTIONAL_COLUMNS = {
        "source_file", "source_type",
        "user", "action", "method", "url_path", "status_code",
        "bytes_uploaded", "bytes_downloaded",
        "urlcategory", "useragent", "app",
        "query_type",
    }

    def parse(self, path: str | Path) -> pd.DataFrame:
        df = parse_cloudflare_gateway_log(path, self.pseudonymizer)
        return self._finalize(df)
