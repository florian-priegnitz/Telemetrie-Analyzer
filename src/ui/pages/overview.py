"""Übersichts-Page: KPIs, Compliance-Ampel, Charts, Top-3-Findings + Report-Export."""

from __future__ import annotations

import json
from typing import Any

import streamlit as st

from src.ui.components.badges import risk_badge
from src.ui.components.db_status import render_db_status
from src.ui.components.help import glossary_block, page_intro
from src.ui.components.kpi_row import render_kpi_row
from src.ui.components.traffic_light import render_compliance_traffic_light

_AUDIENCE_LABELS = {
    "executive": "Executive / CISO",
    "it_sec": "IT-Security",
    "compliance": "Compliance-Officer",
}
_FORMAT_LABELS = {
    "html": "HTML (Browser)",
    "markdown": "Markdown (.md)",
    "json": "JSON (maschinenlesbar)",
}
_MIME_TYPES = {
    "html": "text/html",
    "markdown": "text/markdown",
    "json": "application/json",
}


def _render_export_section(report_data: dict[str, Any]) -> None:
    """Report-Export-Panel: Audience + Format wählen, Download-Button generiert Datei on-demand."""
    with st.expander("📥 **Report exportieren**", expanded=False):
        st.caption(
            "Erzeugt einen pseudonymisierten Report zum Herunterladen. "
            "Drei Zielgruppen-Templates × drei Formate. JSON ist die "
            "maschinenlesbare Struktur für Downstream-Pipelines."
        )
        c_aud, c_fmt = st.columns(2)
        audience = c_aud.selectbox(
            "Zielgruppe",
            options=list(_AUDIENCE_LABELS),
            format_func=lambda k: _AUDIENCE_LABELS[k],
            key="export_audience",
        )
        fmt = c_fmt.selectbox(
            "Format",
            options=list(_FORMAT_LABELS),
            format_func=lambda k: _FORMAT_LABELS[k],
            key="export_format",
        )

        if st.button("🎯 Report generieren", use_container_width=True):
            st.session_state["_export_ready"] = _generate_export(report_data, audience, fmt)

        export = st.session_state.get("_export_ready")
        if export and export.get("audience") == audience and export.get("format") == fmt:
            st.download_button(
                label=f"⬇ {export['filename']} ({len(export['data'])/1024:.1f} KB)",
                data=export["data"],
                file_name=export["filename"],
                mime=_MIME_TYPES[fmt],
                use_container_width=True,
            )
            st.success(f"Report bereit: **{_AUDIENCE_LABELS[audience]}** · "
                       f"{_FORMAT_LABELS[fmt]}")


def _generate_export(report_data: dict[str, Any], audience: str, fmt: str) -> dict[str, Any]:
    """Gibt ein vor-gerendertes Artefakt zurück.

    HTML/Markdown werden während ``run_pipeline()`` pre-rendered und im
    ``report_data["_exports"]``-Block abgelegt, solange die
    DetectionResult-Objekte in-scope sind (nach DSGVO-Reset nicht mehr
    rekonstruierbar). Hier nur Lookup + Download-Bundle bauen.
    """
    if fmt == "json":
        data = json.dumps(report_data, default=str, indent=2, ensure_ascii=False).encode("utf-8")
        return {
            "audience": audience, "format": fmt,
            "filename": f"telemetrie_report_{audience}.json",
            "data": data,
        }

    exports = report_data.get("_exports", {})
    if "error" in exports:
        st.error(f"Export nicht verfügbar: {exports['error']}")
        return {}

    bundle = exports.get(fmt, {})
    rendered = bundle.get(audience) if isinstance(bundle, dict) else None
    if not rendered:
        st.error(f"Kein {fmt}-Report für {audience} verfügbar.")
        return {}

    ext = "html" if fmt == "html" else "md"
    return {
        "audience": audience, "format": fmt,
        "filename": f"telemetrie_report_{audience}.{ext}",
        "data": rendered.encode("utf-8"),
    }


def render(report_data: dict[str, Any]) -> None:
    st.title("📊 Übersicht")
    page_intro(
        title="Übersicht",
        what_you_see=(
            "Schnellüberblick über alle erkannten Schatten-KI-Befunde im hochgeladenen "
            "Log. Vier KPI-Karten oben zeigen Volumen und Reichweite, die "
            "**Compliance-Ampel** zeigt den Erfüllungsgrad pro Framework, und unten "
            "lassen sich Reports direkt für drei Zielgruppen exportieren "
            "(Executive / IT-Security / Compliance × HTML / Markdown / JSON)."
        ),
        key_terms=("erfuellungsgrad", "compliance_ampel", "risk_score", "compliance_mapping"),
    )
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
    st.markdown("")
    _render_export_section(report_data)

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

    st.markdown("---")
    render_db_status(compact=True)

    glossary_block([
        "risk_score",
        "compliance_ampel",
        "endpoint_db_freshness",
        "pseudonymisierung",
    ])
