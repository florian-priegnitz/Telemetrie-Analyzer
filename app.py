"""Telemetrie Analyzer — Streamlit Dashboard.

Start lokal:
    streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from src.ui.components.upload_widget import render_upload_section
from src.ui.pages import compliance, findings, formats, overview, settings, users_patterns
from src.ui.state import init_session_state


_PAGE_FUNCS = {
    "📊 Übersicht": overview.render,
    "🔍 Findings": findings.render,
    "👥 Users & Patterns": users_patterns.render,
    "📋 Compliance": compliance.render,
    "📚 Formate": formats.render,
    "⚙️ Einstellungen": settings.render,
}

# Pages, die unabhaengig vom Pipeline-State erreichbar sind (zeigen eigene Inhalte
# ohne Analyse-Ergebnisse). Alle anderen Pages verlangen zuerst eine Analyse.
_STATE_INDEPENDENT_PAGES = {"📚 Formate", "⚙️ Einstellungen"}


def main() -> None:
    st.set_page_config(
        page_title="Telemetrie Analyzer",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    init_session_state()

    with st.sidebar:
        st.title("🛡️ Telemetrie Analyzer")
        st.caption("Shadow AI Detection · DORA · EU AI Act · ISO 42001 · ISO 27001 · DSGVO")
        st.markdown("---")

        st.markdown("### 📁 Log-Upload")
        render_upload_section()
        st.markdown("---")

        st.markdown("### Navigation")
        page = st.radio(
            "Page", list(_PAGE_FUNCS.keys()), label_visibility="collapsed",
        )
        st.markdown("---")

        # Status-Anzeige
        state = st.session_state.get("pipeline_state", "empty")
        state_label = {
            "empty": "📭 Keine Daten",
            "uploaded": "📥 Bereit zur Analyse",
            "analyzing": "⏳ Analysiere…",
            "analyzed": "✅ Analyse fertig",
            "error": "❌ Fehler",
        }
        st.caption(f"**Status:** {state_label.get(state, state)}")

        salt_fp = (
            (st.session_state.get("report_data") or {})
            .get("report_meta", {}).get("salt_fingerprint", "—")
        )
        st.caption(f"**Pseudonym:** ✓ AKTIV · Salt-FP `{salt_fp}`")

    if state == "error":
        st.error(f"Fehler bei der Analyse: {st.session_state.get('error_message', 'unbekannt')}")
        return

    if state in ("empty", "uploaded") and page not in _STATE_INDEPENDENT_PAGES:
        st.info(
            "👈 Bitte zuerst eine Log-Datei hochladen und 'Analyse starten' klicken. "
            "Siehe **📚 Formate** für alle unterstützten Dateitypen inkl. Sample-Downloads."
        )
        return

    if page in _STATE_INDEPENDENT_PAGES:
        _PAGE_FUNCS[page](st.session_state.get("report_data"))
    else:
        report_data = st.session_state.get("report_data")
        if not report_data:
            st.warning("Bitte erst Analyse starten.")
            return
        _PAGE_FUNCS[page](report_data)


if __name__ == "__main__":
    main()
