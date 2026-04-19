"""Tests für den Zscaler ZIA Web Proxy Parser (E3-1 / Issue #26)."""

import re
from pathlib import Path

import pandas as pd
import pytest

from src.parsers.zscaler import DEFAULT_FIELDS, ZscalerParser, parse_zscaler_log
from src.privacy.pseudonymizer import Pseudonymizer

FIXTURE = Path(__file__).parent.parent / "testdata" / "zscaler_sample.log"

_PSEUDO_KEY = b"zscaler-test-key"


@pytest.fixture
def pseudonymizer():
    return Pseudonymizer(key=_PSEUDO_KEY)


def test_happy_path_parses_fixture(pseudonymizer):
    df = parse_zscaler_log(FIXTURE, pseudonymizer=pseudonymizer)
    assert len(df) == 25
    assert df["timestamp"].dtype == "datetime64[ns]"
    assert df["bytes_uploaded"].dtype == "Int64"
    assert df["bytes_downloaded"].dtype == "Int64"
    assert df["status_code"].dtype == "Int16"
    assert (df["source_type"] == "zscaler").all()


def test_client_and_user_pseudonymized(pseudonymizer):
    df = parse_zscaler_log(FIXTURE, pseudonymizer=pseudonymizer)
    ip_pattern = re.compile(r"^ip_[0-9a-f]+$")
    user_pattern = re.compile(r"^user_[0-9a-f]+$")
    for client in df["client"]:
        assert ip_pattern.match(client)
        assert not re.search(r"10\.\d{1,3}", client)
    for user in df["user"].dropna():
        assert user_pattern.match(user)
        assert "@" not in user


def test_userless_entries_have_none_user(pseudonymizer):
    df = parse_zscaler_log(FIXTURE, pseudonymizer=pseudonymizer)
    # Fixture hat 3 Zeilen mit user='-' → müssen als NaN/None landen
    assert df["user"].isna().sum() == 3


def test_malformed_lines_are_skipped(tmp_path, pseudonymizer):
    content = (
        # valide Zeile
        "23-Jun-2024 10:00:00\talice@acme.corp\t10.0.1.1\thttps://chat.openai.com/\tAllowed\tProd\tChatGPT\t200\t512\t1024\tGET\tMozilla/5.0\n"
        # Unparsebarer Zeitstempel
        "2024-06-23T10:00:01Z\talice@acme.corp\t10.0.1.1\thttps://chat.openai.com/\tAllowed\tProd\tChatGPT\t200\t512\t1024\tGET\tMozilla/5.0\n"
        # Zu wenige Felder
        "23-Jun-2024 10:00:02\talice@acme.corp\t10.0.1.1\thttps://chat.openai.com/\tAllowed\n"
        # Kommentar
        "# comment line should be ignored\n"
        # Leerzeile
        "\n"
        # Kein Host in URL
        "23-Jun-2024 10:00:03\talice@acme.corp\t10.0.1.1\t-\tAllowed\tProd\tUnknown\t200\t1\t1\tGET\t-\n"
        # Fehlender Client
        "23-Jun-2024 10:00:04\talice@acme.corp\t-\thttps://chat.openai.com/\tAllowed\tProd\tChatGPT\t200\t1\t1\tGET\t-\n"
    )
    path = tmp_path / "broken.log"
    path.write_text(content, encoding="utf-8")

    df = parse_zscaler_log(path, pseudonymizer=pseudonymizer)
    assert len(df) == 1
    assert df.iloc[0]["domain"] == "chat.openai.com"


def test_bytes_edge_cases(tmp_path, pseudonymizer):
    content = (
        # Upload=0, Download=0
        "23-Jun-2024 10:00:00\talice\t10.0.1.1\thttps://a.example/\tAllowed\tProd\tX\t200\t0\t0\tGET\tx\n"
        # Upload='-', Download fehlend via '-'
        "23-Jun-2024 10:00:01\talice\t10.0.1.1\thttps://b.example/\tAllowed\tProd\tX\t200\t-\t-\tPOST\tx\n"
        # Sehr grosser Upload (Doc-Upload-Simulation)
        "23-Jun-2024 10:00:02\talice\t10.0.1.1\thttps://c.example/\tAllowed\tProd\tX\t200\t10485760\t1024\tPOST\tx\n"
        # Ungültige Zahl
        "23-Jun-2024 10:00:03\talice\t10.0.1.1\thttps://d.example/\tAllowed\tProd\tX\t200\tfoo\tbar\tGET\tx\n"
    )
    path = tmp_path / "bytes.log"
    path.write_text(content, encoding="utf-8")

    df = parse_zscaler_log(path, pseudonymizer=pseudonymizer)
    assert len(df) == 4

    row_zero = df.iloc[0]
    assert row_zero["bytes_uploaded"] == 0 and row_zero["bytes_downloaded"] == 0

    row_dash = df.iloc[1]
    assert pd.isna(row_dash["bytes_uploaded"])
    assert pd.isna(row_dash["bytes_downloaded"])

    row_big = df.iloc[2]
    assert row_big["bytes_uploaded"] == 10_485_760

    row_bad = df.iloc[3]
    assert pd.isna(row_bad["bytes_uploaded"])
    assert pd.isna(row_bad["bytes_downloaded"])


def test_domain_normalized_lowercase_no_trailing_dot(tmp_path, pseudonymizer):
    content = (
        "23-Jun-2024 10:00:00\talice\t10.0.1.1\thttps://CHAT.OpenAI.COM./v1\tAllowed\tProd\tX\t200\t1\t1\tGET\tx\n"
    )
    path = tmp_path / "case.log"
    path.write_text(content, encoding="utf-8")
    df = parse_zscaler_log(path, pseudonymizer=pseudonymizer)
    assert df.iloc[0]["domain"] == "chat.openai.com"
    assert df.iloc[0]["url_path"] == "/v1"


def test_zscaler_parser_contract_via_class(pseudonymizer):
    parser = ZscalerParser(pseudonymizer=pseudonymizer)
    df = parser.parse(FIXTURE)
    # _finalize hat sortiert + validiert
    assert df["timestamp"].is_monotonic_increasing
    parser.validate_schema(df, strict=True)


def test_default_fields_cover_nss_standard():
    # Nur Mengen-Equality — Reihenfolge ist Deployment-spezifisch konfigurierbar
    assert set(DEFAULT_FIELDS) == {
        "datetime", "user", "clientIP", "url", "action",
        "urlcategory", "app", "respcode", "reqsize", "respsize",
        "method", "useragent",
    }


def test_url_path_truncated_to_first_segment(tmp_path, pseudonymizer):
    # DSGVO Art. 25: volle Pfade können Chat-Titel / Workspace-Namen leaken
    content = (
        "23-Jun-2024 10:00:00\talice\t10.0.1.1\thttps://chat.openai.com/g/g-BhDPQhWuS/cybersecurity-mentor\tAllowed\tProd\tChatGPT\t200\t1\t1\tGET\tx\n"
        "23-Jun-2024 10:00:01\talice\t10.0.1.1\thttps://notion.so/workspace/AI-Notes\tAllowed\tProd\tNotion\t200\t1\t1\tGET\tx\n"
        "23-Jun-2024 10:00:02\talice\t10.0.1.1\thttps://platform.openai.com/api-keys?token=secret\tAllowed\tDev\tChatGPT\t200\t1\t1\tGET\tx\n"
        "23-Jun-2024 10:00:03\talice\t10.0.1.1\thttps://example.com/\tAllowed\tProd\tX\t200\t1\t1\tGET\tx\n"
        "23-Jun-2024 10:00:04\talice\t10.0.1.1\thttps://example.com\tAllowed\tProd\tX\t200\t1\t1\tGET\tx\n"
    )
    path = tmp_path / "paths.log"
    path.write_text(content, encoding="utf-8")
    df = parse_zscaler_log(path, pseudonymizer=pseudonymizer)
    assert df.iloc[0]["url_path"] == "/g"
    assert df.iloc[1]["url_path"] == "/workspace"
    assert df.iloc[2]["url_path"] == "/api-keys"  # Query-String verworfen
    assert df.iloc[3]["url_path"] == "/"
    assert df.iloc[4]["url_path"] is None or df.iloc[4]["url_path"] == ""


def test_fields_validation_rejects_missing_required():
    with pytest.raises(ValueError, match="benötigt mindestens"):
        parse_zscaler_log(
            FIXTURE,
            pseudonymizer=Pseudonymizer(key=_PSEUDO_KEY),
            fields=("datetime", "user", "url", "action"),  # clientIP fehlt
        )


def test_empty_file_returns_empty_df(tmp_path, pseudonymizer):
    path = tmp_path / "empty.log"
    path.write_text("", encoding="utf-8")
    df = parse_zscaler_log(path, pseudonymizer=pseudonymizer)
    assert df.empty
    # dtype-Konsistenz für leeres DF
    assert df["bytes_uploaded"].dtype == "Int64"
