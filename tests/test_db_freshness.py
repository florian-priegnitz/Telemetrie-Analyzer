"""Tests fuer DB-Freshness-Komponente und Coverage-Report (#77)."""

from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import db_coverage_report  # type: ignore  # noqa: E402

from src.database.ai_endpoints import AIEndpointDatabase  # noqa: E402
from src.ui.components import db_status  # noqa: E402

# ---------------------------------------------------------------------------
# Freshness-Logic
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("days_old, expected_emoji", [
    (0, "🟢"),
    (35, "🟢"),
    (36, "🟡"),
    (70, "🟡"),
    (71, "🔴"),
    (365, "🔴"),
])
def test_freshness_signal_thresholds(days_old, expected_emoji):
    last_updated = (date.today() - timedelta(days=days_old)).isoformat()
    emoji, label, age = db_status._freshness_signal(last_updated)
    assert emoji == expected_emoji
    assert age == days_old
    assert label  # nicht leer


def test_freshness_signal_handles_unknown_date():
    emoji, label, age = db_status._freshness_signal("")
    assert emoji == "❓"
    assert age is None
    assert "unbekannt" in label.lower()


def test_freshness_signal_handles_invalid_date():
    emoji, _, age = db_status._freshness_signal("not-a-date")
    assert emoji == "❓"
    assert age is None


# ---------------------------------------------------------------------------
# Coverage-Report rendering
# ---------------------------------------------------------------------------

def test_coverage_report_renders_with_real_db():
    db = AIEndpointDatabase()
    body = db_coverage_report.render_markdown(db)
    assert body.startswith("# AI-Coverage-Report")
    assert f"v{db.version}" in body
    assert "## Kennzahlen" in body
    assert "## Per Kategorie" in body
    assert "## Top-10-Provider" in body
    assert "## Vollständiger Katalog" in body
    # Mindestens ein Endpoint im Output
    assert any(ep.service in body for ep in db.endpoints)


def test_coverage_check_passes_when_synced(tmp_path, monkeypatch):
    db = AIEndpointDatabase()
    body = db_coverage_report.render_markdown(db)
    out = tmp_path / "AI_COVERAGE.md"
    out.write_text(body, encoding="utf-8")

    monkeypatch.setattr(sys, "argv", [
        "db_coverage_report.py", "--check", "--output", str(out),
    ])
    assert db_coverage_report.main() == 0


def test_coverage_check_fails_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(sys, "argv", [
        "db_coverage_report.py", "--check", "--output", str(tmp_path / "nope.md"),
    ])
    assert db_coverage_report.main() == 1


def test_coverage_check_fails_when_drifted(tmp_path, monkeypatch):
    out = tmp_path / "AI_COVERAGE.md"
    out.write_text("# AI-Coverage-Report\n\n(stale)\n", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", [
        "db_coverage_report.py", "--check", "--output", str(out),
    ])
    assert db_coverage_report.main() == 1


def test_strip_today_line_removes_dated_marker():
    text = (
        "# Header\n"
        "_Auto-generiert via `scripts/db_coverage_report.py` am 2026-04-27._\n"
        "Body\n"
    )
    cleaned = db_coverage_report._strip_today_line(text)
    assert "Auto-generiert" not in cleaned
    assert "Header" in cleaned
    assert "Body" in cleaned


# ---------------------------------------------------------------------------
# Repo-AI_COVERAGE.md ist synchron mit der DB (verhindert Drift)
# ---------------------------------------------------------------------------

def test_repo_ai_coverage_md_is_in_sync():
    """Wenn jemand die DB ändert, muss `python scripts/db_coverage_report.py`
    erneut laufen — sonst bricht dieser Test."""
    coverage_md = REPO_ROOT / "docs" / "AI_COVERAGE.md"
    assert coverage_md.exists(), "docs/AI_COVERAGE.md fehlt — Skript ausführen"
    db = AIEndpointDatabase()
    expected = db_coverage_report.render_markdown(db)
    actual = coverage_md.read_text(encoding="utf-8")
    assert (
        db_coverage_report._strip_today_line(actual)
        == db_coverage_report._strip_today_line(expected)
    ), (
        "docs/AI_COVERAGE.md ist out-of-sync mit der DB. "
        "Bitte `python scripts/db_coverage_report.py` ausführen."
    )
