"""End-to-End-Tests: jedes der 13 Testdata-Samples läuft durch die komplette
UI-Pipeline (detect_log_format → run_pipeline → report_data).

Absichert: die UI-Parser-Dispatch-Registry ist vollständig und konsistent
zu ``detect_format()``. Wenn jemand einen neuen Parser zu ``SUPPORTED_PARSERS``
hinzufügt, aber vergisst, ihn in ``_PARSER_DISPATCH`` zu registrieren,
schlägt hier der Roundtrip fehl.

Die Retention wird **deaktiviert** (statische Samples könnten älter als
90 Tage sein → sonst würde Retention alles droppen und die Pipeline crashen).
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from src.parsers.detection import detect_format
from src.privacy.retention import RetentionPolicy

TESTDATA = Path(__file__).parent.parent / "testdata"

# (Datei, Erwarteter Parser-Key, Mindest-Zeilen-Expectation)
SAMPLES = [
    ("pihole_sample.log", "pihole", 10),
    ("squid_sample.log", "squid", 10),
    ("aws_vpc_v2_sample.log", "aws_vpc_flow", 1),
    ("aws_vpc_v5_sample.log", "aws_vpc_flow", 1),
    ("cloudflare_gateway_sample.log", "cloudflare_gateway", 1),
    ("elastic_ecs_sample.log", "elastic_ecs", 1),
    ("entra_signin_sample.log", "entra_id", 1),
    ("fortinet_sample.log", "fortinet", 1),
    ("netskope_sample.log", "netskope", 1),
    ("paloalto_sample.log", "paloalto", 1),
    ("sysmon_sample.log", "sysmon", 1),
    ("umbrella_sample.log", "umbrella", 1),
    ("zscaler_sample.log", "zscaler", 1),
]


@pytest.fixture
def disable_retention():
    """Patched ``load_policy`` im ui.state so, dass Retention deaktiviert ist.

    Notwendig, weil die statischen Samples feste Zeitstempel haben (zum Teil
    aus 2024) und nach der 90-Tage-Default-Policy komplett verworfen würden.
    """
    with patch("src.ui.state.load_policy",
               return_value=RetentionPolicy(enabled=False)):
        yield


@pytest.mark.parametrize("sample_file,expected_parser,min_rows", SAMPLES)
def test_detect_and_dispatch_roundtrip(
    sample_file, expected_parser, min_rows, disable_retention,
):
    path = TESTDATA / sample_file
    if not path.is_file():
        pytest.skip(f"{sample_file} nicht generiert")

    # Import lazy, um Streamlit-Import-Overhead zu vermeiden
    from src.ui.state import run_pipeline

    file_bytes = path.read_bytes()

    # 1. Detection liefert erwarteten Parser
    detected = detect_format(file_bytes)
    assert detected == expected_parser, (
        f"{sample_file}: detect_format liefert {detected}, erwartet {expected_parser}"
    )

    # 2. Dispatch — Pipeline läuft ohne Crash (cache clear damit jedes Sample frisch)
    run_pipeline.clear()
    result = run_pipeline(file_bytes, sample_file, "test-salt", detected)

    assert "findings" in result
    assert "report_meta" in result
    assert "summary" in result

    # 3. Mindest-Erwartung: summary.total_queries >= min_rows
    assert result["summary"]["total_queries"] >= min_rows, (
        f"{sample_file}: nur {result['summary']['total_queries']} Queries geparst"
    )


def test_all_12_parser_keys_have_sample_coverage():
    """Verifiziert, dass jeder SUPPORTED_PARSERS-Key durch mindestens ein
    Sample in SAMPLES abgedeckt ist."""
    from src.parsers.detection import SUPPORTED_PARSERS

    covered = {parser for _, parser, _ in SAMPLES}
    missing = set(SUPPORTED_PARSERS) - covered
    assert not missing, f"Parser ohne Testdata-Coverage: {missing}"
