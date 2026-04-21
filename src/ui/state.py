"""Pipeline-Wrapper für die Streamlit-UI.

Einziger Punkt, an dem die UI mit der Analyse-Pipeline spricht. Pages/Components
importieren ausschliesslich aus diesem Modul (+ Components untereinander).

Caching: Wir cachen das JSON-Dict (nicht den ReportContext), weil ReportContext
Datetime + Dataclass-Listen enthält, die für Streamlits Hash-Funktion problematisch
sind. Aus dem Dict baut die UI bei Bedarf die Anzeige-Strukturen.

Parser-Dispatch: ``_PARSER_DISPATCH`` ist das UI-Gegenstück zu ``_PARSERS`` in
``src/cli.py``. Beide delegieren Format-Erkennung an ``src/parsers/detection.py``
(Single Source of Truth).
"""

from __future__ import annotations

import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any, Literal

import pandas as pd
import streamlit as st

from src.analytics.temporal import build_hourly_heatmap
from src.compliance.engine import ComplianceEngine
from src.detection.engine import DetectionEngine
from src.parsers.detection import detect_format
from src.privacy.k_anonymity import check_k_anonymity
from src.privacy.pseudonymizer import Pseudonymizer
from src.privacy.retention import apply_retention, load_policy, summarize
from src.reports.context import build_context, context_to_json_dict
from src.reports.privacy import get_default_salt, pseudonymize_client

PipelineState = Literal["empty", "uploaded", "analyzing", "analyzed", "error"]
LogFormat = str  # Ein Key aus SUPPORTED_PARSERS oder "unknown"
UNKNOWN_FORMAT = "unknown"


def init_session_state() -> None:
    """Initialisiert Session-State mit Default-Werten (idempotent)."""
    defaults: dict[str, Any] = {
        "pipeline_state": "empty",
        "uploaded_filename": None,
        "uploaded_bytes": None,
        "detected_format": None,
        "report_data": None,  # JSON-Dict (siehe Modul-Docstring)
        "report_salt": get_default_salt(),
        "filter_risk_levels": [],
        "filter_frameworks": [],
        "error_message": None,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def detect_log_format(content: bytes | str) -> LogFormat:
    """Thin-Wrapper um ``src.parsers.detection.detect_format()``.

    Akzeptiert bytes oder str (UI liefert bytes vom Upload-Widget).
    Liefert immer einen String — entweder einen Key aus ``SUPPORTED_PARSERS``
    oder ``"unknown"`` — nie None.
    """
    sample_bytes = content if isinstance(content, bytes) else content.encode("utf-8", errors="replace")
    return detect_format(sample_bytes) or UNKNOWN_FORMAT


def _build_parser_dispatch() -> dict[str, Callable[..., pd.DataFrame]]:
    """Lazy-initialisierte Parser-Registry (analog zu ``src/cli.py::_PARSERS``).

    Wird beim ersten ``run_pipeline()``-Aufruf populiert, um Import-Zeit
    klein zu halten (Streamlit-Cold-Start).
    """
    from src.parsers.aws_vpc_flow import parse_aws_vpc_flow_log
    from src.parsers.cloudflare_gateway import parse_cloudflare_gateway_log
    from src.parsers.elastic_ecs import parse_elastic_ecs_log
    from src.parsers.entra_id import parse_entra_signin_log
    from src.parsers.fortinet import parse_fortinet_log
    from src.parsers.netskope import parse_netskope_log
    from src.parsers.paloalto import parse_paloalto_log
    from src.parsers.pihole import parse_pihole_log
    from src.parsers.squid import parse_squid_log
    from src.parsers.sysmon import parse_sysmon_log
    from src.parsers.umbrella import parse_umbrella_log
    from src.parsers.zscaler import parse_zscaler_log

    return {
        "pihole": parse_pihole_log,
        "squid": parse_squid_log,
        "zscaler": parse_zscaler_log,
        "paloalto": parse_paloalto_log,
        "umbrella": parse_umbrella_log,
        "fortinet": parse_fortinet_log,
        "aws_vpc_flow": parse_aws_vpc_flow_log,
        "entra_id": parse_entra_signin_log,
        "cloudflare_gateway": parse_cloudflare_gateway_log,
        "netskope": parse_netskope_log,
        "sysmon": parse_sysmon_log,
        "elastic_ecs": parse_elastic_ecs_log,
    }


_PARSER_DISPATCH: dict[str, Callable[..., pd.DataFrame]] | None = None


def _get_parser(log_format: str) -> Callable[..., pd.DataFrame]:
    global _PARSER_DISPATCH
    if _PARSER_DISPATCH is None:
        _PARSER_DISPATCH = _build_parser_dispatch()
    if log_format not in _PARSER_DISPATCH:
        supported = ", ".join(sorted(_PARSER_DISPATCH))
        raise ValueError(
            f"Unbekannter Parser {log_format!r}. Verfügbar: {supported}"
        )
    return _PARSER_DISPATCH[log_format]


def _bytes_to_temp(file_bytes: bytes, suffix: str = ".log") -> Path:
    """Schreibt File-Bytes in eine temporäre Datei (Parser akzeptieren nur Pfade)."""
    f = tempfile.NamedTemporaryFile(mode="wb", suffix=suffix, delete=False)
    f.write(file_bytes)
    f.close()
    return Path(f.name)


@st.cache_data(show_spinner="Analysiere Log…", max_entries=5, ttl=3600)
def run_pipeline(
    file_bytes: bytes,
    filename: str,
    salt: str,
    log_format: LogFormat,
) -> dict[str, Any]:
    """Führt Parser → Detection → Compliance → ReportContext-Aufbau aus.

    Caching erfolgt anhand von (file_bytes, filename, salt, log_format) automatisch.

    Returns:
        JSON-serialisiertes Dict (entspricht `context_to_json_dict()`).

    Raises:
        ValueError bei unbekanntem Format oder leerem Result.
    """
    if log_format == UNKNOWN_FORMAT:
        raise ValueError(
            "Log-Format konnte nicht erkannt werden. Bitte Format manuell "
            "über das Upload-Widget wählen oder siehe '📚 Formate'-Page."
        )

    parse_fn = _get_parser(log_format)
    pseudo = Pseudonymizer(key=salt.encode("utf-8"))
    tmp_path = _bytes_to_temp(file_bytes)
    try:
        df = parse_fn(tmp_path, pseudonymizer=pseudo)
    finally:
        tmp_path.unlink(missing_ok=True)

    if df.empty:
        raise ValueError(f"Keine parsbaren Einträge in {filename!r} gefunden.")

    policy = load_policy()
    df_trimmed = apply_retention(df, policy, log_type=log_format)
    retention_report = summarize(df, df_trimmed, policy, log_type=log_format)
    if df_trimmed.empty:
        raise ValueError(
            f"Nach Retention-Trim ({retention_report['days']} Tage) sind keine Einträge "
            f"mehr in {filename!r} vorhanden. Log-Horizont älter als Retention."
        )
    df = df_trimmed

    detection = DetectionEngine().analyze(df)
    compliance = ComplianceEngine().analyze(detection)
    ctx = build_context(detection, compliance, salt=salt)
    result = context_to_json_dict(ctx)
    result["user_patterns"] = _build_user_patterns(df, result["findings"], salt)
    result["retention"] = retention_report
    return result


def _build_user_patterns(
    df: pd.DataFrame,
    findings_json: list[dict[str, Any]],
    salt: str,
) -> dict[str, Any]:
    """Verhaltens-Auswertung pro Client für die 'Users & Patterns'-Page (E2-4).

    Liefert k-Anonymitäts-Check, Top-Clients-Ranking und eine pseudonymisierte
    Stunden-Heatmap. DataFrame wird vor Discard konsumiert; alle Client-Keys
    werden über pseudonymize_client auf `client_<hash>` normalisiert.
    """
    k = check_k_anonymity(df, field="client", minimum_k=5)

    heatmap = build_hourly_heatmap(df)
    heatmap_by_client: dict[str, list[int]] = {}
    if not heatmap.empty:
        for raw_client, row in heatmap.iterrows():
            heatmap_by_client[pseudonymize_client(str(raw_client), salt)] = [
                int(v) for v in row.tolist()
            ]

    by_client: dict[str, dict[str, Any]] = {}
    risk_rank = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    for f in findings_json:
        c = f["client_pseudonym"]
        entry = by_client.setdefault(c, {
            "client_pseudonym": c,
            "services": set(),
            "total_queries": 0,
            "risk_max": 0,
            "risk_level_max": "low",
            "upload_events": 0,
            "has_document_upload": False,
        })
        entry["services"].add(f["service"])
        entry["total_queries"] += f["total_queries"]
        if f["risk_score"] > entry["risk_max"]:
            entry["risk_max"] = f["risk_score"]
        if risk_rank.get(f["risk_level"], 0) > risk_rank.get(entry["risk_level_max"], 0):
            entry["risk_level_max"] = f["risk_level"]
        entry["upload_events"] += f.get("upload_events", 0)
        entry["has_document_upload"] = entry["has_document_upload"] or f.get("has_document_upload", False)

    top_clients = sorted(
        (
            {
                "client_pseudonym": e["client_pseudonym"],
                "service_count": len(e["services"]),
                "services": sorted(e["services"]),
                "total_queries": e["total_queries"],
                "risk_max": e["risk_max"],
                "risk_level_max": e["risk_level_max"],
                "upload_events": e["upload_events"],
                "has_document_upload": e["has_document_upload"],
            }
            for e in by_client.values()
        ),
        key=lambda e: (e["risk_max"], e["total_queries"]),
        reverse=True,
    )

    return {
        "k_anonymity": {
            "observed_k": k.observed_k,
            "minimum_k": k.minimum_k,
            "is_sufficient": k.is_sufficient,
            "reidentification_risk": k.reidentification_risk,
        },
        "top_clients": top_clients,
        "hourly_heatmap": heatmap_by_client,
    }


def reset_pipeline() -> None:
    """Setzt den Pipeline-State auf empty zurück. Behält Salt-Konfiguration."""
    keys = [
        "uploaded_filename", "uploaded_bytes", "detected_format",
        "report_data", "error_message",
    ]
    for k in keys:
        st.session_state[k] = None
    st.session_state.pipeline_state = "empty"
    st.session_state.filter_risk_levels = []
    st.session_state.filter_frameworks = []
    run_pipeline.clear()


def trigger_analysis() -> None:
    """Liest die hochgeladenen Bytes und startet die Pipeline. Setzt State."""
    fb = st.session_state.uploaded_bytes
    fname = st.session_state.uploaded_filename
    fmt = st.session_state.detected_format
    salt = st.session_state.report_salt

    if not fb or not fname or not fmt:
        st.session_state.pipeline_state = "error"
        st.session_state.error_message = "Datei oder Format fehlt."
        return

    st.session_state.pipeline_state = "analyzing"
    try:
        st.session_state.report_data = run_pipeline(fb, fname, salt, fmt)
        st.session_state.pipeline_state = "analyzed"
        st.session_state.error_message = None
        # DSGVO Art. 25: Klartext-Bytes nach Pseudonymisierung im Session-State verwerfen.
        st.session_state.uploaded_bytes = None
    except Exception as exc:
        st.session_state.pipeline_state = "error"
        st.session_state.error_message = f"{type(exc).__name__}: {exc}"
