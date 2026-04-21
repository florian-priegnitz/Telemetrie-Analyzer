"""Parametrisierte Contract-Tests für BaseParser-konforme Parser.

Jeder konkrete Parser (PiholeParser, SquidParser, ...) muss diese Tests
passieren, damit Downstream-Konsumenten (Detection Engine, Behavior
Analytics, UI) verlässlich mit dem DataFrame arbeiten können.
"""

import re

import pandas as pd
import pytest

from src.parsers.aws_vpc_flow import VPCFlowLogsParser
from src.parsers.base import BaseParser
from src.parsers.cloudflare_gateway import CloudflareGatewayParser
from src.parsers.entra_id import EntraIDSignInParser
from src.parsers.fortinet import FortiGateWebfilterParser
from src.parsers.netskope import NetskopeCASBParser
from src.parsers.paloalto import PanOSUrlParser
from src.parsers.pihole import PiholeParser
from src.parsers.squid import SquidParser
from src.parsers.umbrella import UmbrellaDNSParser
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

# PAN-OS Mini-Sample: 2 valide url-Zeilen (45 Felder, Positionen laut DEFAULT_FIELDS)
_PALOALTO_SAMPLE = (
    "1,2024/06/23 08:15:32,SERIAL,THREAT,url,0,2024/06/23 08:15:32,10.0.1.42,203.0.113.1,0.0.0.0,0.0.0.0,allow-ai,alice@acme.corp,,web-browsing,vsys1,trust,untrust,eth1/1,eth1/2,0,,1,1,54321,443,0,0,0x00,ssl,alert,chat.openai.com/,,Computers-and-Internet,informational,c2s,1,0x00,DE,US,,,,,Mozilla/5.0 Chrome/124\n"
    "1,2024/06/23 08:15:40,SERIAL,THREAT,url,0,2024/06/23 08:15:40,10.0.1.50,203.0.113.2,0.0.0.0,0.0.0.0,allow-ai,bob@acme.corp,,web-browsing,vsys1,trust,untrust,eth1/1,eth1/2,0,,2,1,41233,443,0,0,0x00,ssl,alert,claude.ai/chats,,Computers-and-Internet,informational,c2s,2,0x00,DE,US,,,,,Mozilla/5.0 Firefox/125\n"
)

# Netskope CASB Mini-Sample: 2 JSON-NDJSON application events
_NETSKOPE_SAMPLE = (
    '{"_insertion_epoch_timestamp":1719131732,"user":"alice@acme.com","src_ip":"10.0.1.42","hostname":"chat.openai.com","app":"OpenAI ChatGPT","appcategory":"Artificial Intelligence","activity":"Prompt","action":"allow","method":"POST","uri_path":"/backend-api/conversation","bytes_uploaded":2048,"bytes_downloaded":10240}\n'
    '{"_insertion_epoch_timestamp":1719131800,"user":"bob@acme.com","src_ip":"10.0.1.50","hostname":"claude.ai","app":"Anthropic Claude","appcategory":"Artificial Intelligence","activity":"Login","action":"allow","method":"GET","uri_path":"/chats","bytes_uploaded":512,"bytes_downloaded":4096}\n'
)

# Cloudflare Gateway Mini-Sample: 1 DNS + 1 HTTP NDJSON-Event
_CLOUDFLARE_SAMPLE = (
    '{"Datetime":"2024-06-23T08:15:32Z","Email":"alice@acme.com","SrcIP":"10.0.1.42","QueryName":"chat.openai.com","QueryType":"A","QueryCategoryNames":["Generative AI"],"ResolverDecision":"allowed"}\n'
    '{"Datetime":"2024-06-23T08:15:40Z","Email":"bob@acme.com","SrcIP":"10.0.1.50","URL":"https://claude.ai/chats","HTTPMethod":"GET","HTTPStatusCode":200,"UploadBytes":512,"DownloadBytes":4096,"CategoryNames":["Generative AI"],"Action":"allow","UserAgent":"Mozilla/5.0"}\n'
)

# Entra ID Sign-In Mini-Sample: 2 JSONL-Events
_ENTRA_SAMPLE = (
    '{"TimeGenerated":"2024-06-23T08:15:32.000Z","UserPrincipalName":"alice@acme.onmicrosoft.com","UserId":"u1","AppDisplayName":"Microsoft 365 Copilot","AppId":"app1","IPAddress":"203.0.113.42","Status":{"errorCode":0},"ConditionalAccessStatus":"success","AuthenticationProtocol":"oAuth2"}\n'
    '{"TimeGenerated":"2024-06-23T08:16:02.100Z","UserPrincipalName":"bob@acme.onmicrosoft.com","UserId":"u2","AppDisplayName":"ChatGPT Enterprise","AppId":"app2","IPAddress":"203.0.113.50","Status":{"errorCode":0},"ConditionalAccessStatus":"success","AuthenticationProtocol":"oAuth2"}\n'
)

# AWS VPC Flow Logs Mini-Sample: 2 valide v2-Zeilen (whitespace-separated, kein Header)
_AWS_VPC_SAMPLE = (
    "2 123456789010 eni-abc123def 10.0.1.42 52.85.132.1 51234 443 6 5 1024 "
    "1719131732 1719131792 ACCEPT OK\n"
    "2 123456789010 eni-abc123def 10.0.1.50 99.83.157.10 52100 443 6 8 2048 "
    "1719131802 1719131862 ACCEPT OK\n"
)

# Fortinet Mini-Sample: 2 valide webfilter-Zeilen (key=value)
_FORTINET_SAMPLE = (
    'date=2024-06-23 time=08:15:32 logid="0316013056" type="utm" subtype="webfilter" '
    'eventtype="ftgd_allow" level="notice" vd="root" policyid=1 user="alice@acme.corp" '
    'srcip=10.0.1.42 srcport=54321 dstip=203.0.113.50 dstport=443 service="HTTPS" '
    'hostname="chat.openai.com" action="passthrough" url="/" sentbyte=412 rcvdbyte=2048 '
    'method="domain" catdesc="Business Services"\n'
    'date=2024-06-23 time=08:15:40 logid="0316013056" type="utm" subtype="webfilter" '
    'eventtype="ftgd_allow" level="notice" vd="root" policyid=1 user="bob@acme.corp" '
    'srcip=10.0.1.50 srcport=54322 dstip=203.0.113.51 dstport=443 service="HTTPS" '
    'hostname="claude.ai" action="passthrough" url="/chats" sentbyte=520 rcvdbyte=4096 '
    'method="get" catdesc="Business Services"\n'
)

# Umbrella Mini-Sample: Header + 2 valide v10-Zeilen (alle Felder gequotet)
_UMBRELLA_SAMPLE = (
    '"timestamp","most_granular_identity","identities","internal_ip","external_ip","action","query_type","response_code","domain","categories","most_granular_identity_type","identity_types","blocked_categories","rule_id","destination_countries","organization_id"\n'
    '"2024-06-23 08:15:32","alice@acme.corp","alice@acme.corp,HQ","10.0.1.42","203.0.113.1","Allowed","1 (A)","NOERROR","chat.openai.com.","Generative AI","AD User","AD User,Network","","101","US","9999"\n'
    '"2024-06-23 08:15:40","bob@acme.corp","bob@acme.corp,HQ","10.0.1.50","203.0.113.1","Allowed","1 (A)","NOERROR","claude.ai.","Generative AI","AD User","AD User,Network","","101","US","9999"\n'
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


@pytest.fixture
def paloalto_path(tmp_path):
    path = tmp_path / "paloalto.log"
    path.write_text(_PALOALTO_SAMPLE, encoding="utf-8")
    return path


@pytest.fixture
def umbrella_path(tmp_path):
    path = tmp_path / "umbrella.csv"
    path.write_text(_UMBRELLA_SAMPLE, encoding="utf-8")
    return path


@pytest.fixture
def fortinet_path(tmp_path):
    path = tmp_path / "fortinet.log"
    path.write_text(_FORTINET_SAMPLE, encoding="utf-8")
    return path


@pytest.fixture
def aws_vpc_path(tmp_path):
    path = tmp_path / "aws_vpc.log"
    path.write_text(_AWS_VPC_SAMPLE, encoding="utf-8")
    return path


@pytest.fixture
def entra_path(tmp_path):
    path = tmp_path / "entra.jsonl"
    path.write_text(_ENTRA_SAMPLE, encoding="utf-8")
    return path


@pytest.fixture
def cloudflare_path(tmp_path):
    path = tmp_path / "cloudflare.jsonl"
    path.write_text(_CLOUDFLARE_SAMPLE, encoding="utf-8")
    return path


@pytest.fixture
def netskope_path(tmp_path):
    path = tmp_path / "netskope.jsonl"
    path.write_text(_NETSKOPE_SAMPLE, encoding="utf-8")
    return path


@pytest.fixture(
    params=[
        ("pihole", PiholeParser, "pihole_path"),
        ("squid", SquidParser, "squid_path"),
        ("zscaler", ZscalerParser, "zscaler_path"),
        ("paloalto", PanOSUrlParser, "paloalto_path"),
        ("umbrella", UmbrellaDNSParser, "umbrella_path"),
        ("fortinet", FortiGateWebfilterParser, "fortinet_path"),
        ("aws_vpc", VPCFlowLogsParser, "aws_vpc_path"),
        ("entra_id", EntraIDSignInParser, "entra_path"),
        ("cloudflare", CloudflareGatewayParser, "cloudflare_path"),
        ("netskope", NetskopeCASBParser, "netskope_path"),
    ],
    ids=["pihole", "squid", "zscaler", "paloalto", "umbrella", "fortinet", "aws_vpc", "entra_id", "cloudflare", "netskope"],
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
