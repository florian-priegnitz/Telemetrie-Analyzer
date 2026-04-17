"""Daten-Vertrag zwischen Engine-Output und Templates.

Templates dürfen ausschliesslich auf `ReportContext`-Felder zugreifen — niemals
direkt auf Engine-interne Objekte. Das hält die Templates frei von Engine-Wissen
und konzentriert die DSGVO-Filterung auf eine einzige Schicht.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from src.compliance.models import (
    AssessmentStatus,
    ComplianceMapping,
    ComplianceResult,
    ComplianceScore,
    Framework,
    Severity,
)
from src.detection.engine import DetectionResult, Finding
from src.reports.privacy import pseudonymize_client


@dataclass
class FindingView:
    """Pro-Finding-View für Templates (pseudonymisiert, sortier-ready)."""
    client_pseudonym: str
    service: str
    provider: str
    category: str
    risk_level: str
    risk_score: int
    domains: list[str]
    total_queries: int
    queries_per_day: float
    is_systematic: bool
    days_active: int
    first_seen: datetime
    last_seen: datetime
    has_document_upload: bool
    upload_events: int
    total_bytes_uploaded: int
    compliance_mappings: list[ComplianceMapping] = field(default_factory=list)


@dataclass
class FrameworkScoreView:
    framework: str
    framework_label: str
    score_percent: float
    total_controls: int
    triggered_controls: int
    non_compliant: int
    partially_compliant: int
    needs_review: int
    severity_counts: dict[str, int]  # critical/high/medium/low → count


@dataclass
class ReportContext:
    """Render-Kontext, den Templates und JSON-Serializer konsumieren."""
    generated_at: datetime
    period_start: datetime | None
    period_end: datetime | None
    pseudonymized: bool
    salt_fingerprint: str  # ersten 8 Zeichen vom HMAC(salt) — kein Salt-Leak

    # Summary
    total_queries: int
    ai_queries: int
    ai_query_ratio: float
    non_ai_queries: int
    unique_clients: int
    unique_ai_services: int
    upload_events_total: int
    total_bytes_uploaded: int

    # Findings & Frameworks
    findings: list[FindingView]
    top_findings: list[FindingView]  # Top-3 nach risk_score
    framework_scores: list[FrameworkScoreView]
    overall_compliance_percent: float  # Mittelwert über alle Frameworks
    compliance_traffic_light: str  # green / yellow / red

    # Embedded Charts (HTML-Snippets, bereits gerendert)
    charts: dict[str, str] = field(default_factory=dict)


_FRAMEWORK_LABELS: dict[Framework, str] = {
    Framework.DORA: "DORA",
    Framework.EU_AI_ACT: "EU AI Act",
    Framework.ISO_42001: "ISO/IEC 42001",
    Framework.ISO_27001: "ISO/IEC 27001",
    Framework.DSGVO: "DSGVO",
}


def _traffic_light(percent: float) -> str:
    if percent >= 80.0:
        return "green"
    if percent >= 50.0:
        return "yellow"
    return "red"


def _severity_counts_for_framework(
    framework: Framework,
    finding_mappings: dict[int, list[ComplianceMapping]],
) -> dict[str, int]:
    counts = {s.value: 0 for s in Severity}
    for mappings in finding_mappings.values():
        for m in mappings:
            if m.framework == framework:
                counts[m.severity.value] += 1
    return counts


def _build_finding_view(
    finding: Finding, salt: str, mappings: list[ComplianceMapping]
) -> FindingView:
    return FindingView(
        client_pseudonym=pseudonymize_client(finding.client, salt),
        service=finding.service,
        provider=finding.provider,
        category=finding.category,
        risk_level=finding.risk_level,
        risk_score=finding.risk_score,
        domains=finding.domains,
        total_queries=finding.total_queries,
        queries_per_day=finding.queries_per_day,
        is_systematic=finding.is_systematic,
        days_active=finding.days_active,
        first_seen=finding.first_seen,
        last_seen=finding.last_seen,
        has_document_upload=finding.has_document_upload,
        upload_events=finding.upload_events,
        total_bytes_uploaded=finding.total_bytes_uploaded,
        compliance_mappings=mappings,
    )


def _salt_fingerprint(salt: str) -> str:
    """Kurzer Hash des Salts — erlaubt Reproduzierbarkeits-Vergleich, leakt aber nichts."""
    import hashlib
    return hashlib.sha256(salt.encode("utf-8")).hexdigest()[:8]


def build_context(
    detection_result: DetectionResult,
    compliance_result: ComplianceResult,
    salt: str,
    charts: dict[str, str] | None = None,
) -> ReportContext:
    """Baut den ReportContext aus Detection- + Compliance-Result + Salt."""
    findings_view: list[FindingView] = []
    upload_events_total = 0
    total_bytes_uploaded = 0

    for idx, finding in enumerate(detection_result.findings):
        mappings = compliance_result.finding_mappings.get(idx, [])
        view = _build_finding_view(finding, salt, mappings)
        findings_view.append(view)
        upload_events_total += view.upload_events
        total_bytes_uploaded += view.total_bytes_uploaded

    findings_view.sort(key=lambda f: f.risk_score, reverse=True)
    top_findings = findings_view[:3]

    framework_views: list[FrameworkScoreView] = []
    for fw, score in compliance_result.framework_scores.items():
        framework_views.append(FrameworkScoreView(
            framework=fw.value,
            framework_label=_FRAMEWORK_LABELS.get(fw, fw.value),
            score_percent=score.score_percent,
            total_controls=score.total_controls,
            triggered_controls=score.triggered_controls,
            non_compliant=score.non_compliant,
            partially_compliant=score.partially_compliant,
            needs_review=score.needs_review,
            severity_counts=_severity_counts_for_framework(fw, compliance_result.finding_mappings),
        ))

    framework_views.sort(key=lambda fv: fv.score_percent)

    overall = (
        sum(fv.score_percent for fv in framework_views) / len(framework_views)
        if framework_views else 100.0
    )

    return ReportContext(
        generated_at=datetime.now(timezone.utc).replace(tzinfo=None),
        period_start=detection_result.analysis_period_start,
        period_end=detection_result.analysis_period_end,
        pseudonymized=True,
        salt_fingerprint=_salt_fingerprint(salt),
        total_queries=detection_result.total_queries,
        ai_queries=detection_result.ai_queries,
        non_ai_queries=detection_result.non_ai_queries,
        ai_query_ratio=round(detection_result.ai_query_ratio, 4),
        unique_clients=detection_result.unique_clients,
        unique_ai_services=detection_result.unique_ai_services,
        upload_events_total=upload_events_total,
        total_bytes_uploaded=total_bytes_uploaded,
        findings=findings_view,
        top_findings=top_findings,
        framework_scores=framework_views,
        overall_compliance_percent=round(overall, 1),
        compliance_traffic_light=_traffic_light(overall),
        charts=charts or {},
    )


def context_to_json_dict(ctx: ReportContext) -> dict[str, Any]:
    """Serialisiert den ReportContext zu einem JSON-tauglichen dict (ohne Charts)."""
    def _ts(d: datetime | None) -> str | None:
        return d.isoformat() if d else None

    return {
        "report_meta": {
            "generated_at": _ts(ctx.generated_at),
            "version": "0.1.0",
            "pseudonymized": ctx.pseudonymized,
            "salt_fingerprint": ctx.salt_fingerprint,
            "period": {"start": _ts(ctx.period_start), "end": _ts(ctx.period_end)},
        },
        "summary": {
            "total_queries": ctx.total_queries,
            "ai_queries": ctx.ai_queries,
            "non_ai_queries": ctx.non_ai_queries,
            "ai_query_ratio": ctx.ai_query_ratio,
            "unique_clients": ctx.unique_clients,
            "unique_ai_services": ctx.unique_ai_services,
            "upload_events_total": ctx.upload_events_total,
            "total_bytes_uploaded": ctx.total_bytes_uploaded,
            "overall_compliance_percent": ctx.overall_compliance_percent,
            "compliance_traffic_light": ctx.compliance_traffic_light,
        },
        "framework_scores": [
            {
                "framework": fv.framework,
                "framework_label": fv.framework_label,
                "score_percent": fv.score_percent,
                "total_controls": fv.total_controls,
                "triggered_controls": fv.triggered_controls,
                "non_compliant": fv.non_compliant,
                "partially_compliant": fv.partially_compliant,
                "needs_review": fv.needs_review,
                "severity_counts": fv.severity_counts,
            } for fv in ctx.framework_scores
        ],
        "findings": [
            {
                "client_pseudonym": f.client_pseudonym,
                "service": f.service,
                "provider": f.provider,
                "category": f.category,
                "risk_level": f.risk_level,
                "risk_score": f.risk_score,
                "domains": f.domains,
                "total_queries": f.total_queries,
                "queries_per_day": f.queries_per_day,
                "is_systematic": f.is_systematic,
                "days_active": f.days_active,
                "first_seen": _ts(f.first_seen),
                "last_seen": _ts(f.last_seen),
                "has_document_upload": f.has_document_upload,
                "upload_events": f.upload_events,
                "total_bytes_uploaded": f.total_bytes_uploaded,
                "compliance_mappings": [
                    {
                        "framework": m.framework.value,
                        "control_id": m.control_id,
                        "control_name": m.control_name,
                        "severity": m.severity.value,
                        "assessment_status": m.assessment_status.value,
                        "rationale": m.rationale,
                    } for m in f.compliance_mappings
                ],
            } for f in ctx.findings
        ],
    }
