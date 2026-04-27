"""Findings-Page mit Filter-Sidebar + Tabelle + Expander."""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

from src.ui.components.finding_row import render_finding_expander
from src.ui.components.help import page_intro

_RISK_LEVELS = ["critical", "high", "medium", "low"]
_FRAMEWORKS = ["DORA", "EU_AI_ACT", "ISO_42001", "ISO_27001", "DSGVO"]


def render(report_data: dict[str, Any]) -> None:
    st.title("🔍 Findings")
    page_intro(
        title="Findings",
        what_you_see=(
            "Jede Zeile ist ein **Finding** = ein Client × KI-Service über den gesamten "
            "Analysezeitraum. Sortiert nach Risk-Score absteigend. Die Sidebar filtert "
            "nach Risk-Level und Framework; mit Klick auf eine Zeile öffnet sich ein "
            "Expander mit Domains, Compliance-Mappings, Upload-Events und ggf. "
            "LLM-generierter Empfehlung."
        ),
        key_terms=("risk_score", "compliance_mapping", "systematic_threshold", "upload_threshold"),
    )
    findings = report_data.get("findings", [])

    if not findings:
        st.success("Keine Findings — keine Shadow AI im Analysezeitraum.")
        return

    # Sidebar-Filter. Keys sind absichtlich NICHT in init_session_state
    # vorbelegt, damit Streamlit den `default` beim ersten Render nutzt.
    with st.sidebar:
        st.markdown("### Filter")
        selected_risk = st.multiselect(
            "Risk-Level",
            options=_RISK_LEVELS,
            default=_RISK_LEVELS,
            key="filter_risk_levels",
            help="Leere Auswahl = alle anzeigen.",
        )
        selected_fw = st.multiselect(
            "Framework (mind. 1 Mapping)",
            options=_FRAMEWORKS,
            default=_FRAMEWORKS,
            key="filter_frameworks",
            help="Leere Auswahl = alle anzeigen.",
        )
        service_filter = st.text_input("Service enthält…", key="filter_service")

    # Defensive Filter-Semantik: leere Multiselect-Auswahl = kein Filter (alle zeigen).
    risk_filter_active = bool(selected_risk)
    fw_filter_active = bool(selected_fw)

    filtered = [
        f for f in findings
        if (not risk_filter_active or f.get("risk_level") in selected_risk)
        and (not fw_filter_active or any(
            m.get("framework") in selected_fw
            for m in f.get("compliance_mappings", [])
        ))
        and (not service_filter or service_filter.lower() in f.get("service", "").lower())
    ]

    st.caption(f"**{len(filtered)}** von {len(findings)} Findings nach Filter angezeigt.")

    if not filtered:
        st.info("Keine Findings entsprechen den Filterkriterien.")
        return

    df = pd.DataFrame([
        {
            "Service": f["service"],
            "Provider": f["provider"],
            "Risk": f["risk_level"],
            "Score": f["risk_score"],
            "Client": f["client_pseudonym"],
            "Q/Tag": f["queries_per_day"],
            "Sys.": "✓" if f.get("is_systematic") else "—",
            "Upload": "📄" if f.get("has_document_upload") else "—",
        } for f in filtered
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("### Detail")
    for f in filtered:
        render_finding_expander(f)
