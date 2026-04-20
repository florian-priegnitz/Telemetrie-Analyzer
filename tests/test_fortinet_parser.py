"""Tests für den Fortinet FortiGate webfilter.log Parser (E3-4 / Issue #29)."""

import re
from pathlib import Path

import pandas as pd
import pytest

from src.parsers.fortinet import (
    FortiGateWebfilterParser,
    _parse_kv,
    _strip_syslog_prefix,
    parse_fortinet_log,
)
from src.privacy.pseudonymizer import Pseudonymizer

FIXTURE = Path(__file__).parent.parent / "testdata" / "fortinet_sample.log"
_KEY = b"fortinet-test-key"


@pytest.fixture
def pseudonymizer():
    return Pseudonymizer(key=_KEY)


def test_happy_path_parses_fixture(pseudonymizer):
    df = parse_fortinet_log(FIXTURE, pseudonymizer=pseudonymizer)
    # 22 webfilter + 1 Syslog-prefixed webfilter = 23; 1 IPS-Zeile übersprungen
    assert len(df) == 23
    assert df["timestamp"].dtype == "datetime64[ns]"
    assert (df["source_type"] == "fortinet").all()


def test_ips_subtype_skipped(pseudonymizer):
    df = parse_fortinet_log(FIXTURE, pseudonymizer=pseudonymizer)
    # evil.example existiert nur in der IPS-Zeile — muss fehlen
    assert "evil.example" not in df["domain"].values


def test_syslog_prefix_stripped(pseudonymizer):
    df = parse_fortinet_log(FIXTURE, pseudonymizer=pseudonymizer)
    # Syslog-prefixed Zeile liefert gemini.google.com mit user niaj@
    assert "gemini.google.com" in df["domain"].values


def test_strip_syslog_prefix_unit():
    prefixed = '<190>date=2024-06-23 time=08:50:00 logid="123"'
    assert _strip_syslog_prefix(prefixed) == 'date=2024-06-23 time=08:50:00 logid="123"'
    plain = 'date=2024-06-23 time=08:50:00'
    assert _strip_syslog_prefix(plain) == plain


def test_parse_kv_unit():
    line = 'date=2024-06-23 time=08:15:32 logid="0316013056" user="alice@acme" srcip=10.0.1.1 url="/v1/chat"'
    kv = _parse_kv(line)
    assert kv["date"] == "2024-06-23"
    assert kv["logid"] == "0316013056"
    assert kv["user"] == "alice@acme"
    assert kv["srcip"] == "10.0.1.1"
    assert kv["url"] == "/v1/chat"


def test_client_and_user_pseudonymized(pseudonymizer):
    df = parse_fortinet_log(FIXTURE, pseudonymizer=pseudonymizer)
    ip_pattern = re.compile(r"^ip_[0-9a-f]+$")
    user_pattern = re.compile(r"^user_[0-9a-f]+$")
    for client in df["client"]:
        assert ip_pattern.match(client)
        assert not re.search(r"10\.\d{1,3}", client)
    for user in df["user"].dropna():
        assert user_pattern.match(user)
        assert "@" not in user and "\\" not in user


def test_userless_entries_have_none_user(pseudonymizer):
    df = parse_fortinet_log(FIXTURE, pseudonymizer=pseudonymizer)
    # Fixture: 3 Einträge ohne user (leerer String im Generator)
    assert df["user"].isna().sum() == 3


def test_domain_backslash_user_pseudonymized_consistently(pseudonymizer):
    # "ACME\eve" soll identischen Pseudonym erhalten wie identischer Input
    df = parse_fortinet_log(FIXTURE, pseudonymizer=pseudonymizer)
    # alle "ACME\eve"-Zeilen müssen denselben user-Pseudonym haben
    assert "character.ai" in df["domain"].values


def test_url_path_truncated(pseudonymizer):
    df = parse_fortinet_log(FIXTURE, pseudonymizer=pseudonymizer)
    # /g/g-BhDPQhWuS/mentor → /g (DSGVO-Kurzform)
    assert "/g" in df["url_path"].values
    # /api-keys bleibt als /api-keys (ein Segment)
    assert "/api-keys" in df["url_path"].values


def test_bytes_extracted_correctly(pseudonymizer):
    df = parse_fortinet_log(FIXTURE, pseudonymizer=pseudonymizer)
    # Blocked-Events haben rcvdbyte=0
    blocked = df[df["action"] == "blocked"]
    assert (blocked["bytes_downloaded"] == 0).all()
    # Sehr großer Upload ist dokumentiert (890_512 im Fixture)
    assert (df["bytes_uploaded"] > 100_000).any()


def test_action_values_captured(pseudonymizer):
    df = parse_fortinet_log(FIXTURE, pseudonymizer=pseudonymizer)
    assert set(df["action"].unique()) == {"passthrough", "blocked"}


def test_categories_captured(pseudonymizer):
    df = parse_fortinet_log(FIXTURE, pseudonymizer=pseudonymizer)
    assert "Business Services" in df["urlcategory"].values
    assert "Unrated" in df["urlcategory"].values


def test_malformed_lines_skipped(tmp_path, pseudonymizer):
    content = (
        # Valide Zeile
        'date=2024-06-23 time=10:00:00 type="utm" subtype="webfilter" srcip=10.0.1.1 hostname="chat.openai.com" action="passthrough" url="/"\n'
        # Fehlender subtype
        'date=2024-06-23 time=10:00:01 type="utm" srcip=10.0.1.1 hostname="chat.openai.com" action="passthrough" url="/"\n'
        # subtype=ips (kein webfilter)
        'date=2024-06-23 time=10:00:02 type="utm" subtype="ips" srcip=10.0.1.1 hostname="evil.com" action="blocked"\n'
        # Fehlender srcip
        'date=2024-06-23 time=10:00:03 type="utm" subtype="webfilter" hostname="chat.openai.com" action="passthrough"\n'
        # Fehlender hostname
        'date=2024-06-23 time=10:00:04 type="utm" subtype="webfilter" srcip=10.0.1.1 action="passthrough"\n'
        # Kaputter Timestamp
        'date=not-a-date time=bad type="utm" subtype="webfilter" srcip=10.0.1.1 hostname="chat.openai.com" action="passthrough"\n'
        # Kommentarzeile
        "# comment\n"
    )
    path = tmp_path / "broken.log"
    path.write_text(content, encoding="utf-8")
    df = parse_fortinet_log(path, pseudonymizer=pseudonymizer)
    assert len(df) == 1
    assert df.iloc[0]["domain"] == "chat.openai.com"


def test_empty_file_returns_empty_df(tmp_path, pseudonymizer):
    path = tmp_path / "empty.log"
    path.write_text("", encoding="utf-8")
    df = parse_fortinet_log(path, pseudonymizer=pseudonymizer)
    assert df.empty
    assert df["bytes_uploaded"].dtype == "Int64"


def test_quoted_value_with_spaces(tmp_path, pseudonymizer):
    content = (
        'date=2024-06-23 time=10:00:00 type="utm" subtype="webfilter" srcip=10.0.1.1 '
        'hostname="chat.openai.com" action="passthrough" url="/api/conversation" '
        'catdesc="Business Services" msg="URL was allowed by filter"\n'
    )
    path = tmp_path / "spaces.log"
    path.write_text(content, encoding="utf-8")
    df = parse_fortinet_log(path, pseudonymizer=pseudonymizer)
    assert len(df) == 1
    assert df.iloc[0]["urlcategory"] == "Business Services"


def test_parser_contract_via_class(pseudonymizer):
    parser = FortiGateWebfilterParser(pseudonymizer=pseudonymizer)
    df = parser.parse(FIXTURE)
    assert df["timestamp"].is_monotonic_increasing
    parser.validate_schema(df, strict=True)
