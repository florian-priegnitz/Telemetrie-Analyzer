"""Tests für den Claude API Analyzer."""

import json
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from src.analyzer.analyzer import (
    AnalysisResult,
    AnalyzerError,
    ClaudeAnalyzer,
    FindingRecommendation,
)
from src.compliance.engine import ComplianceEngine
from src.compliance.models import ComplianceResult, ComplianceScore, Framework
from src.detection.engine import DetectionResult, Finding


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_finding(**overrides) -> Finding:
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


def _make_detection_result(findings=None) -> DetectionResult:
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


def _sample_api_response() -> str:
    """Valid JSON response as Claude would return."""
    return json.dumps({
        "executive_summary": "Es wurden 2 nicht-autorisierte KI-Dienste erkannt.",
        "risk_assessment": "Mittleres Gesamtrisiko mit kritischen Einzelbefunden.",
        "finding_recommendations": [
            {
                "finding_index": 0,
                "service": "ChatGPT",
                "risk_assessment": "Hohes Risiko durch unkontrollierten Datentransfer.",
                "recommendation": "Sofortige Sperrung und Evaluierung einer Enterprise-Lizenz.",
                "priority": "high",
            }
        ],
        "compliance_summary": {
            "DORA": "Art. 28 verletzt – Drittanbieter nicht registriert.",
            "EU_AI_ACT": "Risikoklassifizierung ausstehend.",
            "ISO_42001": "KI-Inventar unvollständig.",
            "ISO_27001": "Asset-Management-Lücke identifiziert.",
            "DSGVO": "DSFA erforderlich für ChatGPT-Nutzung.",
        },
    }, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestClaudeAnalyzerSkipMode:

    def test_no_api_key_returns_none(self):
        analyzer = ClaudeAnalyzer(api_key=None)
        assert not analyzer.is_available
        result = analyzer.analyze(
            _make_detection_result(),
            ComplianceResult(),
        )
        assert result is None

    def test_empty_string_api_key_is_skip_mode(self):
        analyzer = ClaudeAnalyzer(api_key="")
        assert not analyzer.is_available


class TestPromptBuilding:

    def test_build_prompt_contains_findings(self):
        analyzer = ClaudeAnalyzer(api_key=None)
        finding = _make_finding()
        dr = _make_detection_result([finding])
        engine = ComplianceEngine()
        cr = engine.analyze(dr)

        prompt = analyzer._build_prompt(dr, cr)
        assert "ChatGPT" in prompt
        assert "OpenAI" in prompt
        assert "llm_chatbot" in prompt

    def test_build_prompt_contains_compliance_scores(self):
        analyzer = ClaudeAnalyzer(api_key=None)
        finding = _make_finding()
        dr = _make_detection_result([finding])
        engine = ComplianceEngine()
        cr = engine.analyze(dr)

        prompt = analyzer._build_prompt(dr, cr)
        assert "compliance_scores" in prompt
        assert "DORA" in prompt

    def test_system_prompt_requests_german(self):
        analyzer = ClaudeAnalyzer(api_key=None)
        system = analyzer._system_prompt()
        assert "Deutsch" in system
        assert "JSON" in system


class TestResponseParsing:

    def test_parse_valid_json(self):
        analyzer = ClaudeAnalyzer(api_key=None)
        result = analyzer._parse_response(_sample_api_response())
        assert isinstance(result, AnalysisResult)
        assert "nicht-autorisierte" in result.executive_summary
        assert len(result.finding_recommendations) == 1
        assert result.finding_recommendations[0].service == "ChatGPT"
        assert result.finding_recommendations[0].priority == "high"

    def test_parse_strips_markdown_fences(self):
        analyzer = ClaudeAnalyzer(api_key=None)
        wrapped = f"```json\n{_sample_api_response()}\n```"
        result = analyzer._parse_response(wrapped)
        assert isinstance(result, AnalysisResult)

    def test_parse_invalid_json_raises(self):
        analyzer = ClaudeAnalyzer(api_key=None)
        with pytest.raises(AnalyzerError, match="Ungültige JSON"):
            analyzer._parse_response("not valid json {{{")

    def test_parse_missing_fields_uses_defaults(self):
        analyzer = ClaudeAnalyzer(api_key=None)
        result = analyzer._parse_response("{}")
        assert result.executive_summary == ""
        assert result.finding_recommendations == []
        assert result.compliance_summary == {}


class TestAPIIntegration:

    @patch("src.analyzer.analyzer.anthropic", create=True)
    def test_api_call_returns_analysis(self, mock_anthropic):
        """Mock the entire API flow."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=_sample_api_response())]
        mock_client.messages.create.return_value = mock_response

        analyzer = ClaudeAnalyzer(api_key="test-key")
        analyzer._client = mock_client

        finding = _make_finding()
        dr = _make_detection_result([finding])
        engine = ComplianceEngine()
        cr = engine.analyze(dr)

        result = analyzer.analyze(dr, cr)
        assert isinstance(result, AnalysisResult)
        assert result.model_used == "claude-sonnet-4-20250514"
        mock_client.messages.create.assert_called_once()
