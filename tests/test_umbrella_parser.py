"""Tests für den Cisco Umbrella DNS Security Parser (E3-3 / Issue #28)."""

import csv
import io
import re
from pathlib import Path

import pandas as pd
import pytest

from src.parsers.umbrella import (
    USER_IDENTITY_TYPES,
    UmbrellaDNSParser,
    V10_COLUMNS,
    parse_umbrella_log,
)
from src.privacy.pseudonymizer import Pseudonymizer

FIXTURE = Path(__file__).parent.parent / "testdata" / "umbrella_sample.log"
_KEY = b"umbrella-test-key"


@pytest.fixture
def pseudonymizer():
    return Pseudonymizer(key=_KEY)


def test_happy_path_parses_fixture(pseudonymizer):
    df = parse_umbrella_log(FIXTURE, pseudonymizer=pseudonymizer)
    assert len(df) == 32
    assert df["timestamp"].dtype == "datetime64[ns]"
    assert (df["source_type"] == "umbrella").all()
    # DNS-Logs führen keine Bytes / HTTP-Method
    assert df["bytes_uploaded"].isna().all()
    assert df["method"].isna().all()
    assert df["url_path"].isna().all()


def test_client_pseudonymized_from_internal_ip(pseudonymizer):
    df = parse_umbrella_log(FIXTURE, pseudonymizer=pseudonymizer)
    ip_pattern = re.compile(r"^ip_[0-9a-f]+$")
    for client in df["client"]:
        assert ip_pattern.match(client)
        assert not re.search(r"10\.\d{1,3}", client)


def test_user_pseudonymized_only_for_user_identity_types(pseudonymizer):
    df = parse_umbrella_log(FIXTURE, pseudonymizer=pseudonymizer)
    user_pattern = re.compile(r"^user_[0-9a-f]+$")

    # AD-User-Zeilen haben einen pseudonymen user
    ad_rows = df[df["identity_type"] == "AD User"]
    assert not ad_rows.empty
    for user in ad_rows["user"].dropna():
        assert user_pattern.match(user)
        assert "@" not in user

    # Non-User-Types (Network, Device, Roaming Computer) haben user=NaN
    non_user_rows = df[df["identity_type"].isin(
        ["Network", "Device", "Roaming Computer"]
    )]
    assert not non_user_rows.empty
    assert non_user_rows["user"].isna().all()


def test_blocked_events_flagged(pseudonymizer):
    df = parse_umbrella_log(FIXTURE, pseudonymizer=pseudonymizer)
    blocked = df[df["action"] == "Blocked"]
    # Fixture enthält 5 Blocked-Events (character.ai ×3, poe.com, openrouter.ai)
    assert len(blocked) == 5
    assert set(blocked["domain"].unique()) <= {
        "character.ai", "poe.com", "openrouter.ai",
    }


def test_domain_normalization_strips_trailing_dot(pseudonymizer):
    df = parse_umbrella_log(FIXTURE, pseudonymizer=pseudonymizer)
    assert not df["domain"].str.endswith(".").any()
    assert not df["domain"].str.contains(r"[A-Z]").any()


def test_categories_preserved(pseudonymizer):
    df = parse_umbrella_log(FIXTURE, pseudonymizer=pseudonymizer)
    genai_rows = df[df["urlcategory"].str.contains("Generative AI", na=False)]
    assert len(genai_rows) >= 25  # Mehrheit der Fixture-Zeilen


def test_query_type_extracted(pseudonymizer):
    df = parse_umbrella_log(FIXTURE, pseudonymizer=pseudonymizer)
    assert "1 (A)" in df["query_type"].values
    assert "28 (AAAA)" in df["query_type"].values


def test_header_detection_auto(tmp_path, pseudonymizer):
    # Datei ohne Header → positions-basiertes Parsing
    headerless = tmp_path / "no_header.csv"
    with open(headerless, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        # Eine valide v10-Zeile ohne Header davor
        writer.writerow([
            "2024-06-23 09:00:00", "alice@acme.corp",
            "alice@acme.corp,HQ-Network", "10.0.1.1", "203.0.113.1",
            "Allowed", "1 (A)", "NOERROR", "chat.openai.com.",
            "Generative AI", "AD User", "AD User,Network",
            "", "101", "US", "9999",
        ])

    df = parse_umbrella_log(headerless, pseudonymizer=pseudonymizer)
    assert len(df) == 1
    assert df.iloc[0]["domain"] == "chat.openai.com"


def test_has_header_override(tmp_path, pseudonymizer):
    # Force has_header="no" auf Datei mit Header → die Header-Row wird als
    # Daten interpretiert und beim Timestamp-Parsing verworfen
    f = tmp_path / "with_header.csv"
    with open(f, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, quoting=csv.QUOTE_ALL)
        writer.writerow(list(V10_COLUMNS))
        writer.writerow([
            "2024-06-23 09:00:00", "alice", "alice", "10.0.1.1",
            "203.0.113.1", "Allowed", "1 (A)", "NOERROR",
            "example.com.", "Generative AI", "AD User", "AD User",
            "", "101", "US", "9999",
        ])

    # mit has_header="no" → Header-Zeile fällt weg (INVALID timestamp)
    df = parse_umbrella_log(f, pseudonymizer=pseudonymizer, has_header="no")
    assert len(df) == 1  # nur die valide Daten-Zeile


def test_malformed_lines_skipped(tmp_path, pseudonymizer):
    f = tmp_path / "broken.csv"
    content = io.StringIO()
    writer = csv.writer(content, quoting=csv.QUOTE_ALL)
    writer.writerow(list(V10_COLUMNS))  # Header
    # Valide Zeile
    writer.writerow([
        "2024-06-23 09:00:00", "alice", "alice", "10.0.1.1", "203.0.113.1",
        "Allowed", "1 (A)", "NOERROR", "chat.openai.com.",
        "Generative AI", "AD User", "AD User,Network",
        "", "101", "US", "9999",
    ])
    # Zeitstempel kaputt
    writer.writerow([
        "not-a-date", "alice", "alice", "10.0.1.1", "203.0.113.1",
        "Allowed", "1 (A)", "NOERROR", "chat.openai.com.",
        "Generative AI", "AD User", "AD User,Network",
        "", "101", "US", "9999",
    ])
    # Domain leer
    writer.writerow([
        "2024-06-23 09:00:01", "alice", "alice", "10.0.1.1", "203.0.113.1",
        "Allowed", "1 (A)", "NOERROR", "",
        "Generative AI", "AD User", "AD User,Network",
        "", "101", "US", "9999",
    ])
    # Weder internal_ip noch identity
    writer.writerow([
        "2024-06-23 09:00:02", "", "", "", "203.0.113.1",
        "Allowed", "1 (A)", "NOERROR", "chat.openai.com.",
        "Generative AI", "", "",
        "", "101", "US", "9999",
    ])
    f.write_text(content.getvalue(), encoding="utf-8")

    df = parse_umbrella_log(f, pseudonymizer=pseudonymizer)
    assert len(df) == 1


def test_empty_file_returns_empty_df(tmp_path, pseudonymizer):
    f = tmp_path / "empty.csv"
    f.write_text("", encoding="utf-8")
    df = parse_umbrella_log(f, pseudonymizer=pseudonymizer)
    assert df.empty
    assert df["bytes_uploaded"].dtype == "Int64"


def test_has_header_invalid_value(pseudonymizer):
    with pytest.raises(ValueError, match="has_header"):
        parse_umbrella_log(FIXTURE, pseudonymizer=pseudonymizer, has_header="maybe")


def test_network_identity_falls_back_to_ip(pseudonymizer):
    df = parse_umbrella_log(FIXTURE, pseudonymizer=pseudonymizer)
    # "HQ-Network"-Zeile hat identity_type "Network" → user=None, client aus internal_ip
    network_rows = df[df["identity_type"] == "Network"]
    assert not network_rows.empty
    assert network_rows["user"].isna().all()


def test_parser_contract_via_class(pseudonymizer):
    parser = UmbrellaDNSParser(pseudonymizer=pseudonymizer)
    df = parser.parse(FIXTURE)
    assert df["timestamp"].is_monotonic_increasing
    parser.validate_schema(df, strict=True)


def test_user_identity_types_frozenset():
    assert "AD User" in USER_IDENTITY_TYPES
    assert "User" in USER_IDENTITY_TYPES
    assert "Network" not in USER_IDENTITY_TYPES


def test_utf8_bom_header_is_handled(tmp_path, pseudonymizer):
    # Windows/PowerShell S3-Exporte können einen BOM enthalten → Header-Detect
    # muss trotzdem greifen.
    f = tmp_path / "bom.csv"
    content = (
        '\ufeff"timestamp","most_granular_identity","identities","internal_ip",'
        '"external_ip","action","query_type","response_code","domain","categories",'
        '"most_granular_identity_type","identity_types","blocked_categories",'
        '"rule_id","destination_countries","organization_id"\n'
        '"2024-06-23 09:00:00","alice","alice","10.0.1.1","203.0.113.1",'
        '"Allowed","1 (A)","NOERROR","chat.openai.com.","Generative AI",'
        '"AD User","AD User,Network","","101","US","9999"\n'
    )
    f.write_text(content, encoding="utf-8")
    df = parse_umbrella_log(f, pseudonymizer=pseudonymizer)
    assert len(df) == 1
    assert df.iloc[0]["domain"] == "chat.openai.com"


def test_blocked_by_dns_action_variant(tmp_path, pseudonymizer):
    # Umbrella produziert auch "Blocked by DNS", "Blocked by SWG", "Monitored".
    # Parser reicht action 1:1 durch; Detection-Seite sollte str.startswith("Blocked")
    # verwenden, nicht == "Blocked".
    f = tmp_path / "variants.csv"
    content = (
        '"timestamp","most_granular_identity","identities","internal_ip",'
        '"external_ip","action","query_type","response_code","domain","categories",'
        '"most_granular_identity_type","identity_types","blocked_categories",'
        '"rule_id","destination_countries","organization_id"\n'
        '"2024-06-23 09:00:00","alice","alice","10.0.1.1","203.0.113.1",'
        '"Blocked by DNS","1 (A)","NXDOMAIN","character.ai.","Generative AI",'
        '"AD User","AD User,Network","","101","US","9999"\n'
        '"2024-06-23 09:00:01","bob","bob","10.0.1.2","203.0.113.1",'
        '"Monitored","1 (A)","NOERROR","chat.openai.com.","Generative AI",'
        '"AD User","AD User,Network","","101","US","9999"\n'
    )
    f.write_text(content, encoding="utf-8")
    df = parse_umbrella_log(f, pseudonymizer=pseudonymizer)
    assert len(df) == 2
    assert df.iloc[0]["action"] == "Blocked by DNS"
    assert df.iloc[1]["action"] == "Monitored"
    # Detection-Konvention:
    assert df["action"].str.startswith("Blocked").sum() == 1
