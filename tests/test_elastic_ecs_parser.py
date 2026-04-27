"""Tests für den Elastic Common Schema Parser (E3-10 / Issue #35)."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from src.parsers.elastic_ecs import ElasticECSParser, parse_elastic_ecs_log
from src.privacy.pseudonymizer import Pseudonymizer

FIXTURE = Path(__file__).parent.parent / "testdata" / "elastic_ecs_sample.log"


@pytest.fixture
def pseudo() -> Pseudonymizer:
    return Pseudonymizer(key=b"test-ecs-salt")


@pytest.fixture
def df(pseudo: Pseudonymizer) -> pd.DataFrame:
    return parse_elastic_ecs_log(FIXTURE, pseudonymizer=pseudo)


# ---------------------------------------------------------------------------
# Basis
# ---------------------------------------------------------------------------
def test_returns_non_empty(df: pd.DataFrame) -> None:
    assert not df.empty


def test_required_columns(df: pd.DataFrame) -> None:
    for col in ("timestamp", "client", "domain"):
        assert col in df.columns


def test_timestamp_sorted(df: pd.DataFrame) -> None:
    assert df["timestamp"].is_monotonic_increasing


def test_baseparser_interface(pseudo: Pseudonymizer) -> None:
    parser = ElasticECSParser(pseudonymizer=pseudo)
    out = parser.parse(FIXTURE)
    parser.validate_schema(out)


# ---------------------------------------------------------------------------
# Event-Filter: nur DNS/Network/Web-Events werden durchgelassen
# ---------------------------------------------------------------------------
def test_authentication_events_dropped(df: pd.DataFrame) -> None:
    """Das Auth-Event in der Fixture darf nicht durchkommen."""
    # Fixture hat 11 relevante Events (6 ursprünglich + 5 zusätzliche User für 10-User-Coverage
    # in examples/test_reports/elastic_ecs/, Sprint-10B #73). 3 weiterhin invalide/drop
    # (invalid-timestamp, auth, process).
    assert len(df) == 11


@pytest.mark.parametrize("domain", [
    "chat.openai.com",
    "api.anthropic.com",
    "claude.ai",
    "gemini.google.com",
    "perplexity.ai",
    "midjourney.com",
])
def test_all_ai_domains_parsed(df: pd.DataFrame, domain: str) -> None:
    assert domain in set(df["domain"])


# ---------------------------------------------------------------------------
# Shape-Vielfalt: nested ECS + flat-dotted + mixed
# ---------------------------------------------------------------------------
def test_flat_dotted_shape_supported(df: pd.DataFrame) -> None:
    """Event mit ``source.ip`` als Top-Level-Key statt nested wird erkannt."""
    assert "gemini.google.com" in set(df["domain"])


def test_url_domain_fallback(df: pd.DataFrame) -> None:
    """Wenn nur url.domain gesetzt (kein dns.question.name), wird url.domain verwendet."""
    assert "perplexity.ai" in set(df["domain"])
    assert "api.anthropic.com" in set(df["domain"])


# ---------------------------------------------------------------------------
# DSGVO Art. 25
# ---------------------------------------------------------------------------
def test_clients_pseudonymized(df: pd.DataFrame) -> None:
    for c in df["client"]:
        assert c.startswith("ip_")


def test_users_pseudonymized(df: pd.DataFrame) -> None:
    users = df["user"].dropna().unique()
    assert len(users) > 0
    for u in users:
        assert u.startswith("user_")


def test_url_path_query_stripped(df: pd.DataFrame) -> None:
    """``?q=hello`` darf nicht im url_path enthalten sein."""
    for path in df["url_path"].dropna():
        assert "?" not in path


def test_url_path_truncated_to_first_segment(df: pd.DataFrame) -> None:
    """`/v1/messages` → `/v1` (erstes Segment only)."""
    paths = set(df["url_path"].dropna())
    assert "/v1" in paths or "/search" in paths


# ---------------------------------------------------------------------------
# Normalisierung
# ---------------------------------------------------------------------------
def test_domain_lowercase_no_trailing_dot(df: pd.DataFrame) -> None:
    assert "perplexity.ai" in set(df["domain"])  # "PERPLEXITY.AI." normalisiert
    for d in df["domain"]:
        assert d == d.lower()
        assert not d.endswith(".")


# ---------------------------------------------------------------------------
# HTTP-Metadaten
# ---------------------------------------------------------------------------
def test_http_status_parsed(df: pd.DataFrame) -> None:
    assert df["status_code"].dtype == "Int32"
    assert 200 in set(df["status_code"].dropna())


def test_bytes_uploaded_parsed(df: pd.DataFrame) -> None:
    """Große Upload-Events werden als Int64 korrekt übernommen (Detection-relevant)."""
    assert df["bytes_uploaded"].dtype == "Int64"
    assert 2048000 in set(df["bytes_uploaded"].dropna())


def test_method_parsed(df: pd.DataFrame) -> None:
    methods = set(df["method"].dropna())
    assert "POST" in methods
    assert "GET" in methods


def test_asn_org_preserved(df: pd.DataFrame) -> None:
    assert "CLOUDFLARENET" in set(df["asn_org"].dropna())


# ---------------------------------------------------------------------------
# Robustheit
# ---------------------------------------------------------------------------
def test_invalid_timestamp_dropped(df: pd.DataFrame) -> None:
    assert "skip.me" not in set(df["domain"])


def test_empty_file_returns_empty_df(tmp_path: Path, pseudo: Pseudonymizer) -> None:
    f = tmp_path / "e.log"
    f.write_text("", encoding="utf-8")
    out = parse_elastic_ecs_log(f, pseudonymizer=pseudo)
    assert out.empty


def test_malformed_json_skipped(tmp_path: Path, pseudo: Pseudonymizer) -> None:
    f = tmp_path / "m.log"
    f.write_text(
        "not json\n"
        + json.dumps({
            "@timestamp": "2026-04-18T10:00:00Z",
            "event": {"category": "dns"},
            "dns": {"question": {"name": "valid.example"}},
            "source": {"ip": "10.0.0.1"},
        }) + "\n",
        encoding="utf-8",
    )
    out = parse_elastic_ecs_log(f, pseudonymizer=pseudo)
    assert len(out) == 1
    assert out.iloc[0]["domain"] == "valid.example"


def test_source_type_marker(df: pd.DataFrame) -> None:
    assert (df["source_type"] == "elastic_ecs").all()


# ---------------------------------------------------------------------------
# Category-Liste (Array-Form) wird unterstützt
# ---------------------------------------------------------------------------
def test_category_as_list_supported(tmp_path: Path, pseudo: Pseudonymizer) -> None:
    """event.category kann Array oder String sein — beides muss akzeptiert werden."""
    f = tmp_path / "l.log"
    f.write_text(json.dumps({
        "@timestamp": "2026-04-18T11:00:00Z",
        "event": {"category": ["network", "dns"]},
        "dns": {"question": {"name": "list.ok"}},
        "source": {"ip": "10.0.0.5"},
    }) + "\n", encoding="utf-8")
    out = parse_elastic_ecs_log(f, pseudonymizer=pseudo)
    assert len(out) == 1
