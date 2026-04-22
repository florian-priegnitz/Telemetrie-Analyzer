"""End-to-End-Integrationstests für die vollständige Analyse-Pipeline.

Deckt den kompletten Happy-Path ab:
    Log-Datei → Parser → Retention → Detection → Compliance → Report

Im Gegensatz zu den Unit-Tests der einzelnen Module prüfen diese E2E-Tests
das Zusammenspiel aller Schichten. Wenn ein Modul-Refactor die API bricht,
ohne dass Unit-Tests es bemerken, schlagen diese Tests an.

Testdaten: `testdata/pihole_sample.log`, `testdata/elastic_ecs_sample.log`.
Beide sind synthetisch und im Repo committed — keine Live-Daten, keine PII.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from src.compliance.engine import ComplianceEngine
from src.compliance.models import ComplianceResult
from src.detection.engine import DetectionEngine, DetectionResult
from src.parsers.elastic_ecs import parse_elastic_ecs_log
from src.parsers.pihole import parse_pihole_log
from src.privacy.pseudonymizer import Pseudonymizer
from src.privacy.retention import RetentionPolicy, apply_retention
from src.reports import ReportGenerator
from src.reports.context import build_context, context_to_json_dict
from src.reports.privacy import assert_no_plaintext

ROOT = Path(__file__).parent.parent
TESTDATA = ROOT / "testdata"
_FIXED_SALT = "e2e-test-salt"


# ---------------------------------------------------------------------------
# Pi-hole: Happy-Path
# ---------------------------------------------------------------------------
class TestPiholePipelineE2E:

    @pytest.fixture(scope="class")
    def pipeline(self) -> tuple[pd.DataFrame, DetectionResult, ComplianceResult]:
        sample = TESTDATA / "pihole_sample.log"
        if not sample.is_file():
            pytest.skip("pihole_sample.log not generated — run testdata/generator")
        pseudo = Pseudonymizer(key=_FIXED_SALT.encode())
        df = parse_pihole_log(sample, pseudonymizer=pseudo)
        # Retention deaktivieren — Sample ist statisch und könnte älter als 90d sein
        df = apply_retention(df, RetentionPolicy(enabled=False))
        detection = DetectionEngine().analyze(df)
        compliance = ComplianceEngine().analyze(detection)
        return df, detection, compliance

    def test_parser_produces_events(self, pipeline) -> None:
        df, _, _ = pipeline
        assert not df.empty
        assert len(df) > 100, f"Erwartet > 100 Events in Sample, bekam {len(df)}"

    def test_all_clients_pseudonymized(self, pipeline) -> None:
        df, _, _ = pipeline
        assert all(c.startswith("ip_") for c in df["client"])

    def test_detection_finds_ai_usage(self, pipeline) -> None:
        _, detection, _ = pipeline
        assert len(detection.findings) > 0, "DetectionEngine findet keine AI-Nutzung"

    def test_compliance_mappings_present(self, pipeline) -> None:
        _, _, compliance = pipeline
        # mindestens 1 Framework sollte betroffen sein
        assert len(compliance.framework_scores) > 0

    def test_report_json_roundtrip(self, pipeline) -> None:
        _, detection, compliance = pipeline
        ctx = build_context(detection, compliance, salt=_FIXED_SALT)
        payload = context_to_json_dict(ctx)
        # Muss serialisierbar sein (kein Dataclass-Overhang)
        serialized = json.dumps(payload, default=str)
        reparsed = json.loads(serialized)
        assert "findings" in reparsed
        assert "report_meta" in reparsed

    def test_report_html_contains_compliance_sections(self, pipeline, tmp_path: Path) -> None:
        _, detection, compliance = pipeline
        gen = ReportGenerator(detection, compliance, salt=_FIXED_SALT)
        paths = gen.write(tmp_path, audience="compliance", format="html")
        path_list = paths if isinstance(paths, list) else [paths]
        html = Path(path_list[0]).read_text(encoding="utf-8")
        # Alle 5 Frameworks sollten im Compliance-Report auftauchen
        for framework in ("DORA", "EU AI Act", "ISO 42001", "ISO 27001", "DSGVO"):
            assert framework in html, f"{framework} fehlt im HTML-Report"

    def test_report_passes_privacy_assertion(self, pipeline, tmp_path: Path) -> None:
        """Alle gerenderten Reports müssen `assert_no_plaintext` passieren."""
        _, detection, compliance = pipeline
        gen = ReportGenerator(detection, compliance, salt=_FIXED_SALT)
        paths = gen.write(tmp_path, audience="all", format="html")
        for path_item in (paths if isinstance(paths, list) else [paths]):
            html = Path(path_item).read_text(encoding="utf-8")
            assert_no_plaintext(html)

    def test_salt_fingerprint_reproducible(self, pipeline) -> None:
        """Gleicher Salt → gleicher Fingerprint (für reproduzierbare Reports)."""
        _, detection, compliance = pipeline
        ctx_a = build_context(detection, compliance, salt=_FIXED_SALT)
        ctx_b = build_context(detection, compliance, salt=_FIXED_SALT)
        fp_a = context_to_json_dict(ctx_a)["report_meta"]["salt_fingerprint"]
        fp_b = context_to_json_dict(ctx_b)["report_meta"]["salt_fingerprint"]
        assert fp_a == fp_b


# ---------------------------------------------------------------------------
# Elastic ECS: Happy-Path — verifiziert neue Parser-Integration in Wave 2
# ---------------------------------------------------------------------------
class TestElasticECSPipelineE2E:

    @pytest.fixture(scope="class")
    def pipeline(self) -> tuple[pd.DataFrame, DetectionResult, ComplianceResult]:
        sample = TESTDATA / "elastic_ecs_sample.log"
        assert sample.is_file()
        pseudo = Pseudonymizer(key=_FIXED_SALT.encode())
        df = parse_elastic_ecs_log(sample, pseudonymizer=pseudo)
        df = apply_retention(df, RetentionPolicy(enabled=False))
        detection = DetectionEngine().analyze(df)
        compliance = ComplianceEngine().analyze(detection)
        return df, detection, compliance

    def test_ecs_parser_produces_events(self, pipeline) -> None:
        df, _, _ = pipeline
        assert not df.empty

    def test_ecs_detects_known_ai_services(self, pipeline) -> None:
        """Mindestens eines der Sample-Domains (chat.openai.com, claude.ai,
        perplexity.ai, ...) muss als Finding registriert werden."""
        _, detection, _ = pipeline
        services = {f.service for f in detection.findings}
        # Mindestens ein AI-Service erkannt (genauer Match hängt von DB-Version ab)
        assert len(services) >= 1, f"Keine Services erkannt; Findings: {detection.findings}"


# ---------------------------------------------------------------------------
# Pipeline-Invarianten (Smoke) — unabhängig vom Input
# ---------------------------------------------------------------------------
def test_empty_dataframe_pipeline_is_safe() -> None:
    """Pipeline über leeres DataFrame darf nicht crashen."""
    df = pd.DataFrame(columns=["timestamp", "client", "domain"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    detection = DetectionEngine().analyze(df)
    compliance = ComplianceEngine().analyze(detection)
    assert detection.findings == []
    # Compliance-Aggregate über leere Findings
    ctx = build_context(detection, compliance, salt=_FIXED_SALT)
    payload = context_to_json_dict(ctx)
    assert payload["findings"] == []
