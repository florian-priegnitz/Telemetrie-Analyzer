"""Tests für den Squid Proxy Access Log Parser."""

import tempfile
from pathlib import Path

import pandas as pd

from src.parsers.squid import parse_squid_log
from src.privacy.pseudonymizer import Pseudonymizer

NATIVE_SAMPLE = (
    "1709971200.123 234 192.168.1.42 TCP_MISS/200 1547 POST "
    "https://api.openai.com/v1/chat - HIER_DIRECT/1.2.3.4 application/json\n"
    "1709971205.456 89 192.168.1.10 TCP_HIT/200 612 GET "
    "https://www.google.com/ - HIER_DIRECT/8.8.8.8 text/html\n"
    "1709971210.789 12 192.168.1.42 TCP_TUNNEL/200 8421 CONNECT "
    "claude.ai:443 - HIER_DIRECT/1.2.3.5 -\n"
)

COMMON_SAMPLE = (
    '192.168.1.42 - - [09/Mar/2024:08:15:32 +0000] '
    '"POST https://api.openai.com/v1/chat HTTP/1.1" 200 1547\n'
    '192.168.1.10 - - [09/Mar/2024:08:16:00 +0000] '
    '"GET https://www.google.com/ HTTP/1.1" 200 612\n'
)


def _write_temp_log(content: str) -> Path:
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False, encoding="utf-8")
    f.write(content)
    f.close()
    return Path(f.name)


def test_parse_native_basic_line():
    path = _write_temp_log(NATIVE_SAMPLE)
    pseudo = Pseudonymizer(key=b"test-key")
    df = parse_squid_log(path, pseudonymizer=pseudo)

    assert len(df) == 3
    assert "timestamp" in df.columns
    assert "bytes_uploaded" in df.columns
    assert "domain" in df.columns
    assert df.iloc[0]["method"] == "POST"
    assert df.iloc[0]["status_code"] == 200


def test_parse_common_format_line():
    path = _write_temp_log(COMMON_SAMPLE)
    df = parse_squid_log(path, pseudonymizer=Pseudonymizer(key=b"k"), format="common")
    assert len(df) == 2
    assert df.iloc[0]["bytes_uploaded"] == 1547


def test_format_auto_detection_native():
    path = _write_temp_log(NATIVE_SAMPLE)
    df = parse_squid_log(path, pseudonymizer=Pseudonymizer(key=b"k"), format="auto")
    assert len(df) == 3


def test_format_auto_detection_common():
    path = _write_temp_log(COMMON_SAMPLE)
    df = parse_squid_log(path, pseudonymizer=Pseudonymizer(key=b"k"), format="auto")
    assert len(df) == 2


def test_domain_extracted_from_url():
    path = _write_temp_log(NATIVE_SAMPLE)
    df = parse_squid_log(path, pseudonymizer=Pseudonymizer(key=b"k"))
    assert "api.openai.com" in df["domain"].values
    assert "www.google.com" in df["domain"].values


def test_domains_lowercase_and_no_trailing_dot():
    sample = (
        "1709971200.000 100 10.0.0.1 TCP_MISS/200 500 GET "
        "https://API.OpenAI.COM./v1/x - HIER_DIRECT/1.1.1.1 text/html\n"
    )
    path = _write_temp_log(sample)
    df = parse_squid_log(path, pseudonymizer=Pseudonymizer(key=b"k"))
    assert df.iloc[0]["domain"] == "api.openai.com"


def test_ips_pseudonymized():
    path = _write_temp_log(NATIVE_SAMPLE)
    pseudo = Pseudonymizer(key=b"test-key")
    df = parse_squid_log(path, pseudonymizer=pseudo)
    for client in df["client"]:
        assert client.startswith("ip_")
        assert "192.168" not in client


def test_same_ip_same_pseudonym():
    path = _write_temp_log(NATIVE_SAMPLE)
    pseudo = Pseudonymizer(key=b"test-key")
    df = parse_squid_log(path, pseudonymizer=pseudo)
    # 192.168.1.42 erscheint zweimal (Zeile 1 und 3)
    rows_42_origin = df[df["domain"].isin(["api.openai.com", "claude.ai"])]
    assert rows_42_origin["client"].nunique() == 1


def test_bytes_uploaded_present_and_int64():
    path = _write_temp_log(NATIVE_SAMPLE)
    df = parse_squid_log(path, pseudonymizer=Pseudonymizer(key=b"k"))
    assert str(df["bytes_uploaded"].dtype) == "Int64"
    assert df.iloc[0]["bytes_uploaded"] == 1547


def test_connect_tunnel_method():
    path = _write_temp_log(NATIVE_SAMPLE)
    df = parse_squid_log(path, pseudonymizer=Pseudonymizer(key=b"k"))
    connect_rows = df[df["method"] == "CONNECT"]
    assert len(connect_rows) == 1
    assert connect_rows.iloc[0]["domain"] == "claude.ai"


def test_invalid_lines_skipped():
    sample = NATIVE_SAMPLE + "this is garbage\n\nmore garbage line without numbers\n"
    path = _write_temp_log(sample)
    df = parse_squid_log(path, pseudonymizer=Pseudonymizer(key=b"k"))
    assert len(df) == 3  # nur die 3 validen aus NATIVE_SAMPLE


def test_empty_log():
    path = _write_temp_log("")
    df = parse_squid_log(path, pseudonymizer=Pseudonymizer(key=b"k"))
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
    assert "bytes_uploaded" in df.columns


def test_source_type_squid():
    path = _write_temp_log(NATIVE_SAMPLE)
    df = parse_squid_log(path, pseudonymizer=Pseudonymizer(key=b"k"))
    assert (df["source_type"] == "squid").all()
