"""CI-Branding für die Streamlit-UI.

Verantwortet: Globales CSS, Lineal-Bildmarke, Plotly-Theme, Severity-Farben.
Token-getrieben via CSS-Custom-Properties (siehe ``static/branding.css``).

Public API:
    inject_global_css() — einmalige CSS-Injection pro Streamlit-Run
    render_lineal()      — Lineal-Bildmarke (3 Segmente)
    severity_color(level)               — Risk-Hex
    compliance_status_color(status)     — Compliance-Hex
    get_plotly_template()               — Plotly-Layout-Template
    SEVERITY_COLORS / COMPLIANCE_STATUS_COLORS — Dicts
    FAVICON_PATH                        — Pfad auf das SVG-Favicon
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import streamlit as st

_STATIC = Path(__file__).resolve().parent / "static"

SEVERITY_COLORS: dict[str, str] = {
    "critical": "#9B4A2F",
    "high":     "#C26B4A",
    "medium":   "#B07A10",
    "low":      "rgba(12, 26, 50, 0.40)",
}

COMPLIANCE_STATUS_COLORS: dict[str, str] = {
    "compliant":              "#1A6B3A",
    "partially_compliant":    "#B07A10",
    "non_compliant":          "#9B4A2F",
    "needs_review":           "rgba(12, 26, 50, 0.40)",
}


def severity_color(level: str) -> str:
    """Mapped Risk-Severity (`critical`/`high`/`medium`/`low`) auf CI-Hex."""
    return SEVERITY_COLORS.get(level.lower(), SEVERITY_COLORS["low"])


def compliance_status_color(status: str) -> str:
    """Mapped Compliance-Status auf CI-Hex (Ampel: rot/gold/grün)."""
    return COMPLIANCE_STATUS_COLORS.get(status.lower(), COMPLIANCE_STATUS_COLORS["needs_review"])


@lru_cache(maxsize=1)
def _read_css() -> str:
    return (_STATIC / "branding.css").read_text(encoding="utf-8")


@lru_cache(maxsize=1)
def _read_plotly_template() -> dict[str, Any]:
    return json.loads((_STATIC / "plotly_theme.json").read_text(encoding="utf-8"))


def inject_global_css() -> None:
    """Injiziert das globale CSS einmalig pro Streamlit-Run.

    Idempotent: mehrfache Aufrufe sind harmlos (Streamlit dedupliziert Markdown-
    Output am DOM-Diff, aber wir setzen einen Session-Flag für Klarheit).
    """
    if st.session_state.get("_branding_css_injected"):
        return
    css = _read_css()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.session_state["_branding_css_injected"] = True


def render_lineal() -> None:
    """Rendert die Lineal-Bildmarke (3 Segmente: Bar / Linie / Quadrat).

    Visuelle Logo-Ersatzform — typisch im Sidebar-Header und einmal pro Page
    oben im Main-Container.
    """
    st.markdown(
        '<div class="ta-lineal">'
        '<div class="ta-lineal__bar"></div>'
        '<div class="ta-lineal__line"></div>'
        '<div class="ta-lineal__square"></div>'
        '</div>',
        unsafe_allow_html=True,
    )


def get_plotly_template() -> dict[str, Any]:
    """CI-konformes Plotly-Layout-Template (Farb-Sequenz + Mono-Achsen).

    Anwendung: ``fig.update_layout(**get_plotly_template()["layout"])``.
    """
    return _read_plotly_template()


FAVICON_PATH: Path = _STATIC / "favicon.svg"


__all__ = [
    "inject_global_css",
    "render_lineal",
    "severity_color",
    "compliance_status_color",
    "get_plotly_template",
    "SEVERITY_COLORS",
    "COMPLIANCE_STATUS_COLORS",
    "FAVICON_PATH",
]
