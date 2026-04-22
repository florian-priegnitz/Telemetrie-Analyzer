"""Tests für ASN-Fallback (E1-7, Issue #15)."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from src.detection.asn_fallback import AsnDatabase
from src.detection.engine import DetectionEngine

_DEFAULT_DB = Path(__file__).resolve().parent.parent / "data" / "ai_ip_ranges.json"


# ---------------------------------------------------------------------------
# AsnDatabase — lookup + data integrity
# ---------------------------------------------------------------------------

class TestAsnDatabase:

    def setup_method(self):
        self.db = AsnDatabase()

    def test_default_db_loads(self):
        assert self.db.version
        assert self.db.updated

    def test_anthropic_range_matches(self):
        # 160.79.104.0/23 — erstes Drittel der Range
        match = self.db.lookup("160.79.104.42")
        assert match is not None
        assert match.provider == "Anthropic"
        assert match.service_hint == "Anthropic Claude"
        assert match.confidence == "low"

    def test_unknown_ip_returns_none(self):
        assert self.db.lookup("8.8.8.8") is None

    def test_invalid_ip_returns_none(self):
        assert self.db.lookup("nonsense") is None
        assert self.db.lookup("") is None
        assert self.db.lookup("999.999.999.999") is None

    def test_all_matches_are_low_confidence(self):
        """#15 Akzeptanzkriterium: Match-Confidence ist immer 'low'."""
        # Sample je einen bekannten Provider an
        samples = [
            ("160.79.104.1", "Anthropic"),
            ("23.102.140.113", "OpenAI"),
            ("34.64.1.1", "Google Vertex AI"),
            ("3.210.1.1", "AWS Bedrock"),
            ("20.50.1.1", "Azure OpenAI"),
        ]
        for ip, expected in samples:
            match = self.db.lookup(ip)
            assert match is not None, f"{expected} range sollte {ip} matchen"
            assert match.provider == expected
            assert match.confidence == "low"

    def test_ranges_do_not_overlap(self):
        """Kein ASN-Range darf mit einem anderen überlappen (ambiguer Lookup)."""
        networks = [net for net, _ in self.db._networks]
        for i, a in enumerate(networks):
            for b in networks[i + 1 :]:
                if a.version != b.version:
                    continue
                assert not a.overlaps(b), f"Overlap: {a} und {b}"


# ---------------------------------------------------------------------------
# DetectionEngine — opt-in integration
# ---------------------------------------------------------------------------

class TestDetectionEngineAsnFallback:

    def _df(self, rows: list[dict]) -> pd.DataFrame:
        return pd.DataFrame(rows)

    def test_asn_fallback_disabled_by_default(self):
        """Ohne Opt-in bleibt Anthropic-IP unerkannt."""
        engine = DetectionEngine()
        df = self._df([
            {"timestamp": datetime(2026, 4, 1, 10), "client": "ip_a", "domain": "160.79.104.1"},
        ])
        result = engine.analyze(df)
        assert result.ai_queries == 0

    def test_asn_fallback_matches_anthropic_ip_when_enabled(self):
        engine = DetectionEngine(enable_asn_fallback=True)
        df = self._df([
            {"timestamp": datetime(2026, 4, 1, 10), "client": "ip_a", "domain": "160.79.104.1"},
            {"timestamp": datetime(2026, 4, 1, 11), "client": "ip_a", "domain": "160.79.104.1"},
        ])
        result = engine.analyze(df)
        assert result.ai_queries == 2
        assert len(result.findings) == 1
        f = result.findings[0]
        assert f.service == "Anthropic Claude"
        assert f.provider == "Anthropic"
        assert f.category == "llm_api"

    def test_asn_fallback_runs_after_other_lookups(self):
        """Bekannte Domain gewinnt auch bei aktivem ASN-Fallback."""
        engine = DetectionEngine(enable_asn_fallback=True)
        df = self._df([
            {"timestamp": datetime(2026, 4, 1, 10), "client": "ip_a", "domain": "chat.openai.com"},
        ])
        result = engine.analyze(df)
        assert result.ai_queries == 1
        # Match kommt aus Domain-Lookup, nicht ASN
        assert result.findings[0].service == "OpenAI ChatGPT"

    def test_asn_fallback_ignores_non_ip_values(self):
        """Unbekannte Domains (die keine IPs sind) triggern keinen ASN-Lookup."""
        engine = DetectionEngine(enable_asn_fallback=True)
        df = self._df([
            {"timestamp": datetime(2026, 4, 1, 10), "client": "ip_a", "domain": "example.com"},
        ])
        result = engine.analyze(df)
        assert result.ai_queries == 0

    def test_asn_fallback_ignored_ip_outside_ranges(self):
        """IP außerhalb aller Provider-Ranges bleibt unerkannt."""
        engine = DetectionEngine(enable_asn_fallback=True)
        df = self._df([
            {"timestamp": datetime(2026, 4, 1, 10), "client": "ip_a", "domain": "8.8.8.8"},
        ])
        result = engine.analyze(df)
        assert result.ai_queries == 0

    def test_custom_asn_db_used_when_supplied(self):
        """Tests dürfen eine eigene AsnDatabase via Constructor injecten."""
        custom = AsnDatabase(db_path=_DEFAULT_DB)  # gleiche Daten, aber über Path
        engine = DetectionEngine(enable_asn_fallback=True, asn_db=custom)
        df = self._df([
            {"timestamp": datetime(2026, 4, 1, 10), "client": "ip_a", "domain": "160.79.104.1"},
        ])
        result = engine.analyze(df)
        assert result.ai_queries == 1
