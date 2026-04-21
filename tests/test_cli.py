"""Tests für das CLI-Entry-Point (src/cli.py / Issue #3)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.cli import _auto_detect_parser, main

ROOT = Path(__file__).parent.parent
TESTDATA = ROOT / "testdata"


# ---------------------------------------------------------------------------
# Auto-Detect
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("file_name,expected_parser", [
    ("pihole_sample.log", "pihole"),
    ("sysmon_sample.log", "sysmon"),
    ("elastic_ecs_sample.log", "elastic_ecs"),
])
def test_auto_detect_parser(file_name: str, expected_parser: str) -> None:
    path = TESTDATA / file_name
    if not path.is_file():
        pytest.skip(f"{file_name} not generated")
    detected = _auto_detect_parser(path)
    assert detected == expected_parser


def test_auto_detect_raises_on_empty(tmp_path: Path) -> None:
    empty = tmp_path / "empty.log"
    empty.write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="leer"):
        _auto_detect_parser(empty)


# ---------------------------------------------------------------------------
# analyze-Command — Happy-Path JSON nach stdout
# ---------------------------------------------------------------------------
def test_analyze_stdout_json(capsys, tmp_path: Path) -> None:
    sample = TESTDATA / "pihole_sample.log"
    if not sample.is_file():
        pytest.skip("pihole_sample.log missing")
    rc = main([
        "analyze", str(sample),
        "--parser", "pihole",
        "--format", "json",
        "--stdout",
        "--salt", "test-salt",
        "--no-retention",
    ])
    assert rc == 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert "findings" in payload
    assert "report_meta" in payload


# ---------------------------------------------------------------------------
# analyze-Command — HTML-Output in Verzeichnis
# ---------------------------------------------------------------------------
def test_analyze_html_to_dir(tmp_path: Path) -> None:
    sample = TESTDATA / "pihole_sample.log"
    if not sample.is_file():
        pytest.skip("pihole_sample.log missing")
    out = tmp_path / "reports"
    rc = main([
        "analyze", str(sample),
        "--parser", "pihole",
        "--format", "html",
        "--audience", "executive",
        "--out", str(out),
        "--salt", "test-salt",
        "--no-retention",
    ])
    assert rc == 0
    html_files = list(out.glob("*.html"))
    assert len(html_files) >= 1, f"Keine HTML-Dateien in {out}"


# ---------------------------------------------------------------------------
# Fehler-Handling — nicht-existente Datei
# ---------------------------------------------------------------------------
def test_analyze_missing_file_returns_2(tmp_path: Path, capsys) -> None:
    rc = main(["analyze", str(tmp_path / "does-not-exist.log")])
    assert rc == 2
    err = capsys.readouterr().err
    assert "nicht gefunden" in err


# ---------------------------------------------------------------------------
# validate-db-Command
# ---------------------------------------------------------------------------
def test_validate_db_passes(capsys) -> None:
    rc = main(["validate-db"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Endpoints" in out
    assert "Schema valid" in out


# ---------------------------------------------------------------------------
# Unbekannter Parser → Exit 2
# ---------------------------------------------------------------------------
def test_unknown_parser_returns_error(tmp_path: Path) -> None:
    sample = tmp_path / "x.log"
    sample.write_text("irrelevant\n", encoding="utf-8")
    with pytest.raises(SystemExit) as exc_info:
        main(["analyze", str(sample), "--parser", "nonexistent-parser"])
    assert exc_info.value.code == 2
