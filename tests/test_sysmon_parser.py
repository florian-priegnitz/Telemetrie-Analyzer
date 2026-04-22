"""Tests für den Windows Sysmon Event 22 Parser (E3-9 / Issue #34)."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from src.parsers.sysmon import SysmonParser, parse_sysmon_log
from src.privacy.pseudonymizer import Pseudonymizer

FIXTURE = Path(__file__).parent.parent / "testdata" / "sysmon_sample.log"


@pytest.fixture
def pseudo() -> Pseudonymizer:
    return Pseudonymizer(key=b"test-sysmon-salt")


@pytest.fixture
def df(pseudo: Pseudonymizer) -> pd.DataFrame:
    return parse_sysmon_log(FIXTURE, pseudonymizer=pseudo)


# ---------------------------------------------------------------------------
# Basis-Vertrag + BaseParser-Compliance
# ---------------------------------------------------------------------------
def test_returns_non_empty_dataframe(df: pd.DataFrame) -> None:
    assert not df.empty


def test_required_columns_present(df: pd.DataFrame) -> None:
    for col in ("timestamp", "client", "domain"):
        assert col in df.columns


def test_timestamp_sorted_ascending(df: pd.DataFrame) -> None:
    assert df["timestamp"].is_monotonic_increasing


def test_timestamp_dtype_datetime64_ns(df: pd.DataFrame) -> None:
    assert df["timestamp"].dtype == "datetime64[ns]"


def test_baseparser_interface(pseudo: Pseudonymizer) -> None:
    parser = SysmonParser(pseudonymizer=pseudo)
    out = parser.parse(FIXTURE)
    assert not out.empty
    parser.validate_schema(out)


# ---------------------------------------------------------------------------
# Event-Filter: nur EventID 22 wird akzeptiert
# ---------------------------------------------------------------------------
def test_non_event22_is_dropped(df: pd.DataFrame) -> None:
    """Die Fixture enthält ein EventID=1 Event — muss verworfen werden."""
    # 7 valide Event-22 im Fixture (3 flat + 2 winlogbeat + 1 sentinel + 1 trailing epsilon), 3 invalide/drop
    assert len(df) == 7


# ---------------------------------------------------------------------------
# Flat-Shape, Winlogbeat-Shape, Sentinel-Shape werden alle geparst
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("query", [
    "chat.openai.com",
    "api.anthropic.com",
    "copilot.microsoft.com",
    "claude.ai",
    "gemini.google.com",
    "perplexity.ai",
])
def test_queries_parsed_across_shapes(df: pd.DataFrame, query: str) -> None:
    assert query in set(df["domain"])


# ---------------------------------------------------------------------------
# DSGVO Art. 25 — Pseudonymisierung + Basename-Only für Image
# ---------------------------------------------------------------------------
def test_clients_are_pseudonymized(df: pd.DataFrame) -> None:
    for client in df["client"]:
        assert client.startswith("ip_")


def test_users_are_pseudonymized(df: pd.DataFrame) -> None:
    users = df["user"].dropna().unique()
    assert len(users) > 0
    for user in users:
        assert user.startswith("user_")


def test_same_host_yields_same_pseudonym(df: pd.DataFrame) -> None:
    """Zwei WKS-ALPHA-Events erwarten identisches Pseudonym."""
    alpha_rows = df[df["domain"].isin({"chat.openai.com", "api.anthropic.com"})]
    assert len(alpha_rows["client"].unique()) == 1


def test_image_path_truncated_to_basename(df: pd.DataFrame) -> None:
    """C:\\Users\\alice\\AppData\\...\\Cursor.exe → Cursor.exe."""
    assert "Cursor.exe" in set(df["process"].dropna())
    assert "firefox.exe" in set(df["process"].dropna())
    # Kein Pfad-Separator mehr drin
    for p in df["process"].dropna():
        assert "\\" not in p and "/" not in p


# ---------------------------------------------------------------------------
# Domain-Normalisierung (lowercase, trailing dot)
# ---------------------------------------------------------------------------
def test_domain_is_lowercase_no_trailing_dot(df: pd.DataFrame) -> None:
    # "ChatGPT.OpenAI.Com." aus Fixture → "chatgpt.openai.com"
    assert "chatgpt.openai.com" in set(df["domain"])
    for d in df["domain"]:
        assert d == d.lower()
        assert not d.endswith(".")


# ---------------------------------------------------------------------------
# Robustheit: ungültige Einträge werden verworfen, nicht geraist
# ---------------------------------------------------------------------------
def test_invalid_timestamp_dropped(df: pd.DataFrame) -> None:
    """'invalid-timestamp' in Fixture darf nicht im DataFrame landen."""
    assert "should.be.dropped" not in set(df["domain"])


def test_empty_query_name_dropped(df: pd.DataFrame) -> None:
    assert not (df["domain"] == "").any()


def test_empty_file_returns_empty_df(tmp_path: Path, pseudo: Pseudonymizer) -> None:
    empty = tmp_path / "empty.log"
    empty.write_text("", encoding="utf-8")
    out = parse_sysmon_log(empty, pseudonymizer=pseudo)
    assert out.empty
    assert list(out.columns) == [
        "timestamp", "client", "domain", "source_file", "source_type",
        "user", "process", "status_code",
    ]


def test_malformed_json_skipped(tmp_path: Path, pseudo: Pseudonymizer) -> None:
    bad = tmp_path / "bad.log"
    bad.write_text(
        "this is not json\n"
        '{"EventID": 22, "UtcTime": "2026-04-18 10:00:00", '
        '"QueryName": "good.example.com", "Computer": "H1"}\n'
        "broken{json\n",
        encoding="utf-8",
    )
    out = parse_sysmon_log(bad, pseudonymizer=pseudo)
    assert len(out) == 1
    assert out.iloc[0]["domain"] == "good.example.com"


# ---------------------------------------------------------------------------
# Status-Code-Preservation
# ---------------------------------------------------------------------------
def test_status_code_preserved(df: pd.DataFrame) -> None:
    """QueryStatus=0 (erfolgreich) wird als Int32(0) übernommen."""
    assert df["status_code"].dtype == "Int32"
    assert (df["status_code"] == 0).sum() >= 6


# ---------------------------------------------------------------------------
# source_type-Marker — Detection-Engine kann nach Parser-Herkunft filtern
# ---------------------------------------------------------------------------
def test_source_type_marker(df: pd.DataFrame) -> None:
    assert (df["source_type"] == "sysmon").all()


# ---------------------------------------------------------------------------
# User-Normalisierung: DOMAIN\user → pseudonym bleibt identisch unabhängig
# vom Domain-Präfix? (Nein, absichtlich: CONTOSO\alice != alice, sonst Kollisionen)
# ---------------------------------------------------------------------------
def test_domain_prefixed_users_are_distinct(tmp_path: Path, pseudo: Pseudonymizer) -> None:
    """CONTOSO\\alice und alice ergeben absichtlich unterschiedliche Pseudonyme."""
    f = tmp_path / "x.log"
    f.write_text(
        json.dumps({"EventID": 22, "UtcTime": "2026-04-18 09:00:00",
                    "QueryName": "a.com", "Computer": "H1", "User": "CONTOSO\\alice"}) + "\n"
        + json.dumps({"EventID": 22, "UtcTime": "2026-04-18 09:00:01",
                      "QueryName": "b.com", "Computer": "H1", "User": "alice"}) + "\n",
        encoding="utf-8",
    )
    out = parse_sysmon_log(f, pseudonymizer=pseudo)
    assert len(out) == 2
    assert out["user"].nunique() == 2
