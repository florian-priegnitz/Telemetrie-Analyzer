"""Findings-Page mit Filter-Sidebar + Tabelle + Expander."""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

from src.ui.components.finding_row import render_finding_expander

_RISK_LEVELS = ["critical", "high", "medium", "low"]
_FRAMEWORKS = ["DORA", "EU_AI_ACT", "ISO_42001", "ISO_27001", "DSGVO"]


def render(report_data: dict[str, Any]) -> None:
    st.title("🔍 Findings")
    findings = report_data.get("findings", [])

    if not findings:
        st.success("Keine Findings — keine Shadow AI im Analysezeitraum.")
        return

    # Sidebar-Filter
    with st.sidebar:
        st.markdown("### Filter")
        selected_risk = st.multiselect(
            "Risk-Level",
            options=_RISK_LEVELS,
            default=st.session_state.get("filter_risk_levels") or _RISK_LEVELS,
            key="filter_risk_levels",
        )
        selected_fw = st.multiselect(
            "Framework (mind. 1 Mapping)",
            options=_FRAMEWORKS,
            default=st.session_state.get("filter_frameworks") or _FRAMEWORKS,
            key="filter_frameworks",
        )
        service_filter = st.text_input("Service enthält…", key="filter_service")

    filtered = [
        f for f in findings
        if f.get("risk_level") in selected_risk
        and any(m.get("framework") in selected_fw for m in f.get("compliance_mappings", []))
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
