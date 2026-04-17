"""Tests für die Detection Engine."""

import tempfile
from pathlib import Path

from src.parsers.pihole import parse_pihole_log
from src.privacy.pseudonymizer import Pseudonymizer
from src.detection.engine import (
    DetectionEngine,
    SYSTEMATIC_THRESHOLD,
    UPLOAD_THRESHOLD_BYTES,
    UPLOAD_RISK_BOOST,
)


def _make_log(lines: list[str]) -> Path:
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False, encoding="utf-8")
    f.write("\n".join(lines) + "\n")
    f.close()
    return Path(f.name)


def _log_line(month: str, day: int, hour: int, minute: int, domain: str, client: str) -> str:
    return f"{month} {day:2d} {hour:02d}:{minute:02d}:00 dnsmasq[1234]: query[A] {domain} from {client}"


class TestDetectionEngine:

    def test_empty_dataframe(self):
        import pandas as pd
        engine = DetectionEngine()
        result = engine.analyze(pd.DataFrame())
        assert result.total_queries == 0
        assert result.findings == []

    def test_no_ai_traffic(self):
        lines = [
            _log_line("Mar", 1, 10, i, "www.google.com", "192.168.1.1")
            for i in range(20)
        ]
        path = _make_log(lines)
        pseudo = Pseudonymizer(key=b"test")
        df = parse_pihole_log(path, pseudonymizer=pseudo, year=2026)
        result = DetectionEngine().analyze(df)

        assert result.total_queries == 20
        assert result.ai_queries == 0
        assert result.findings == []

    def test_detect_chatgpt(self):
        lines = [
            _log_line("Mar", 1, 10, i, "chat.openai.com", "192.168.1.42")
            for i in range(15)
        ]
        path = _make_log(lines)
        pseudo = Pseudonymizer(key=b"test")
        df = parse_pihole_log(path, pseudonymizer=pseudo, year=2026)
        result = DetectionEngine().analyze(df)

        assert result.ai_queries == 15
        assert len(result.findings) == 1
        assert result.findings[0].service == "OpenAI ChatGPT"
        assert result.findings[0].is_systematic  # 15 > 10 threshold

    def test_multiple_services_one_client(self):
        lines = [
            _log_line("Mar", 1, 10, 0, "chat.openai.com", "192.168.1.10"),
            _log_line("Mar", 1, 10, 1, "claude.ai", "192.168.1.10"),
            _log_line("Mar", 1, 10, 2, "chat.deepseek.com", "192.168.1.10"),
        ]
        path = _make_log(lines)
        pseudo = Pseudonymizer(key=b"test")
        df = parse_pihole_log(path, pseudonymizer=pseudo, year=2026)
        result = DetectionEngine().analyze(df)

        assert len(result.findings) == 3
        assert result.unique_ai_services == 3

    def test_same_service_different_clients(self):
        lines = [
            _log_line("Mar", 1, 10, 0, "chat.openai.com", "192.168.1.10"),
            _log_line("Mar", 1, 10, 1, "chat.openai.com", "192.168.1.20"),
        ]
        path = _make_log(lines)
        pseudo = Pseudonymizer(key=b"test")
        df = parse_pihole_log(path, pseudonymizer=pseudo, year=2026)
        result = DetectionEngine().analyze(df)

        # Verschiedene Clients = verschiedene Findings
        assert len(result.findings) == 2
        assert result.unique_ai_services == 1

    def test_risk_score_critical_systematic(self):
        """Kritischer Dienst + systematische Nutzung = hoher Score."""
        lines = [
            _log_line("Mar", 1, 10, i, "chat.deepseek.com", "192.168.1.1")
            for i in range(20)
        ]
        path = _make_log(lines)
        pseudo = Pseudonymizer(key=b"test")
        df = parse_pihole_log(path, pseudonymizer=pseudo, year=2026)
        result = DetectionEngine().analyze(df)

        finding = result.findings[0]
        assert finding.risk_level == "critical"
        assert finding.is_systematic
        assert finding.risk_score >= 85

    def test_risk_score_low_occasional(self):
        """Niedriges Risiko + gelegentlich = niedriger Score."""
        lines = [
            _log_line("Mar", 1, 10, 0, "suno.com", "192.168.1.1"),
        ]
        path = _make_log(lines)
        pseudo = Pseudonymizer(key=b"test")
        df = parse_pihole_log(path, pseudonymizer=pseudo, year=2026)
        result = DetectionEngine().analyze(df)

        finding = result.findings[0]
        assert finding.risk_level == "low"
        assert finding.risk_score <= 30

    def test_ai_query_ratio(self):
        lines = [
            _log_line("Mar", 1, 10, 0, "chat.openai.com", "192.168.1.1"),
            _log_line("Mar", 1, 10, 1, "www.google.com", "192.168.1.1"),
            _log_line("Mar", 1, 10, 2, "www.google.com", "192.168.1.1"),
            _log_line("Mar", 1, 10, 3, "www.google.com", "192.168.1.1"),
        ]
        path = _make_log(lines)
        pseudo = Pseudonymizer(key=b"test")
        df = parse_pihole_log(path, pseudonymizer=pseudo, year=2026)
        result = DetectionEngine().analyze(df)

        assert result.ai_query_ratio == 0.25

    def test_findings_sorted_by_risk_score(self):
        lines = [
            _log_line("Mar", 1, 10, 0, "suno.com", "192.168.1.1"),          # low
            _log_line("Mar", 1, 10, 1, "chat.deepseek.com", "192.168.1.1"), # critical
            _log_line("Mar", 1, 10, 2, "www.deepl.com", "192.168.1.1"),     # medium
        ]
        path = _make_log(lines)
        pseudo = Pseudonymizer(key=b"test")
        df = parse_pihole_log(path, pseudonymizer=pseudo, year=2026)
        result = DetectionEngine().analyze(df)

        scores = [f.risk_score for f in result.findings]
        assert scores == sorted(scores, reverse=True)


class TestTestdataGenerator:

    def test_generate_log(self):
        from src.testdata.generator import generate_pihole_log
        with tempfile.TemporaryDirectory() as tmpdir:
            path = generate_pihole_log(
                Path(tmpdir) / "test.log",
                days=3,
                queries_per_day=100,
                seed=42,
            )
            assert path.exists()
            assert path.stat().st_size > 0
            lines = path.read_text().splitlines()
            assert len(lines) > 100  # 3 Tage * ~100/Tag

    def test_generated_log_is_parseable(self):
        from src.testdata.generator import generate_pihole_log
        with tempfile.TemporaryDirectory() as tmpdir:
            path = generate_pihole_log(
                Path(tmpdir) / "test.log",
                days=2,
                queries_per_day=50,
                seed=123,
            )
            pseudo = Pseudonymizer(key=b"test")
            df = parse_pihole_log(path, pseudonymizer=pseudo, year=2026)
            assert len(df) > 0
            assert "domain" in df.columns

    def test_generated_log_contains_ai_traffic(self):
        from src.testdata.generator import generate_pihole_log
        with tempfile.TemporaryDirectory() as tmpdir:
            path = generate_pihole_log(
                Path(tmpdir) / "test.log",
                days=7,
                queries_per_day=500,
                seed=42,
            )
            pseudo = Pseudonymizer(key=b"test")
            df = parse_pihole_log(path, pseudonymizer=pseudo, year=2026)
            result = DetectionEngine().analyze(df)

            assert result.ai_queries > 0
            assert len(result.findings) > 0

    def test_reproducible_with_seed(self):
        from src.testdata.generator import generate_pihole_log
        with tempfile.TemporaryDirectory() as tmpdir:
            p1 = generate_pihole_log(Path(tmpdir) / "a.log", days=1, queries_per_day=50, seed=99)
            p2 = generate_pihole_log(Path(tmpdir) / "b.log", days=1, queries_per_day=50, seed=99)
            assert p1.read_text() == p2.read_text()


class TestUploadDetection:
    """Tests für Volumen-Detection (>500 KB Upload = document_upload)."""

    def _make_squid_df(self, rows: list[dict]):
        import pandas as pd
        df = pd.DataFrame(rows)
        df["bytes_uploaded"] = df["bytes_uploaded"].astype("Int64")
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df

    def test_document_upload_detected(self):
        df = self._make_squid_df([
            {"timestamp": "2026-03-01 10:00:00", "domain": "chat.openai.com",
             "client": "ip_aaa", "bytes_uploaded": UPLOAD_THRESHOLD_BYTES + 100},
        ])
        result = DetectionEngine().analyze(df)
        assert len(result.findings) == 1
        f = result.findings[0]
        assert f.has_document_upload is True
        assert f.upload_events == 1
        assert f.total_bytes_uploaded == UPLOAD_THRESHOLD_BYTES + 100

    def test_upload_below_threshold_not_flagged(self):
        df = self._make_squid_df([
            {"timestamp": "2026-03-01 10:00:00", "domain": "chat.openai.com",
             "client": "ip_bbb", "bytes_uploaded": UPLOAD_THRESHOLD_BYTES - 1},
        ])
        result = DetectionEngine().analyze(df)
        assert len(result.findings) == 1
        f = result.findings[0]
        assert f.has_document_upload is False
        assert f.upload_events == 0

    def test_risk_score_boost_with_upload(self):
        # Kritischer Service (DeepSeek) ohne Upload
        df_no_upload = self._make_squid_df([
            {"timestamp": "2026-03-01 10:00:00", "domain": "chat.deepseek.com",
             "client": "ip_ccc", "bytes_uploaded": 1000},
        ])
        result_no = DetectionEngine().analyze(df_no_upload)
        score_no_upload = result_no.findings[0].risk_score

        # Gleicher Service mit document_upload
        df_upload = self._make_squid_df([
            {"timestamp": "2026-03-01 10:00:00", "domain": "chat.deepseek.com",
             "client": "ip_ddd", "bytes_uploaded": UPLOAD_THRESHOLD_BYTES + 1000},
        ])
        result_yes = DetectionEngine().analyze(df_upload)
        score_with_upload = result_yes.findings[0].risk_score

        # Boost-Differenz, gecappt bei 100
        assert score_with_upload >= min(score_no_upload + UPLOAD_RISK_BOOST, 100)

    def test_pihole_dataframe_no_upload_columns(self):
        """Pi-hole-DataFrames haben keine bytes_uploaded — Findings müssen weiter funktionieren."""
        lines = [
            f"Mar  1 10:0{i}:00 dnsmasq[1234]: query[A] chat.openai.com from 192.168.1.42"
            for i in range(5)
        ]
        path = _make_log(lines)
        df = parse_pihole_log(path, pseudonymizer=Pseudonymizer(key=b"t"), year=2026)
        result = DetectionEngine().analyze(df)
        assert len(result.findings) == 1
        f = result.findings[0]
        assert f.has_document_upload is False
        assert f.upload_events == 0
        assert f.total_bytes_uploaded == 0
