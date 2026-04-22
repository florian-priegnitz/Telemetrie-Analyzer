"""Tests für Compliance Models und Engine."""

from datetime import datetime
from pathlib import Path

import pytest
import yaml

from src.compliance.engine import ComplianceEngine
from src.compliance.models import (
    AssessmentStatus,
    ComplianceMapping,
    ComplianceScore,
    Framework,
    Severity,
)
from src.detection.engine import DetectionResult, Finding

_CRA_YAML_PATH = Path(__file__).resolve().parent.parent / "mappings" / "cra.yaml"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_finding(**overrides) -> Finding:
    """Create a Finding with sensible defaults, overridable per test."""
    defaults = dict(
        client="ip_abc123",
        service="ChatGPT",
        provider="OpenAI",
        category="llm_chatbot",
        risk_level="high",
        domains=["chat.openai.com"],
        total_queries=50,
        first_seen=datetime(2025, 1, 1),
        last_seen=datetime(2025, 1, 7),
        days_active=7,
        queries_per_day=7.1,
        is_systematic=False,
    )
    defaults.update(overrides)
    return Finding(**defaults)


def _make_result(findings: list[Finding] | None = None) -> DetectionResult:
    """Wrap findings into a DetectionResult."""
    findings = findings or []
    return DetectionResult(
        findings=findings,
        total_queries=100,
        ai_queries=50,
        non_ai_queries=50,
        analysis_period_start=datetime(2025, 1, 1),
        analysis_period_end=datetime(2025, 1, 7),
        unique_clients=1,
        unique_ai_services=len(findings),
    )


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------

class TestComplianceModels:

    def test_framework_enum_values(self):
        assert Framework.DORA.value == "DORA"
        assert Framework.DSGVO.value == "DSGVO"
        assert Framework.CRA.value == "CRA"

    def test_framework_enum_count(self):
        assert len(Framework) == 6

    def test_severity_enum_values(self):
        assert Severity.CRITICAL.value == "critical"
        assert Severity.LOW.value == "low"

    def test_assessment_status_enum(self):
        assert AssessmentStatus.NON_COMPLIANT.value == "non_compliant"
        assert AssessmentStatus.COMPLIANT.value == "compliant"

    def test_compliance_mapping_creation(self):
        m = ComplianceMapping(
            framework=Framework.DORA,
            control_id="Art. 28",
            control_name="ICT Third-Party Risk",
            severity=Severity.HIGH,
            assessment_status=AssessmentStatus.NON_COMPLIANT,
            rationale="Test rationale",
        )
        assert m.framework == Framework.DORA
        assert m.control_id == "Art. 28"

    def test_compliance_score_percent(self):
        score = ComplianceScore(
            framework=Framework.ISO_27001,
            total_controls=3,
            triggered_controls=2,
            non_compliant=1,
            partially_compliant=1,
            needs_review=0,
        )
        # 3 total - 2 bad = 1 compliant → 33.3%
        assert score.score_percent == pytest.approx(33.3, abs=0.1)

    def test_compliance_score_all_compliant(self):
        score = ComplianceScore(
            framework=Framework.DSGVO,
            total_controls=3,
            triggered_controls=0,
            non_compliant=0,
            partially_compliant=0,
            needs_review=0,
        )
        assert score.score_percent == 100.0

    def test_compliance_score_zero_controls(self):
        score = ComplianceScore(
            framework=Framework.DORA,
            total_controls=0,
            triggered_controls=0,
            non_compliant=0,
            partially_compliant=0,
            needs_review=0,
        )
        assert score.score_percent == 100.0


# ---------------------------------------------------------------------------
# Engine tests
# ---------------------------------------------------------------------------

class TestComplianceEngine:

    def setup_method(self):
        self.engine = ComplianceEngine()

    def test_empty_findings(self):
        result = self.engine.analyze(_make_result([]))
        assert result.finding_mappings == {}
        # All frameworks should have scores with 0 triggered
        for fw in Framework:
            assert result.framework_scores[fw].triggered_controls == 0

    def test_high_risk_finding_triggers_all_frameworks(self):
        finding = _make_finding(risk_level="high", category="llm_chatbot")
        result = self.engine.analyze(_make_result([finding]))
        mappings = result.finding_mappings[0]
        frameworks_hit = {m.framework for m in mappings}
        assert frameworks_hit == set(Framework)

    def test_critical_finding_triggers_dsgvo_art35(self):
        finding = _make_finding(risk_level="critical")
        result = self.engine.analyze(_make_result([finding]))
        mappings = result.finding_mappings[0]
        dsgvo_controls = [m.control_id for m in mappings if m.framework == Framework.DSGVO]
        assert "Art. 35" in dsgvo_controls

    def test_low_risk_no_dsgvo_art35(self):
        finding = _make_finding(risk_level="low")
        result = self.engine.analyze(_make_result([finding]))
        mappings = result.finding_mappings[0]
        dsgvo_controls = [m.control_id for m in mappings if m.framework == Framework.DSGVO]
        assert "Art. 35" not in dsgvo_controls

    def test_systematic_triggers_monitoring_controls(self):
        finding = _make_finding(is_systematic=True, queries_per_day=15.0)
        result = self.engine.analyze(_make_result([finding]))
        mappings = result.finding_mappings[0]
        control_ids = [(m.framework, m.control_id) for m in mappings]
        assert (Framework.ISO_27001, "A.8.16") in control_ids
        assert (Framework.DORA, "Art. 5") in control_ids
        assert (Framework.ISO_42001, "8.4") in control_ids

    def test_non_systematic_skips_monitoring(self):
        finding = _make_finding(is_systematic=False)
        result = self.engine.analyze(_make_result([finding]))
        mappings = result.finding_mappings[0]
        control_ids = [(m.framework, m.control_id) for m in mappings]
        assert (Framework.ISO_27001, "A.8.16") not in control_ids
        assert (Framework.DORA, "Art. 5") not in control_ids

    def test_code_assistant_triggers_eu_ai_act_art6(self):
        finding = _make_finding(category="code_assistant", service="Copilot")
        result = self.engine.analyze(_make_result([finding]))
        mappings = result.finding_mappings[0]
        eu_controls = [m.control_id for m in mappings if m.framework == Framework.EU_AI_ACT]
        assert "Art. 6" in eu_controls

    def test_image_gen_no_eu_ai_act_art6(self):
        finding = _make_finding(category="image_generation", risk_level="medium")
        result = self.engine.analyze(_make_result([finding]))
        mappings = result.finding_mappings[0]
        eu_controls = [m.control_id for m in mappings if m.framework == Framework.EU_AI_ACT]
        assert "Art. 6" not in eu_controls

    def test_high_risk_score_non_compliant(self):
        """risk_score >= 70 → non_compliant."""
        finding = _make_finding(
            risk_level="critical", is_systematic=True, queries_per_day=15.0,
        )
        assert finding.risk_score >= 70
        result = self.engine.analyze(_make_result([finding]))
        mappings = result.finding_mappings[0]
        assert all(m.assessment_status == AssessmentStatus.NON_COMPLIANT for m in mappings)

    def test_low_risk_score_needs_review(self):
        """risk_score < 40 → needs_review."""
        finding = _make_finding(risk_level="low", is_systematic=False, days_active=1)
        assert finding.risk_score < 40
        result = self.engine.analyze(_make_result([finding]))
        mappings = result.finding_mappings[0]
        assert all(m.assessment_status == AssessmentStatus.NEEDS_REVIEW for m in mappings)

    def test_finding_compliance_mappings_populated(self):
        """Engine populates finding.compliance_mappings in-place."""
        finding = _make_finding()
        self.engine.analyze(_make_result([finding]))
        assert len(finding.compliance_mappings) > 0
        assert isinstance(finding.compliance_mappings[0], ComplianceMapping)

    def test_framework_scores_present(self):
        finding = _make_finding()
        result = self.engine.analyze(_make_result([finding]))
        assert len(result.framework_scores) == len(Framework)
        for fw, score in result.framework_scores.items():
            assert score.framework == fw
            assert score.total_controls > 0

    def test_multiple_findings_worst_status_wins(self):
        """When two findings trigger the same control, worst status is used for scoring."""
        low_finding = _make_finding(risk_level="low", is_systematic=False, days_active=1)
        critical_finding = _make_finding(
            risk_level="critical", is_systematic=True,
            service="Copilot", category="code_assistant",
        )
        result = self.engine.analyze(_make_result([low_finding, critical_finding]))
        # ISO 27001 A.5.9 triggered by both – worst should be non_compliant
        iso_score = result.framework_scores[Framework.ISO_27001]
        assert iso_score.non_compliant >= 1

    def test_rationale_contains_service_name(self):
        finding = _make_finding(service="DeepSeek", provider="DeepSeek AI")
        result = self.engine.analyze(_make_result([finding]))
        mappings = result.finding_mappings[0]
        assert all("DeepSeek" in m.rationale for m in mappings)


# ---------------------------------------------------------------------------
# CRA-specific rule tests (Issue #42 — Regulation (EU) 2024/2847)
# ---------------------------------------------------------------------------

class TestComplianceEngineCRA:

    def setup_method(self):
        self.engine = ComplianceEngine()

    def _cra_controls(self, finding: Finding) -> list[str]:
        result = self.engine.analyze(_make_result([finding]))
        return [
            m.control_id
            for m in result.finding_mappings[0]
            if m.framework == Framework.CRA
        ]

    def test_any_finding_triggers_cra_art6(self):
        """Art. 6 (Essential Requirements) must trigger for every finding."""
        for risk in ("low", "medium", "high", "critical"):
            controls = self._cra_controls(_make_finding(risk_level=risk))
            assert "Art. 6" in controls, f"Art. 6 missing for risk_level={risk}"

    def test_high_risk_category_triggers_cra_art7(self):
        controls = self._cra_controls(_make_finding(category="code_assistant"))
        assert "Art. 7" in controls

    def test_non_high_risk_category_skips_cra_art7(self):
        controls = self._cra_controls(_make_finding(
            category="image_generation", risk_level="low",
        ))
        assert "Art. 7" not in controls

    def test_llm_api_triggers_cra_art10(self):
        controls = self._cra_controls(_make_finding(category="llm_api"))
        assert "Art. 10" in controls

    def test_image_gen_skips_cra_art10(self):
        controls = self._cra_controls(_make_finding(category="image_generation"))
        assert "Art. 10" not in controls

    def test_document_upload_triggers_cra_art11(self):
        controls = self._cra_controls(_make_finding(has_document_upload=True))
        assert "Art. 11" in controls

    def test_no_upload_skips_cra_art11(self):
        controls = self._cra_controls(_make_finding(has_document_upload=False))
        assert "Art. 11" not in controls

    def test_high_risk_level_triggers_cra_art13(self):
        controls = self._cra_controls(_make_finding(risk_level="high"))
        assert "Art. 13" in controls

    def test_low_risk_level_skips_cra_art13(self):
        controls = self._cra_controls(_make_finding(risk_level="low"))
        assert "Art. 13" not in controls

    def test_systematic_triggers_cra_art14(self):
        controls = self._cra_controls(_make_finding(
            is_systematic=True, queries_per_day=15.0,
        ))
        assert "Art. 14" in controls

    def test_non_systematic_skips_cra_art14(self):
        controls = self._cra_controls(_make_finding(is_systematic=False))
        assert "Art. 14" not in controls

    def test_cloud_service_triggers_cra_art24(self):
        controls = self._cra_controls(_make_finding(category="llm_chatbot"))
        assert "Art. 24" in controls

    def test_cra_in_framework_scores(self):
        finding = _make_finding()
        result = self.engine.analyze(_make_result([finding]))
        assert Framework.CRA in result.framework_scores
        cra_score = result.framework_scores[Framework.CRA]
        assert cra_score.total_controls == 7

    def test_cra_critical_finding_non_compliant(self):
        finding = _make_finding(
            risk_level="critical",
            is_systematic=True,
            category="code_assistant",
            has_document_upload=True,
            queries_per_day=15.0,
        )
        result = self.engine.analyze(_make_result([finding]))
        cra_mappings = [
            m for m in result.finding_mappings[0] if m.framework == Framework.CRA
        ]
        # All 7 CRA controls should hit for a maxed-out finding
        assert len(cra_mappings) == 7
        assert all(
            m.assessment_status == AssessmentStatus.NON_COMPLIANT
            for m in cra_mappings
        )


# ---------------------------------------------------------------------------
# CRA YAML metadata registry (mappings/cra.yaml)
# ---------------------------------------------------------------------------

class TestCRAYamlRegistry:

    def test_cra_yaml_exists(self):
        assert _CRA_YAML_PATH.exists(), f"Missing {_CRA_YAML_PATH}"

    def test_cra_yaml_loads(self):
        data = yaml.safe_load(_CRA_YAML_PATH.read_text(encoding="utf-8"))
        assert isinstance(data, dict)
        assert "framework" in data
        assert "controls" in data

    def test_cra_yaml_framework_metadata(self):
        data = yaml.safe_load(_CRA_YAML_PATH.read_text(encoding="utf-8"))
        fw = data["framework"]
        assert fw["id"] == "CRA"
        assert fw["regulation_id"] == "Regulation (EU) 2024/2847"

    def test_cra_yaml_control_ids_match_engine(self):
        """YAML must list exactly the controls emitted by the engine."""
        data = yaml.safe_load(_CRA_YAML_PATH.read_text(encoding="utf-8"))
        yaml_ids = {c["id"] for c in data["controls"]}

        engine = ComplianceEngine()
        finding = _make_finding(
            risk_level="critical",
            is_systematic=True,
            category="code_assistant",
            has_document_upload=True,
        )
        result = engine.analyze(_make_result([finding]))
        engine_ids = {
            m.control_id for m in result.finding_mappings[0]
            if m.framework == Framework.CRA
        }
        assert yaml_ids == engine_ids, (
            f"YAML/engine drift: yaml={yaml_ids}, engine={engine_ids}"
        )

    def test_cra_yaml_control_schema(self):
        data = yaml.safe_load(_CRA_YAML_PATH.read_text(encoding="utf-8"))
        required = {"id", "name", "article_title", "description", "applies_to"}
        for ctrl in data["controls"]:
            missing = required - ctrl.keys()
            assert not missing, f"Control {ctrl.get('id')} missing {missing}"
