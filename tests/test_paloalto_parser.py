"""Tests für den Palo Alto PAN-OS URL-Filtering Parser (E3-2 / Issue #27)."""

import re
from pathlib import Path

import pandas as pd
import pytest

from src.parsers.paloalto import (
    DEFAULT_FIELDS,
    PanOSUrlParser,
    _strip_syslog_prefix,
    parse_paloalto_log,
)
from src.privacy.pseudonymizer import Pseudonymizer

FIXTURE = Path(__file__).parent.parent / "testdata" / "paloalto_sample.log"
_KEY = b"paloalto-test-key"


@pytest.fixture
def pseudonymizer():
    return Pseudonymizer(key=_KEY)


def test_happy_path_parses_fixture(pseudonymizer):
    df = parse_paloalto_log(FIXTURE, pseudonymizer=pseudonymizer)
    # 20 URL-Zeilen + 1 mit Syslog-Prefix = 21; virus-Zeile übersprungen
    assert len(df) == 21
    assert df["timestamp"].dtype == "datetime64[ns]"
    assert (df["source_type"] == "paloalto").all()
    # PAN-OS-URL-Logs führen keine Bytes
    assert df["bytes_uploaded"].isna().all()
    assert df["bytes_downloaded"].isna().all()


def test_virus_subtype_is_skipped(pseudonymizer):
    df = parse_paloalto_log(FIXTURE, pseudonymizer=pseudonymizer)
    # evil.example-Domain existiert nur in der virus-Zeile, die gefiltert wird
    assert "evil.example" not in df["domain"].values


def test_syslog_prefix_is_stripped(pseudonymizer):
    df = parse_paloalto_log(FIXTURE, pseudonymizer=pseudonymizer)
    # gemini.google.com Eintrag ist in Syslog-prefixed Zeile
    assert "gemini.google.com" in df["domain"].values


def test_strip_syslog_prefix_unit():
    prefixed = "<14>Jun 23 10:00:00 FW-01 1,2024/06/23 10:00:00,SERIAL,THREAT,url"
    assert _strip_syslog_prefix(prefixed) == "1,2024/06/23 10:00:00,SERIAL,THREAT,url"
    # Ohne Prefix bleibt die Zeile gleich
    plain = "1,2024/06/23 10:00:00,SERIAL,THREAT,url"
    assert _strip_syslog_prefix(plain) == plain


def test_client_and_user_pseudonymized(pseudonymizer):
    df = parse_paloalto_log(FIXTURE, pseudonymizer=pseudonymizer)
    ip_pattern = re.compile(r"^ip_[0-9a-f]+$")
    user_pattern = re.compile(r"^user_[0-9a-f]+$")
    for client in df["client"]:
        assert ip_pattern.match(client)
        assert not re.search(r"10\.\d{1,3}", client)
    for user in df["user"].dropna():
        assert user_pattern.match(user)
        assert "@" not in user


def test_userless_entries_have_none_user(pseudonymizer):
    df = parse_paloalto_log(FIXTURE, pseudonymizer=pseudonymizer)
    # Fixture: 3 Einträge mit user=""
    assert df["user"].isna().sum() == 3


def test_url_path_truncated_to_first_segment(pseudonymizer):
    df = parse_paloalto_log(FIXTURE, pseudonymizer=pseudonymizer)
    mentor_row = df[df["url_path"] == "/g"]
    assert not mentor_row.empty  # /g/g-BhDPQhWuS/mentor → /g
    backend_row = df[
        (df["domain"] == "chat.openai.com") & (df["url_path"] == "/backend-api")
    ]
    assert not backend_row.empty


def test_malformed_lines_are_skipped(tmp_path, pseudonymizer):
    content = (
        # Valide URL-Zeile (Position 44 = useragent, 45 Felder 0–44)
        "1,2024/06/23 10:00:00,SERIAL,THREAT,url,0,2024/06/23 10:00:00,10.0.1.1,203.0.113.1,0.0.0.0,0.0.0.0,allow,alice,,web-browsing,vsys1,trust,untrust,eth1/1,eth1/2,0,,1,1,443,443,0,0,0x00,tcp,alert,chat.openai.com/,,Computers,informational,c2s,1,0x00,DE,US,,,,,Mozilla\n"
        # Zu wenige Felder
        "1,2024/06/23 10:00:01,SERIAL,THREAT,url,0,2024/06/23 10:00:01,10.0.1.1\n"
        # Kaputter Zeitstempel
        "1,INVALID,SERIAL,THREAT,url,0,NOT-A-TIMESTAMP,10.0.1.1,203.0.113.2,0.0.0.0,0.0.0.0,allow,alice,,web-browsing,vsys1,trust,untrust,eth1/1,eth1/2,0,,2,1,443,443,0,0,0x00,tcp,alert,chat.openai.com/,,Computers,informational,c2s,1,0x00,DE,US,,,,,Mozilla\n"
        # Kommentar
        "# comment\n"
        # Leerer src_ip
        "1,2024/06/23 10:00:03,SERIAL,THREAT,url,0,2024/06/23 10:00:03,,203.0.113.3,0.0.0.0,0.0.0.0,allow,alice,,web-browsing,vsys1,trust,untrust,eth1/1,eth1/2,0,,3,1,443,443,0,0,0x00,tcp,alert,chat.openai.com/,,Computers,informational,c2s,1,0x00,DE,US,,,,,Mozilla\n"
    )
    path = tmp_path / "broken.log"
    path.write_text(content, encoding="utf-8")
    df = parse_paloalto_log(path, pseudonymizer=pseudonymizer)
    assert len(df) == 1
    assert df.iloc[0]["domain"] == "chat.openai.com"


def test_fields_validation_rejects_missing_required(pseudonymizer):
    bad_fields = dict(DEFAULT_FIELDS)
    del bad_fields["url"]
    with pytest.raises(ValueError, match="benötigt mindestens"):
        parse_paloalto_log(FIXTURE, pseudonymizer=pseudonymizer, fields=bad_fields)


def test_empty_file_returns_empty_df(tmp_path, pseudonymizer):
    path = tmp_path / "empty.log"
    path.write_text("", encoding="utf-8")
    df = parse_paloalto_log(path, pseudonymizer=pseudonymizer)
    assert df.empty
    assert df["bytes_uploaded"].dtype == "Int64"


def test_panos_parser_contract_via_class(pseudonymizer):
    parser = PanOSUrlParser(pseudonymizer=pseudonymizer)
    df = parser.parse(FIXTURE)
    assert df["timestamp"].is_monotonic_increasing
    parser.validate_schema(df, strict=True)


def test_default_fields_cover_required_positions():
    required = {"subtype", "generated_time", "src_ip", "url"}
    assert required.issubset(DEFAULT_FIELDS.keys())


def test_csv_quoting_in_useragent(tmp_path, pseudonymizer):
    # Useragent mit Komma → muss quoted werden (CSV-Reader muss handhaben)
    line = '1,2024/06/23 10:00:00,SERIAL,THREAT,url,0,2024/06/23 10:00:00,10.0.1.1,203.0.113.1,0.0.0.0,0.0.0.0,allow,alice,,web-browsing,vsys1,trust,untrust,eth1/1,eth1/2,0,,1,1,443,443,0,0,0x00,tcp,alert,chat.openai.com/,,Computers,informational,c2s,1,0x00,DE,US,,,,,"Mozilla/5.0, Extra/1.0"'
    path = tmp_path / "quoted.log"
    path.write_text(line + "\n", encoding="utf-8")
    df = parse_paloalto_log(path, pseudonymizer=pseudonymizer)
    assert len(df) == 1
    assert df.iloc[0]["useragent"] == "Mozilla/5.0, Extra/1.0"
