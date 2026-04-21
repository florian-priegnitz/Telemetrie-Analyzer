"""Tests für Multi-Fallback-Lookup in der Detection Engine (#50 IP-Match + #52 Alias-Match)."""

from __future__ import annotations

import pandas as pd
import pytest

from src.database.ai_endpoints import AIEndpointDatabase
from src.detection.engine import DetectionEngine


@pytest.fixture
def db() -> AIEndpointDatabase:
    return AIEndpointDatabase()


@pytest.fixture
def engine(db: AIEndpointDatabase) -> DetectionEngine:
    return DetectionEngine(db=db)


# ---------------------------------------------------------------------------
# Direktes Matching-Helpers
# ---------------------------------------------------------------------------
class TestMatchEndpoint:

    def test_none_value_returns_none(self, engine: DetectionEngine) -> None:
        assert engine._match_endpoint(None) is None
        assert engine._match_endpoint("") is None
        assert engine._match_endpoint("   ") is None

    def test_subdomain_match(self, engine: DetectionEngine) -> None:
        ep = engine._match_endpoint("chat.openai.com")
        assert ep is not None
        assert ep.service == "OpenAI ChatGPT"

    def test_alias_match_entra_app_name(self, engine: DetectionEngine) -> None:
        """Entra-Sign-In-Event mit AppDisplayName='ChatGPT' muss matchen (#52)."""
        ep = engine._match_endpoint("ChatGPT")
        assert ep is not None
        assert ep.service == "OpenAI ChatGPT"

    def test_alias_match_case_insensitive(self, engine: DetectionEngine) -> None:
        ep = engine._match_endpoint("claude")
        assert ep is not None
        assert ep.service == "Anthropic Claude"

    def test_alias_github_copilot(self, engine: DetectionEngine) -> None:
        """Entra loggt 'GitHub Copilot' als App-Name — muss direkt matchen."""
        ep = engine._match_endpoint("GitHub Copilot")
        assert ep is not None
        assert ep.service == "GitHub Copilot"

    def test_ip_range_fallback(self, engine: DetectionEngine) -> None:
        """IP im Range 140.82.112.0/20 muss auf GitHub Copilot matchen (#50)."""
        ep = engine._match_endpoint("140.82.120.5")
        assert ep is not None
        assert ep.service == "GitHub Copilot"

    def test_ip_outside_known_ranges_returns_none(self, engine: DetectionEngine) -> None:
        """Zufällige Public-IP darf nicht matchen."""
        ep = engine._match_endpoint("8.8.8.8")
        assert ep is None

    def test_subdomain_takes_precedence_over_alias(self, engine: DetectionEngine) -> None:
        """Wenn ein Eintrag als Domain existiert, wird nicht nach Alias gesucht."""
        ep = engine._match_endpoint("claude.ai")
        assert ep is not None
        assert ep.service == "Anthropic Claude"


# ---------------------------------------------------------------------------
# Ende-zu-Ende — DetectionEngine erkennt App-Namen und IP-Ranges
# ---------------------------------------------------------------------------
class TestAnalyzeWithMultifallback:

    def test_entra_style_app_name_detected(self, engine: DetectionEngine) -> None:
        """DataFrame mit domain='Microsoft 365 Copilot' (Entra-Style) → Finding."""
        df = pd.DataFrame({
            "timestamp": pd.to_datetime(["2026-04-18 09:00", "2026-04-18 09:05"]),
            "client": ["ip_client1", "ip_client1"],
            "domain": ["Microsoft 365 Copilot", "Microsoft 365 Copilot"],
        })
        result = engine.analyze(df)
        assert result.ai_queries == 2
        assert result.unique_ai_services == 1

    def test_mixed_domain_and_ip_detection(self, engine: DetectionEngine) -> None:
        """Mix aus Domain, Alias und IP wird alles erkannt."""
        df = pd.DataFrame({
            "timestamp": pd.to_datetime([
                "2026-04-18 09:00",
                "2026-04-18 09:05",
                "2026-04-18 09:10",
            ]),
            "client": ["ip_c1", "ip_c1", "ip_c1"],
            "domain": [
                "chat.openai.com",     # Subdomain-Match
                "ChatGPT",              # Alias-Match
                "140.82.120.5",         # IP-Match (GitHub Copilot)
            ],
        })
        result = engine.analyze(df)
        assert result.ai_queries == 3
        services = {f.service for f in result.findings}
        assert "OpenAI ChatGPT" in services
        assert "GitHub Copilot" in services

    def test_non_matching_domains_not_counted(self, engine: DetectionEngine) -> None:
        """Nicht-AI-Domains (Firmen-Intranet, Public Services) werden nicht gemappt."""
        df = pd.DataFrame({
            "timestamp": pd.to_datetime(["2026-04-18 09:00"]),
            "client": ["ip_c1"],
            "domain": ["intranet.corp.local"],
        })
        result = engine.analyze(df)
        assert result.ai_queries == 0
