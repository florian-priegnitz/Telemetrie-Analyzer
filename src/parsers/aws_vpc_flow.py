"""Parser für AWS VPC Flow Logs (Version 2 Default + Version 5 Custom).

Issue #30 (E3-5). AWS VPC Flow Logs sind whitespace-separierte Textzeilen mit
Netzwerk-Metadaten pro Flow-Aggregate (typisch 60s-Fenster). Dieser Parser
unterstützt:

- **v2 Default-Format** (14 Felder, kein Header): ``version account-id
  interface-id srcaddr dstaddr srcport dstport protocol packets bytes start
  end action log-status``
- **v5 Custom-Format** (mit Header-Row): frei konfigurierbare Feld-Reihenfolge.
  Wenn die erste Zeile mit ``version`` beginnt, wird sie als Header interpretiert
  und Felder werden per Name gelesen.

Mapping auf unser Common-Schema:
- ``start`` (Unix-Epoch)               → ``timestamp`` (UTC tz-naive)
- ``srcaddr``                          → ``client`` (pseudonymisiert, ``ip_*``)
- ``pkt-dst-aws-service`` (v5)         → ``domain`` (z.B. ``BEDROCK``, ``SAGEMAKER``)
                                          Fallback: ``dstaddr`` (als IP-String)
- ``pkt-src-aws-service`` (v5)         → ``app`` (AWS-Service-Absender)
- ``bytes``                            → ``bytes_uploaded``
- ``action``                           → ``action`` (``ACCEPT`` / ``REJECT``)
- ``dstport``                          → ``status_code`` bleibt NA — dst_port ist
                                          Netzwerk-Port, kein HTTP-Status

**Shadow-AI-Detection-Ansatz:** VPC Flow Logs sehen typischerweise nur IPs,
nicht Domains. Für AWS-native AI-Workloads (Bedrock, SageMaker, Comprehend,
Rekognition, Polly, Textract, Lex, Translate) liefert das v5-Custom-Feld
``pkt-dst-aws-service`` jedoch den Service-Namen direkt → dieser wird als
``domain`` genutzt und macht AWS-AI-Traffic sichtbar.

**BEKANNTE LIMITATION** — externe AI-Dienste über NAT/Internet-Gateway:
``domain`` enthält die public Dest-IP als String. Die aktuelle
``DetectionEngine`` nutzt ``lookup_subdomain`` (Hostname-Matching) und matcht
daher KEINE IP-Adressen. Für Shadow-AI-Detection auf externen Services braucht
es einen IP→Service-Mapping-Schritt (ASN-Lookup / CIDR-Mapping, siehe #15
E1-7). Bis dahin sind externe AI-Flows im v2-Output sichtbar, werden aber nicht
automatisch als „AI" klassifiziert. Follow-up-Issue tracked diesen Gap.

**Skip-Regeln:** ``log-status`` in ``{NODATA, SKIPDATA, "-"}`` wird übersprungen
(kein Flow-Record). Zeilen ohne ``srcaddr``/``dstaddr`` werden verworfen.

DSGVO Art. 25: ``srcaddr`` wird pseudonymisiert (``ip_*``). Public ``dstaddr``
wird 1:1 übernommen (kein personenbezogener Bezug, aber als ``domain`` strik-
ter zu bewerten — Downstream sollte IP-Domänen nicht in Reports anzeigen,
sondern nur nach Service-Mapping-Auflösung).

Referenz: https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-records-examples.html
"""

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.parsers.base import BaseParser
from src.privacy.pseudonymizer import Pseudonymizer

# v2 Default-Feldreihenfolge (14 Positionen)
V2_FIELDS: tuple[str, ...] = (
    "version", "account-id", "interface-id",
    "srcaddr", "dstaddr", "srcport", "dstport",
    "protocol", "packets", "bytes",
    "start", "end", "action", "log-status",
)

_COLUMNS = [
    "timestamp", "client", "domain", "source_file", "source_type",
    "user", "action", "method", "url_path", "status_code",
    "bytes_uploaded", "bytes_downloaded", "urlcategory", "useragent", "app",
]

_SKIP_STATUSES = frozenset({"NODATA", "SKIPDATA", "-"})


def _empty_df() -> pd.DataFrame:
    df = pd.DataFrame(columns=_COLUMNS)
    return df.astype({
        "bytes_uploaded": "Int64",
        "bytes_downloaded": "Int64",
        "status_code": "Int16",
    })


def _detect_header(first_line: str) -> bool:
    """True wenn die erste Zeile eine Feld-Header-Zeile ist."""
    if not first_line:
        return False
    first_token = first_line.strip().split(None, 1)[0] if first_line.strip() else ""
    return first_token == "version"


def _parse_int(value: str | None) -> int | None:
    if not value or value == "-":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def parse_aws_vpc_flow_log(
    source: Path | str,
    pseudonymizer: Pseudonymizer | None = None,
    fields: tuple[str, ...] | None = None,
) -> pd.DataFrame:
    """Parst AWS VPC Flow Logs (v2 default oder v5 custom) in ein DataFrame.

    Args:
        source: Pfad zur Log-Datei.
        pseudonymizer: Pseudonymizer für ``srcaddr``. Wenn None, wird einer erzeugt.
        fields: Explizite Feldreihenfolge (überschreibt Header-Auto-Detection
            und V2_FIELDS-Default).

    Returns:
        DataFrame mit ``_COLUMNS``. Leere Datei oder nur unparsebare Zeilen
        ergeben leeres DF (mit korrekten dtypes).
    """
    if pseudonymizer is None:
        pseudonymizer = Pseudonymizer()

    source = Path(source)
    records: list[dict] = []

    with open(source, encoding="utf-8", errors="replace") as f:
        first_line = f.readline()
        if not first_line:
            return _empty_df()

        if fields is not None:
            active_fields = fields
            rows_source = _prepend_line(first_line, f)
        elif _detect_header(first_line):
            active_fields = tuple(first_line.strip().split())
            rows_source = f
        else:
            active_fields = V2_FIELDS
            rows_source = _prepend_line(first_line, f)

        idx_map = {name: i for i, name in enumerate(active_fields)}

        # Pflicht-Felder für unser Mapping
        required = {"srcaddr", "dstaddr", "start", "action", "log-status"}
        missing = required - set(active_fields)
        if missing:
            raise ValueError(
                f"VPC Flow Logs benötigen mindestens Felder {sorted(required)}, "
                f"fehlen: {sorted(missing)}"
            )

        for raw_line in rows_source:
            record = _build_record(raw_line, idx_map, source.name, pseudonymizer)
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


def _prepend_line(first: str, rest):
    yield first
    yield from rest


def _get(parts: list[str], idx_map: dict[str, int], name: str) -> str | None:
    if name not in idx_map:
        return None
    i = idx_map[name]
    if i >= len(parts):
        return None
    val = parts[i].strip()
    if not val or val == "-":
        return None
    return val


def _build_record(
    raw_line: str,
    idx_map: dict[str, int],
    source_name: str,
    pseudonymizer: Pseudonymizer,
) -> dict | None:
    line = raw_line.strip()
    if not line or line.startswith("#"):
        return None
    parts = line.split()
    if len(parts) <= max(idx_map.values()):
        return None

    log_status = _get(parts, idx_map, "log-status")
    if log_status is None or log_status in _SKIP_STATUSES:
        return None

    start_raw = _get(parts, idx_map, "start")
    if not start_raw or not start_raw.isdigit():
        return None
    try:
        ts = datetime.fromtimestamp(int(start_raw), tz=timezone.utc).replace(tzinfo=None)
    except (ValueError, OSError, OverflowError):
        return None

    srcaddr = _get(parts, idx_map, "srcaddr")
    dstaddr = _get(parts, idx_map, "dstaddr")
    if not srcaddr or not dstaddr:
        return None

    # domain: bevorzugt pkt-dst-aws-service (v5), fallback dstaddr
    pkt_dst_service = _get(parts, idx_map, "pkt-dst-aws-service")
    domain = pkt_dst_service or dstaddr

    pkt_src_service = _get(parts, idx_map, "pkt-src-aws-service")

    return {
        "timestamp": ts,
        "client": pseudonymizer.pseudonymize_ip(srcaddr),
        "domain": domain.lower().rstrip("."),
        "source_file": source_name,
        "source_type": "aws_vpc_flow",
        "user": None,  # VPC Flow Logs kennen keinen User-Kontext
        "action": _get(parts, idx_map, "action"),
        "method": None,  # Layer-4, keine HTTP-Method
        "url_path": None,  # Layer-4, keine URL
        "status_code": None,  # dstport ist Netz-Port, kein HTTP-Status
        "bytes_uploaded": _parse_int(_get(parts, idx_map, "bytes")),
        "bytes_downloaded": None,  # VPC-Flow misst nur Summe pro Richtung
        "urlcategory": None,
        "useragent": None,
        "app": pkt_src_service.lower() if pkt_src_service else None,
    }


class VPCFlowLogsParser(BaseParser):
    """BaseParser-konformer Wrapper für AWS VPC Flow Logs (v2 + v5 custom)."""

    OPTIONAL_COLUMNS = {
        "source_file", "source_type",
        "user", "action", "method", "url_path", "status_code",
        "bytes_uploaded", "bytes_downloaded",
        "urlcategory", "useragent", "app",
    }

    def parse(
        self,
        path: str | Path,
        fields: tuple[str, ...] | None = None,
    ) -> pd.DataFrame:
        df = parse_aws_vpc_flow_log(path, self.pseudonymizer, fields=fields)
        return self._finalize(df)
