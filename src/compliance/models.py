"""Compliance data models for regulatory framework mapping."""

from dataclasses import dataclass, field
from enum import Enum


class Framework(str, Enum):
    """Supported regulatory frameworks."""
    DORA = "DORA"
    EU_AI_ACT = "EU_AI_ACT"
    ISO_42001 = "ISO_42001"
    ISO_27001 = "ISO_27001"
    DSGVO = "DSGVO"


class Severity(str, Enum):
    """Severity levels for compliance findings."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AssessmentStatus(str, Enum):
    """Assessment status for compliance controls."""
    NON_COMPLIANT = "non_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NEEDS_REVIEW = "needs_review"
    COMPLIANT = "compliant"


@dataclass
class ComplianceMapping:
    """Maps a finding to a specific regulatory control."""
    framework: Framework
    control_id: str
    control_name: str
    severity: Severity
    assessment_status: AssessmentStatus
    rationale: str


@dataclass
class ComplianceScore:
    """Compliance score for a single framework."""
    framework: Framework
    total_controls: int
    triggered_controls: int
    non_compliant: int
    partially_compliant: int
    needs_review: int

    @property
    def score_percent(self) -> float:
        """Compliance score as percentage (0-100). Higher = more compliant."""
        if self.total_controls == 0:
            return 100.0
        compliant = self.total_controls - (
            self.non_compliant + self.partially_compliant + self.needs_review
        )
        return round(compliant / self.total_controls * 100, 1)


@dataclass
class ComplianceResult:
    """Complete compliance analysis result."""
    finding_mappings: dict[int, list[ComplianceMapping]] = field(default_factory=dict)
    framework_scores: dict[Framework, ComplianceScore] = field(default_factory=dict)
