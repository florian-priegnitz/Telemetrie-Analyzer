"""Claude API Analyzer – KI-gestützte Analyse von Shadow-AI-Findings."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime

from src.compliance.models import ComplianceResult, Framework
from src.detection.engine import DetectionResult

logger = logging.getLogger(__name__)


class AnalyzerError(Exception):
    """Raised when Claude API analysis fails."""


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
    compliance_summary: dict[str, str]  # framework name -> assessment text
    model_used: str
    timestamp: datetime = field(default_factory=datetime.now)


class ClaudeAnalyzer:
    """Analysiert Detection- und Compliance-Ergebnisse mit Claude API.

    Operates in skip mode when no API key is provided (returns None).
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "claude-sonnet-4-20250514",
    ):
        self._client = None
        self._model = model

        if api_key:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=api_key)
            except ImportError:
                logger.warning("anthropic package not installed, running in skip mode")

    @property
    def is_available(self) -> bool:
        """Whether the analyzer has an active API client."""
        return self._client is not None

    def analyze(
        self,
        detection_result: DetectionResult,
        compliance_result: ComplianceResult,
    ) -> AnalysisResult | None:
        """Analyze findings using Claude API.

        Returns None if no API key (skip mode) or on API error.
        """
        if not self._client:
            logger.info("Claude Analyzer: Skip mode (no API key)")
            return None

        prompt = self._build_prompt(detection_result, compliance_result)

        try:
            response = self._client.messages.create(
                model=self._model,
                max_tokens=4096,
                system=self._system_prompt(),
                messages=[{"role": "user", "content": prompt}],
            )

            response_text = response.content[0].text
            return self._parse_response(response_text)

        except Exception as e:
            logger.error("Claude API error: %s", e)
            raise AnalyzerError(f"API-Analyse fehlgeschlagen: {e}") from e

    def _system_prompt(self) -> str:
        return (
            "Du bist ein erfahrener IT-Security- und Compliance-Analyst in einem "
            "deutschen Finanzunternehmen. Du analysierst Shadow-AI-Nutzung und "
            "bewertest Risiken im Kontext von DORA, EU AI Act, ISO 42001, ISO 27001 "
            "und DSGVO.\n\n"
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
        """Parse Claude's JSON response into AnalysisResult."""
        # Strip markdown code fences if present
        text = response_text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()

        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise AnalyzerError(f"Ungültige JSON-Antwort von Claude: {e}") from e

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
            model_used=self._model,
        )
