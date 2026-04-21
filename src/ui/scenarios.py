"""Demo-Scenario-Registry für Ein-Klick-Start ohne manuellen File-Upload.

Jedes Scenario referenziert eine mitgelieferte Sample-Datei (entweder das
Unit-Test-Fixture ``testdata/*_sample.log`` oder das angereicherte
``testdata/demo/*_demo.log``) plus eine kurze Beschreibung für die UI.

Die Registry wird vom Upload-Widget und vom Empty-State-Onboarding
gelesen. Beim Klick auf einen Scenario-Button werden die File-Bytes
direkt in den Session-State geschrieben (so, als hätte der User
hochgeladen) — Format ist vor-gesetzt und Analyse startet mit dem
nächsten Reload.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

TESTDATA = Path(__file__).resolve().parent.parent.parent / "testdata"
DEMO_DIR = TESTDATA / "demo"


@dataclass(frozen=True)
class Scenario:
    key: str
    label: str                 # UI-Button-Label (kurz)
    description: str           # 1-Satz-Erklärung
    parser: str                # Key aus SUPPORTED_PARSERS
    file_path: Path            # Absoluter Pfad zur Sample-Datei
    expected_highlights: str   # Was der User in der Analyse sehen wird

    @property
    def exists(self) -> bool:
        return self.file_path.is_file()

    @property
    def size_kb(self) -> float:
        if not self.exists:
            return 0.0
        return self.file_path.stat().st_size / 1024


# Reihenfolge = UI-Darstellung. Die 4 angereicherten demo/*-Samples zuerst
# (sie zeigen Detection+Heatmap am klarsten), dann die 8 kompakten Original-
# Fixtures. Pi-hole-Sample (1000+ Events) ist der klare Demo-King.
SCENARIOS: tuple[Scenario, ...] = (
    Scenario(
        key="pihole",
        label="🔥 Pi-hole (größtes Sample, ~2800 Events)",
        description="DNS-Queries eines 7-Tage-Zeitraums — gemischter Business-Traffic plus Shadow-AI",
        parser="pihole",
        file_path=TESTDATA / "pihole_sample.log",
        expected_highlights="11 Findings über 9 AI-Services (ChatGPT, Claude, Copilot, Cursor, …), "
                            "volle Heatmap, Off-Hours-Pattern",
    ),
    Scenario(
        key="squid",
        label="Squid Proxy (~1700 Events)",
        description="HTTP-Proxy-Logs mit Upload-Volumen — Document-Upload-Detection greift",
        parser="squid",
        file_path=TESTDATA / "squid_sample.log",
        expected_highlights="Findings mit `has_document_upload=true` bei >500 KB POST",
    ),
    Scenario(
        key="netskope_demo",
        label="Netskope CASB — angereichert (100 Events)",
        description="Cloud-CASB mit Activity-Feld (Prompt/Upload File) — klassifiziert 1.550+ AI-Apps",
        parser="netskope",
        file_path=DEMO_DIR / "netskope_demo.log",
        expected_highlights="AI-Kategorie-Klassifikation, Upload-Activities markiert, "
                            "12 User-Pseudonyme in Heatmap",
    ),
    Scenario(
        key="sysmon_demo",
        label="Windows Sysmon — angereichert (80 Events)",
        description="Endpoint-DNS mit Prozess-Attribution — welches Executable query AI?",
        parser="sysmon",
        file_path=DEMO_DIR / "sysmon_demo.log",
        expected_highlights="Heatmap nach Workstation, Process-Names zeigen Cursor/Code/Browser",
    ),
    Scenario(
        key="elastic_ecs_demo",
        label="Elastic ECS — angereichert (80 Events)",
        description="Vendor-agnostisches Schema — DNS + HTTP gemischt, Upload-Bytes",
        parser="elastic_ecs",
        file_path=DEMO_DIR / "elastic_ecs_demo.log",
        expected_highlights="6 AI-Domains, gemischte Methods (GET/POST), ASN-Organisation für "
                            "AI-Hosts",
    ),
    Scenario(
        key="aws_vpc_v5_demo",
        label="AWS VPC Flow v5 — angereichert (60 Events)",
        description="Layer-4-Flows mit pkt-dst-aws-service — AWS-native AI (Bedrock, SageMaker)",
        parser="aws_vpc_flow",
        file_path=DEMO_DIR / "aws_vpc_v5_demo.log",
        expected_highlights="AI-Services BEDROCK/SAGEMAKER als `domain`, ohne Layer-7-Klartext",
    ),
    Scenario(
        key="zscaler",
        label="Zscaler ZIA (kompakt)",
        description="TSV Web-Proxy-Log mit URL-Category — AI-Apps als separate Kategorie",
        parser="zscaler",
        file_path=TESTDATA / "zscaler_sample.log",
        expected_highlights="URL-Category-Feld und Upload-Volumen bei POST-Requests",
    ),
    Scenario(
        key="paloalto",
        label="Palo Alto PAN-OS (kompakt)",
        description="URL-Filtering-CSV mit User-ID und Action (allow/block)",
        parser="paloalto",
        file_path=TESTDATA / "paloalto_sample.log",
        expected_highlights="User-ID-Integration, URL-Category-Entscheidungen",
    ),
    Scenario(
        key="umbrella",
        label="Cisco Umbrella (kompakt)",
        description="Cloud-DNS mit Identity-Awareness — AD-User pro Query sichtbar",
        parser="umbrella",
        file_path=TESTDATA / "umbrella_sample.log",
        expected_highlights="Most-Granular-Identity-Types (user/computer/AD), Categories",
    ),
    Scenario(
        key="fortinet",
        label="FortiGate UTM (kompakt)",
        description="Syslog key=value — TLS-SNI-Inspection ohne MITM-Proxy",
        parser="fortinet",
        file_path=TESTDATA / "fortinet_sample.log",
        expected_highlights="Hostname via SNI, Categories, Action (passthrough/blocked)",
    ),
    Scenario(
        key="entra_signin",
        label="Azure Entra Sign-In (kompakt)",
        description="OAuth/SSO-Logs — AppDisplayName via Alias-Lookup erkannt",
        parser="entra_id",
        file_path=TESTDATA / "entra_signin_sample.log",
        expected_highlights="3-Wege-Action (success/blocked/failed), Entra-Alias-Match "
                            "(ChatGPT Enterprise, GitHub Copilot)",
    ),
    Scenario(
        key="cloudflare_gateway",
        label="Cloudflare Gateway (kompakt)",
        description="DNS + HTTP in einer NDJSON-Datei — Zero-Trust-Remote-Worker",
        parser="cloudflare_gateway",
        file_path=TESTDATA / "cloudflare_gateway_sample.log",
        expected_highlights="source_type unterscheidet DNS vs HTTP, Email-basierte User-IDs",
    ),
)


def get_scenario(key: str) -> Scenario | None:
    for scenario in SCENARIOS:
        if scenario.key == key:
            return scenario
    return None


def available_scenarios() -> list[Scenario]:
    """Liefert nur Scenarios, deren Sample-Datei existiert (z.B. Squid nach Generator-Lauf)."""
    return [s for s in SCENARIOS if s.exists]
