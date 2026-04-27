"""Tests fuer scripts/verify_screenshots.py (#75, Sprint 10D)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import verify_screenshots  # type: ignore  # noqa: E402

CHECKLIST_FIXTURE = """\
# Screenshot-Checkliste

- [ ] 00_onboarding.png — Welcome
- [ ] 01_overview_loaded.png — KPIs sichtbar
- [x] 02_findings_filter_critical.png — bereits abgehakt
- [ ] 03_users_top10.png — Top-10
* Folgender Eintrag passt nicht zum Schema und wird ignoriert:
- [ ] kein_schema_match.png
- [ ] 99_offline_setup.png — Terminal
"""


def _make_checklist(tmp_path: Path) -> Path:
    p = tmp_path / "CHECKLIST.md"
    p.write_text(CHECKLIST_FIXTURE, encoding="utf-8")
    return p


def test_parse_extracts_only_numbered_pngs(tmp_path):
    checklist = _make_checklist(tmp_path)
    expected = verify_screenshots.parse_checklist(checklist)
    assert expected == [
        "00_onboarding.png",
        "01_overview_loaded.png",
        "02_findings_filter_critical.png",
        "03_users_top10.png",
        "99_offline_setup.png",
    ]


def test_check_reports_missing(tmp_path):
    checklist = _make_checklist(tmp_path)
    screenshots = tmp_path / "screenshots"
    screenshots.mkdir()
    # Nur zwei der fuenf vorhanden
    (screenshots / "00_onboarding.png").write_bytes(b"\x89PNG")
    (screenshots / "99_offline_setup.png").write_bytes(b"\x89PNG")

    present, missing = verify_screenshots.check(checklist, screenshots)
    assert present == ["00_onboarding.png", "99_offline_setup.png"]
    assert missing == [
        "01_overview_loaded.png",
        "02_findings_filter_critical.png",
        "03_users_top10.png",
    ]


def test_check_all_present(tmp_path):
    checklist = _make_checklist(tmp_path)
    screenshots = tmp_path / "screenshots"
    screenshots.mkdir()
    for name in verify_screenshots.parse_checklist(checklist):
        (screenshots / name).write_bytes(b"\x89PNG")
    present, missing = verify_screenshots.check(checklist, screenshots)
    assert len(present) == 5
    assert missing == []


def test_main_warn_returns_zero_on_missing(tmp_path, monkeypatch, capsys):
    checklist = _make_checklist(tmp_path)
    screenshots = tmp_path / "screenshots"
    screenshots.mkdir()
    monkeypatch.setattr(sys, "argv", [
        "verify_screenshots.py",
        "--checklist", str(checklist),
        "--screenshots-dir", str(screenshots),
    ])
    rc = verify_screenshots.main()
    captured = capsys.readouterr()
    assert rc == 0  # warn mode: missing != error
    assert "OK: 0/5" in captured.out
    assert "FEHLEND: 5" in captured.out


def test_main_strict_returns_one_on_missing(tmp_path, monkeypatch):
    checklist = _make_checklist(tmp_path)
    screenshots = tmp_path / "screenshots"
    screenshots.mkdir()
    monkeypatch.setattr(sys, "argv", [
        "verify_screenshots.py",
        "--checklist", str(checklist),
        "--screenshots-dir", str(screenshots),
        "--strict",
    ])
    rc = verify_screenshots.main()
    assert rc == 1


def test_main_returns_zero_when_all_present(tmp_path, monkeypatch):
    checklist = _make_checklist(tmp_path)
    screenshots = tmp_path / "screenshots"
    screenshots.mkdir()
    for name in verify_screenshots.parse_checklist(checklist):
        (screenshots / name).write_bytes(b"\x89PNG")
    monkeypatch.setattr(sys, "argv", [
        "verify_screenshots.py",
        "--checklist", str(checklist),
        "--screenshots-dir", str(screenshots),
        "--strict",
    ])
    rc = verify_screenshots.main()
    assert rc == 0


def test_missing_checklist_warn_returns_zero(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", [
        "verify_screenshots.py",
        "--checklist", str(tmp_path / "nope.md"),
    ])
    rc = verify_screenshots.main()
    captured = capsys.readouterr()
    assert rc == 0
    assert "nicht gefunden" in captured.err


def test_missing_checklist_strict_returns_one(tmp_path, monkeypatch):
    monkeypatch.setattr(sys, "argv", [
        "verify_screenshots.py",
        "--checklist", str(tmp_path / "nope.md"),
        "--strict",
    ])
    rc = verify_screenshots.main()
    assert rc == 1
