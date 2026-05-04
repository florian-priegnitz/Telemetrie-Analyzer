"""Expander-Zeile für ein einzelnes Finding mit Compliance-Mappings als Sub-Tabelle."""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

from src.ui.components.badges import risk_badge


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

        _render_risk_score_breakdown(finding)


# Mirror der Schwellwerte aus src/detection/engine.py — bewusst dupliziert,
# weil die Page nur lesend visualisiert. Falls die Engine-Werte sich aendern,
# muss diese Map mitziehen (Test-Coverage in tests/test_findings_page.py).
_RISK_BASE = {"critical": 70, "high": 50, "medium": 30, "low": 10}
_UPLOAD_RISK_BOOST = 20
_OFF_HOURS_TRIGGER_RATIO = 0.3
_OFF_HOURS_RISK_BOOST = 15


def _render_risk_score_breakdown(finding: dict[str, Any]) -> None:
    """Zeigt die additiven Bestandteile des Risk-Scores nach engine.py-Logik."""
    risk_level = finding.get("risk_level", "low")
    is_systematic = bool(finding.get("is_systematic"))
    days_active = int(finding.get("days_active", 0) or 0)
    queries_per_day = float(finding.get("queries_per_day", 0) or 0)
    has_upload = bool(finding.get("has_document_upload"))
    off_hours = float(finding.get("off_hours_ratio", 0) or 0)
    score = int(finding.get("risk_score", 0) or 0)

    with st.expander("Risk-Score-Aufschluesselung", expanded=False):
        breakdown: list[str] = [f"**Gesamt: {score}/100**", ""]
        breakdown.append(
            f"- Basis-Risk ({risk_level}): {_RISK_BASE.get(risk_level, 30)}"
        )
        if is_systematic:
            breakdown.append("- Systematisch (>10 Q/Tag): +15")
        if days_active > 7:
            breakdown.append(f"- Tage aktiv ({days_active} > 7): +10")
        elif days_active > 1:
            breakdown.append(f"- Tage aktiv ({days_active} > 1): +5")
        if queries_per_day > 50:
            breakdown.append(f"- Queries/Tag ({queries_per_day:.1f} > 50): +5")
        if has_upload:
            breakdown.append(f"- Dokument-Upload (>500 KB): +{_UPLOAD_RISK_BOOST}")
        if off_hours > _OFF_HOURS_TRIGGER_RATIO:
            breakdown.append(
                f"- Off-Hours-Anteil ({off_hours:.0%} > "
                f"{_OFF_HOURS_TRIGGER_RATIO:.0%}): +{_OFF_HOURS_RISK_BOOST}"
            )
        breakdown.append("")
        breakdown.append(
            "_Score wird auf max. 100 gekappt. Quelle: "
            "`src/detection/engine.py:Finding.risk_score`._"
        )
        st.markdown("\n".join(breakdown))
