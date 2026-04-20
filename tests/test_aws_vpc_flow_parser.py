"""Tests für den AWS VPC Flow Logs Parser (E3-5 / Issue #30)."""

import re
from pathlib import Path

import pandas as pd
import pytest

from src.parsers.aws_vpc_flow import (
    V2_FIELDS,
    VPCFlowLogsParser,
    _detect_header,
    parse_aws_vpc_flow_log,
)
from src.privacy.pseudonymizer import Pseudonymizer

V2_FIXTURE = Path(__file__).parent.parent / "testdata" / "aws_vpc_v2_sample.log"
V5_FIXTURE = Path(__file__).parent.parent / "testdata" / "aws_vpc_v5_sample.log"
_KEY = b"aws-vpc-test-key"


@pytest.fixture
def pseudonymizer():
    return Pseudonymizer(key=_KEY)


def test_v2_default_format_parses(pseudonymizer):
    df = parse_aws_vpc_flow_log(V2_FIXTURE, pseudonymizer=pseudonymizer)
    # 22 valide Zeilen (NODATA-Zeile wird übersprungen)
    assert len(df) == 22
    assert df["timestamp"].dtype == "datetime64[ns]"
    assert (df["source_type"] == "aws_vpc_flow").all()
    # v2 hat keinen User-Kontext
    assert df["user"].isna().all()
    # domain fällt auf IP-String zurück (keine pkt-dst-aws-service in v2)
    assert "52.85.132.1" in df["domain"].values


def test_v5_header_auto_detection(pseudonymizer):
    df = parse_aws_vpc_flow_log(V5_FIXTURE, pseudonymizer=pseudonymizer)
    # 12 Zeilen (alle OK-Status)
    assert len(df) == 12
    # Shadow-AI-Highlight: AWS-Services als domain, nicht IP
    assert "bedrock" in df["domain"].values  # lowercased
    assert "sagemaker" in df["domain"].values


def test_v5_pkt_dst_aws_service_preferred_over_ip(pseudonymizer):
    df = parse_aws_vpc_flow_log(V5_FIXTURE, pseudonymizer=pseudonymizer)
    # BEDROCK-Zeilen haben domain=bedrock, nicht die 10.0.0.5 dest-IP
    bedrock = df[df["domain"] == "bedrock"]
    assert not bedrock.empty
    # Die service-lose Zeile fällt auf dstaddr zurück
    assert "52.85.132.1" in df["domain"].values


def test_nodata_status_skipped(pseudonymizer):
    df = parse_aws_vpc_flow_log(V2_FIXTURE, pseudonymizer=pseudonymizer)
    # NODATA wurde übersprungen → 22 statt 23
    assert len(df) == 22


def test_client_pseudonymized(pseudonymizer):
    df = parse_aws_vpc_flow_log(V2_FIXTURE, pseudonymizer=pseudonymizer)
    ip_pattern = re.compile(r"^ip_[0-9a-f]+$")
    for client in df["client"]:
        assert ip_pattern.match(client)
        assert not re.search(r"10\.\d{1,3}", client)


def test_action_captured(pseudonymizer):
    df = parse_aws_vpc_flow_log(V2_FIXTURE, pseudonymizer=pseudonymizer)
    assert "ACCEPT" in df["action"].values
    assert "REJECT" in df["action"].values


def test_bytes_uploaded_extracted(pseudonymizer):
    df = parse_aws_vpc_flow_log(V2_FIXTURE, pseudonymizer=pseudonymizer)
    assert df["bytes_uploaded"].dtype == "Int64"
    # großer Upload ist in fixture (890512)
    assert (df["bytes_uploaded"] > 100_000).any()


def test_timestamp_from_unix_epoch(pseudonymizer):
    df = parse_aws_vpc_flow_log(V2_FIXTURE, pseudonymizer=pseudonymizer)
    # 1719131732 → 2024-06-23 08:35:32 UTC
    assert df["timestamp"].min().strftime("%Y-%m-%d") == "2024-06-23"


def test_detect_header_unit():
    assert _detect_header("version account-id interface-id srcaddr dstaddr")
    assert not _detect_header("2 123456789010 eni-abc123 10.0.1.42")
    assert not _detect_header("")


def test_missing_required_fields_rejected(tmp_path, pseudonymizer):
    # Header ohne srcaddr → ValueError
    f = tmp_path / "bad_header.log"
    f.write_text("version account-id interface-id dstaddr start end action log-status\n", encoding="utf-8")
    with pytest.raises(ValueError, match="benötigen mindestens"):
        parse_aws_vpc_flow_log(f, pseudonymizer=pseudonymizer)


def test_malformed_lines_skipped(tmp_path, pseudonymizer):
    content = (
        # Valide v2-Zeile
        "2 123456789010 eni-abc123 10.0.1.1 52.85.132.1 51234 443 6 5 1024 1719131732 1719131792 ACCEPT OK\n"
        # Kaputter Timestamp (nicht-numerisch)
        "2 123456789010 eni-abc123 10.0.1.2 52.85.132.1 51234 443 6 5 1024 NOTANUMBER 1719131792 ACCEPT OK\n"
        # Zu wenige Felder
        "2 123456789010 eni-abc123 10.0.1.3\n"
        # Kommentar
        "# comment\n"
        # NODATA
        "2 123456789010 eni-abc123 - - - - - - - 1719131792 1719131852 - NODATA\n"
        # SKIPDATA
        "2 123456789010 eni-abc123 - - - - - - - 1719131852 1719131912 - SKIPDATA\n"
    )
    f = tmp_path / "broken.log"
    f.write_text(content, encoding="utf-8")
    df = parse_aws_vpc_flow_log(f, pseudonymizer=pseudonymizer)
    assert len(df) == 1
    assert df.iloc[0]["domain"] == "52.85.132.1"


def test_empty_file_returns_empty_df(tmp_path, pseudonymizer):
    f = tmp_path / "empty.log"
    f.write_text("", encoding="utf-8")
    df = parse_aws_vpc_flow_log(f, pseudonymizer=pseudonymizer)
    assert df.empty
    assert df["bytes_uploaded"].dtype == "Int64"


def test_custom_fields_override(tmp_path, pseudonymizer):
    # Custom reduced field-order (kein Header in Datei)
    custom_fields = (
        "version", "account-id", "interface-id",
        "srcaddr", "dstaddr", "srcport", "dstport",
        "protocol", "packets", "bytes",
        "start", "end", "action", "log-status",
    )
    f = tmp_path / "custom.log"
    f.write_text(
        "2 123 eni-1 10.0.1.1 52.85.132.1 51234 443 6 5 1024 1719131732 1719131792 ACCEPT OK\n",
        encoding="utf-8",
    )
    df = parse_aws_vpc_flow_log(f, pseudonymizer=pseudonymizer, fields=custom_fields)
    assert len(df) == 1


def test_parser_contract_via_class(pseudonymizer):
    parser = VPCFlowLogsParser(pseudonymizer=pseudonymizer)
    df = parser.parse(V2_FIXTURE)
    assert df["timestamp"].is_monotonic_increasing
    parser.validate_schema(df, strict=True)


def test_v2_fields_constant_has_14_fields():
    assert len(V2_FIELDS) == 14


def test_domain_lowercased(pseudonymizer):
    df = parse_aws_vpc_flow_log(V5_FIXTURE, pseudonymizer=pseudonymizer)
    for domain in df["domain"]:
        assert domain == domain.lower()
