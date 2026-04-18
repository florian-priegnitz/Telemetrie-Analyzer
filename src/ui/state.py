"""Pipeline-Wrapper für die Streamlit-UI.

Einziger Punkt, an dem die UI mit der Analyse-Pipeline spricht. Pages/Components
importieren ausschliesslich aus diesem Modul (+ Components untereinander).

Caching: Wir cachen das JSON-Dict (nicht den ReportContext), weil ReportContext
Datetime + Dataclass-Listen enthält, die für Streamlits Hash-Funktion problematisch
sind. Aus dem Dict baut die UI bei Bedarf die Anzeige-Strukturen.
"""

from __future__ import annotations

import re
import tempfile
from pathlib import Path
from typing import Any, Literal

import pandas as pd
import streamlit as st

from src.analytics.temporal import build_hourly_heatmap
from src.compliance.engine import ComplianceEngine
from src.detection.engine import DetectionEngine
from src.parsers.pihole import parse_pihole_log
from src.parsers.squid import parse_squid_log
from src.privacy.k_anonymity import check_k_anonymity
from src.privacy.pseudonymizer import Pseudonymizer
from src.reports.context import build_context, context_to_json_dict
from src.reports.privacy import get_default_salt, pseudonymize_client


PipelineState = Literal["empty", "uploaded", "analyzing", "analyzed", "error"]
LogFormat = Literal["pihole", "squid", "unknown"]

_PIHOLE_PATTERN = re.compile(
    r"^\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+dnsmasq\[\d+\]:\s+query\["
)
_SQUID_NATIVE_PATTERN = re.compile(r"^\d+\.\d+\s+\d+\s+\S+\s+\S+/\d+\s+\d+\s+")


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
    """Heuristische Format-Erkennung anhand der ersten 20 nicht-leeren Zeilen.

    Mehrheits-Voting gegen die beiden Regex-Muster.
    """
    if isinstance(content, bytes):
        text = content.decode("utf-8", errors="replace")
    else:
        text = content

    pihole_hits = 0
    squid_hits = 0
    sample = 0
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        sample += 1
        if _PIHOLE_PATTERN.match(line):
            pihole_hits += 1
        elif _SQUID_NATIVE_PATTERN.match(line):
            squid_hits += 1
        if sample >= 20:
            break

    if pihole_hits == 0 and squid_hits == 0:
        return "unknown"
    return "pihole" if pihole_hits >= squid_hits else "squid"


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
    if log_format == "unknown":
        raise ValueError("Log-Format konnte nicht erkannt werden.")

    pseudo = Pseudonymizer(key=salt.encode("utf-8"))
    tmp_path = _bytes_to_temp(file_bytes)
    try:
        if log_format == "pihole":
            df = parse_pihole_log(tmp_path, pseudonymizer=pseudo)
        else:
            df = parse_squid_log(tmp_path, pseudonymizer=pseudo)
    finally:
        tmp_path.unlink(missing_ok=True)

    if df.empty:
        raise ValueError(f"Keine parsbaren Einträge in {filename!r} gefunden.")

    detection = DetectionEngine().analyze(df)
    compliance = ComplianceEngine().analyze(detection)
    ctx = build_context(detection, compliance, salt=salt)
    result = context_to_json_dict(ctx)
    result["user_patterns"] = _build_user_patterns(df, result["findings"], salt)
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
