"""Tests für die Demo-Scenario-Registry (src/ui/scenarios.py).

Prüft, dass alle registrierten Scenarios konsistent sind und die
referenzierten Sample-Dateien existieren.
"""

from __future__ import annotations

import pytest

from src.parsers.detection import SUPPORTED_PARSERS
from src.ui.scenarios import SCENARIOS, available_scenarios, get_scenario


def test_all_scenarios_have_unique_keys():
    keys = [s.key for s in SCENARIOS]
    assert len(keys) == len(set(keys)), f"Duplicate scenario keys: {keys}"


def test_all_scenarios_reference_known_parser():
    for s in SCENARIOS:
        assert s.parser in SUPPORTED_PARSERS, (
            f"Scenario {s.key} referenziert unbekannten Parser: {s.parser}"
        )


def test_all_referenced_files_exist():
    """Jede in der Registry angegebene Datei muss im testdata/ liegen."""
    missing = [s for s in SCENARIOS if not s.exists]
    assert not missing, (
        f"Sample-Dateien fehlen: {[str(s.file_path) for s in missing]}"
    )


def test_each_parser_has_at_least_one_scenario():
    """Alle 12 Parser sollten in der Scenario-Liste vertreten sein."""
    covered = {s.parser for s in SCENARIOS}
    missing = set(SUPPORTED_PARSERS) - covered
    assert not missing, f"Parser ohne Scenario: {missing}"


def test_get_scenario_by_key():
    s = get_scenario("pihole")
    assert s is not None
    assert s.parser == "pihole"


def test_get_scenario_unknown_returns_none():
    assert get_scenario("does-not-exist") is None


def test_available_scenarios_are_non_empty():
    """Basis-Smoke: mindestens ein Scenario muss nutzbar sein."""
    scenarios = available_scenarios()
    assert len(scenarios) >= 1


@pytest.mark.parametrize("scenario_key", [s.key for s in SCENARIOS])
def test_scenario_file_loadable(scenario_key):
    """Jede Scenario-Datei muss mit dem angegebenen Parser geladen werden können."""
    from unittest.mock import patch

    from src.parsers.detection import detect_format
    from src.privacy.retention import RetentionPolicy
    from src.ui.state import run_pipeline

    s = get_scenario(scenario_key)
    assert s is not None
    if not s.exists:
        pytest.skip(f"{s.file_path} nicht generiert")

    # Detection soll den Parser-Key zurückliefern
    detected = detect_format(s.file_path.read_bytes())
    assert detected == s.parser, (
        f"{scenario_key}: detected={detected}, erwartet {s.parser}"
    )

    # Pipeline darf nicht crashen (Retention deaktiviert für Edge-Cases)
    with patch("src.ui.state.load_policy",
               return_value=RetentionPolicy(enabled=False)):
        run_pipeline.clear()
        result = run_pipeline(
            s.file_path.read_bytes(), s.file_path.name, "test-salt", s.parser,
        )
    assert "findings" in result
    assert "_exports" in result
