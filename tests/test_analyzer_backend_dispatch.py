"""Tests verifying ClaudeAnalyzer dispatches correctly across backends (#72)."""

from __future__ import annotations

import json
from datetime import datetime
from unittest.mock import MagicMock

from src.analyzer.analyzer import AnalysisResult, ClaudeAnalyzer
from src.analyzer.backends import OllamaBackend
from src.compliance.engine import ComplianceEngine
from src.detection.engine import DetectionResult, Finding


def _make_finding(**overrides) -> Finding:
    defaults = dict(
        client="ip_abc",
        service="ChatGPT",
        provider="OpenAI",
        category="llm_chatbot",
        risk_level="high",
        domains=["chat.openai.com"],
        total_queries=42,
        first_seen=datetime(2025, 1, 1),
        last_seen=datetime(2025, 1, 7),
        days_active=7,
        queries_per_day=6.0,
        is_systematic=False,
    )
    defaults.update(overrides)
    return Finding(**defaults)


def _make_dr(findings=None) -> DetectionResult:
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


def _sample_response() -> str:
    return json.dumps({
        "executive_summary": "Zwei nicht-autorisierte KI-Dienste erkannt.",
        "risk_assessment": "Mittleres Gesamtrisiko.",
        "finding_recommendations": [
            {
                "finding_index": 0,
                "service": "ChatGPT",
                "risk_assessment": "Hoch",
                "recommendation": "Sperren",
                "priority": "high",
            }
        ],
        "compliance_summary": {
            "DORA": "Art. 28 verletzt",
            "EU_AI_ACT": "offen",
            "ISO_42001": "offen",
            "ISO_27001": "offen",
            "DSGVO": "DSFA nötig",
        },
    }, ensure_ascii=False)


class TestSkipMode:

    def test_no_backend_no_key_skip(self, monkeypatch):
        monkeypatch.delenv("LLM_BACKEND", raising=False)
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        analyzer = ClaudeAnalyzer()
        assert analyzer.backend_name == "skip"
        assert analyzer.is_available is False

    def test_explicit_skip_via_env(self, monkeypatch):
        monkeypatch.setenv("LLM_BACKEND", "skip")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "ignored")
        analyzer = ClaudeAnalyzer(api_key="ignored-too")
        assert analyzer.is_available is False
        result = analyzer.analyze(_make_dr(), ComplianceEngine().analyze(_make_dr()))
        assert result is None


class TestBackendInjection:

    def test_inject_custom_backend(self):
        fake = MagicMock()
        fake.name = "fake"
        fake.model = "fake-model"
        fake.is_available = True
        fake.chat.return_value = _sample_response()

        analyzer = ClaudeAnalyzer(backend=fake)
        assert analyzer.backend_name == "fake"
        assert analyzer.is_available is True
        assert analyzer.active_model == "fake-model"

        finding = _make_finding()
        dr = _make_dr([finding])
        cr = ComplianceEngine().analyze(dr)
        result = analyzer.analyze(dr, cr)

        assert isinstance(result, AnalysisResult)
        assert result.backend_used == "fake"
        assert result.model_used == "fake-model"
        fake.chat.assert_called_once()
        # System prompt passed first, user prompt second
        args, kwargs = fake.chat.call_args
        assert "DORA" in args[0]  # system prompt mentions frameworks
        assert "ChatGPT" in args[1]  # user prompt contains the finding

    def test_explicit_ollama_via_env(self, monkeypatch):
        monkeypatch.setenv("LLM_BACKEND", "ollama")
        analyzer = ClaudeAnalyzer()
        assert analyzer.backend_name == "ollama"
        # Backend instance is OllamaBackend even if server unreachable
        assert isinstance(analyzer._backend, OllamaBackend)


class TestBackwardsCompatibility:
    """The old ClaudeAnalyzer(api_key=...) + analyzer._client = mock pattern must work."""

    def test_legacy_client_injection(self):
        analyzer = ClaudeAnalyzer(api_key="test-key")
        # Legacy tests reach in and replace the underlying anthropic client.
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=_sample_response())]
        mock_client.messages.create.return_value = mock_response
        analyzer._client = mock_client

        finding = _make_finding()
        dr = _make_dr([finding])
        cr = ComplianceEngine().analyze(dr)
        result = analyzer.analyze(dr, cr)

        assert isinstance(result, AnalysisResult)
        assert result.backend_used == "anthropic"
        mock_client.messages.create.assert_called_once()
