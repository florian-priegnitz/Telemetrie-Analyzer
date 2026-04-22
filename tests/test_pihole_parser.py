"""Tests für den Pi-hole DNS Log Parser."""

import tempfile
from pathlib import Path

import pandas as pd

from src.parsers.pihole import parse_pihole_ftl_csv, parse_pihole_log
from src.privacy.pseudonymizer import Pseudonymizer

SAMPLE_LOG = """\
Mar  9 08:15:32 dnsmasq[1234]: query[A] chat.openai.com from 192.168.1.42
Mar  9 08:15:33 dnsmasq[1234]: query[AAAA] chat.openai.com from 192.168.1.42
Mar  9 08:16:01 dnsmasq[1234]: query[A] api.anthropic.com from 192.168.1.10
Mar  9 08:16:05 dnsmasq[1234]: forwarded chat.openai.com to 1.1.1.1
Mar  9 08:17:00 dnsmasq[1234]: query[A] www.google.com from 192.168.1.42
Mar  9 09:00:00 dnsmasq[1234]: query[A] claude.ai from 192.168.1.55
"""


def _write_temp_log(content: str) -> Path:
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False, encoding="utf-8")
    f.write(content)
    f.close()
    return Path(f.name)


def test_parse_basic_log():
    path = _write_temp_log(SAMPLE_LOG)
    pseudo = Pseudonymizer(key=b"test-key")
    df = parse_pihole_log(path, pseudonymizer=pseudo, year=2026)

    # Nur query-Zeilen werden geparst, nicht "forwarded"
    assert len(df) == 5
    assert list(df.columns) == [
        "timestamp", "query_type", "domain", "client", "source_file", "source_type",
    ]
    assert (df["source_type"] == "pihole").all()


def test_domains_are_lowercase():
    path = _write_temp_log("Mar  1 10:00:00 dnsmasq[1]: query[A] Chat.OpenAI.COM from 10.0.0.1\n")
    df = parse_pihole_log(path, year=2026)
    assert df.iloc[0]["domain"] == "chat.openai.com"


def test_ips_are_pseudonymized():
    path = _write_temp_log(SAMPLE_LOG)
    pseudo = Pseudonymizer(key=b"test-key")
    df = parse_pihole_log(path, pseudonymizer=pseudo, year=2026)

    # Keine echten IPs im Output
    for client in df["client"]:
        assert client.startswith("ip_")
        assert "192.168" not in client


def test_same_ip_same_pseudonym():
    path = _write_temp_log(SAMPLE_LOG)
    pseudo = Pseudonymizer(key=b"test-key")
    df = parse_pihole_log(path, pseudonymizer=pseudo, year=2026)

    # 192.168.1.42 kommt 3x vor → selbes Pseudonym
    client_42 = df[df["domain"].isin(["chat.openai.com", "www.google.com"])]["client"]
    assert client_42.nunique() == 1


def test_timestamp_parsing():
    path = _write_temp_log(SAMPLE_LOG)
    df = parse_pihole_log(path, year=2026)
    assert df["timestamp"].dtype == "datetime64[ns]"
    assert df.iloc[0]["timestamp"].month == 3
    assert df.iloc[0]["timestamp"].day == 9


def test_empty_log():
    path = _write_temp_log("")
    df = parse_pihole_log(path)
    assert len(df) == 0
    assert isinstance(df, pd.DataFrame)


def test_trailing_dot_removed():
    path = _write_temp_log("Mar  1 10:00:00 dnsmasq[1]: query[A] api.openai.com. from 10.0.0.1\n")
    df = parse_pihole_log(path, year=2026)
    assert df.iloc[0]["domain"] == "api.openai.com"


def test_ftl_csv_parser():
    csv_content = "timestamp,type,domain,client,status\n1709971200,A,chat.openai.com,192.168.1.5,2\n1709971260,AAAA,claude.ai,192.168.1.10,2\n"
    path = _write_temp_log(csv_content)
    path = path.rename(path.with_suffix(".csv"))
    pseudo = Pseudonymizer(key=b"csv-test")
    df = parse_pihole_ftl_csv(path, pseudonymizer=pseudo)

    assert len(df) == 2
    assert df.iloc[0]["client"].startswith("ip_")
    assert df["timestamp"].dtype == "datetime64[ns]"
