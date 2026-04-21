"""Upload-Widget mit Format-Detection und State-Transition.

Nach dem UI-Formats-Parity-Refactor (Sprint 7) unterstützt das Widget alle
12 Parser aus ``SUPPORTED_PARSERS``. Labels und Override-Dropdown werden
aus ``PARSER_LABELS`` (Single Source of Truth in ``src/parsers/detection.py``)
erzeugt.
"""

from __future__ import annotations

import streamlit as st

from src.parsers.detection import PARSER_LABELS, SUPPORTED_PARSERS
from src.ui.state import UNKNOWN_FORMAT, detect_log_format, reset_pipeline, trigger_analysis

_UPLOAD_LABEL = "Log-Datei (12 Formate — Auto-Detect)"
_UPLOAD_HELP = (
    "Pi-hole · Squid · Zscaler · PAN-OS · Umbrella · FortiGate · "
    "AWS VPC Flow · Entra ID · Cloudflare Gateway · Netskope · "
    "Sysmon · Elastic ECS — Details siehe Page **📚 Formate**."
)


def render_upload_section() -> None:
    """File-Uploader + Format-Anzeige + Analyse-Button."""
    uploaded = st.file_uploader(
        _UPLOAD_LABEL,
        type=["log", "txt", "csv", "json", "jsonl", "ndjson"],
        accept_multiple_files=False,
        key="_uploader",
        help=_UPLOAD_HELP,
    )

    if uploaded is not None and uploaded.name != st.session_state.get("uploaded_filename"):
        file_bytes = uploaded.read()
        if not file_bytes:
            st.error("Die hochgeladene Datei ist leer.")
            return
        detected = detect_log_format(file_bytes)
        st.session_state.uploaded_bytes = file_bytes
        st.session_state.uploaded_filename = uploaded.name
        st.session_state.detected_format = detected
        st.session_state.pipeline_state = "uploaded"
        st.session_state.report_data = None
        st.session_state.error_message = None

    fname = st.session_state.get("uploaded_filename")
    fmt = st.session_state.get("detected_format")
    if not (fname and fmt):
        return

    if fmt == UNKNOWN_FORMAT:
        st.warning(
            f"**{fname}** — Format **nicht erkannt**. "
            "Bitte unten manuell auswählen oder siehe 📚 Formate-Page für "
            "unterstützte Varianten."
        )
        override = st.selectbox(
            "Format manuell wählen",
            options=list(SUPPORTED_PARSERS),
            format_func=lambda key: PARSER_LABELS.get(key, key),
            key="_format_override",
        )
        col_a, col_b = st.columns(2)
        if col_a.button("Format anwenden", use_container_width=True):
            st.session_state.detected_format = override
            st.rerun()
        if col_b.button("🗑 Reset", use_container_width=True):
            reset_pipeline()
            st.rerun()
        return

    # Erkanntes Format (oder manuell zugewiesen): zeige Label + Analyse-Button
    label = PARSER_LABELS.get(fmt, fmt)
    st.success(f"**{fname}** · Format: **{label}**")
    st.caption("ℹ️ Details zum Parsing und Feld-Mapping siehe Page **📚 Formate**.")

    state = st.session_state.get("pipeline_state")
    disabled = state == "analyzing"
    has_bytes = bool(st.session_state.get("uploaded_bytes"))

    # Nach erfolgreicher Analyse sind die Klartext-Bytes aus DSGVO-Gruenden
    # geloescht — "Neu analysieren" benoetigt einen erneuten Upload.
    if state == "analyzed" and not has_bytes:
        st.info("Analyse abgeschlossen. Für eine neue Analyse bitte die Datei erneut hochladen.")
    elif has_bytes:
        if st.button(
            "🚀 Analyse starten" if state != "analyzed" else "🔄 Neu analysieren",
            disabled=disabled, use_container_width=True,
        ):
            trigger_analysis()
            st.rerun()

    if st.button("🗑 Reset", use_container_width=True):
        reset_pipeline()
        st.rerun()
