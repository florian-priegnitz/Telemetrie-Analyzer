"""Tests fuer src/ui/branding.py — CI-Branding (Bauhaus, Sprint 13)."""

from __future__ import annotations

import json
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

STATIC = Path(__file__).resolve().parent.parent / "src" / "ui" / "static"


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


def test_branding_css_file_exists_and_has_ci_tokens() -> None:
    css_path = STATIC / "branding.css"
    assert css_path.exists(), "branding.css fehlt"
    css = css_path.read_text(encoding="utf-8")
    for token in (
        "--c-acc: #9B4A2F",
        "--c-gold: #B07A10",
        "--c-green: #1A6B3A",
        "--c-ink: #0C1A32",
        "DM Sans",
        "Share Tech Mono",
        ".ta-lineal",
    ):
        assert token in css, f"CI-Token fehlt in branding.css: {token!r}"


def test_favicon_exists_and_has_lineal_geometry() -> None:
    assert FAVICON_PATH.exists(), "favicon.svg fehlt"
    svg = FAVICON_PATH.read_text(encoding="utf-8")
    for marker in ("#9B4A2F", "#0C1A32", "#B07A10", '<svg', '<rect'):
        assert marker in svg, f"Lineal-Geometrie unvollstaendig: {marker!r} fehlt"


def test_plotly_template_is_valid_json_and_uses_ci_palette() -> None:
    tpl = get_plotly_template()
    assert "layout" in tpl
    layout = tpl["layout"]
    assert layout["paper_bgcolor"] == "#FFFFFF"
    assert "#9B4A2F" in layout["colorway"]
    assert "#B07A10" in layout["colorway"]
    assert "#1A6B3A" in layout["colorway"]
    assert layout["font"]["family"].startswith("DM Sans")


def test_plotly_template_file_round_trips_json() -> None:
    raw = (STATIC / "plotly_telemetrie_theme.json").read_text(encoding="utf-8")
    parsed = json.loads(raw)
    assert parsed["layout"]["plot_bgcolor"] == "#FFFFFF"


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
