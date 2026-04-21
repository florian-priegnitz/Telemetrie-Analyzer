"""Compliance-Page: 5 Tabs für Frameworks mit Score-Cards + Mapping-Tabellen."""

from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.ui.components.framework_card import render_framework_card

_RISK_COLORS = {"critical": "#B60205", "high": "#D93F0B", "medium": "#FBCA04", "low": "#0E8A16"}

# Assessment-Status → Emoji-Badge (kurz + scanbar in Tabellen)
_STATUS_BADGES = {
    "non_compliant": "❌ non-compliant",
    "partially_compliant": "⚠️ partially",
    "needs_review": "🔍 needs review",
    "compliant": "✅ compliant",
}


def _format_status(raw: str | None) -> str:
    if not raw:
        return "—"
    return _STATUS_BADGES.get(raw, raw)


def render(report_data: dict[str, Any]) -> None:
    st.title("📋 Compliance")

    framework_scores = report_data.get("framework_scores", [])
    findings = report_data.get("findings", [])

    if not framework_scores:
        st.info("Keine Compliance-Scores verfügbar — bitte zuerst Analyse durchführen.")
        return

    # Cross-Framework-Summary über allen Tabs
    summary = report_data.get("summary", {})
    overall_percent = summary.get("overall_compliance_percent", 0)
    total_findings = len(findings)
    st.markdown(
        f"**Übergreifender Compliance-Score:** {overall_percent:.1f}% · "
        f"**{total_findings}** Findings betreffen insgesamt "
        f"{sum(len(f.get('compliance_mappings', [])) for f in findings)} Kontroll-Verletzungen "
        f"über {len(framework_scores)} Frameworks."
    )
    st.caption(
        "Jeder Tab zeigt einen Score zwischen 0 und 100%. Ein Finding kann mehrere "
        "Kontrollen in mehreren Frameworks gleichzeitig verletzen."
    )

    # Stable Order (analog Compliance-Modell)
    order = ["DORA", "EU_AI_ACT", "ISO_42001", "ISO_27001", "DSGVO"]
    fw_by_id = {fv["framework"]: fv for fv in framework_scores}
    ordered = [fw_by_id[fw_id] for fw_id in order if fw_id in fw_by_id]

    tab_labels = [fv["framework_label"] for fv in ordered]
    tabs = st.tabs(tab_labels)

    for tab, fv in zip(tabs, ordered):
        with tab:
            render_framework_card(fv)

            # Severity-Verteilung
            sev = fv.get("severity_counts", {})
            if any(sev.values()):
                fig = go.Figure(data=[go.Bar(
                    x=["critical", "high", "medium", "low"],
                    y=[sev.get(k, 0) for k in ("critical", "high", "medium", "low")],
                    marker_color=[_RISK_COLORS[k] for k in ("critical", "high", "medium", "low")],
                )])
                fig.update_layout(
                    height=260, title="Severity der Mappings",
                    margin=dict(l=20, r=20, t=40, b=20),
                )
                st.plotly_chart(fig, use_container_width=True)

            # Mapping-Tabelle: alle Mappings für dieses Framework
            rows = []
            for f in findings:
                for m in f.get("compliance_mappings", []):
                    if m.get("framework") != fv["framework"]:
                        continue
                    rows.append({
                        "Control": m.get("control_id"),
                        "Control-Name": m.get("control_name"),
                        "Service": f.get("service"),
                        "Severity": m.get("severity"),
                        "Status": _format_status(m.get("assessment_status")),
                        "Begründung": m.get("rationale"),
                    })
            if rows:
                st.markdown(f"**{len(rows)} Kontroll-Verletzungen für "
                            f"{fv['framework_label']}:**")
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            else:
                st.success(f"Keine Verletzungen für {fv['framework_label']}.")
