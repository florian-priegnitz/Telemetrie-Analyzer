"""Übersichts-Page: KPIs, Compliance-Ampel, 2 Charts, Top-3-Findings."""

from __future__ import annotations

from typing import Any

import streamlit as st

from src.ui.components.badges import risk_badge
from src.ui.components.kpi_row import render_kpi_row
from src.ui.components.traffic_light import render_compliance_traffic_light


def render(report_data: dict[str, Any]) -> None:
    st.title("📊 Übersicht")
    summary = report_data.get("summary", {})
    period = report_data.get("report_meta", {}).get("period", {})

    st.caption(
        f"Zeitraum: {period.get('start', '—')[:10]} bis {period.get('end', '—')[:10]} · "
        f"{summary.get('unique_ai_services', 0)} KI-Dienste erkannt · "
        f"{summary.get('unique_clients', 0)} betroffene Clients"
    )

    render_kpi_row(report_data)
    st.markdown("")
    render_compliance_traffic_light(report_data)

    # Für Charts brauchen wir einen ReportContext — aus dem Dict re-hydrieren wäre umständlich.
    # Pragmatik: wir nutzen die Daten direkt aus dem Dict für eigene Streamlit-Charts.
    st.markdown("### Compliance-Score pro Framework")
    framework_scores = report_data.get("framework_scores", [])
    if framework_scores:
        import plotly.graph_objects as go
        labels = [fv["framework_label"] for fv in framework_scores]
        scores = [fv["score_percent"] for fv in framework_scores]
        colors = ["#0E8A16" if s >= 80 else "#D4A72C" if s >= 50 else "#B60205" for s in scores]
        fig = go.Figure(data=[go.Bar(
            x=labels, y=scores, marker_color=colors,
            text=[f"{s:.1f}%" for s in scores], textposition="outside",
        )])
        fig.update_layout(height=350, yaxis=dict(range=[0, 105], title="Erfüllt %"),
                          margin=dict(l=20, r=20, t=20, b=40))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Keine Framework-Scores verfügbar.")

    st.markdown("### Top-Risiken")
    findings = sorted(
        report_data.get("findings", []),
        key=lambda f: f.get("risk_score", 0),
        reverse=True,
    )[:3]
    if findings:
        for i, f in enumerate(findings, 1):
            st.markdown(
                f"**{i}. {f.get('service', 'Unbekannt')}** ({f.get('provider', '—')}) — "
                f"{risk_badge(f.get('risk_level', 'low'))} Score **{f.get('risk_score', 0)}** · "
                f"{f.get('queries_per_day', 0)} Queries/Tag durch `{f.get('client_pseudonym', '—')}`"
                + (" · 📄 **Dokument-Upload erkannt**" if f.get("has_document_upload") else ""),
                unsafe_allow_html=True,
            )
    else:
        st.success("Keine Findings im Analysezeitraum — keine Shadow AI erkannt.")
