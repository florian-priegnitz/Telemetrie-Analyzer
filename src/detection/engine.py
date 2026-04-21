"""Detection Engine – Erkennung von Shadow AI Nutzung in DNS-Daten.

Matching von DNS-Queries gegen die AI Endpoint Database,
Frequenz-Analyse und Klassifizierung.
"""

from dataclasses import dataclass, field
from datetime import datetime

import pandas as pd

from src.analytics.temporal import off_hours_ratio
from src.database.ai_endpoints import AIEndpoint, AIEndpointDatabase


@dataclass
class Finding:
    """Ein erkanntes Shadow-AI-Nutzungsmuster."""
    client: str
    service: str
    provider: str
    category: str
    risk_level: str
    domains: list[str]
    total_queries: int
    first_seen: datetime
    last_seen: datetime
    days_active: int
    queries_per_day: float
    is_systematic: bool  # >10 Requests/Tag
    compliance_mappings: list = field(default_factory=list)
    upload_events: int = 0
    total_bytes_uploaded: int = 0
    has_document_upload: bool = False
    off_hours_ratio: float = 0.0  # Anteil Queries außerhalb Business-Hours (E2-2)

    @property
    def risk_score(self) -> int:
        """Risiko-Score 0-100 basierend auf Nutzungsmuster und Dienst-Risiko."""
        base = {"critical": 70, "high": 50, "medium": 30, "low": 10}
        score = base.get(self.risk_level, 30)

        # Systematische Nutzung erhöht Score
        if self.is_systematic:
            score += 15

        # Langfristige Nutzung (>7 Tage) erhöht Score
        if self.days_active > 7:
            score += 10
        elif self.days_active > 1:
            score += 5

        # Hohe Frequenz erhöht Score
        if self.queries_per_day > 50:
            score += 5

        # Document-Upload erhöht Score (Datenabfluss-Risiko)
        if self.has_document_upload:
            score += UPLOAD_RISK_BOOST

        # Off-Hours-Nutzung erhöht Score (Anomalie-Indikator, E2-2)
        if self.off_hours_ratio > OFF_HOURS_TRIGGER_RATIO:
            score += OFF_HOURS_RISK_BOOST

        return min(score, 100)


@dataclass
class DetectionResult:
    """Gesamtergebnis einer Detection-Analyse."""
    findings: list[Finding]
    total_queries: int
    ai_queries: int
    non_ai_queries: int
    analysis_period_start: datetime | None
    analysis_period_end: datetime | None
    unique_clients: int
    unique_ai_services: int

    @property
    def ai_query_ratio(self) -> float:
        if self.total_queries == 0:
            return 0.0
        return self.ai_queries / self.total_queries


SYSTEMATIC_THRESHOLD = 10  # Requests pro Tag
UPLOAD_THRESHOLD_BYTES = 500 * 1024  # >500 KB = vermutlich Dokument-Upload (CLAUDE.md)
UPLOAD_RISK_BOOST = 20  # Additiv zum Base-Score wenn Dokument-Upload erkannt
OFF_HOURS_TRIGGER_RATIO = 0.3  # ab 30% Off-Hours-Queries gilt Nutzung als anomal (E2-2)
OFF_HOURS_RISK_BOOST = 15  # Additiv wenn off_hours_ratio > OFF_HOURS_TRIGGER_RATIO


class DetectionEngine:
    """Erkennt Shadow-AI-Nutzung durch Matching und Frequenz-Analyse."""

    def __init__(self, db: AIEndpointDatabase | None = None):
        self._db = db or AIEndpointDatabase()

    def analyze(self, df: pd.DataFrame) -> DetectionResult:
        """Analysiert ein DNS-Query-DataFrame auf Shadow-AI-Nutzung.

        Args:
            df: DataFrame mit Spalten: timestamp, domain, client
                (wie von parse_pihole_log erzeugt)

        Returns:
            DetectionResult mit allen erkannten Findings
        """
        if df.empty:
            return DetectionResult(
                findings=[], total_queries=0, ai_queries=0,
                non_ai_queries=0, analysis_period_start=None,
                analysis_period_end=None, unique_clients=0,
                unique_ai_services=0,
            )

        # AI-Domains matchen — Multi-Fallback:
        # 1. Subdomain-Match gegen `domains` (Default-Pfad)
        # 2. Alias-Match (Entra AppDisplayName o.ä. — #52)
        # 3. IP-Range-Match (AWS VPC Flow mit dstaddr=IP — #50)
        df = df.copy()
        df["ai_match"] = df["domain"].apply(self._match_endpoint)

        ai_df = df[df["ai_match"].notna()]
        findings = self._build_findings(ai_df)

        return DetectionResult(
            findings=findings,
            total_queries=len(df),
            ai_queries=len(ai_df),
            non_ai_queries=len(df) - len(ai_df),
            analysis_period_start=df["timestamp"].min(),
            analysis_period_end=df["timestamp"].max(),
            unique_clients=df["client"].nunique(),
            unique_ai_services=len({f.service for f in findings}),
        )

    def _match_endpoint(self, value: str | None) -> AIEndpoint | None:
        """Multi-Fallback-Lookup für heterogene ``domain``-Werte.

        Reihenfolge: Subdomain → Alias → IP-Range. Der erste Treffer gewinnt.
        Leere / None-Werte liefern None zurück.
        """
        if not value or not isinstance(value, str):
            return None
        text = value.strip()
        if not text:
            return None
        if result := self._db.lookup_subdomain(text):
            return result
        if result := self._db.lookup_alias(text):
            return result
        # IP-Range-Fallback (#50): nur wenn value wie eine IP aussieht
        if text.replace(".", "").replace(":", "").isalnum() and any(c.isdigit() for c in text):
            if result := self._db.lookup_ip(text):
                return result
        return None

    def _build_findings(self, ai_df: pd.DataFrame) -> list[Finding]:
        """Gruppiert AI-Queries nach Client+Service und erzeugt Findings."""
        if ai_df.empty:
            return []

        has_upload_col = "bytes_uploaded" in ai_df.columns
        findings: list[Finding] = []

        # Gruppierung nach Client und Service
        for (client, service), group in ai_df.groupby(
            [ai_df["client"], ai_df["ai_match"].apply(lambda ep: ep.service)]
        ):
            endpoint: AIEndpoint = group["ai_match"].iloc[0]
            first_seen = group["timestamp"].min()
            last_seen = group["timestamp"].max()
            days_active = max((last_seen - first_seen).days, 1)
            queries_per_day = len(group) / days_active

            upload_events = 0
            total_bytes_uploaded = 0
            has_document_upload = False
            if has_upload_col:
                uploads = group["bytes_uploaded"].dropna()
                if not uploads.empty:
                    total_bytes_uploaded = int(uploads.sum())
                    upload_events = int((uploads > UPLOAD_THRESHOLD_BYTES).sum())
                    has_document_upload = upload_events > 0

            findings.append(Finding(
                client=client,
                service=service,
                provider=endpoint.provider,
                category=endpoint.category,
                risk_level=endpoint.risk_level,
                domains=sorted(group["domain"].unique().tolist()),
                total_queries=len(group),
                first_seen=first_seen.to_pydatetime(),
                last_seen=last_seen.to_pydatetime(),
                days_active=days_active,
                queries_per_day=round(queries_per_day, 1),
                is_systematic=queries_per_day > SYSTEMATIC_THRESHOLD,
                upload_events=upload_events,
                total_bytes_uploaded=total_bytes_uploaded,
                has_document_upload=has_document_upload,
                off_hours_ratio=round(off_hours_ratio(group), 3),
            ))

        # Sortierung: höchster Risk-Score zuerst
        findings.sort(key=lambda f: f.risk_score, reverse=True)
        return findings
