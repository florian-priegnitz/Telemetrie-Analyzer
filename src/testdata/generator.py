"""Generator für synthetische Pi-hole DNS- und Squid Proxy-Testlogs.

Erzeugt realistische Logs mit einer Mischung aus normalem Traffic
und Shadow-AI-Nutzung durch verschiedene Clients.

CLI:
    python -m src.testdata.generator --format pihole --days 7 --queries-per-day 500
    python -m src.testdata.generator --format squid  --days 7 --queries-per-day 500
    python -m src.testdata.generator --format both
"""

import argparse
import math
import random
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


def _pick_event(rng: random.Random, current_date: datetime) -> tuple[datetime, str, str]:
    """Wählt Timestamp, Client und Domain für ein Event."""
    # Zufällige Uhrzeit, gewichtet auf Arbeitszeit (8-18 Uhr)
    if rng.random() < 0.8:
        hour = rng.randint(8, 17)
    else:
        hour = rng.randint(0, 23)
    minute = rng.randint(0, 59)
    second = rng.randint(0, 59)
    ts = current_date.replace(hour=hour, minute=minute, second=second)

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


def _sample_upload_bytes(rng: random.Random, domain: str) -> int:
    """Log-normal verteiltes Upload-Volumen.

    - 80% kleine Requests (~400 B – 4 KB)
    - 15% mittlere POSTs (~10 KB – 100 KB)
    - 5% Document-Upload-Spikes (~500 KB – 5 MB)

    AI-Domains mit typischen Uploads bekommen erhöhte Spike-Wahrscheinlichkeit.
    """
    spike_chance = 0.05
    if domain in UPLOAD_PRONE_AI_DOMAINS:
        spike_chance = 0.18

    bucket = rng.random()
    if bucket < spike_chance:
        return int(math.exp(rng.normalvariate(14.0, 0.8)))
    elif bucket < spike_chance + 0.15:
        return int(math.exp(rng.normalvariate(10.0, 1.0)))
    return int(math.exp(rng.normalvariate(6.0, 1.2)))


def _format_squid(ts: datetime, domain: str, client: str, rng: random.Random) -> str:
    method = rng.choices(["GET", "POST", "CONNECT", "GET", "GET"], k=1)[0]
    bytes_uploaded = _sample_upload_bytes(rng, domain)
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
            ts, client, domain = _pick_event(rng, current_date)
            line = formatter(ts, domain, client, pid, rng) if formatter is _format_pihole \
                else formatter(ts, domain, client, rng)
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
) -> Path:
    """Generiert ein synthetisches Pi-hole DNS-Log."""
    return _generate_log(output_path, days, queries_per_day, start_date, seed, _format_pihole)


def generate_squid_log(
    output_path: Path | str,
    days: int = 7,
    queries_per_day: int = 500,
    start_date: datetime | None = None,
    seed: int = 42,
) -> Path:
    """Generiert ein synthetisches Squid Native Access Log mit Upload-Volumen."""
    return _generate_log(output_path, days, queries_per_day, start_date, seed, _format_squid)


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Erzeugt synthetische Pi-hole oder Squid Logs für Tests."
    )
    parser.add_argument(
        "--format", choices=["pihole", "squid", "both"], default="pihole",
        help="Log-Format (default: pihole)",
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
        help="Output-Verzeichnis (default: testdata/)",
    )
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    if args.format in ("pihole", "both"):
        out = generate_pihole_log(
            args.out_dir / "pihole_sample.log",
            days=args.days, queries_per_day=args.queries_per_day, seed=args.seed,
        )
        print(f"Pi-hole Log: {out} ({out.stat().st_size / 1024:.1f} KB)")

    if args.format in ("squid", "both"):
        out = generate_squid_log(
            args.out_dir / "squid_sample.log",
            days=args.days, queries_per_day=args.queries_per_day, seed=args.seed,
        )
        print(f"Squid Log:   {out} ({out.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    _cli()
