"""Plotly-Chart-Helfer für Reports.

Alle Achsen-Labels MÜSSEN pseudonymisiert sein (keine Klartext-IPs).
Die Charts werden als HTML-Snippets (`<div>...`) zurückgegeben — `include_plotlyjs="cdn"`
um Report-Größe klein zu halten.
"""

from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go

from src.reports.context import ReportContext


_PLOTLY_KW = dict(include_plotlyjs="cdn", full_html=False)
_OFFLINE_KW = dict(include_plotlyjs="inline", full_html=False)
_RISK_COLORS = {"critical": "#B60205", "high": "#D93F0B", "medium": "#FBCA04", "low": "#0E8A16"}
_TRAFFIC_COLORS = {"green": "#0E8A16", "yellow": "#FBCA04", "red": "#B60205"}


def _kw(offline: bool) -> dict:
    return _OFFLINE_KW if offline else _PLOTLY_KW


def _empty_fallback(message: str, as_figure: bool) -> "str | go.Figure":
    """Liefert Fallback je nach Output-Modus."""
    if as_figure:
        fig = go.Figure()
        fig.add_annotation(text=message, showarrow=False, font=dict(size=14, color="#57606a"))
        fig.update_layout(height=200, xaxis=dict(visible=False), yaxis=dict(visible=False))
        return fig
    return f"<p><em>{message}</em></p>"


def render_framework_scores_bar(
    ctx: ReportContext, offline: bool = False, as_figure: bool = False,
) -> "str | go.Figure":
    """Bar-Chart: Compliance-Score pro Framework (Executive)."""
    if not ctx.framework_scores:
        return _empty_fallback("Keine Framework-Scores verfügbar.", as_figure)

    labels = [fv.framework_label for fv in ctx.framework_scores]
    scores = [fv.score_percent for fv in ctx.framework_scores]
    colors = [_TRAFFIC_COLORS[
        "green" if s >= 80 else "yellow" if s >= 50 else "red"
    ] for s in scores]

    fig = go.Figure(data=[go.Bar(x=labels, y=scores, marker_color=colors,
                                  text=[f"{s:.1f}%" for s in scores], textposition="outside")])
    fig.update_layout(
        title="Compliance-Score pro Framework",
        yaxis=dict(title="Erfüllungsgrad (%)", range=[0, 105]),
        xaxis=dict(title=""),
        height=380, margin=dict(l=40, r=20, t=60, b=40),
    )
    if as_figure:
        return fig
    return fig.to_html(**_kw(offline))


def render_risk_distribution_donut(
    ctx: ReportContext, offline: bool = False, as_figure: bool = False,
) -> "str | go.Figure":
    """Donut-Chart: Verteilung der Findings nach Risk-Level (IT-Security)."""
    if not ctx.findings:
        return _empty_fallback("Keine Findings.", as_figure)

    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for f in ctx.findings:
        counts[f.risk_level] = counts.get(f.risk_level, 0) + 1

    labels = list(counts.keys())
    values = list(counts.values())
    colors = [_RISK_COLORS[label] for label in labels]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5, marker_colors=colors)])
    fig.update_layout(title="Findings nach Risiko-Stufe", height=350,
                      margin=dict(l=20, r=20, t=60, b=20))
    if as_figure:
        return fig
    return fig.to_html(**_kw(offline))


def render_top_clients_bar(
    ctx: ReportContext, top_n: int = 10, offline: bool = False, as_figure: bool = False,
) -> "str | go.Figure":
    """Horizontaler Bar-Chart: Top-N pseudonymisierte Clients nach Anzahl Findings."""
    if not ctx.findings:
        return _empty_fallback("Keine Findings.", as_figure)

    by_client: dict[str, int] = {}
    for f in ctx.findings:
        by_client[f.client_pseudonym] = by_client.get(f.client_pseudonym, 0) + 1

    items = sorted(by_client.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
    labels = [k for k, _ in items][::-1]
    values = [v for _, v in items][::-1]

    fig = go.Figure(data=[go.Bar(x=values, y=labels, orientation="h", marker_color="#1D76DB")])
    fig.update_layout(
        title=f"Top {top_n} Clients nach Findings (pseudonymisiert)",
        xaxis=dict(title="Anzahl Findings"),
        yaxis=dict(title=""),
        height=max(280, len(items) * 28 + 100),
        margin=dict(l=120, r=20, t=60, b=40),
    )
    if as_figure:
        return fig
    return fig.to_html(**_kw(offline))


def render_severity_stacked_bar(
    ctx: ReportContext, offline: bool = False, as_figure: bool = False,
) -> "str | go.Figure":
    """Stacked-Bar: Severity-Verteilung pro Framework (Compliance)."""
    if not ctx.framework_scores:
        return _empty_fallback("Keine Framework-Scores verfügbar.", as_figure)

    frameworks = [fv.framework_label for fv in ctx.framework_scores]
    fig = go.Figure()
    for sev in ("critical", "high", "medium", "low"):
        fig.add_trace(go.Bar(
            name=sev.capitalize(),
            x=frameworks,
            y=[fv.severity_counts.get(sev, 0) for fv in ctx.framework_scores],
            marker_color=_RISK_COLORS[sev],
        ))
    fig.update_layout(
        barmode="stack",
        title="Severity-Verteilung pro Framework",
        yaxis=dict(title="Anzahl Mappings"),
        height=380, margin=dict(l=40, r=20, t=60, b=40),
    )
    if as_figure:
        return fig
    return fig.to_html(**_kw(offline))


def build_all_charts(ctx: ReportContext, offline: bool = False) -> dict[str, str]:
    """Rendert alle Charts und gibt ein Dict {chart_name: html_snippet} zurück."""
    return {
        "framework_scores_bar": render_framework_scores_bar(ctx, offline=offline),
        "risk_distribution_donut": render_risk_distribution_donut(ctx, offline=offline),
        "top_clients_bar": render_top_clients_bar(ctx, offline=offline),
        "severity_stacked_bar": render_severity_stacked_bar(ctx, offline=offline),
    }


def build_all_figures(ctx: ReportContext) -> dict[str, "go.Figure"]:
    """Rendert alle Charts als plotly Figure-Objekte (für Streamlit st.plotly_chart)."""
    return {
        "framework_scores_bar": render_framework_scores_bar(ctx, as_figure=True),
        "risk_distribution_donut": render_risk_distribution_donut(ctx, as_figure=True),
        "top_clients_bar": render_top_clients_bar(ctx, as_figure=True),
        "severity_stacked_bar": render_severity_stacked_bar(ctx, as_figure=True),
    }
