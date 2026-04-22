"""Tests für den Azure Entra ID Sign-In Parser (E3-6 / Issue #31)."""

import json
import re
from pathlib import Path

import pytest

from src.parsers.entra_id import (
    EntraIDSignInParser,
    _derive_action,
    _parse_timestamp,
    parse_entra_signin_log,
)
from src.privacy.pseudonymizer import Pseudonymizer

FIXTURE = Path(__file__).parent.parent / "testdata" / "entra_signin_sample.log"
_KEY = b"entra-test-key"


@pytest.fixture
def pseudonymizer():
    return Pseudonymizer(key=_KEY)


def test_happy_path_parses_fixture(pseudonymizer):
    df = parse_entra_signin_log(FIXTURE, pseudonymizer=pseudonymizer)
    assert len(df) == 20
    assert df["timestamp"].dtype == "datetime64[ns]"
    assert (df["source_type"] == "azure_entra").all()
    # Sign-In-Logs haben keine Bytes / url_path
    assert df["bytes_uploaded"].isna().all()
    assert df["url_path"].isna().all()


def test_app_display_name_becomes_domain(pseudonymizer):
    df = parse_entra_signin_log(FIXTURE, pseudonymizer=pseudonymizer)
    # Shadow-AI-Highlight: AI-Apps als domain (lowercased)
    assert "microsoft 365 copilot" in df["domain"].values
    assert "chatgpt enterprise" in df["domain"].values
    assert "claude enterprise" in df["domain"].values


def test_user_principal_pseudonymized(pseudonymizer):
    df = parse_entra_signin_log(FIXTURE, pseudonymizer=pseudonymizer)
    user_pattern = re.compile(r"^user_[0-9a-f]+$")
    for user in df["user"].dropna():
        assert user_pattern.match(user)
        assert "@" not in user
        assert "onmicrosoft.com" not in user


def test_ip_pseudonymized(pseudonymizer):
    df = parse_entra_signin_log(FIXTURE, pseudonymizer=pseudonymizer)
    ip_pattern = re.compile(r"^ip_[0-9a-f]+$")
    user_pattern = re.compile(r"^user_[0-9a-f]+$")
    # Jeder client matcht entweder ip_* oder user_* (UserId-Fallback bei leerer IP)
    for client in df["client"]:
        assert ip_pattern.match(client) or user_pattern.match(client)
        assert not re.search(r"203\.0\.113", client)
        assert not re.search(r"2001:", client)


def test_empty_ip_fallback_to_user_id(pseudonymizer):
    # Fixture-Zeile #11 hat leere IPAddress → client soll user_*-Pseudonym sein
    df = parse_entra_signin_log(FIXTURE, pseudonymizer=pseudonymizer)
    user_pattern = re.compile(r"^user_[0-9a-f]+$")
    fallback_clients = [c for c in df["client"] if user_pattern.match(c)]
    assert len(fallback_clients) >= 1


def test_action_success(pseudonymizer):
    df = parse_entra_signin_log(FIXTURE, pseudonymizer=pseudonymizer)
    assert "success" in df["action"].values


def test_action_blocked_from_conditional_access(pseudonymizer):
    # Fixture #6 (eve) + #15 (niaj) → ConditionalAccessStatus=failure → blocked
    df = parse_entra_signin_log(FIXTURE, pseudonymizer=pseudonymizer)
    blocked = df[df["action"] == "blocked"]
    assert len(blocked) == 2
    assert "perplexity ai" in blocked["domain"].values
    assert "microsoft 365 copilot" in blocked["domain"].values


def test_action_failed_from_error_code(pseudonymizer):
    # Fixture #14 (mallory 50126) + #18 (trent 500121) → failed
    # Azure errorCodes passen nicht in Int16 → status_code bleibt NA;
    # Semantik ist über action="failed" vollständig abgebildet.
    df = parse_entra_signin_log(FIXTURE, pseudonymizer=pseudonymizer)
    failed = df[df["action"] == "failed"]
    assert len(failed) == 2
    assert failed["status_code"].isna().all()


def test_derive_action_unit():
    assert _derive_action({"ConditionalAccessStatus": "failure"}) == "blocked"
    assert _derive_action({"Status": {"errorCode": 50126}}) == "failed"
    assert _derive_action({"Status": {"errorCode": 0}, "ConditionalAccessStatus": "success"}) == "success"
    assert _derive_action({"Status": {"errorCode": 0}, "ConditionalAccessStatus": "notApplied"}) == "success"
    assert _derive_action({}) == "success"  # Defensive default


def test_ipv6_address_pseudonymized(pseudonymizer):
    # Fixture #20 hat IPv6 "2001:db8::1"
    df = parse_entra_signin_log(FIXTURE, pseudonymizer=pseudonymizer)
    ipv6_rows = df[df["domain"] == "deepseek"]
    assert not ipv6_rows.empty
    assert ipv6_rows.iloc[0]["client"].startswith("ip_")


def test_parse_timestamp_variants():
    assert _parse_timestamp("2024-06-23T08:15:32.000Z") is not None
    assert _parse_timestamp("2024-06-23T08:15:32+00:00") is not None
    assert _parse_timestamp("not-a-date") is None
    assert _parse_timestamp("") is None
    assert _parse_timestamp(None) is None


def test_malformed_lines_skipped(tmp_path, pseudonymizer):
    content = (
        # Valide Zeile
        json.dumps({
            "TimeGenerated": "2024-06-23T10:00:00Z",
            "UserPrincipalName": "a@x.com", "UserId": "u1",
            "AppDisplayName": "ChatGPT Enterprise", "AppId": "app1",
            "IPAddress": "10.0.0.1",
            "Status": {"errorCode": 0},
        }) + "\n"
        # Kein JSON
        "not-json-at-all\n"
        # JSON aber kein Object (List)
        "[1,2,3]\n"
        # Leere Zeile
        "\n"
        # Kommentar
        "# comment\n"
        # JSON ohne AppDisplayName
        + json.dumps({
            "TimeGenerated": "2024-06-23T10:00:01Z",
            "UserPrincipalName": "a@x.com", "UserId": "u1",
            "IPAddress": "10.0.0.1",
            "Status": {"errorCode": 0},
        }) + "\n"
        # JSON ohne client (keine IP, keine UserId)
        + json.dumps({
            "TimeGenerated": "2024-06-23T10:00:02Z",
            "UserPrincipalName": "a@x.com",
            "AppDisplayName": "ChatGPT Enterprise",
            "Status": {"errorCode": 0},
        }) + "\n"
        # JSON mit kaputtem Timestamp
        + json.dumps({
            "TimeGenerated": "not-a-date",
            "UserPrincipalName": "a@x.com", "UserId": "u1",
            "AppDisplayName": "ChatGPT Enterprise",
            "IPAddress": "10.0.0.1",
            "Status": {"errorCode": 0},
        }) + "\n"
    )
    f = tmp_path / "broken.jsonl"
    f.write_text(content, encoding="utf-8")
    df = parse_entra_signin_log(f, pseudonymizer=pseudonymizer)
    assert len(df) == 1
    assert df.iloc[0]["domain"] == "chatgpt enterprise"


def test_empty_file_returns_empty_df(tmp_path, pseudonymizer):
    f = tmp_path / "empty.jsonl"
    f.write_text("", encoding="utf-8")
    df = parse_entra_signin_log(f, pseudonymizer=pseudonymizer)
    assert df.empty
    assert df["bytes_uploaded"].dtype == "Int64"


def test_parser_contract_via_class(pseudonymizer):
    parser = EntraIDSignInParser(pseudonymizer=pseudonymizer)
    df = parser.parse(FIXTURE)
    assert df["timestamp"].is_monotonic_increasing
    parser.validate_schema(df, strict=True)


def test_status_code_always_na():
    # Azure errorCodes sprengen Int16; Semantik ist in action gekapselt
    df = parse_entra_signin_log(FIXTURE, pseudonymizer=Pseudonymizer(key=_KEY))
    assert df["status_code"].dtype == "Int16"
    assert df["status_code"].isna().all()


def test_authentication_protocol_as_method(pseudonymizer):
    df = parse_entra_signin_log(FIXTURE, pseudonymizer=pseudonymizer)
    # AuthenticationProtocol wird in method-Spalte gemappt
    assert "oAuth2" in df["method"].values


def test_app_id_preserved(pseudonymizer):
    df = parse_entra_signin_log(FIXTURE, pseudonymizer=pseudonymizer)
    # AppId-GUID wird in app-Spalte erhalten
    assert df["app"].str.startswith("00000000").all()
