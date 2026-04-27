"""Claude API Analyzer – KI-gestützte Analyse von Shadow-AI-Findings.

Supports pluggable backends (Anthropic cloud / Ollama self-hosted / skip).
The legacy `ClaudeAnalyzer` API stays intact so existing callers and tests
continue to work without changes.
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime

from src.analyzer.backends import (
    AnthropicBackend,
    BackendError,
    LLMBackend,
    select_backend,
)
from src.compliance.models import ComplianceResult
from src.detection.engine import DetectionResult

logger = logging.getLogger(__name__)


class AnalyzerError(Exception):
    """Raised when LLM analysis fails."""


@dataclass
class FindingRecommendation:
    """KI-generierte Empfehlung für ein einzelnes Finding."""
    finding_index: int
    service: str
    risk_assessment: str
    recommendation: str
    priority: str  # critical, high, medium, low


@dataclass
class AnalysisResult:
    """Vollständiges KI-Analyse-Ergebnis."""
    executive_summary: str
    risk_assessment: str
    finding_recommendations: list[FindingRecommendation]
    compliance_summary: dict[str, str]
    model_used: str
    backend_used: str = "anthropic"
    timestamp: datetime = field(default_factory=datetime.now)


class ClaudeAnalyzer:
    """Analysiert Detection- und Compliance-Ergebnisse mit einem LLM-Backend.

    Operates in skip mode when no backend is available (returns None).
    The class name is kept for backwards-compat — internally it now
    dispatches to a pluggable LLMBackend (Anthropic, Ollama, …).
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        backend: LLMBackend | None = None,
    ):
        self._model = model or "claude-sonnet-4-20250514"
        self._backend: LLMBackend | None = None
        self._client = None  # legacy attribute — used only by old tests/callers

        if backend is not None:
            self._backend = backend
            return

        # Resolve via env when no explicit backend given.
        env_choice = (os.environ.get("LLM_BACKEND") or "").strip().lower()
        if env_choice in {"ollama", "skip"} or env_choice == "anthropic":
            self._backend = select_backend(name=env_choice, api_key=api_key, model=model)
            return

        # Legacy auto path: stay on Anthropic if a key is provided.
        if api_key:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=api_key)
            except ImportError:
                logger.warning("anthropic package not installed, running in skip mode")

    @property
    def is_available(self) -> bool:
        """Whether the analyzer can serve a request."""
        if self._backend is not None:
            return self._backend.is_available
        return self._client is not None

    @property
    def backend_name(self) -> str:
        """Returns the active backend identifier (anthropic / ollama / skip)."""
        if self._backend is not None:
            return self._backend.name
        if self._client is not None:
            return "anthropic"
        return "skip"

    @property
    def active_model(self) -> str:
        """Effective model name from the active backend."""
        if self._backend is not None:
            return self._backend.model
        return self._model

    def analyze(
        self,
        detection_result: DetectionResult,
        compliance_result: ComplianceResult,
    ) -> AnalysisResult | None:
        """Analyze findings using the configured LLM backend.

        Returns None when no backend is available (skip mode) or on backend error.
        """
        if not self.is_available:
            logger.info("LLM Analyzer: skip mode (backend=%s)", self.backend_name)
            return None

        prompt = self._build_prompt(detection_result, compliance_result)
        system = self._system_prompt()

        try:
            response_text = self._dispatch_chat(system, prompt)
        except BackendError as exc:
            logger.error("LLM backend error: %s", exc)
            raise AnalyzerError(f"API-Analyse fehlgeschlagen: {exc}") from exc
        except Exception as exc:
            logger.error("LLM dispatch error: %s", exc)
            raise AnalyzerError(f"API-Analyse fehlgeschlagen: {exc}") from exc

        result = self._parse_response(response_text)
        result.backend_used = self.backend_name
        return result

    def _dispatch_chat(self, system: str, user: str) -> str:
        """Route the chat call to either the new backend or the legacy client."""
        if self._backend is not None:
            return self._backend.chat(system, user, max_tokens=4096)
        # Legacy direct-anthropic path (kept for backwards-compat).
        response = self._client.messages.create(
            model=self._model,
            max_tokens=4096,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return response.content[0].text

    def _system_prompt(self) -> str:
        return (
            "Du bist ein erfahrener IT-Security- und Compliance-Analyst in einem "
            "deutschen Finanzunternehmen. Du analysierst Shadow-AI-Nutzung und "
            "bewertest Risiken im Kontext von DORA, EU AI Act, ISO 42001, ISO 27001, "
            "DSGVO und dem EU Cyber Resilience Act (CRA).\n\n"
            "Antworte immer auf Deutsch. Gib deine Analyse als valides JSON zurück.\n\n"
            "JSON-Schema:\n"
            "{\n"
            '  "executive_summary": "string (3-5 Sätze für CISO)",\n'
            '  "risk_assessment": "string (Gesamtrisikobewertung)",\n'
            '  "finding_recommendations": [\n'
            "    {\n"
            '      "finding_index": int,\n'
            '      "service": "string",\n'
            '      "risk_assessment": "string",\n'
            '      "recommendation": "string (konkrete Handlungsempfehlung)",\n'
            '      "priority": "critical|high|medium|low"\n'
            "    }\n"
            "  ],\n"
            '  "compliance_summary": {\n'
            '    "DORA": "string",\n'
            '    "EU_AI_ACT": "string",\n'
            '    "ISO_42001": "string",\n'
            '    "ISO_27001": "string",\n'
            '    "DSGVO": "string"\n'
            "  }\n"
            "}\n\n"
            "Gib NUR das JSON zurück, ohne Markdown-Codeblöcke oder Erklärungen."
        )

    def _build_prompt(
        self,
        detection_result: DetectionResult,
        compliance_result: ComplianceResult,
    ) -> str:
        """Build structured prompt with findings and compliance data."""
        findings_data = []
        for idx, finding in enumerate(detection_result.findings):
            mappings = compliance_result.finding_mappings.get(idx, [])
            findings_data.append({
                "index": idx,
                "service": finding.service,
                "provider": finding.provider,
                "category": finding.category,
                "risk_level": finding.risk_level,
                "risk_score": finding.risk_score,
                "total_queries": finding.total_queries,
                "days_active": finding.days_active,
                "queries_per_day": finding.queries_per_day,
                "is_systematic": finding.is_systematic,
                "compliance_controls": [
                    {
                        "framework": m.framework.value,
                        "control_id": m.control_id,
                        "severity": m.severity.value,
                        "status": m.assessment_status.value,
                    }
                    for m in mappings
                ],
            })

        scores_data = {
            fw.value: {
                "score_percent": score.score_percent,
                "non_compliant": score.non_compliant,
                "partially_compliant": score.partially_compliant,
            }
            for fw, score in compliance_result.framework_scores.items()
        }

        data = {
            "analysis_period": {
                "start": str(detection_result.analysis_period_start),
                "end": str(detection_result.analysis_period_end),
            },
            "total_queries": detection_result.total_queries,
            "ai_queries": detection_result.ai_queries,
            "ai_query_ratio": round(detection_result.ai_query_ratio, 4),
            "unique_clients": detection_result.unique_clients,
            "findings": findings_data,
            "compliance_scores": scores_data,
        }

        return (
            "Analysiere die folgenden Shadow-AI-Erkennungen und erstelle eine "
            "Risikobewertung mit Handlungsempfehlungen.\n\n"
            f"{json.dumps(data, indent=2, ensure_ascii=False)}"
        )

    def _parse_response(self, response_text: str) -> AnalysisResult:
        """Parse the backend's JSON response into AnalysisResult."""
        text = response_text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise AnalyzerError(f"Ungültige JSON-Antwort vom Backend: {e}") from e

        recommendations = [
            FindingRecommendation(
                finding_index=r.get("finding_index", i),
                service=r.get("service", ""),
                risk_assessment=r.get("risk_assessment", ""),
                recommendation=r.get("recommendation", ""),
                priority=r.get("priority", "medium"),
            )
            for i, r in enumerate(data.get("finding_recommendations", []))
        ]

        return AnalysisResult(
            executive_summary=data.get("executive_summary", ""),
            risk_assessment=data.get("risk_assessment", ""),
            finding_recommendations=recommendations,
            compliance_summary=data.get("compliance_summary", {}),
            model_used=self.active_model,
            backend_used=self.backend_name,
        )


# Re-export for direct module-level imports used by tests / settings.
__all__ = [
    "AnalysisResult",
    "AnalyzerError",
    "AnthropicBackend",
    "ClaudeAnalyzer",
    "FindingRecommendation",
    "select_backend",
]
