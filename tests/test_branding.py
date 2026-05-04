"""Tests fuer src/ui/branding.py — CI-Branding-Wrapper (Bauhaus, Sprint 13).

Branding-Logik liegt in `bauhaus-streamlit` (Issue #89). Diese Tests
verifizieren primaer, dass der Re-Export funktioniert und die fuer den
Telemetrie-Analyzer relevanten Severity-/Status-Mappings stimmen.
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


def test_favicon_path_is_provided_by_package() -> None:
    """FAVICON_PATH wird aus dem bauhaus-streamlit-Paket re-exportiert."""
    assert isinstance(FAVICON_PATH, Path)
    # Pfad zeigt in die Paket-Resources, Datei existiert.
    assert FAVICON_PATH.exists(), f"favicon.svg fehlt im Paket: {FAVICON_PATH}"
    svg = FAVICON_PATH.read_text(encoding="utf-8")
    for marker in ("#9B4A2F", "#0C1A32", "#B07A10", "<svg", "<rect"):
        assert marker in svg, f"Lineal-Geometrie unvollstaendig: {marker!r} fehlt"


def test_plotly_template_uses_ci_palette() -> None:
    tpl = get_plotly_template()
    assert "layout" in tpl
    layout = tpl["layout"]
    assert layout["paper_bgcolor"] == "#FFFFFF"
    assert "#9B4A2F" in layout["colorway"]
    assert "#B07A10" in layout["colorway"]
    assert "#1A6B3A" in layout["colorway"]
    assert layout["font"]["family"].startswith("DM Sans")


def test_branding_module_re_exports_from_package() -> None:
    """Smoke-Test: branding.py ist nun ein Wrapper auf bauhaus_streamlit."""
    import bauhaus_streamlit

    from src.ui import branding

    assert branding.severity_color is bauhaus_streamlit.severity_color
    assert branding.compliance_status_color is bauhaus_streamlit.compliance_status_color
    assert branding.inject_global_css is bauhaus_streamlit.inject_global_css
    assert branding.render_lineal is bauhaus_streamlit.render_lineal
    assert branding.SEVERITY_COLORS is bauhaus_streamlit.SEVERITY_COLORS


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
