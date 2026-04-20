"""Tests für den Cloudflare Gateway Parser (E3-7 / Issue #32)."""

import json
import re
from pathlib import Path

import pytest

from src.parsers.cloudflare_gateway import (
    CloudflareGatewayParser,
    _normalize_categories,
    _parse_timestamp,
    parse_cloudflare_gateway_log,
)
from src.privacy.pseudonymizer import Pseudonymizer

FIXTURE = Path(__file__).parent.parent / "testdata" / "cloudflare_gateway_sample.log"
_KEY = b"cloudflare-test-key"


@pytest.fixture
def pseudonymizer():
    return Pseudonymizer(key=_KEY)


def test_happy_path_parses_fixture(pseudonymizer):
    df = parse_cloudflare_gateway_log(FIXTURE, pseudonymizer=pseudonymizer)
    # 12 DNS + 10 HTTP = 22
    assert len(df) == 22


def test_dns_and_http_split_by_source_type(pseudonymizer):
    df = parse_cloudflare_gateway_log(FIXTURE, pseudonymizer=pseudonymizer)
    dns = df[df["source_type"] == "cloudflare_gateway_dns"]
    http = df[df["source_type"] == "cloudflare_gateway_http"]
    assert len(dns) == 12
    assert len(http) == 10


def test_dns_fields_only_for_dns_records(pseudonymizer):
    df = parse_cloudflare_gateway_log(FIXTURE, pseudonymizer=pseudonymizer)
    dns = df[df["source_type"] == "cloudflare_gateway_dns"]
    # DNS hat query_type, keine HTTP-Felder
    assert dns["query_type"].notna().all()
    assert dns["method"].isna().all()
    assert dns["status_code"].isna().all()
    assert dns["bytes_uploaded"].isna().all()


def test_http_fields_only_for_http_records(pseudonymizer):
    df = parse_cloudflare_gateway_log(FIXTURE, pseudonymizer=pseudonymizer)
    http = df[df["source_type"] == "cloudflare_gateway_http"]
    # HTTP hat method, status_code, bytes, useragent — aber KEIN query_type
    assert http["method"].notna().all()
    assert http["status_code"].notna().all()
    assert http["bytes_uploaded"].notna().all()
    assert http["useragent"].notna().all()
    assert http["query_type"].isna().all()


def test_src_ip_and_email_pseudonymized(pseudonymizer):
    df = parse_cloudflare_gateway_log(FIXTURE, pseudonymizer=pseudonymizer)
    ip_pattern = re.compile(r"^ip_[0-9a-f]+$")
    user_pattern = re.compile(r"^user_[0-9a-f]+$")
    for client in df["client"]:
        assert ip_pattern.match(client)
        assert not re.search(r"10\.\d{1,3}", client)
    for user in df["user"].dropna():
        assert user_pattern.match(user)
        assert "@" not in user


def test_empty_email_yields_none_user(pseudonymizer):
    df = parse_cloudflare_gateway_log(FIXTURE, pseudonymizer=pseudonymizer)
    # Fixture: 4 Zeilen mit leerer Email (2 DNS + keine HTTP derzeit, 2 DNS)
    assert df["user"].isna().sum() >= 2


def test_dns_action_values(pseudonymizer):
    df = parse_cloudflare_gateway_log(FIXTURE, pseudonymizer=pseudonymizer)
    dns = df[df["source_type"] == "cloudflare_gateway_dns"]
    assert "allowed" in dns["action"].values
    assert "blocked" in dns["action"].values


def test_http_action_values(pseudonymizer):
    df = parse_cloudflare_gateway_log(FIXTURE, pseudonymizer=pseudonymizer)
    http = df[df["source_type"] == "cloudflare_gateway_http"]
    assert "allow" in http["action"].values
    assert "block" in http["action"].values
    assert "isolate" in http["action"].values


def test_url_path_truncated(pseudonymizer):
    df = parse_cloudflare_gateway_log(FIXTURE, pseudonymizer=pseudonymizer)
    # Fixture-URL /g/g-BhDPQhWuS/mentor → /g (DSGVO-Truncation)
    paths = df["url_path"].dropna().unique()
    assert "/g" in paths
    assert "/backend-api" in paths


def test_categories_joined_from_list(pseudonymizer):
    df = parse_cloudflare_gateway_log(FIXTURE, pseudonymizer=pseudonymizer)
    assert df["urlcategory"].str.contains("Generative AI", na=False).sum() >= 20
    # Multi-Category Zeilen haben Komma-getrennte Werte
    assert df["urlcategory"].str.contains(", ", na=False).any()


def test_normalize_categories_unit():
    assert _normalize_categories(None) is None
    assert _normalize_categories([]) is None
    assert _normalize_categories(["A"]) == "A"
    assert _normalize_categories(["A", "B"]) == "A, B"
    assert _normalize_categories("Single") == "Single"
    assert _normalize_categories("") is None


def test_parse_timestamp_iso8601():
    assert _parse_timestamp("2024-06-23T08:15:32Z") is not None
    assert _parse_timestamp("2024-06-23T08:15:32+00:00") is not None
    assert _parse_timestamp("invalid") is None
    assert _parse_timestamp(None) is None


def test_malformed_lines_skipped(tmp_path, pseudonymizer):
    content = (
        # Valide DNS-Zeile
        json.dumps({
            "Datetime": "2024-06-23T10:00:00Z",
            "SrcIP": "10.0.1.1",
            "QueryName": "chat.openai.com",
            "QueryType": "A",
            "ResolverDecision": "allowed",
        }) + "\n"
        # Kein JSON
        "not-json\n"
        # JSON aber kein Object
        "[1,2,3]\n"
        # Kaputter Timestamp
        + json.dumps({
            "Datetime": "not-a-date",
            "SrcIP": "10.0.1.1",
            "QueryName": "chat.openai.com",
        }) + "\n"
        # Fehlender SrcIP
        + json.dumps({
            "Datetime": "2024-06-23T10:00:01Z",
            "QueryName": "chat.openai.com",
        }) + "\n"
        # DNS ohne QueryName
        + json.dumps({
            "Datetime": "2024-06-23T10:00:02Z",
            "SrcIP": "10.0.1.1",
            "QueryType": "A",
        }) + "\n"
        # HTTP ohne URL
        + json.dumps({
            "Datetime": "2024-06-23T10:00:03Z",
            "SrcIP": "10.0.1.1",
            "HTTPMethod": "GET",
            "HTTPStatusCode": 200,
        }) + "\n"
        # Leere Zeile
        "\n"
        # Kommentar
        "# comment\n"
    )
    f = tmp_path / "broken.jsonl"
    f.write_text(content, encoding="utf-8")
    df = parse_cloudflare_gateway_log(f, pseudonymizer=pseudonymizer)
    assert len(df) == 1
    assert df.iloc[0]["domain"] == "chat.openai.com"
    assert df.iloc[0]["source_type"] == "cloudflare_gateway_dns"


def test_empty_file_returns_empty_df(tmp_path, pseudonymizer):
    f = tmp_path / "empty.jsonl"
    f.write_text("", encoding="utf-8")
    df = parse_cloudflare_gateway_log(f, pseudonymizer=pseudonymizer)
    assert df.empty
    assert df["bytes_uploaded"].dtype == "Int64"


def test_http_detection_by_status_code_only(tmp_path, pseudonymizer):
    # Falls URL fehlt aber HTTPStatusCode vorhanden → als HTTP erkannt (skip:
    # URL-Pflicht-Check greift, Zeile verworfen)
    f = tmp_path / "http_no_url.jsonl"
    f.write_text(json.dumps({
        "Datetime": "2024-06-23T10:00:00Z",
        "SrcIP": "10.0.1.1",
        "HTTPStatusCode": 200,
    }) + "\n", encoding="utf-8")
    df = parse_cloudflare_gateway_log(f, pseudonymizer=pseudonymizer)
    assert df.empty


def test_parser_contract_via_class(pseudonymizer):
    parser = CloudflareGatewayParser(pseudonymizer=pseudonymizer)
    df = parser.parse(FIXTURE)
    assert df["timestamp"].is_monotonic_increasing
    parser.validate_schema(df, strict=True)


def test_domain_lowercased(pseudonymizer):
    df = parse_cloudflare_gateway_log(FIXTURE, pseudonymizer=pseudonymizer)
    for domain in df["domain"].dropna():
        assert domain == domain.lower()
        assert not domain.endswith(".")


def test_matched_category_names_fallback(tmp_path, pseudonymizer):
    # MatchedCategoryNames wird genutzt wenn QueryCategoryNames fehlt
    content = json.dumps({
        "Datetime": "2024-06-23T10:00:00Z",
        "SrcIP": "10.0.1.1",
        "QueryName": "chat.openai.com",
        "QueryType": "A",
        "ResolverDecision": "allowed",
        "MatchedCategoryNames": ["Generative AI"],  # statt QueryCategoryNames
    }) + "\n"
    f = tmp_path / "matched.jsonl"
    f.write_text(content, encoding="utf-8")
    df = parse_cloudflare_gateway_log(f, pseudonymizer=pseudonymizer)
    assert len(df) == 1
    assert df.iloc[0]["urlcategory"] == "Generative AI"


def test_dns_beats_http_when_both_indicators_present(tmp_path, pseudonymizer):
    # Schema-Drift-Schutz: QueryName hat Vorrang vor HTTPStatusCode
    content = json.dumps({
        "Datetime": "2024-06-23T10:00:00Z",
        "SrcIP": "10.0.1.1",
        "QueryName": "chat.openai.com",
        "QueryType": "A",
        "ResolverDecision": "allowed",
        "HTTPStatusCode": 200,  # Noise-Feld
    }) + "\n"
    f = tmp_path / "mixed.jsonl"
    f.write_text(content, encoding="utf-8")
    df = parse_cloudflare_gateway_log(f, pseudonymizer=pseudonymizer)
    assert len(df) == 1
    assert df.iloc[0]["source_type"] == "cloudflare_gateway_dns"
