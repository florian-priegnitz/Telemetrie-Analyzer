"""Tests für AI Endpoint DB Versionierung + Diff (E1-6, Issue #14)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.database.ai_endpoints import AIEndpointDatabase
from src.database.versioning import (
    DiffReport,
    EndpointChange,
    compute_diff,
    diff_databases,
    list_versions,
    load_version,
    version_path,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_VERSIONS_DIR = _REPO_ROOT / "data" / "versions"


# ---------------------------------------------------------------------------
# AIEndpointDatabase exposes version metadata
# ---------------------------------------------------------------------------

class TestDatabaseVersionProperties:

    def test_default_db_has_version(self):
        db = AIEndpointDatabase()
        assert db.version  # non-empty
        assert db.version == "2.2.0"

    def test_last_updated_present(self):
        db = AIEndpointDatabase()
        assert db.last_updated  # non-empty ISO date


# ---------------------------------------------------------------------------
# Snapshot discovery
# ---------------------------------------------------------------------------

class TestVersionDiscovery:

    def test_versions_dir_contains_2_2_0(self):
        assert (_VERSIONS_DIR / "2.2.0.json").exists()

    def test_list_versions_sorted(self):
        versions = list_versions()
        assert "2.2.0" in versions
        assert versions == sorted(versions)

    def test_version_path_returns_absolute(self):
        p = version_path("2.2.0")
        assert p.is_absolute()
        assert p.name == "2.2.0.json"


# ---------------------------------------------------------------------------
# load_version
# ---------------------------------------------------------------------------

class TestLoadVersion:

    def test_load_existing_version(self):
        data = load_version("2.2.0")
        assert "endpoints" in data
        assert isinstance(data["endpoints"], list)
        assert data["version"] == "2.2.0"

    def test_load_missing_version_raises(self):
        with pytest.raises(FileNotFoundError) as exc_info:
            load_version("99.99.99")
        assert "2.2.0" in str(exc_info.value)  # Hint mit verfügbaren Versionen


# ---------------------------------------------------------------------------
# diff_databases (pure function)
# ---------------------------------------------------------------------------

class TestDiffDatabases:

    def _db(self, endpoints: list[dict], version: str = "1.0.0") -> dict:
        return {"version": version, "endpoints": endpoints}

    def test_empty_equal_dbs_no_diff(self):
        db = self._db([])
        report = diff_databases(db, db)
        assert report.is_empty

    def test_added_service(self):
        old = self._db([])
        new = self._db([{
            "service": "ChatGPT", "provider": "OpenAI", "category": "llm_chatbot",
            "risk_level": "high", "domains": ["chat.openai.com"],
        }])
        report = diff_databases(old, new)
        assert len(report.added) == 1
        assert report.added[0]["service"] == "ChatGPT"
        assert not report.removed
        assert not report.changed

    def test_removed_service(self):
        old = self._db([{
            "service": "Old", "provider": "P", "category": "llm_api",
            "risk_level": "high", "domains": ["old.com"],
        }])
        new = self._db([])
        report = diff_databases(old, new)
        assert len(report.removed) == 1
        assert report.removed[0]["service"] == "Old"

    def test_changed_risk_level(self):
        base = {
            "service": "X", "provider": "P", "category": "llm_api",
            "domains": ["x.com"], "risk_level": "medium",
        }
        new = dict(base, risk_level="critical")
        report = diff_databases(self._db([base]), self._db([new]))
        assert len(report.changed) == 1
        change = report.changed[0]
        assert change.service == "X"
        assert change.field_name == "risk_level"
        assert change.from_value == "medium"
        assert change.to_value == "critical"

    def test_domain_order_not_treated_as_change(self):
        """Reine Reihenfolge-Änderungen sollen kein Diff erzeugen."""
        old = {
            "service": "X", "provider": "P", "category": "llm_api",
            "risk_level": "high", "domains": ["a.com", "b.com"],
        }
        new = dict(old, domains=["b.com", "a.com"])
        report = diff_databases(self._db([old]), self._db([new]))
        assert not report.changed

    def test_alias_addition_triggers_change(self):
        old = {
            "service": "X", "provider": "P", "category": "llm_api",
            "risk_level": "high", "domains": ["x.com"], "aliases": [],
        }
        new = dict(old, aliases=["X-Pro"])
        report = diff_databases(self._db([old]), self._db([new]))
        assert len(report.changed) == 1
        assert report.changed[0].field_name == "aliases"

    def test_multiple_changes_same_service(self):
        old = {
            "service": "X", "provider": "OldProv", "category": "llm_api",
            "risk_level": "medium", "domains": ["x.com"],
        }
        new = dict(old, provider="NewProv", risk_level="high")
        report = diff_databases(self._db([old]), self._db([new]))
        assert len(report.changed) == 2  # provider + risk_level
        fields = {c.field_name for c in report.changed}
        assert fields == {"provider", "risk_level"}


# ---------------------------------------------------------------------------
# compute_diff (via file system)
# ---------------------------------------------------------------------------

class TestComputeDiff:

    def test_same_version_diff_is_empty(self):
        report = compute_diff("2.2.0", "2.2.0")
        assert report.is_empty

    def test_versions_in_report_header(self):
        report = compute_diff("2.2.0", "2.2.0")
        assert report.from_version == "2.2.0"
        assert report.to_version == "2.2.0"


# ---------------------------------------------------------------------------
# DiffReport formatting
# ---------------------------------------------------------------------------

class TestDiffReportFormat:

    def test_empty_report_human_readable(self):
        report = DiffReport(from_version="1.0.0", to_version="1.0.0")
        text = report.format_text()
        assert "1.0.0 → 1.0.0" in text
        assert "Keine Änderungen" in text

    def test_added_section_rendered(self):
        report = DiffReport(
            from_version="1.0", to_version="1.1",
            added=[{"service": "Y", "provider": "Z", "category": "llm_api",
                    "risk_level": "high"}],
        )
        text = report.format_text()
        assert "Hinzugefügt (1)" in text
        assert "Y" in text and "Z" in text

    def test_changed_section_rendered(self):
        report = DiffReport(
            from_version="1.0", to_version="1.1",
            changed=[EndpointChange("X", "risk_level", "medium", "high")],
        )
        text = report.format_text()
        assert "Geändert (1)" in text
        assert "X.risk_level" in text
        assert "medium → high" in text


# ---------------------------------------------------------------------------
# ReportGenerator wires DB metadata into output (#14)
# ---------------------------------------------------------------------------

class TestReportGeneratorDbVersion:

    def test_db_version_auto_loaded_in_report(self):
        from src.detection.engine import DetectionResult
        from src.reports import ReportGenerator

        det = DetectionResult(
            findings=[], total_queries=0, ai_queries=0, non_ai_queries=0,
            analysis_period_start=None, analysis_period_end=None,
            unique_clients=0, unique_ai_services=0,
        )
        from src.compliance.models import ComplianceResult
        comp = ComplianceResult()

        gen = ReportGenerator(det, comp, salt="fixed-salt")
        out = gen.render(audience="all", format="html")
        assert isinstance(out, dict)
        # Alle HTML-Audiences enthalten die DB-Version im Footer
        for audience_html in out.values():
            assert "AI Endpoint DB" in audience_html
            assert "2.2.0" in audience_html

    def test_explicit_empty_db_version_suppresses_footer(self):
        from src.compliance.models import ComplianceResult
        from src.detection.engine import DetectionResult
        from src.reports import ReportGenerator

        det = DetectionResult(
            findings=[], total_queries=0, ai_queries=0, non_ai_queries=0,
            analysis_period_start=None, analysis_period_end=None,
            unique_clients=0, unique_ai_services=0,
        )
        gen = ReportGenerator(
            det, ComplianceResult(), salt="fixed-salt",
            db_version="", db_last_updated="",
        )
        html = gen.render(audience="compliance", format="html")
        assert "AI Endpoint DB" not in html

    def test_json_output_has_ai_endpoint_db_block(self):
        from src.compliance.models import ComplianceResult
        from src.detection.engine import DetectionResult
        from src.reports import ReportGenerator

        det = DetectionResult(
            findings=[], total_queries=0, ai_queries=0, non_ai_queries=0,
            analysis_period_start=None, analysis_period_end=None,
            unique_clients=0, unique_ai_services=0,
        )
        gen = ReportGenerator(det, ComplianceResult(), salt="fixed-salt")
        out = gen.render(audience="all", format="json")
        assert isinstance(out, dict)
        meta = out["report_meta"]
        assert "ai_endpoint_db" in meta
        assert meta["ai_endpoint_db"]["version"] == "2.2.0"


# ---------------------------------------------------------------------------
# data/CHANGELOG_AI_ENDPOINTS.md — documented Semver rules
# ---------------------------------------------------------------------------

def test_changelog_file_exists():
    path = _REPO_ROOT / "data" / "CHANGELOG_AI_ENDPOINTS.md"
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "Semver-Konvention" in content
    assert "[2.2.0]" in content


def test_snapshot_matches_live_db():
    """data/versions/2.2.0.json muss identisch zu data/ai_endpoints.json sein
    (Drift-Guard — wenn der User ai_endpoints.json ändert, muss die
    Version bumped und ein neuer Snapshot erzeugt werden).
    """
    live = json.loads((_REPO_ROOT / "data" / "ai_endpoints.json").read_text(encoding="utf-8"))
    snap = json.loads((_VERSIONS_DIR / "2.2.0.json").read_text(encoding="utf-8"))
    assert live == snap, (
        "data/ai_endpoints.json wurde seit 2.2.0 geändert — bitte Version bumpen "
        "und neuen Snapshot in data/versions/ ablegen."
    )
