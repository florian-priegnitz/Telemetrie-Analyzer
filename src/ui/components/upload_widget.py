"""Upload-Widget mit Format-Detection und State-Transition."""

from __future__ import annotations

import streamlit as st

from src.ui.state import detect_log_format, reset_pipeline, trigger_analysis


def render_upload_section() -> None:
    """File-Uploader + Format-Anzeige + Analyse-Button."""
    uploaded = st.file_uploader(
        "Log-Datei (Pi-hole oder Squid)",
        type=["log", "txt", "csv"],
        accept_multiple_files=False,
        key="_uploader",
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
    if fname and fmt:
        fmt_label = {"pihole": "Pi-hole DNS", "squid": "Squid Proxy", "unknown": "Unbekannt"}
        st.caption(f"**{fname}** — Format: {fmt_label.get(fmt, fmt)}")

        if fmt == "unknown":
            override = st.selectbox(
                "Format manuell wählen",
                options=["pihole", "squid"],
                key="_format_override",
            )
            if st.button("Format anwenden"):
                st.session_state.detected_format = override
                st.rerun()
        else:
            state = st.session_state.get("pipeline_state")
            disabled = state == "analyzing"
            # Nach erfolgreicher Analyse sind die Klartext-Bytes aus DSGVO-Gruenden
            # geloescht — "Neu analysieren" benoetigt einen erneuten Upload.
            has_bytes = bool(st.session_state.get("uploaded_bytes"))
            if state == "analyzed" and not has_bytes:
                st.info("Analyse abgeschlossen. Fuer eine neue Analyse bitte die Datei erneut hochladen.")
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
