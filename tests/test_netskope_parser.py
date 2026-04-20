"""Tests für den Netskope CASB Parser (E3-8 / Issue #33)."""

import json
import re
from pathlib import Path

import pytest

from src.parsers.netskope import (
    NetskopeCASBParser,
    _parse_timestamp,
    parse_netskope_log,
)
from src.privacy.pseudonymizer import Pseudonymizer

FIXTURE = Path(__file__).parent.parent / "testdata" / "netskope_sample.log"
_KEY = b"netskope-test-key"


@pytest.fixture
def pseudonymizer():
    return Pseudonymizer(key=_KEY)


def test_happy_path_parses_fixture(pseudonymizer):
    df = parse_netskope_log(FIXTURE, pseudonymizer=pseudonymizer)
    assert len(df) == 18
    assert df["timestamp"].dtype == "datetime64[ns]"
    assert (df["source_type"] == "netskope").all()


def test_ai_app_category_preserved(pseudonymizer):
    df = parse_netskope_log(FIXTURE, pseudonymizer=pseudonymizer)
    ai_events = df[df["urlcategory"] == "Artificial Intelligence"]
    # 16 Events haben AI-Kategorie (Notion + GitHub sind "Collaboration"/"Software Development")
    assert len(ai_events) == 16


def test_activity_values_captured(pseudonymizer):
    df = parse_netskope_log(FIXTURE, pseudonymizer=pseudonymizer)
    # Shadow-AI-relevante Activities: Prompt, Completion, Upload File
    activities = df["activity"].unique()
    assert "Prompt" in activities
    assert "Completion" in activities
    assert "Upload File" in activities
    assert "Login" in activities


def test_app_name_preserved(pseudonymizer):
    df = parse_netskope_log(FIXTURE, pseudonymizer=pseudonymizer)
    apps = set(df["app"].unique())
    # Bekannte AI-Apps im Fixture
    for expected in ["OpenAI ChatGPT", "Anthropic Claude", "Google Gemini", "Microsoft Copilot"]:
        assert expected in apps


def test_client_and_user_pseudonymized(pseudonymizer):
    df = parse_netskope_log(FIXTURE, pseudonymizer=pseudonymizer)
    ip_pattern = re.compile(r"^ip_[0-9a-f]+$")
    user_pattern = re.compile(r"^user_[0-9a-f]+$")
    for client in df["client"]:
        assert ip_pattern.match(client)
        assert not re.search(r"10\.\d{1,3}", client)
    for user in df["user"].dropna():
        assert user_pattern.match(user)
        assert "@" not in user


def test_empty_user_yields_none(pseudonymizer):
    df = parse_netskope_log(FIXTURE, pseudonymizer=pseudonymizer)
    # Fixture: 2 Events mit leerem user (#6 Copilot + #10 Perplexity)
    assert df["user"].isna().sum() == 2


def test_upload_file_detection(pseudonymizer):
    df = parse_netskope_log(FIXTURE, pseudonymizer=pseudonymizer)
    uploads = df[df["activity"] == "Upload File"]
    assert len(uploads) == 2
    # Sehr große Uploads sind typisch für Doc-zu-AI-Leaks
    assert (uploads["bytes_uploaded"] > 500_000).any()


def test_action_values_distributed(pseudonymizer):
    df = parse_netskope_log(FIXTURE, pseudonymizer=pseudonymizer)
    actions = set(df["action"].unique())
    assert "allow" in actions
    assert "block" in actions
    assert "alert" in actions


def test_url_path_truncated(pseudonymizer):
    df = parse_netskope_log(FIXTURE, pseudonymizer=pseudonymizer)
    # /backend-api/conversation → /backend-api (DSGVO-Truncation)
    assert "/backend-api" in df["url_path"].values
    assert "/v1" in df["url_path"].values


def test_parse_timestamp_prefers_insertion_epoch():
    event = {"_insertion_epoch_timestamp": 1719131732, "timestamp": 1719131000}
    ts = _parse_timestamp(event)
    assert ts is not None
    assert ts.strftime("%Y-%m-%d %H:%M:%S") == "2024-06-23 08:35:32"


def test_parse_timestamp_fallback_to_timestamp():
    event = {"timestamp": 1719131732}
    ts = _parse_timestamp(event)
    assert ts is not None


def test_parse_timestamp_handles_invalid():
    assert _parse_timestamp({"timestamp": "not-a-number"}) is None
    assert _parse_timestamp({}) is None


def test_malformed_lines_skipped(tmp_path, pseudonymizer):
    content = (
        # Valide Zeile
        json.dumps({
            "_insertion_epoch_timestamp": 1719131732,
            "user": "alice@acme.com",
            "src_ip": "10.0.1.1",
            "hostname": "chat.openai.com",
            "app": "OpenAI ChatGPT",
            "appcategory": "Artificial Intelligence",
            "activity": "Prompt",
            "action": "allow",
        }) + "\n"
        # Kein JSON
        "not-json\n"
        # JSON-Liste
        "[]\n"
        # Fehlender Timestamp
        + json.dumps({
            "user": "a@x.com",
            "src_ip": "10.0.1.1",
            "hostname": "chat.openai.com",
            "app": "OpenAI ChatGPT",
        }) + "\n"
        # Fehlender src_ip
        + json.dumps({
            "_insertion_epoch_timestamp": 1719131733,
            "user": "a@x.com",
            "hostname": "chat.openai.com",
            "app": "OpenAI ChatGPT",
        }) + "\n"
        # Fehlender hostname UND app → kein Domain-Quell
        + json.dumps({
            "_insertion_epoch_timestamp": 1719131734,
            "user": "a@x.com",
            "src_ip": "10.0.1.1",
        }) + "\n"
    )
    f = tmp_path / "broken.jsonl"
    f.write_text(content, encoding="utf-8")
    df = parse_netskope_log(f, pseudonymizer=pseudonymizer)
    assert len(df) == 1
    assert df.iloc[0]["domain"] == "chat.openai.com"


def test_empty_file_returns_empty_df(tmp_path, pseudonymizer):
    f = tmp_path / "empty.jsonl"
    f.write_text("", encoding="utf-8")
    df = parse_netskope_log(f, pseudonymizer=pseudonymizer)
    assert df.empty
    assert df["bytes_uploaded"].dtype == "Int64"


def test_hostname_fallback_to_app(tmp_path, pseudonymizer):
    # Kein hostname → app wird als domain genutzt (Schema-Dehnung)
    content = json.dumps({
        "_insertion_epoch_timestamp": 1719131732,
        "user": "a@x.com",
        "src_ip": "10.0.1.1",
        "app": "OpenAI ChatGPT",
        "appcategory": "Artificial Intelligence",
    }) + "\n"
    f = tmp_path / "no_host.jsonl"
    f.write_text(content, encoding="utf-8")
    df = parse_netskope_log(f, pseudonymizer=pseudonymizer)
    assert len(df) == 1
    assert df.iloc[0]["domain"] == "openai chatgpt"


def test_userip_fallback_to_src_ip(tmp_path, pseudonymizer):
    # Kein src_ip → userip wird als client-Quelle genutzt
    content = json.dumps({
        "_insertion_epoch_timestamp": 1719131732,
        "user": "a@x.com",
        "userip": "10.0.1.1",
        "hostname": "chat.openai.com",
        "app": "OpenAI ChatGPT",
    }) + "\n"
    f = tmp_path / "userip.jsonl"
    f.write_text(content, encoding="utf-8")
    df = parse_netskope_log(f, pseudonymizer=pseudonymizer)
    assert len(df) == 1
    assert df.iloc[0]["client"].startswith("ip_")


def test_parser_contract_via_class(pseudonymizer):
    parser = NetskopeCASBParser(pseudonymizer=pseudonymizer)
    df = parser.parse(FIXTURE)
    assert df["timestamp"].is_monotonic_increasing
    parser.validate_schema(df, strict=True)
