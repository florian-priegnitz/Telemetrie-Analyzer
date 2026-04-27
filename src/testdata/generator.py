"""Generator für synthetische Pi-hole DNS- und Squid Proxy-Testlogs.

Erzeugt realistische Logs mit einer Mischung aus normalem Traffic
und Shadow-AI-Nutzung durch verschiedene Clients.

Szenario-Profile (--scenario):
    clean              keine AI-Nutzung, reine Baseline
    low-risk           gelegentliche medium-risk Services, unter Schwellwert
    systematic         >10 Req/Tag/User, high/critical Services
    upload-leak        POST-Spikes >500 KB an Claude/ChatGPT (Datenabfluss)
    enterprise-mixed   ~30 Clients, realistische Verteilung (Default)

CLI:
    python -m src.testdata.generator --scenario enterprise-mixed --format both
    python -m src.testdata.generator --scenario all --format both
    python -m src.testdata.generator --format pihole --days 7 --queries-per-day 500
"""

import argparse
import math
import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

# Normale Domains (Hintergrund-Traffic)
NORMAL_DOMAINS = [
    "www.google.com", "google.com", "dns.google",
    "www.microsoft.com", "login.microsoftonline.com", "outlook.office365.com",
    "github.com", "api.github.com",
    "stackoverflow.com",
    "www.heise.de", "www.spiegel.de",
    "cdn.jsdelivr.net", "cdnjs.cloudflare.com",
    "registry.npmjs.org", "pypi.org",
    "slack.com", "app.slack.com",
    "teams.microsoft.com",
    "s3.amazonaws.com", "ec2.eu-central-1.amazonaws.com",
]

# Shadow-AI-Domains (die erkannt werden sollen)
AI_DOMAINS = [
    "chat.openai.com", "api.openai.com",
    "claude.ai", "api.anthropic.com",
    "gemini.google.com",
    "copilot.github.com", "api.githubcopilot.com",
    "copilot.microsoft.com",
    "www.perplexity.ai",
    "chat.deepseek.com",
    "api.mistral.ai",
    "www.midjourney.com",
    "app.grammarly.com",
    "www.deepl.com", "api-free.deepl.com",
    "huggingface.co",
    "cursor.sh", "api2.cursor.sh",
]

# AI-Domains, bei denen Datei-Uploads typisch sind
UPLOAD_PRONE_AI_DOMAINS = {
    "chat.openai.com", "claude.ai", "gemini.google.com",
    "www.perplexity.ai", "chat.deepseek.com",
}

# Client-IPs
CLIENTS = [
    "192.168.1.10", "192.168.1.11", "192.168.1.12",
    "192.168.1.20", "192.168.1.21",
    "192.168.1.30",
    "192.168.1.100", "192.168.1.101", "192.168.1.102",
    "10.0.0.5", "10.0.0.6",
]

# Client-Profile: verschiedene Nutzungsmuster
CLIENT_PROFILES = {
    # Entwickler mit intensiver Copilot-Nutzung
    "192.168.1.10": {"ai_domains": ["copilot.github.com", "api.githubcopilot.com", "chat.openai.com"], "ai_weight": 0.3},
    # Analyst der DeepL und ChatGPT nutzt
    "192.168.1.20": {"ai_domains": ["chat.openai.com", "www.deepl.com", "api-free.deepl.com"], "ai_weight": 0.15},
    # Heavy Shadow AI User
    "192.168.1.30": {"ai_domains": ["chat.openai.com", "claude.ai", "chat.deepseek.com", "www.perplexity.ai", "cursor.sh", "api2.cursor.sh"], "ai_weight": 0.4},
    # Gelegentlicher Nutzer
    "192.168.1.100": {"ai_domains": ["gemini.google.com", "app.grammarly.com"], "ai_weight": 0.05},
    # Kein AI-Nutzer
    "192.168.1.11": {"ai_domains": [], "ai_weight": 0.0},
    "192.168.1.12": {"ai_domains": [], "ai_weight": 0.0},
}

_MONTHS_ABBR = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]


@dataclass
class ScenarioConfig:
    """Konfiguration eines Testszenarios."""
    name: str
    description: str
    clients: list[str]
    client_profiles: dict[str, dict]
    upload_spike_domains: set[str] = field(default_factory=set)
    upload_spike_chance: float = 0.18  # Default aus _sample_upload_bytes


# Größere Client-Pools für realistische Enterprise-Mischung
_ENTERPRISE_CLIENTS = [f"192.168.10.{i}" for i in range(10, 40)]

SCENARIO_PROFILES: dict[str, ScenarioConfig] = {
    # 1. Clean Baseline — keine AI-Nutzung, erwartet 0 Findings
    "clean": ScenarioConfig(
        name="clean",
        description="Reine Baseline ohne KI-Nutzung — Negativ-Test für False-Positives",
        clients=["192.168.1.10", "192.168.1.11", "192.168.1.12", "192.168.1.20"],
        client_profiles={
            ip: {"ai_domains": [], "ai_weight": 0.0}
            for ip in ["192.168.1.10", "192.168.1.11", "192.168.1.12", "192.168.1.20"]
        },
    ),

    # 2. Low-Risk — medium-risk Services, unter SYSTEMATIC_THRESHOLD
    "low-risk": ScenarioConfig(
        name="low-risk",
        description="Gelegentliche Nutzung von medium-risk Services (DeepL, Grammarly), <10 Req/Tag",
        clients=["192.168.1.20", "192.168.1.21", "192.168.1.22", "192.168.1.23"],
        client_profiles={
            "192.168.1.20": {"ai_domains": ["www.deepl.com", "api-free.deepl.com"], "ai_weight": 0.01},
            "192.168.1.21": {"ai_domains": ["app.grammarly.com"], "ai_weight": 0.008},
            "192.168.1.22": {"ai_domains": [], "ai_weight": 0.0},
            "192.168.1.23": {"ai_domains": [], "ai_weight": 0.0},
        },
    ),

    # 3. Systematic — klare Schwellwert-Trigger, high/critical Services
    "systematic": ScenarioConfig(
        name="systematic",
        description="Systematische Nutzung >10 Req/Tag, high/critical Services (ChatGPT, Cursor)",
        clients=["192.168.1.30", "192.168.1.31", "192.168.1.32", "192.168.1.33"],
        client_profiles={
            "192.168.1.30": {"ai_domains": ["chat.openai.com", "api.openai.com"], "ai_weight": 0.35},
            "192.168.1.31": {"ai_domains": ["cursor.sh", "api2.cursor.sh"], "ai_weight": 0.3},
            "192.168.1.32": {"ai_domains": ["claude.ai", "api.anthropic.com"], "ai_weight": 0.25},
            "192.168.1.33": {"ai_domains": [], "ai_weight": 0.0},
        },
    ),

    # 4. Upload-Leak — POST-Spikes >500 KB (Datenabfluss)
    "upload-leak": ScenarioConfig(
        name="upload-leak",
        description="Dokument-Uploads >500 KB an Claude/ChatGPT — Datenabfluss-Szenario",
        clients=["192.168.1.40", "192.168.1.41", "192.168.1.42"],
        client_profiles={
            "192.168.1.40": {"ai_domains": ["claude.ai"], "ai_weight": 0.4},
            "192.168.1.41": {"ai_domains": ["chat.openai.com"], "ai_weight": 0.35},
            "192.168.1.42": {"ai_domains": [], "ai_weight": 0.0},
        },
        upload_spike_domains={"claude.ai", "chat.openai.com"},
        upload_spike_chance=0.55,  # massive Erhöhung gegenüber Default 0.18
    ),

    # 6. KRITIS-KMU Shadow AI — 50-User KRITIS-Sektor-KMU mit ausgepraegter Schatten-KI
    "kritis-kmu-shadow-ai": ScenarioConfig(
        name="kritis-kmu-shadow-ai",
        description=(
            "KRITIS-KMU mit 50 Usern: 15 Heavy / 20 Systematic / 10 Casual / 5 Clean — "
            "Demo-Datensatz fuer Vertriebs- und Audit-Argumentation"
        ),
        clients=[f"10.42.0.{i}" for i in range(10, 60)],
        client_profiles={
            # 15 Heavy Shadow-AI User (10.42.0.10–24): ChatGPT/Claude/Cursor/Deepseek
            **{
                f"10.42.0.{10 + i}": {
                    "ai_domains": [
                        "chat.openai.com", "claude.ai", "cursor.sh",
                        "api2.cursor.sh", "chat.deepseek.com",
                    ],
                    "ai_weight": 0.40 + (i % 3) * 0.04,  # 0.40, 0.44, 0.48 …
                }
                for i in range(15)
            },
            # 20 Systematic User (10.42.0.25–44): >10 Req/Tag, klare Schwellwert-Trigger
            **{
                f"10.42.0.{25 + i}": {
                    "ai_domains": [
                        ["chat.openai.com", "api.openai.com"],
                        ["claude.ai", "api.anthropic.com"],
                        ["copilot.github.com", "api.githubcopilot.com"],
                        ["www.perplexity.ai", "perplexity.ai"],
                        ["gemini.google.com"],
                    ][i % 5],
                    "ai_weight": 0.15 + (i % 4) * 0.025,  # 0.150–0.225
                }
                for i in range(20)
            },
            # 10 Casual User (10.42.0.45–54): DeepL/Grammarly/Midjourney
            **{
                f"10.42.0.{45 + i}": {
                    "ai_domains": [
                        ["www.deepl.com", "api-free.deepl.com"],
                        ["app.grammarly.com"],
                        ["www.midjourney.com"],
                        ["huggingface.co"],
                        ["api.mistral.ai"],
                    ][i % 5],
                    "ai_weight": 0.03 + (i % 3) * 0.01,  # 0.03–0.05
                }
                for i in range(10)
            },
            # 5 Clean User (10.42.0.55–59): kein AI-Traffic
            **{f"10.42.0.{55 + i}": {"ai_domains": [], "ai_weight": 0.0} for i in range(5)},
        },
        upload_spike_domains={"chat.openai.com", "claude.ai", "api.anthropic.com"},
        upload_spike_chance=0.30,
    ),

    # 5. Enterprise-Mixed — ~30 Clients, realistische Verteilung über alle Risk-Level
    "enterprise-mixed": ScenarioConfig(
        name="enterprise-mixed",
        description="Realistisches Enterprise-Bild mit 30 Clients und diversen Risk-Levels",
        clients=_ENTERPRISE_CLIENTS,
        client_profiles={
            # Heavy Shadow-AI User (2 Stück) — kritisch
            "192.168.10.10": {"ai_domains": ["chat.openai.com", "claude.ai", "cursor.sh", "api2.cursor.sh", "chat.deepseek.com"], "ai_weight": 0.45},
            "192.168.10.11": {"ai_domains": ["copilot.github.com", "api.githubcopilot.com", "chat.openai.com"], "ai_weight": 0.4},
            # Systematic User (4 Stück) — high
            "192.168.10.12": {"ai_domains": ["chat.openai.com", "api.openai.com"], "ai_weight": 0.2},
            "192.168.10.13": {"ai_domains": ["claude.ai"], "ai_weight": 0.18},
            "192.168.10.14": {"ai_domains": ["gemini.google.com"], "ai_weight": 0.15},
            "192.168.10.15": {"ai_domains": ["www.perplexity.ai", "perplexity.ai"], "ai_weight": 0.12},
            # Gelegentliche Nutzer (6 Stück) — medium
            "192.168.10.16": {"ai_domains": ["www.deepl.com", "api-free.deepl.com"], "ai_weight": 0.04},
            "192.168.10.17": {"ai_domains": ["app.grammarly.com"], "ai_weight": 0.03},
            "192.168.10.18": {"ai_domains": ["www.midjourney.com"], "ai_weight": 0.02},
            "192.168.10.19": {"ai_domains": ["huggingface.co"], "ai_weight": 0.025},
            "192.168.10.20": {"ai_domains": ["api.mistral.ai"], "ai_weight": 0.03},
            "192.168.10.21": {"ai_domains": ["gemini.google.com"], "ai_weight": 0.02},
            # Restliche 18 Clients: kein AI-Traffic
            **{f"192.168.10.{i}": {"ai_domains": [], "ai_weight": 0.0} for i in range(22, 40)},
        },
        upload_spike_domains={"chat.openai.com", "claude.ai"},
        upload_spike_chance=0.22,  # leicht erhöht gegenüber Default
    ),
}


def _pick_event(
    rng: random.Random,
    current_date: datetime,
    scenario: ScenarioConfig | None = None,
) -> tuple[datetime, str, str]:
    """Wählt Timestamp, Client und Domain für ein Event.

    Args:
        rng: Random-Generator (seed-gesteuert für Reproduzierbarkeit)
        current_date: Tag, in dem das Event liegt
        scenario: Optional, bestimmt Clients und AI-Profile. Bei None → Legacy-Verhalten
                  mit CLIENTS / CLIENT_PROFILES (Rückwärtskompatibilität).
    """
    # Zufällige Uhrzeit, gewichtet auf Arbeitszeit (8-18 Uhr)
    if rng.random() < 0.8:
        hour = rng.randint(8, 17)
    else:
        hour = rng.randint(0, 23)
    minute = rng.randint(0, 59)
    second = rng.randint(0, 59)
    ts = current_date.replace(hour=hour, minute=minute, second=second)

    if scenario is not None:
        client = rng.choice(scenario.clients)
        profile = scenario.client_profiles.get(client)
    else:
        client = rng.choice(CLIENTS)
        profile = CLIENT_PROFILES.get(client)

    if profile and profile["ai_domains"] and rng.random() < profile["ai_weight"]:
        domain = rng.choice(profile["ai_domains"])
    else:
        domain = rng.choice(NORMAL_DOMAINS)

    return ts, client, domain


def _format_pihole(ts: datetime, domain: str, client: str, pid: int, rng: random.Random) -> str:
    qtype = rng.choice(["A", "AAAA", "A", "A"])
    month_str = _MONTHS_ABBR[ts.month - 1]
    day_str = f"{ts.day:2d}"
    return (
        f"{month_str} {day_str} {ts.hour:02d}:{ts.minute:02d}:{ts.second:02d} "
        f"dnsmasq[{pid}]: query[{qtype}] {domain} from {client}"
    )


def _sample_upload_bytes(
    rng: random.Random,
    domain: str,
    scenario: ScenarioConfig | None = None,
) -> int:
    """Log-normal verteiltes Upload-Volumen.

    - 80% kleine Requests (~400 B – 4 KB)
    - 15% mittlere POSTs (~10 KB – 100 KB)
    - 5% Document-Upload-Spikes (~500 KB – 5 MB)

    Szenarien können die Spike-Wahrscheinlichkeit gezielt für bestimmte Domains
    erhöhen (z.B. upload-leak → 0.55 für claude.ai/chat.openai.com), um die
    Detection-Schwelle UPLOAD_THRESHOLD_BYTES=500KB zuverlässig zu treffen.
    """
    spike_chance = 0.05
    if scenario is not None and domain in scenario.upload_spike_domains:
        spike_chance = scenario.upload_spike_chance
    elif domain in UPLOAD_PRONE_AI_DOMAINS:
        spike_chance = 0.18

    bucket = rng.random()
    if bucket < spike_chance:
        return int(math.exp(rng.normalvariate(14.0, 0.8)))
    elif bucket < spike_chance + 0.15:
        return int(math.exp(rng.normalvariate(10.0, 1.0)))
    return int(math.exp(rng.normalvariate(6.0, 1.2)))


def _format_squid(
    ts: datetime,
    domain: str,
    client: str,
    rng: random.Random,
    scenario: ScenarioConfig | None = None,
) -> str:
    method = rng.choices(["GET", "POST", "CONNECT", "GET", "GET"], k=1)[0]
    bytes_uploaded = _sample_upload_bytes(rng, domain, scenario)
    elapsed = rng.randint(10, 800)
    code_status = rng.choices(["TCP_MISS/200", "TCP_HIT/200", "TCP_TUNNEL/200", "TCP_MISS/204"], k=1)[0]
    if method == "CONNECT":
        url = f"{domain}:443"
        content_type = "-"
    else:
        path = rng.choice(["/", "/api/v1/chat", "/v1/messages", "/upload", "/api/completions"])
        url = f"https://{domain}{path}"
        content_type = rng.choice(["application/json", "application/json", "text/html", "multipart/form-data"])
    epoch = ts.timestamp()
    return (
        f"{epoch:.3f} {elapsed} {client} {code_status} {bytes_uploaded} "
        f"{method} {url} - HIER_DIRECT/1.2.3.4 {content_type}"
    )


def _generate_log(
    output_path: Path | str,
    days: int,
    queries_per_day: int,
    start_date: datetime | None,
    seed: int,
    formatter,
    scenario: ScenarioConfig | None = None,
) -> Path:
    rng = random.Random(seed)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if start_date is None:
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days)

    pid = rng.randint(1000, 9999)
    events: list[tuple[datetime, str]] = []

    for day_offset in range(days):
        current_date = start_date + timedelta(days=day_offset)
        # Weniger Traffic am Wochenende
        day_queries = queries_per_day if current_date.weekday() < 5 else queries_per_day // 3

        for _ in range(day_queries):
            ts, client, domain = _pick_event(rng, current_date, scenario)
            if formatter is _format_pihole:
                line = formatter(ts, domain, client, pid, rng)
            else:
                line = formatter(ts, domain, client, rng, scenario)
            events.append((ts, line))

    events.sort(key=lambda x: x[0])
    with open(output_path, "w", encoding="utf-8") as f:
        for _, line in events:
            f.write(line + "\n")

    return output_path


def generate_pihole_log(
    output_path: Path | str,
    days: int = 7,
    queries_per_day: int = 500,
    start_date: datetime | None = None,
    seed: int = 42,
    scenario: str | ScenarioConfig | None = None,
) -> Path:
    """Generiert ein synthetisches Pi-hole DNS-Log.

    Args:
        scenario: Name eines Szenarios aus SCENARIO_PROFILES oder ScenarioConfig.
                  None → Legacy-Verhalten mit globalen CLIENT_PROFILES.
    """
    cfg = _resolve_scenario(scenario)
    return _generate_log(output_path, days, queries_per_day, start_date, seed, _format_pihole, cfg)


def generate_squid_log(
    output_path: Path | str,
    days: int = 7,
    queries_per_day: int = 500,
    start_date: datetime | None = None,
    seed: int = 42,
    scenario: str | ScenarioConfig | None = None,
) -> Path:
    """Generiert ein synthetisches Squid Native Access Log mit Upload-Volumen.

    Args:
        scenario: Name eines Szenarios aus SCENARIO_PROFILES oder ScenarioConfig.
                  None → Legacy-Verhalten mit globalen CLIENT_PROFILES.
    """
    cfg = _resolve_scenario(scenario)
    return _generate_log(output_path, days, queries_per_day, start_date, seed, _format_squid, cfg)


def _resolve_scenario(scenario: str | ScenarioConfig | None) -> ScenarioConfig | None:
    if scenario is None or isinstance(scenario, ScenarioConfig):
        return scenario
    if scenario not in SCENARIO_PROFILES:
        raise ValueError(
            f"Unbekanntes Szenario: {scenario!r}. "
            f"Verfügbar: {sorted(SCENARIO_PROFILES.keys())}"
        )
    return SCENARIO_PROFILES[scenario]


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Erzeugt synthetische Pi-hole oder Squid Logs für Tests.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Verfügbare Szenarien:\n  " + "\n  ".join(
            f"{cfg.name:<18} {cfg.description}" for cfg in SCENARIO_PROFILES.values()
        ),
    )
    parser.add_argument(
        "--format", choices=["pihole", "squid", "both"], default="pihole",
        help="Log-Format (default: pihole)",
    )
    parser.add_argument(
        "--scenario",
        choices=[*SCENARIO_PROFILES.keys(), "all", "legacy"],
        default="legacy",
        help="Szenario-Profil (default: legacy = alter gemischter Traffic)",
    )
    parser.add_argument("--days", type=int, default=7, help="Anzahl Tage (default: 7)")
    parser.add_argument(
        "--queries-per-day", type=int, default=500,
        help="Durchschnittliche Queries pro Tag (default: 500)",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random Seed (default: 42)")
    parser.add_argument(
        "--out-dir", type=Path,
        default=Path(__file__).parent.parent.parent / "testdata",
        help="Output-Verzeichnis (default: testdata/ bzw. testdata/scenarios/ bei --scenario)",
    )
    args = parser.parse_args()

    if args.scenario == "all":
        target_scenarios = list(SCENARIO_PROFILES.keys())
    elif args.scenario == "legacy":
        target_scenarios = [None]  # None = alte CLIENT_PROFILES
    else:
        target_scenarios = [args.scenario]

    # Bei named scenarios in testdata/scenarios/ ablegen
    if args.scenario != "legacy":
        out_dir = args.out_dir / "scenarios"
    else:
        out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    for scn in target_scenarios:
        prefix = scn if scn else "sample"
        if args.format in ("pihole", "both"):
            out = generate_pihole_log(
                out_dir / f"{prefix}_pihole.log",
                days=args.days, queries_per_day=args.queries_per_day,
                seed=args.seed, scenario=scn,
            )
            print(f"Pi-hole [{prefix}]: {out} ({out.stat().st_size / 1024:.1f} KB)")

        if args.format in ("squid", "both"):
            out = generate_squid_log(
                out_dir / f"{prefix}_squid.log",
                days=args.days, queries_per_day=args.queries_per_day,
                seed=args.seed, scenario=scn,
            )
            print(f"Squid   [{prefix}]: {out} ({out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    _cli()
