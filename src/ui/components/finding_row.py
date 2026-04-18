"""Expander-Zeile für ein einzelnes Finding mit Compliance-Mappings als Sub-Tabelle."""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

from src.ui.components.badges import risk_badge, severity_badge, status_badge


def render_finding_expander(finding: dict[str, Any]) -> None:
    service = finding.get("service", "?")
    provider = finding.get("provider", "?")
    risk_level = finding.get("risk_level", "low")
    risk_score = finding.get("risk_score", 0)
    client = finding.get("client_pseudonym", "?")
    qpd = finding.get("queries_per_day", 0)
    has_upload = finding.get("has_document_upload", False)

    upload_marker = " · 📄 Upload" if has_upload else ""
    header = (
        f"{service} ({provider}) — {risk_level} · "
        f"Score {risk_score} · {client} · {qpd}/Tag{upload_marker}"
    )

    with st.expander(header):
        col1, col2 = st.columns([2, 3])
        with col1:
            st.markdown(
                f"**Risiko:** {risk_badge(risk_level)}<br>"
                f"**Score:** {risk_score}/100<br>"
                f"**Kategorie:** {finding.get('category', '—')}<br>"
                f"**Systematisch:** {'Ja' if finding.get('is_systematic') else 'Nein'}<br>"
                f"**Tage aktiv:** {finding.get('days_active', '—')}",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"**Client (pseudonymisiert):** `{client}`<br>"
                f"**Queries gesamt:** {finding.get('total_queries', '—')}<br>"
                f"**Domains:** {', '.join(finding.get('domains', []))}<br>"
                f"**Upload-Volumen:** {finding.get('total_bytes_uploaded', 0):,} B "
                f"({finding.get('upload_events', 0)} Events &gt;500 KB)",
                unsafe_allow_html=True,
            )

        mappings = finding.get("compliance_mappings", [])
        if mappings:
            st.markdown("**Compliance-Mappings:**")
            df = pd.DataFrame([
                {
                    "Framework": m.get("framework"),
                    "Control": m.get("control_id"),
                    "Name": m.get("control_name"),
                    "Severity": m.get("severity"),
                    "Status": m.get("assessment_status"),
                    "Begründung": m.get("rationale"),
                } for m in mappings
            ])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Keine Compliance-Mappings für dieses Finding.")
