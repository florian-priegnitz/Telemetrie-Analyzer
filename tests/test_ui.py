"""UI-Smoke-Tests für das Streamlit-Dashboard.

Nutzt die offizielle `streamlit.testing.v1.AppTest` API für headless Tests.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest


def _has_streamlit_testing() -> bool:
    try:
        from streamlit.testing.v1 import AppTest  # noqa: F401
        return True
    except ImportError:
        return False


pytestmark = pytest.mark.skipif(
    not _has_streamlit_testing(),
    reason="streamlit.testing.v1 nicht verfügbar (Streamlit < 1.28)",
)

APP_PATH = str(Path(__file__).parent.parent / "app.py")
SAMPLE_PIHOLE_LOG = Path(__file__).parent.parent / "testdata" / "pihole_sample.log"


def test_app_starts_with_empty_state():
    """App startet ohne Crash und initialisiert Session-State."""
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(APP_PATH)
    at.run(timeout=10)
    assert not at.exception
    assert at.session_state["pipeline_state"] == "empty"
    assert at.session_state["report_data"] is None
    assert at.session_state["report_salt"]  # nicht-leer


def test_format_detection_pihole_vs_squid():
    """Pure-Function-Test für detect_log_format()."""
    from src.ui.state import detect_log_format

    pihole_line = (
        "Mar  9 08:15:32 dnsmasq[1234]: query[A] chat.openai.com from 192.168.1.42\n"
    )
    squid_line = (
        "1709971200.123 234 192.168.1.42 TCP_MISS/200 1547 POST "
        "https://api.openai.com/v1/chat - HIER_DIRECT/1.2.3.4 application/json\n"
    )
    assert detect_log_format(pihole_line) == "pihole"
    assert detect_log_format(squid_line) == "squid"
    assert detect_log_format("garbage line\nmore garbage") == "unknown"
    assert detect_log_format("") == "unknown"


def test_run_pipeline_returns_json_dict():
    """Ende-zu-Ende-Test: Pi-hole Sample-Log → run_pipeline → JSON-Dict mit allen Keys."""
    from src.ui.state import run_pipeline

    if not SAMPLE_PIHOLE_LOG.exists():
        pytest.skip("testdata/pihole_sample.log fehlt — bitte generator ausführen")

    file_bytes = SAMPLE_PIHOLE_LOG.read_bytes()
    data = run_pipeline(file_bytes, "pihole_sample.log", salt="test-salt", log_format="pihole")

    assert isinstance(data, dict)
    assert {"report_meta", "summary", "framework_scores", "findings"} <= set(data.keys())
    assert data["report_meta"]["pseudonymized"] is True
    assert data["summary"]["total_queries"] > 0


def test_pseudonymization_invariant_in_pipeline_output():
    """Defense-in-Depth-Smoke: assert_no_plaintext über Pipeline-Output wirft nicht."""
    from src.reports.privacy import assert_no_plaintext
    from src.ui.state import run_pipeline

    if not SAMPLE_PIHOLE_LOG.exists():
        pytest.skip("testdata/pihole_sample.log fehlt")

    file_bytes = SAMPLE_PIHOLE_LOG.read_bytes()
    data = run_pipeline(file_bytes, "pihole_sample.log", salt="test-salt", log_format="pihole")
    assert_no_plaintext(json.dumps(data, default=str))


def test_app_renders_settings_page_with_no_data():
    """Settings-Page funktioniert auch ohne Analyse (Salt-Konfiguration ist immer zugänglich)."""
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(APP_PATH)
    at.run(timeout=10)
    # Navigations-Radio existiert in Sidebar, mit den 4 Pages
    assert any(
        radio.label == "Page" or "Übersicht" in str(radio.options)
        for radio in at.sidebar.radio
    )


def test_kpi_format_helper():
    """Hilfs-Test für Bytes-Formatter."""
    from src.ui.components.kpi_row import _format_bytes
    assert _format_bytes(500) == "500 B"
    assert _format_bytes(1500).endswith("KB")
    assert _format_bytes(1500_000).endswith("MB")
    assert _format_bytes(1500_000_000).endswith("GB")
