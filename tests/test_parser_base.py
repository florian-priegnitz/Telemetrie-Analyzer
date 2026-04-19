"""Parametrisierte Contract-Tests für BaseParser-konforme Parser.

Jeder konkrete Parser (PiholeParser, SquidParser, ...) muss diese Tests
passieren, damit Downstream-Konsumenten (Detection Engine, Behavior
Analytics, UI) verlässlich mit dem DataFrame arbeiten können.
"""

import re

import pandas as pd
import pytest

from src.parsers.base import BaseParser
from src.parsers.pihole import PiholeParser
from src.parsers.squid import SquidParser
from src.parsers.zscaler import ZscalerParser
from src.privacy.pseudonymizer import Pseudonymizer


_PIHOLE_SAMPLE = (
    "Mar  9 08:15:32 dnsmasq[1234]: query[A] chat.openai.com from 192.168.1.42\n"
    "Mar  9 08:15:33 dnsmasq[1234]: query[AAAA] chat.openai.com from 192.168.1.42\n"
    "Mar  9 08:15:40 dnsmasq[1234]: query[A] api.openai.com from 192.168.1.50\n"
)

_SQUID_SAMPLE = (
    "1709971200.123 234 192.168.1.42 TCP_MISS/200 1547 POST "
    "https://api.openai.com/v1/chat - HIER_DIRECT/1.2.3.4 application/json\n"
    "1709971205.456 89 192.168.1.50 TCP_MISS/200 512 GET "
    "https://chat.openai.com/ - HIER_DIRECT/1.2.3.4 text/html\n"
)

_ZSCALER_SAMPLE = (
    "23-Jun-2024 08:15:32\talice@acme.corp\t10.0.1.42\thttps://chat.openai.com/\tAllowed\tProductivity\tChatGPT\t200\t412\t2048\tGET\tMozilla/5.0\n"
    "23-Jun-2024 08:15:40\tbob@acme.corp\t10.0.1.50\thttps://claude.ai/chats\tAllowed\tProductivity\tClaude\t200\t520\t4096\tGET\tMozilla/5.0\n"
)


@pytest.fixture
def pseudonymizer():
    return Pseudonymizer(key=b"contract-test-key")


@pytest.fixture
def pihole_path(tmp_path):
    path = tmp_path / "pihole.log"
    path.write_text(_PIHOLE_SAMPLE, encoding="utf-8")
    return path


@pytest.fixture
def squid_path(tmp_path):
    path = tmp_path / "squid.log"
    path.write_text(_SQUID_SAMPLE, encoding="utf-8")
    return path


@pytest.fixture
def zscaler_path(tmp_path):
    path = tmp_path / "zscaler.log"
    path.write_text(_ZSCALER_SAMPLE, encoding="utf-8")
    return path


@pytest.fixture(
    params=[
        ("pihole", PiholeParser, "pihole_path"),
        ("squid", SquidParser, "squid_path"),
        ("zscaler", ZscalerParser, "zscaler_path"),
    ],
    ids=["pihole", "squid", "zscaler"],
)
def parser_and_df(request, pseudonymizer):
    _, parser_cls, path_fixture = request.param
    path = request.getfixturevalue(path_fixture)
    parser = parser_cls(pseudonymizer)
    df = parser.parse(path)
    return parser, df


def test_required_columns_present(parser_and_df):
    _, df = parser_and_df
    assert BaseParser.REQUIRED_COLUMNS.issubset(set(df.columns)), (
        f"REQUIRED_COLUMNS fehlen: {BaseParser.REQUIRED_COLUMNS - set(df.columns)}"
    )


def test_timestamp_is_datetime64_sorted(parser_and_df):
    _, df = parser_and_df
    assert not df.empty, "Sample sollte Records liefern"
    assert df["timestamp"].dtype == "datetime64[ns]"
    assert df["timestamp"].is_monotonic_increasing


_CLIENT_PATTERN = re.compile(r"^(ip|user)_[0-9a-f]+$")


def test_client_pseudonymized(parser_and_df):
    _, df = parser_and_df
    for client in df["client"]:
        assert _CLIENT_PATTERN.match(str(client)), (
            f"Client '{client}' folgt nicht dem Pseudonym-Muster"
        )
        # Defensive: keine klartext-IPs
        assert not re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}", str(client))


def test_domain_normalized(parser_and_df):
    _, df = parser_and_df
    for domain in df["domain"].dropna():
        assert domain == domain.lower()
        assert not domain.endswith(".")


def test_validate_schema_rejects_missing():
    parser = PiholeParser()
    bad_df = pd.DataFrame({"foo": [1, 2]})
    with pytest.raises(ValueError, match="Fehlende Pflicht-Spalten"):
        parser.validate_schema(bad_df)


def test_validate_schema_strict_rejects_extra():
    parser = PiholeParser()
    df = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                ["2026-01-01 10:00:00", "2026-01-01 10:05:00"]
            ),
            "client": ["ip_abc12345", "ip_abc12345"],
            "domain": ["example.com", "example.com"],
            "rogue_column": ["x", "y"],
        }
    )
    parser.validate_schema(df, strict=False)
    with pytest.raises(ValueError, match="Unerwartete Spalten"):
        parser.validate_schema(df, strict=True)


def test_validate_schema_rejects_unsorted():
    parser = PiholeParser()
    df = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                ["2026-01-01 10:05:00", "2026-01-01 10:00:00"]
            ),
            "client": ["ip_abc", "ip_abc"],
            "domain": ["example.com", "example.com"],
        }
    )
    with pytest.raises(ValueError, match="nicht aufsteigend sortiert"):
        parser.validate_schema(df)


def test_validate_schema_passes_on_empty():
    parser = PiholeParser()
    parser.validate_schema(pd.DataFrame())  # darf nicht werfen


def test_parse_empty_file_passes_validation(tmp_path, pseudonymizer):
    empty_log = tmp_path / "empty.log"
    empty_log.write_text("", encoding="utf-8")
    pihole = PiholeParser(pseudonymizer)
    df_pihole = pihole.parse(empty_log)
    assert df_pihole.empty  # keine Exception

    squid = SquidParser(pseudonymizer)
    df_squid = squid.parse(empty_log)
    assert df_squid.empty
