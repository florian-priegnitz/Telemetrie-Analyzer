"""Parser für Cisco Umbrella DNS Security Logs (CSV-Export aus S3).

Issue #28 (E3-3). Cisco Umbrella exportiert DNS-Events alle 10 Minuten als
gzip-CSV in S3-Buckets. Dieser Parser liest das **Version-10-Format** mit
Header-Row (Standard seit 2024). Legacy-Exports ohne Header werden erkannt
und positions-basiert geparst.

Spalten-Schema v10 (Reihenfolge im Export):
    timestamp, most_granular_identity, identities, internal_ip, external_ip,
    action, query_type, response_code, domain, categories,
    most_granular_identity_type, identity_types, blocked_categories,
    rule_id, destination_countries, organization_id

Mapping auf unser Common-Schema:
- timestamp                        → ``timestamp``
- internal_ip || identity          → ``client``  (pseudonymisiert, ``ip_*``)
- most_granular_identity           → ``user``    (falls identity_type in USER_TYPES, sonst None)
- most_granular_identity_type      → ``identity_type`` (Optional-Spalte)
- action                           → ``action``  ("Allowed" / "Blocked" / ...)
- domain                           → ``domain``  (lowercase, trailing "." entfernt)
- categories                       → ``urlcategory`` (komma-separierte Liste)
- query_type                       → ``query_type`` (z.B. ``1 (A)``)

DSGVO Art. 25: ``most_granular_identity`` kann AD-Username, Device-Name oder
Network-Name sein. Wird konsequent pseudonymisiert — entweder als ``user_*``
(bei Identity-Type "User"/"AD User") oder als Teil des ``client``-Feldes.

Umbrella-Kategorien enthalten seit 2024 ``Generative AI`` / ``Conversational AI``
als first-class Flag für Shadow-AI-Detection.

Referenz:
https://docs.umbrella.com/umbrella-user-guide/docs/dns-log-formats
"""

import csv
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.parsers.base import BaseParser
from src.privacy.pseudonymizer import Pseudonymizer

V10_COLUMNS: tuple[str, ...] = (
    "timestamp",
    "most_granular_identity",
    "identities",
    "internal_ip",
    "external_ip",
    "action",
    "query_type",
    "response_code",
    "domain",
    "categories",
    "most_granular_identity_type",
    "identity_types",
    "blocked_categories",
    "rule_id",
    "destination_countries",
    "organization_id",
)

USER_IDENTITY_TYPES: frozenset[str] = frozenset({
    "User", "AD User", "Active Directory User",
})

_TIMESTAMP_FMT = "%Y-%m-%d %H:%M:%S"

_COLUMNS = [
    "timestamp", "client", "domain", "source_file", "source_type",
    "user", "action", "method", "url_path", "status_code",
    "bytes_uploaded", "bytes_downloaded", "urlcategory", "useragent", "app",
    "identity_type", "query_type",
]


def _empty_df() -> pd.DataFrame:
    df = pd.DataFrame(columns=_COLUMNS)
    return df.astype({
        "bytes_uploaded": "Int64",
        "bytes_downloaded": "Int64",
        "status_code": "Int16",
    })


def _detect_header(first_line: str) -> bool:
    """True wenn die erste Zeile eine Umbrella-Header-Row ist."""
    if not first_line:
        return False
    head = first_line.strip().lower()
    return "timestamp" in head and ("identity" in head or "domain" in head)


def parse_umbrella_log(
    source: Path | str,
    pseudonymizer: Pseudonymizer | None = None,
    has_header: str = "auto",
) -> pd.DataFrame:
    """Parst einen Cisco Umbrella DNS CSV-Export in ein DataFrame.

    Args:
        source: Pfad zur CSV-Datei (nicht gzip — entpacken vor Übergabe).
        pseudonymizer: Pseudonymizer für IPs und User-Identities.
        has_header: "auto" (Default, Header wird erkannt), "yes" oder "no".

    Returns:
        DataFrame mit ``_COLUMNS``. Bei leerer Datei oder nur Header: leeres DF
        mit korrekten dtypes. Nicht-parsebare Zeilen werden übersprungen.

    Raises:
        ValueError: ``has_header`` ist kein gültiger Wert.
    """
    if has_header not in ("auto", "yes", "no"):
        raise ValueError(f"has_header muss 'auto'|'yes'|'no' sein, ist '{has_header}'")

    if pseudonymizer is None:
        pseudonymizer = Pseudonymizer()

    source = Path(source)
    records: list[dict] = []

    with open(source, encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.reader(f)
        try:
            first_row = next(reader)
        except StopIteration:
            return _empty_df()

        if has_header == "auto":
            header_present = _detect_header(",".join(first_row))
        else:
            header_present = has_header == "yes"

        if header_present:
            columns = tuple(c.strip().lower() for c in first_row)
            rows_iter = reader
        else:
            columns = V10_COLUMNS
            rows_iter = _prepend_first_row(first_row, reader)

        col_idx = {name: i for i, name in enumerate(columns)}
        if "timestamp" not in col_idx or "domain" not in col_idx:
            return _empty_df()

        for parts in rows_iter:
            record = _build_record(parts, col_idx, source.name, pseudonymizer)
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


def _prepend_first_row(first, reader):
    yield first
    yield from reader


def _get(parts: list[str], idx_map: dict[str, int], name: str) -> str | None:
    if name not in idx_map:
        return None
    i = idx_map[name]
    if i >= len(parts):
        return None
    val = parts[i].strip()
    return val or None


def _build_record(
    parts: list[str],
    idx_map: dict[str, int],
    source_name: str,
    pseudonymizer: Pseudonymizer,
) -> dict | None:
    ts_raw = _get(parts, idx_map, "timestamp")
    if not ts_raw:
        return None
    try:
        ts = datetime.strptime(ts_raw, _TIMESTAMP_FMT)
    except ValueError:
        return None

    domain_raw = _get(parts, idx_map, "domain")
    if not domain_raw:
        return None
    domain = domain_raw.lower().rstrip(".")
    if not domain:
        return None

    identity = _get(parts, idx_map, "most_granular_identity")
    internal_ip = _get(parts, idx_map, "internal_ip")
    identity_type = _get(parts, idx_map, "most_granular_identity_type")

    # client: bevorzugt internal_ip, fallback auf identity-Hash
    client_seed = internal_ip or identity
    if not client_seed:
        return None
    client = pseudonymizer.pseudonymize_ip(client_seed)

    # user: nur wenn Identity-Type user-artig ist
    user = None
    if identity and identity_type in USER_IDENTITY_TYPES:
        user = pseudonymizer.pseudonymize_user(identity)

    return {
        "timestamp": ts,
        "client": client,
        "domain": domain,
        "source_file": source_name,
        "source_type": "umbrella",
        "user": user,
        "action": _get(parts, idx_map, "action"),
        "method": None,  # DNS-Logs: keine HTTP-Method
        "url_path": None,  # DNS-Logs: keine Path-Information
        "status_code": None,  # response_code ist Text (NOERROR), nicht HTTP-Status
        "bytes_uploaded": None,  # DNS-Logs: keine Bytes
        "bytes_downloaded": None,
        "urlcategory": _get(parts, idx_map, "categories"),
        "useragent": None,
        "app": None,
        "identity_type": identity_type,
        "query_type": _get(parts, idx_map, "query_type"),
    }


class UmbrellaDNSParser(BaseParser):
    """BaseParser-konformer Wrapper für Cisco Umbrella DNS-CSV-Exporte."""

    OPTIONAL_COLUMNS = {
        "source_file", "source_type",
        "user", "action", "method", "url_path", "status_code",
        "bytes_uploaded", "bytes_downloaded",
        "urlcategory", "useragent", "app",
        "identity_type", "query_type",
    }

    def parse(
        self,
        path: str | Path,
        has_header: str = "auto",
    ) -> pd.DataFrame:
        df = parse_umbrella_log(path, self.pseudonymizer, has_header=has_header)
        return self._finalize(df)
