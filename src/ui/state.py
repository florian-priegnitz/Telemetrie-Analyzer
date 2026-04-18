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

import streamlit as st

from src.compliance.engine import ComplianceEngine
from src.detection.engine import DetectionEngine
from src.parsers.pihole import parse_pihole_log
from src.parsers.squid import parse_squid_log
from src.privacy.pseudonymizer import Pseudonymizer
from src.reports.context import build_context, context_to_json_dict
from src.reports.privacy import get_default_salt


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
    return context_to_json_dict(ctx)


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
