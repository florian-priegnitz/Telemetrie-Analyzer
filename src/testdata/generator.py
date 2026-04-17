"""Generator für synthetische Pi-hole DNS-Testlogs.

Erzeugt realistische Logs mit einer Mischung aus normalem Traffic
und Shadow-AI-Nutzung durch verschiedene Clients.
"""

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


def generate_pihole_log(
    output_path: Path | str,
    days: int = 7,
    queries_per_day: int = 500,
    start_date: datetime | None = None,
    seed: int = 42,
) -> Path:
    """Generiert ein synthetisches Pi-hole DNS-Log.

    Args:
        output_path: Zieldatei
        days: Anzahl Tage zu simulieren
        queries_per_day: Durchschnittliche Queries pro Tag
        start_date: Startdatum (default: 7 Tage vor heute)
        seed: Random Seed für Reproduzierbarkeit

    Returns:
        Pfad zur erzeugten Datei
    """
    rng = random.Random(seed)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if start_date is None:
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days)

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    lines: list[str] = []
    pid = rng.randint(1000, 9999)

    for day_offset in range(days):
        current_date = start_date + timedelta(days=day_offset)
        # Weniger Traffic am Wochenende
        day_queries = queries_per_day if current_date.weekday() < 5 else queries_per_day // 3

        for _ in range(day_queries):
            # Zufällige Uhrzeit, gewichtet auf Arbeitszeit (8-18 Uhr)
            if rng.random() < 0.8:
                hour = rng.randint(8, 17)
            else:
                hour = rng.randint(0, 23)
            minute = rng.randint(0, 59)
            second = rng.randint(0, 59)

            client = rng.choice(CLIENTS)
            profile = CLIENT_PROFILES.get(client)

            # Domain auswählen basierend auf Client-Profil
            if profile and profile["ai_domains"] and rng.random() < profile["ai_weight"]:
                domain = rng.choice(profile["ai_domains"])
            else:
                domain = rng.choice(NORMAL_DOMAINS)

            qtype = rng.choice(["A", "AAAA", "A", "A"])  # A ist häufiger
            month_str = months[current_date.month - 1]
            day_str = f"{current_date.day:2d}"

            line = (
                f"{month_str} {day_str} {hour:02d}:{minute:02d}:{second:02d} "
                f"dnsmasq[{pid}]: query[{qtype}] {domain} from {client}"
            )
            lines.append((current_date.replace(hour=hour, minute=minute, second=second), line))

    # Nach Timestamp sortieren
    lines.sort(key=lambda x: x[0])

    with open(output_path, "w", encoding="utf-8") as f:
        for _, line in lines:
            f.write(line + "\n")

    return output_path


if __name__ == "__main__":
    out = generate_pihole_log(
        Path(__file__).parent.parent.parent / "testdata" / "pihole_sample.log",
        days=7,
        queries_per_day=500,
    )
    print(f"Testdaten generiert: {out} ({out.stat().st_size / 1024:.1f} KB)")
