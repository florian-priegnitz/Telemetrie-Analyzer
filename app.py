"""Telemetrie Analyzer — Streamlit Dashboard.

Start lokal:
    streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from src.ui.branding import FAVICON_PATH, inject_global_css, render_lineal
from src.ui.components.upload_widget import render_upload_section
from src.ui.pages import (
    compliance,
    findings,
    formats,
    overview,
    sessions,
    settings,
    users_patterns,
)
from src.ui.state import init_session_state

_PAGE_FUNCS = {
    "📊 Übersicht": overview.render,
    "🔍 Findings": findings.render,
    "👥 Users & Patterns": users_patterns.render,
    "🔗 Sessions": sessions.render,
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
        page_icon=str(FAVICON_PATH) if FAVICON_PATH.exists() else "🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    init_session_state()
    inject_global_css()

    with st.sidebar:
        render_lineal()
        st.markdown(
            '<div class="ta-meta">SHADOW AI · COMPLIANCE</div>',
            unsafe_allow_html=True,
        )
        st.title("Telemetrie Analyzer")
        st.caption("DORA · EU AI Act · ISO 42001 · ISO 27001 · DSGVO · CRA")
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

    render_lineal()

    if state in ("empty", "uploaded") and page not in _STATE_INDEPENDENT_PAGES:
        from src.ui.components.upload_widget import render_scenario_buttons

        st.markdown("## 👋 Willkommen beim Telemetrie Analyzer")
        st.markdown(
            "Shadow-AI-Detection für 12 Telemetrie-Log-Formate, mit Compliance-Mapping auf "
            "**DORA · EU AI Act · ISO 42001 · ISO 27001 · DSGVO**."
        )

        col_left, col_right = st.columns([3, 2])
        with col_left:
            st.markdown("### 🎬 Direkt mit einem Demo starten")
            st.caption(
                "Kein Log zur Hand? Ein Klick lädt eines der synthetischen Samples "
                "(RFC 1918 IPs, keine PII) in die Pipeline — dann links **🚀 Analyse starten**."
            )
            render_scenario_buttons(key_prefix="welcome")

        with col_right:
            st.markdown("### 📖 Oder eigenes Log hochladen")
            st.markdown(
                "- Upload-Widget in der Sidebar (12 Formate, Auto-Detect)\n"
                "- `.log` / `.csv` / `.json` / `.jsonl` / `.ndjson`\n"
                "- Bei unbekanntem Format: manueller Dropdown\n"
                "- Rohdaten werden **nur in-memory** verarbeitet, "
                "Pseudonymisierung läuft schon im Parser\n\n"
                "Siehe Page **📚 Formate** für Feld-Mapping pro Tool und Testdata-Downloads."
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
