"""Anreicherung der statischen Samples mit realistischen Demo-Daten.

Motivation: die handgeschriebenen ``testdata/*_sample.log`` sind bewusst
klein gehalten — sie sind Unit-Test-Fixtures, die spezifisches
Parser-Verhalten testen. Für den UI-Demo (Scenario-Buttons) brauchen
wir größere Samples mit Client-Diversität, Zeit-Spread und AI-Service-
Vielfalt.

Lösung: dieses Skript erzeugt ``testdata/demo/*_demo.log`` mit
~60-100 Events — rein synthetisch, seed-reproduzierbar. Die Original-
Fixtures bleiben unangetastet.

Idempotent: überschreibt existierende demo/*-Dateien.

Usage:
    python scripts/enrich_samples.py
"""

from __future__ import annotations

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTDATA = ROOT / "testdata"


# 7-Tages-Fenster endend gestern — bleibt klar innerhalb 90-Tage-Retention
END_DATE = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
START_DATE = END_DATE - timedelta(days=6)

SEED = 42
rng = random.Random(SEED)


# ---------------------------------------------------------------------------
# Geteilte Daten-Pools (quer über Formate konsistent, damit z.B. ein Client
# in sysmon auch in netskope auftaucht — ergibt einen besseren Demo)
# ---------------------------------------------------------------------------
USERS = ["alice", "bob", "carol", "david", "eve", "frank", "grace", "henry",
         "iris", "jack", "kate", "leo"]
EMAIL_DOMAIN = "acme.onmicrosoft.com"
CLIENT_IPS = [f"10.0.1.{n}" for n in range(40, 60)] + [f"10.0.2.{n}" for n in range(10, 30)]
HOSTNAMES = [f"WKS-{u[:3].upper()}{i:02d}" for i, u in enumerate(USERS)]

# AI-Endpunkte mit realistischer Verteilung
AI_DOMAINS = [
    ("chat.openai.com", "OpenAI ChatGPT", "critical"),
    ("api.openai.com", "OpenAI API", "critical"),
    ("claude.ai", "Anthropic Claude", "high"),
    ("api.anthropic.com", "Anthropic API", "high"),
    ("copilot.microsoft.com", "Microsoft Copilot", "high"),
    ("gemini.google.com", "Google Gemini", "high"),
    ("perplexity.ai", "Perplexity AI", "high"),
    ("www.perplexity.ai", "Perplexity AI", "high"),
    ("api.mistral.ai", "Mistral AI", "high"),
    ("chat.deepseek.com", "DeepSeek", "critical"),
    ("cursor.sh", "Cursor", "critical"),
    ("github.com", "GitHub Copilot", "critical"),
    ("api.github.com", "GitHub Copilot", "critical"),
    ("www.midjourney.com", "Midjourney", "high"),
    ("grok.com", "xAI Grok", "high"),
    ("app.notion.so", "Notion AI", "medium"),
    ("app.grammarly.com", "Grammarly AI", "medium"),
    ("www.deepl.com", "DeepL", "medium"),
]
# 10% non-AI (damit Detection einen Kontrast zeigt)
NOISE_DOMAINS = ["www.microsoft.com", "teams.microsoft.com", "dns.google",
                 "registry.npmjs.org", "pypi.org"]


def _random_timestamp(seed_offset: int = 0) -> datetime:
    """Zufälliges datetime im 7-Tages-Fenster, mit Business-Hours-Bias (70% 08-18 Uhr)."""
    days_in = rng.randint(0, 6)
    if rng.random() < 0.7:
        hour = rng.randint(8, 18)
    else:
        hour = rng.randint(0, 23)
    base = START_DATE + timedelta(days=days_in, hours=hour,
                                   minutes=rng.randint(0, 59),
                                   seconds=rng.randint(0, 59))
    return base


def _pick_ai() -> tuple[str, str, str]:
    """Weighted AI pick: 70% high/critical, 30% medium."""
    if rng.random() < 0.7:
        pool = [ai for ai in AI_DOMAINS if ai[2] in ("critical", "high")]
    else:
        pool = AI_DOMAINS
    return rng.choice(pool)


# ---------------------------------------------------------------------------
# Enrichers pro Format
# ---------------------------------------------------------------------------
def enrich_elastic_ecs(n_events: int = 80) -> str:
    """Elastic Common Schema NDJSON — mix aus DNS und HTTP events."""
    lines = []
    for _ in range(n_events):
        ts = _random_timestamp()
        user = rng.choice(USERS)
        ip = rng.choice(CLIENT_IPS)
        if rng.random() < 0.2:  # 20% non-AI noise
            domain = rng.choice(NOISE_DOMAINS)
        else:
            domain, _, _ = _pick_ai()

        if rng.random() < 0.5:
            # DNS event
            event = {
                "@timestamp": ts.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                "event": {"category": ["network", "dns"], "type": ["info"], "action": "lookup"},
                "dns": {"question": {"name": domain, "type": "A"}},
                "source": {"ip": ip},
                "user": {"name": user},
                "host": {"name": rng.choice(HOSTNAMES)},
            }
        else:
            # HTTP event
            method = rng.choice(["GET", "POST", "POST", "POST"])
            body_bytes = rng.randint(500000, 3000000) if method == "POST" and rng.random() < 0.3 else rng.randint(200, 5000)
            event = {
                "@timestamp": ts.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                "event": {"category": "web", "action": "http-request"},
                "http": {
                    "request": {"method": method, "body": {"bytes": body_bytes}},
                    "response": {"status_code": 200}
                },
                "url": {"domain": domain, "path": "/v1/messages", "full": f"https://{domain}/v1/messages"},
                "source": {"ip": ip},
                "user": {"name": user},
                "user_agent": {"original": "Mozilla/5.0 (X11; Linux) Chrome/124"},
            }
        lines.append(json.dumps(event))
    # Chronologisch sortieren für realistisches Tool-Output
    lines.sort(key=lambda s: json.loads(s)["@timestamp"])
    return "\n".join(lines) + "\n"


def enrich_sysmon(n_events: int = 80) -> str:
    """Windows Sysmon EventID 22 (DNS Query) mit Flat- und Winlogbeat-Shape."""
    lines = []
    processes = ["firefox.exe", "chrome.exe", "msedge.exe", "Cursor.exe",
                 "Code.exe", "brave.exe", "Teams.exe", "Outlook.exe", "powershell.exe"]
    for _ in range(n_events):
        ts = _random_timestamp()
        host = rng.choice(HOSTNAMES)
        user = rng.choice(USERS)
        proc = rng.choice(processes)
        domain = rng.choice(NOISE_DOMAINS) if rng.random() < 0.2 else _pick_ai()[0]
        # 70% Flat-Shape (häufigstes Format), 30% Winlogbeat
        if rng.random() < 0.7:
            event = {
                "EventID": 22,
                "UtcTime": ts.strftime("%Y-%m-%d %H:%M:%S.000"),
                "QueryName": domain,
                "QueryStatus": "0",
                "Image": proc,
                "Computer": host,
                "User": f"CONTOSO\\{user}",
            }
        else:
            event = {
                "@timestamp": ts.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                "event": {"code": "22"},
                "host": {"name": host},
                "user": {"name": user},
                "winlog": {
                    "event_data": {"QueryName": domain, "QueryStatus": "0", "Image": proc}
                }
            }
        lines.append(json.dumps(event))
    lines.sort(key=lambda s: (
        json.loads(s).get("UtcTime") or json.loads(s).get("@timestamp", "")
    ))
    return "\n".join(lines) + "\n"


def enrich_netskope(n_events: int = 100) -> str:
    """Netskope CASB NDJSON mit Activity-Feld (Prompt/Completion/Upload File)."""
    activities = ["Login", "Prompt", "Completion", "Upload File", "Download File", "Browse"]
    actions = ["allow", "allow", "allow", "alert", "block"]
    lines = []
    for _ in range(n_events):
        ts = _random_timestamp()
        user = rng.choice(USERS)
        ip = rng.choice(CLIENT_IPS)
        domain, service, _ = _pick_ai() if rng.random() < 0.85 else (rng.choice(NOISE_DOMAINS), "misc", "low")
        activity = rng.choice(activities)
        event = {
            "_insertion_epoch_timestamp": int(ts.timestamp()),
            "timestamp": int(ts.timestamp()),
            "user": f"{user}@acme.com",
            "userkey": f"key-{user}",
            "src_ip": ip,
            "src_country": "DE",
            "hostname": domain,
            "app": service,
            "appcategory": "Artificial Intelligence" if service != "misc" else "Business",
            "action": rng.choice(actions),
            "activity": activity,
            "method": "POST" if activity in ("Prompt", "Upload File") else "GET",
            "url": f"https://{domain}/v1/chat",
            "uri_path": "/v1/chat",
            "bytes_uploaded": rng.randint(500000, 2500000) if activity == "Upload File" else rng.randint(200, 8000),
            "bytes_downloaded": rng.randint(5000, 80000),
            "useragent": "netskope-cli/2.0",
        }
        lines.append(json.dumps(event))
    lines.sort(key=lambda s: json.loads(s)["_insertion_epoch_timestamp"])
    return "\n".join(lines) + "\n"


def enrich_aws_vpc_v5(n_events: int = 60) -> str:
    """AWS VPC Flow Logs v5 Custom mit pkt-dst-aws-service-Feld."""
    header = ("version account-id interface-id srcaddr dstaddr srcport dstport "
              "protocol packets bytes start end action log-status "
              "pkt-src-aws-service pkt-dst-aws-service\n")
    lines = [header.strip()]
    aws_services = ["BEDROCK", "SAGEMAKER", "COMPREHEND", "-", "API_GATEWAY", "S3", "-"]
    for _ in range(n_events):
        ts = _random_timestamp()
        start_epoch = int(ts.timestamp())
        end_epoch = start_epoch + rng.randint(10, 300)
        src = rng.choice(CLIENT_IPS)
        # AWS internal IPs für AI-Services (fiktiv)
        dst = f"52.{rng.randint(80, 200)}.{rng.randint(0, 255)}.{rng.randint(1, 254)}"
        src_port = rng.randint(30000, 65535)
        dst_port = rng.choice([443, 443, 443, 80, 8080])
        pkt_src = "-"
        pkt_dst = rng.choice(aws_services)
        packets = rng.randint(5, 200)
        bytes_ = rng.randint(1000, 2_000_000)
        action = rng.choice(["ACCEPT", "ACCEPT", "ACCEPT", "REJECT"])
        line = (f"5 123456789010 eni-abc123def{rng.randint(100, 999):04d} "
                f"{src} {dst} {src_port} {dst_port} 6 {packets} {bytes_} "
                f"{start_epoch} {end_epoch} {action} OK {pkt_src} {pkt_dst}")
        lines.append(line)
    # Datenzeilen nach Start sortieren, Header bleibt erste Zeile
    lines[1:] = sorted(lines[1:], key=lambda s: int(s.split()[10]))
    return "\n".join(lines) + "\n"


def main() -> int:
    enrichers = {
        "elastic_ecs_demo.log": enrich_elastic_ecs,
        "sysmon_demo.log": enrich_sysmon,
        "netskope_demo.log": enrich_netskope,
        "aws_vpc_v5_demo.log": enrich_aws_vpc_v5,
    }
    demo_dir = TESTDATA / "demo"
    demo_dir.mkdir(exist_ok=True)
    print(f"Zeit-Fenster: {START_DATE.date()} .. {END_DATE.date()}")
    print(f"Seed: {SEED}")
    print(f"Output: {demo_dir}\n")
    for filename, fn in enrichers.items():
        content = fn()
        path = demo_dir / filename
        path.write_text(content, encoding="utf-8")
        after_lines = content.count("\n")
        print(f"  OK {filename}: {after_lines} Zeilen")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
