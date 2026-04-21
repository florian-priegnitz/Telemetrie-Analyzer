"""Inline-HTML-Badges für Risk-Level, Severity, Compliance-Status."""

from __future__ import annotations

_RISK_COLORS = {
    "critical": ("#B60205", "#FFFFFF", "🔴"),
    "high": ("#D93F0B", "#FFFFFF", "🟠"),
    "medium": ("#FBCA04", "#1f2328", "🟡"),
    "low": ("#0E8A16", "#FFFFFF", "🟢"),
}

_STATUS_COLORS = {
    "non_compliant": ("#B60205", "#FFFFFF", "❌"),
    "partially_compliant": ("#FBCA04", "#1f2328", "⚠️"),
    "needs_review": ("#BFD4F2", "#1f2328", "🔍"),
    "compliant": ("#0E8A16", "#FFFFFF", "✅"),
}

_TRAFFIC_LIGHT = {
    "green": "#0E8A16",
    "yellow": "#D4A72C",
    "red": "#B60205",
}


def risk_badge(level: str) -> str:
    bg, fg, icon = _RISK_COLORS.get(level, ("#888", "#fff", "•"))
    return (
        f'<span style="background-color:{bg};color:{fg};padding:2px 10px;'
        f'border-radius:12px;font-size:0.85em;font-weight:600;">'
        f"{icon} {level}</span>"
    )


def severity_badge(severity: str) -> str:
    return risk_badge(severity)  # gleiche Farbskala


def status_badge(status: str) -> str:
    bg, fg, icon = _STATUS_COLORS.get(status, ("#888", "#fff", "•"))
    label = status.replace("_", " ")
    return (
        f'<span style="background-color:{bg};color:{fg};padding:2px 10px;'
        f'border-radius:12px;font-size:0.85em;font-weight:600;">'
        f"{icon} {label}</span>"
    )


def traffic_light_dot(state: str, size_px: int = 24) -> str:
    color = _TRAFFIC_LIGHT.get(state, "#888")
    return (
        f'<span style="display:inline-block;width:{size_px}px;height:{size_px}px;'
        f'border-radius:50%;background:{color};vertical-align:middle;"></span>'
    )
