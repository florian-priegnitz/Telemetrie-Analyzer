"""Unit-Tests für das Detection-Shared-Module (src/parsers/detection.py).

Prüft, dass alle 12 Parser-Formate anhand der ersten Bytes eindeutig
erkannt werden — ohne den tatsächlichen Parse-Lauf. Ambiguität und
Unknown-Handling werden separat getestet.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.parsers.detection import (
    PARSER_LABELS,
    PARSER_METADATA,
    SUPPORTED_PARSERS,
    detect_format,
)

TESTDATA = Path(__file__).parent.parent / "testdata"


# ---------------------------------------------------------------------------
# Struktur-Invarianten
# ---------------------------------------------------------------------------
def test_supported_parsers_count_is_12():
    """Das Schema-Versprechen in den Docs: genau 12 Formate."""
    assert len(SUPPORTED_PARSERS) == 12


def test_all_parsers_have_labels():
    for key in SUPPORTED_PARSERS:
        assert key in PARSER_LABELS, f"Label fehlt für {key}"
        assert PARSER_LABELS[key], f"Label leer für {key}"


def test_all_parsers_have_metadata():
    for key in SUPPORTED_PARSERS:
        meta = PARSER_METADATA.get(key)
        assert meta is not None, f"Metadata fehlt für {key}"
        # Minimum-Keys
        for required_key in ("source", "file_type", "sample_file",
                             "field_mapping", "risk_signal"):
            assert required_key in meta, f"{key}: fehlt {required_key}"
        assert isinstance(meta["field_mapping"], dict)
        assert meta["field_mapping"], f"{key}: field_mapping ist leer"


# ---------------------------------------------------------------------------
# Detection — Happy-Path je Sample
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("sample_file,expected_parser", [
    ("pihole_sample.log", "pihole"),
    ("squid_sample.log", "squid"),
    ("aws_vpc_v2_sample.log", "aws_vpc_flow"),
    ("aws_vpc_v5_sample.log", "aws_vpc_flow"),
    ("cloudflare_gateway_sample.log", "cloudflare_gateway"),
    ("elastic_ecs_sample.log", "elastic_ecs"),
    ("entra_signin_sample.log", "entra_id"),
    ("fortinet_sample.log", "fortinet"),
    ("netskope_sample.log", "netskope"),
    ("paloalto_sample.log", "paloalto"),
    ("sysmon_sample.log", "sysmon"),
    ("umbrella_sample.log", "umbrella"),
    ("zscaler_sample.log", "zscaler"),
])
def test_detect_format_recognizes_all_samples(sample_file, expected_parser):
    path = TESTDATA / sample_file
    if not path.is_file():
        pytest.skip(f"{sample_file} nicht generiert")
    detected = detect_format(path.read_bytes())
    assert detected == expected_parser, (
        f"{sample_file}: erwartet {expected_parser}, bekam {detected}"
    )


# ---------------------------------------------------------------------------
# Edge-Cases
# ---------------------------------------------------------------------------
def test_empty_bytes_return_none():
    assert detect_format(b"") is None


def test_whitespace_only_returns_none():
    assert detect_format(b"   \n\t\n") is None


def test_unrelated_text_returns_none():
    assert detect_format(b"This is a generic text file\nnot a log\n") is None


def test_arbitrary_csv_without_markers_returns_none():
    """Irgendein CSV ohne AI-Log-Marker darf nicht als paloalto/umbrella erkannt werden."""
    sample = b"name,age,city\nAlice,30,Hamburg\nBob,25,Berlin\n"
    assert detect_format(sample) is None


def test_json_without_known_keys_returns_none():
    """Generisches JSON ohne Marker soll nicht auf ECS fallen (Breaking-Change)."""
    sample = b'{"hello": "world", "n": 1}\n'
    assert detect_format(sample) is None


# ---------------------------------------------------------------------------
# Mehrdeutigkeits-Tests — eindeutige Marker gewinnen
# ---------------------------------------------------------------------------
def test_sysmon_wins_over_ecs_when_queryname_present():
    sample = (b'{"EventID": 22, "UtcTime": "2026-01-01 00:00:00", '
              b'"QueryName": "a.example", "Computer": "H1"}\n')
    assert detect_format(sample) == "sysmon"


def test_cloudflare_wins_over_ecs_when_datetime_plus_srcip():
    sample = (b'{"Datetime": "2024-06-23T08:15:32Z", "SrcIP": "10.0.0.1", '
              b'"QueryName": "x.com"}\n')
    assert detect_format(sample) == "cloudflare_gateway"


def test_netskope_wins_via_insertion_epoch_timestamp():
    sample = b'{"_insertion_epoch_timestamp": 1719131732, "user": "a@b.c"}\n'
    assert detect_format(sample) == "netskope"
