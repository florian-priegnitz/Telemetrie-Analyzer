"""Integrationstests für die Szenario-Profile des Testdaten-Generators.

Jedes Szenario wird end-to-end geprüft: Generator → Parser → DetectionEngine.
Deterministisch über festen Seed, DSGVO-sicher (synthetische Daten).

Detection-Schwellen (src/detection/engine.py):
    SYSTEMATIC_THRESHOLD   = 10 Requests/Tag
    UPLOAD_THRESHOLD_BYTES = 500 KB
    UPLOAD_RISK_BOOST      = +20 auf Score
"""

from pathlib import Path

import pytest

from src.detection.engine import DetectionEngine
from src.parsers.pihole import parse_pihole_log
from src.parsers.squid import parse_squid_log
from src.privacy.pseudonymizer import Pseudonymizer
from src.testdata.generator import (
    SCENARIO_PROFILES,
    generate_pihole_log,
    generate_squid_log,
)

SEED = 1337
DAYS = 7
QPD = 400  # queries per day


@pytest.fixture
def pseudo():
    """Deterministischer Pseudonymizer für Tests."""
    return Pseudonymizer(key=b"scenario-test-salt")


def _detect_from_pihole(path: Path, pseudo: Pseudonymizer):
    df = parse_pihole_log(path, pseudonymizer=pseudo)
    return DetectionEngine().analyze(df)


def _detect_from_squid(path: Path, pseudo: Pseudonymizer):
    df = parse_squid_log(path, pseudonymizer=pseudo)
    return DetectionEngine().analyze(df)


# ---------------------------------------------------------------------------
# 1. clean — keine AI-Nutzung
# ---------------------------------------------------------------------------
def test_clean_scenario_yields_no_findings(tmp_path: Path, pseudo: Pseudonymizer):
    log = generate_pihole_log(
        tmp_path / "clean.log",
        days=DAYS, queries_per_day=QPD, seed=SEED, scenario="clean",
    )
    result = _detect_from_pihole(log, pseudo)

    assert result.total_queries > 0, "Generator hat keine Logs erzeugt"
    assert result.ai_queries == 0, "Clean-Szenario darf keine AI-Queries enthalten"
    assert result.findings == [], "Clean-Szenario darf keine Findings erzeugen"


# ---------------------------------------------------------------------------
# 2. low-risk — unter systematic-Schwelle, nur medium-risk Services
# ---------------------------------------------------------------------------
def test_low_risk_scenario_below_systematic_threshold(tmp_path: Path, pseudo: Pseudonymizer):
    log = generate_pihole_log(
        tmp_path / "low-risk.log",
        days=DAYS, queries_per_day=QPD, seed=SEED, scenario="low-risk",
    )
    result = _detect_from_pihole(log, pseudo)

    assert result.ai_queries > 0, "Low-risk braucht wenigstens vereinzelte AI-Queries"

    if result.findings:
        # Keine Finding darf systematic sein (queries_per_day ≤ 10)
        for f in result.findings:
            assert not f.is_systematic, (
                f"Finding sollte unter SYSTEMATIC_THRESHOLD liegen, "
                f"ist aber bei {f.queries_per_day:.1f} Req/Tag ({f.service})"
            )
            assert f.risk_level in ("medium", "low"), (
                f"Low-risk darf nur medium/low Services enthalten, "
                f"hat aber {f.risk_level} ({f.service})"
            )
            assert not f.has_document_upload, "Low-risk darf keine Uploads haben"


# ---------------------------------------------------------------------------
# 3. systematic — >10 Req/Tag, high/critical Services
# ---------------------------------------------------------------------------
def test_systematic_scenario_triggers_threshold(tmp_path: Path, pseudo: Pseudonymizer):
    log = generate_pihole_log(
        tmp_path / "systematic.log",
        days=DAYS, queries_per_day=QPD, seed=SEED, scenario="systematic",
    )
    result = _detect_from_pihole(log, pseudo)

    assert len(result.findings) >= 2, (
        f"Systematic-Szenario sollte ≥2 Findings haben, hat {len(result.findings)}"
    )

    systematic_findings = [f for f in result.findings if f.is_systematic]
    assert len(systematic_findings) >= 2, (
        f"Mindestens 2 Findings sollten is_systematic=True sein, "
        f"ist aber {len(systematic_findings)}"
    )

    # Mindestens ein kritischer Service (Cursor)
    assert any(f.risk_level == "critical" for f in result.findings), \
        "Systematic muss mindestens einen critical-Service enthalten"

    # Score-Bereich: base 50-70 + 15 (systematic) + 5-10 (days) = 65-95
    scored = [f.risk_score for f in systematic_findings]
    assert all(s >= 65 for s in scored), f"Scores zu niedrig: {scored}"


# ---------------------------------------------------------------------------
# 4. upload-leak — POST-Spikes >500 KB
# ---------------------------------------------------------------------------
def test_upload_leak_scenario_detects_document_upload(tmp_path: Path, pseudo: Pseudonymizer):
    log = generate_squid_log(
        tmp_path / "upload-leak.log",
        days=DAYS, queries_per_day=QPD, seed=SEED, scenario="upload-leak",
    )
    result = _detect_from_squid(log, pseudo)

    upload_findings = [f for f in result.findings if f.has_document_upload]
    assert upload_findings, (
        "Upload-leak-Szenario muss has_document_upload=True erzeugen"
    )

    # Mindestens ein Upload-Finding >500 KB bestätigt
    assert any(
        f.total_bytes_uploaded > 500 * 1024 and f.upload_events >= 1
        for f in upload_findings
    )

    # Score muss durch UPLOAD_RISK_BOOST (+20) deutlich erhöht sein
    top_score = max(f.risk_score for f in upload_findings)
    assert top_score >= 90, (
        f"Upload-leak sollte Score ≥90 haben (base high=50 + systematic 15 + days 10 "
        f"+ upload-boost 20 = 95), ist aber {top_score}"
    )


# ---------------------------------------------------------------------------
# 5. enterprise-mixed — realistische Verteilung, alle Risk-Level
# ---------------------------------------------------------------------------
def test_enterprise_mixed_scenario_has_diversity(tmp_path: Path, pseudo: Pseudonymizer):
    # QPD * 4: mit 30 Clients würde sonst jeder Heavy-User nur ~13 Events/Tag
    # bekommen, was zu wenig ist, um die Systematic-Schwelle (>10 AI-Req/Tag) zu
    # reißen. Enterprise-realistisch sind ohnehin höhere Volumina.
    log = generate_squid_log(
        tmp_path / "enterprise-mixed.log",
        days=DAYS, queries_per_day=QPD * 4, seed=SEED, scenario="enterprise-mixed",
    )
    result = _detect_from_squid(log, pseudo)

    assert len(result.findings) >= 5, (
        f"Enterprise-mixed sollte ≥5 Findings haben, hat {len(result.findings)}"
    )

    # Mindestens 3 unterschiedliche Risk-Level vertreten
    risk_levels = {f.risk_level for f in result.findings}
    assert len(risk_levels) >= 3, (
        f"Enterprise-mixed sollte ≥3 verschiedene Risk-Levels haben, hat {risk_levels}"
    )

    # Mindestens 4 verschiedene Services
    services = {f.service for f in result.findings}
    assert len(services) >= 4, (
        f"Enterprise-mixed sollte ≥4 verschiedene Services haben, hat {services}"
    )

    # Mindestens ein Heavy-User mit systematischer Nutzung
    assert any(f.is_systematic for f in result.findings), \
        "Enterprise-mixed muss mindestens ein systematisches Finding haben"


# ---------------------------------------------------------------------------
# Meta-Test: Alle Szenarien aus SCENARIO_PROFILES sind abgedeckt
# ---------------------------------------------------------------------------
def test_all_scenarios_are_tested():
    """Sicherheitsnetz: neue Szenarien ohne Test fallen hier auf."""
    tested = {"clean", "low-risk", "systematic", "upload-leak", "enterprise-mixed"}
    assert set(SCENARIO_PROFILES.keys()) == tested, (
        f"Neue Szenarien ohne Test: {set(SCENARIO_PROFILES.keys()) - tested}"
    )


# ---------------------------------------------------------------------------
# Backward-Compat: Legacy-Aufruf ohne scenario=... muss weiter funktionieren
# ---------------------------------------------------------------------------
def test_legacy_generator_still_works(tmp_path: Path, pseudo: Pseudonymizer):
    log = generate_pihole_log(
        tmp_path / "legacy.log",
        days=3, queries_per_day=100, seed=SEED,
    )
    df = parse_pihole_log(log, pseudonymizer=pseudo)
    assert len(df) > 0
