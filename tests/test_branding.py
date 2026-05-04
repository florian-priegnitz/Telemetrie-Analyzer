"""Tests für src/ui/branding.py — CI-Branding der Telemetrie-Analyzer-UI.

Verifiziert die Severity-/Compliance-Status-Mappings, das Plotly-Template,
die CSS-Token-Vollständigkeit und den Favicon-Pfad.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.ui.branding import (
    COMPLIANCE_STATUS_COLORS,
    FAVICON_PATH,
    SEVERITY_COLORS,
    compliance_status_color,
    get_plotly_template,
    severity_color,
)


@pytest.mark.parametrize(
    "level,hex_value",
    [
        ("critical", "#9B4A2F"),
        ("high",     "#C26B4A"),
        ("medium",   "#B07A10"),
        ("low",      "rgba(12, 26, 50, 0.40)"),
    ],
)
def test_severity_color_returns_ci_hex(level: str, hex_value: str) -> None:
    assert severity_color(level) == hex_value


def test_severity_color_is_case_insensitive() -> None:
    assert severity_color("CRITICAL") == "#9B4A2F"
    assert severity_color("High") == "#C26B4A"


def test_severity_color_unknown_falls_back_to_low() -> None:
    assert severity_color("not-a-real-level") == SEVERITY_COLORS["low"]


@pytest.mark.parametrize(
    "status,hex_value",
    [
        ("compliant",            "#1A6B3A"),
        ("partially_compliant",  "#B07A10"),
        ("non_compliant",        "#9B4A2F"),
    ],
)
def test_compliance_status_color_uses_traffic_light_palette(status: str, hex_value: str) -> None:
    assert compliance_status_color(status) == hex_value


def test_compliance_status_color_unknown_falls_back() -> None:
    assert compliance_status_color("xyz") == COMPLIANCE_STATUS_COLORS["needs_review"]


def test_favicon_path_points_to_existing_svg() -> None:
    """FAVICON_PATH zeigt auf das Lineal-SVG unter src/ui/static/."""
    assert isinstance(FAVICON_PATH, Path)
    assert FAVICON_PATH.exists(), f"favicon.svg fehlt: {FAVICON_PATH}"
    svg = FAVICON_PATH.read_text(encoding="utf-8")
    for marker in ("#9B4A2F", "#0C1A32", "#B07A10", "<svg", "<rect"):
        assert marker in svg, f"Lineal-Geometrie unvollständig: {marker!r} fehlt"


def test_plotly_template_uses_ci_palette() -> None:
    tpl = get_plotly_template()
    assert "layout" in tpl
    layout = tpl["layout"]
    assert layout["paper_bgcolor"] == "#FFFFFF"
    assert "#9B4A2F" in layout["colorway"]
    assert "#B07A10" in layout["colorway"]
    assert "#1A6B3A" in layout["colorway"]
    assert layout["font"]["family"].startswith("DM Sans")


def test_branding_css_has_required_tokens() -> None:
    """CSS-Token-Vollständigkeit: alle CI-Custom-Properties + Klassen sind da."""
    from src.ui.branding import _read_css

    css = _read_css()
    for token in (
        "--c-bg",
        "--c-acc",
        "--c-ink",
        ".ta-lineal",
        ".ta-sev-critical",
        "DM Sans",
        "Share Tech Mono",
    ):
        assert token in css, f"CI-Token fehlt in branding.css: {token!r}"


def _has_streamlit_testing() -> bool:
    try:
        from streamlit.testing.v1 import AppTest  # noqa: F401
        return True
    except ImportError:
        return False


@pytest.mark.skipif(
    not _has_streamlit_testing(),
    reason="streamlit.testing.v1 nicht verfuegbar",
)
def test_inject_global_css_runs_in_app_without_error() -> None:
    """Smoke-Test: app.py startet mit Branding-Injection ohne Exception."""
    from streamlit.testing.v1 import AppTest

    app_path = str(Path(__file__).resolve().parent.parent / "app.py")
    at = AppTest.from_file(app_path)
    at.run(timeout=10)
    assert not at.exception
    # CSS-Inject-Flag ist nach Run gesetzt
    assert at.session_state["_branding_css_injected"] is True
