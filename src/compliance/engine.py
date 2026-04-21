"""Compliance Engine – Maps detection findings to regulatory framework controls."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from src.compliance.models import (
    AssessmentStatus,
    ComplianceMapping,
    ComplianceResult,
    ComplianceScore,
    Framework,
    Severity,
)
from src.detection.engine import DetectionResult, Finding

# ---------------------------------------------------------------------------
# Rule definitions
# ---------------------------------------------------------------------------

# All cloud/SaaS categories (all AI services are cloud-hosted)
_CLOUD_CATEGORIES = {
    "llm_chatbot", "code_assistant", "image_generation", "ml_platform",
    "content_generation", "writing_assistant", "translation", "productivity_ai",
    "speech_to_text", "text_to_speech", "video_generation", "llm_api",
    "audio_generation",
}

# High-risk AI categories per EU AI Act
_HIGH_RISK_AI_CATEGORIES = {"code_assistant", "llm_chatbot", "llm_api", "ml_platform"}


def _severity_from_risk(finding: Finding) -> Severity:
    """Derive severity directly from finding risk_level."""
    return Severity(finding.risk_level)


def _status_from_score(finding: Finding) -> AssessmentStatus:
    """Derive assessment status from risk_score thresholds."""
    score = finding.risk_score
    if score >= 70:
        return AssessmentStatus.NON_COMPLIANT
    if score >= 40:
        return AssessmentStatus.PARTIALLY_COMPLIANT
    return AssessmentStatus.NEEDS_REVIEW


@dataclass
class _Rule:
    """Internal rule mapping a condition to a compliance control."""
    framework: Framework
    control_id: str
    control_name: str
    condition: Callable[[Finding], bool]
    severity_fn: Callable[[Finding], Severity]
    rationale_template: str


def _build_rules() -> list[_Rule]:
    """Build the complete rule table for all frameworks."""
    return [
        # --- ISO 27001 ---
        _Rule(
            framework=Framework.ISO_27001,
            control_id="A.5.9",
            control_name="Inventory of Information and Other Associated Assets",
            condition=lambda f: True,  # every shadow AI = unmanaged asset
            severity_fn=_severity_from_risk,
            rationale_template="Nicht-inventarisierter KI-Dienst '{service}' von {provider} erkannt.",
        ),
        _Rule(
            framework=Framework.ISO_27001,
            control_id="A.5.23",
            control_name="Information Security for Use of Cloud Services",
            condition=lambda f: f.category in _CLOUD_CATEGORIES,
            severity_fn=_severity_from_risk,
            rationale_template="Cloud-basierter KI-Dienst '{service}' ohne Sicherheitsbewertung genutzt.",
        ),
        _Rule(
            framework=Framework.ISO_27001,
            control_id="A.8.16",
            control_name="Monitoring Activities",
            condition=lambda f: f.is_systematic,
            severity_fn=lambda f: Severity.HIGH if f.risk_score >= 50 else Severity.MEDIUM,
            rationale_template="Systematische Nutzung von '{service}' ({queries_per_day} Queries/Tag) ohne Monitoring.",
        ),

        # --- DORA ---
        _Rule(
            framework=Framework.DORA,
            control_id="Art. 28",
            control_name="ICT Third-Party Risk",
            condition=lambda f: True,  # all external AI = third-party ICT
            severity_fn=_severity_from_risk,
            rationale_template="Nicht-autorisierter ICT-Drittanbieter '{service}' ({provider}) im Einsatz.",
        ),
        _Rule(
            framework=Framework.DORA,
            control_id="Art. 5",
            control_name="ICT Governance",
            condition=lambda f: f.is_systematic,
            severity_fn=lambda f: Severity.HIGH,
            rationale_template="Systematische Nutzung von '{service}' ohne ICT-Governance-Freigabe.",
        ),
        _Rule(
            framework=Framework.DORA,
            control_id="Art. 6",
            control_name="ICT Risk Management Framework",
            condition=lambda f: f.risk_level in ("critical", "high"),
            severity_fn=_severity_from_risk,
            rationale_template="Hochrisiko-KI-Dienst '{service}' (Risiko: {risk_level}) ohne Risikomanagement.",
        ),

        # --- EU AI Act ---
        _Rule(
            framework=Framework.EU_AI_ACT,
            control_id="Art. 6",
            control_name="Classification Rules for High-Risk AI Systems",
            condition=lambda f: f.category in _HIGH_RISK_AI_CATEGORIES,
            severity_fn=_severity_from_risk,
            rationale_template="KI-System '{service}' (Kategorie: {category}) erfordert Risikoklassifizierung.",
        ),
        _Rule(
            framework=Framework.EU_AI_ACT,
            control_id="Art. 9",
            control_name="Risk Management System",
            condition=lambda f: f.risk_score >= 50,
            severity_fn=lambda f: Severity.HIGH,
            rationale_template="KI-Dienst '{service}' mit Risk-Score {risk_score} ohne Risk-Management-System.",
        ),
        _Rule(
            framework=Framework.EU_AI_ACT,
            control_id="Art. 53",
            control_name="Obligations for Providers of General-Purpose AI Models",
            condition=lambda f: "llm" in f.category or f.category == "ml_platform",
            severity_fn=lambda f: Severity.MEDIUM,
            rationale_template="GPAI-Modell '{service}' ohne Transparenz-Dokumentation im Einsatz.",
        ),

        # --- ISO 42001 ---
        _Rule(
            framework=Framework.ISO_42001,
            control_id="6.1.2",
            control_name="AI Risk Assessment",
            condition=lambda f: True,  # every AI = needs risk assessment
            severity_fn=_severity_from_risk,
            rationale_template="KI-Dienst '{service}' ohne AI-Risikobewertung im Einsatz.",
        ),
        _Rule(
            framework=Framework.ISO_42001,
            control_id="8.4",
            control_name="AI System Operation",
            condition=lambda f: f.is_systematic,
            severity_fn=lambda f: Severity.HIGH,
            rationale_template="Systematischer Betrieb von '{service}' ohne definierte Betriebsprozesse.",
        ),

        # --- DSGVO ---
        _Rule(
            framework=Framework.DSGVO,
            control_id="Art. 6",
            control_name="Rechtmäßigkeit der Verarbeitung",
            condition=lambda f: True,  # data sent to external AI = processing
            severity_fn=_severity_from_risk,
            rationale_template="Datenverarbeitung durch '{service}' ({provider}) ohne Rechtsgrundlage.",
        ),
        _Rule(
            framework=Framework.DSGVO,
            control_id="Art. 25",
            control_name="Datenschutz durch Technikgestaltung",
            condition=lambda f: True,
            severity_fn=lambda f: Severity.MEDIUM,
            rationale_template="KI-Dienst '{service}' ohne Privacy-by-Design-Bewertung.",
        ),
        _Rule(
            framework=Framework.DSGVO,
            control_id="Art. 35",
            control_name="Datenschutz-Folgenabschätzung",
            condition=lambda f: f.risk_level in ("critical", "high"),
            severity_fn=lambda f: Severity.HIGH,
            rationale_template="Hochrisiko-KI-Dienst '{service}' erfordert DSFA (Datentransfer an {provider}).",
        ),
    ]


# Total number of unique controls across all frameworks
_CONTROLS_PER_FRAMEWORK: dict[Framework, int] = {
    Framework.ISO_27001: 3,   # A.5.9, A.5.23, A.8.16
    Framework.DORA: 3,        # Art. 5, Art. 6, Art. 28
    Framework.EU_AI_ACT: 3,   # Art. 6, Art. 9, Art. 53
    Framework.ISO_42001: 2,   # 6.1.2, 8.4
    Framework.DSGVO: 3,       # Art. 6, Art. 25, Art. 35
}


# ---------------------------------------------------------------------------
# Compliance Engine
# ---------------------------------------------------------------------------

class ComplianceEngine:
    """Maps detection findings to regulatory compliance controls."""

    def __init__(self) -> None:
        self._rules = _build_rules()

    def analyze(self, detection_result: DetectionResult) -> ComplianceResult:
        """Analyze all findings and produce compliance mappings and scores.

        Also populates each finding's compliance_mappings list in-place.
        """
        finding_mappings: dict[int, list[ComplianceMapping]] = {}

        for idx, finding in enumerate(detection_result.findings):
            mappings = self._map_finding(finding)
            finding_mappings[idx] = mappings
            finding.compliance_mappings = mappings

        framework_scores = self._compute_scores(finding_mappings)

        return ComplianceResult(
            finding_mappings=finding_mappings,
            framework_scores=framework_scores,
        )

    def _map_finding(self, finding: Finding) -> list[ComplianceMapping]:
        """Apply all rules to a single finding."""
        mappings: list[ComplianceMapping] = []

        for rule in self._rules:
            if not rule.condition(finding):
                continue

            rationale = rule.rationale_template.format(
                service=finding.service,
                provider=finding.provider,
                category=finding.category,
                risk_level=finding.risk_level,
                risk_score=finding.risk_score,
                queries_per_day=finding.queries_per_day,
            )

            mappings.append(ComplianceMapping(
                framework=rule.framework,
                control_id=rule.control_id,
                control_name=rule.control_name,
                severity=rule.severity_fn(finding),
                assessment_status=_status_from_score(finding),
                rationale=rationale,
            ))

        return mappings

    def _compute_scores(
        self, all_mappings: dict[int, list[ComplianceMapping]]
    ) -> dict[Framework, ComplianceScore]:
        """Aggregate mappings into per-framework compliance scores."""
        # Collect worst status per (framework, control_id)
        worst: dict[tuple[Framework, str], AssessmentStatus] = {}

        for mappings in all_mappings.values():
            for m in mappings:
                key = (m.framework, m.control_id)
                status_rank = {
                    AssessmentStatus.NON_COMPLIANT: 3,
                    AssessmentStatus.PARTIALLY_COMPLIANT: 2,
                    AssessmentStatus.NEEDS_REVIEW: 1,
                    AssessmentStatus.COMPLIANT: 0,
                }
                current = worst.get(key)
                if current is None or status_rank[m.assessment_status] > status_rank[current]:
                    worst[key] = m.assessment_status

        # Build scores per framework
        scores: dict[Framework, ComplianceScore] = {}
        for fw in Framework:
            triggered: dict[str, AssessmentStatus] = {
                ctrl: status for (f, ctrl), status in worst.items() if f == fw
            }
            non_c = sum(1 for s in triggered.values() if s == AssessmentStatus.NON_COMPLIANT)
            partial = sum(1 for s in triggered.values() if s == AssessmentStatus.PARTIALLY_COMPLIANT)
            review = sum(1 for s in triggered.values() if s == AssessmentStatus.NEEDS_REVIEW)

            scores[fw] = ComplianceScore(
                framework=fw,
                total_controls=_CONTROLS_PER_FRAMEWORK[fw],
                triggered_controls=len(triggered),
                non_compliant=non_c,
                partially_compliant=partial,
                needs_review=review,
            )

        return scores
