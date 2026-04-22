"""Monthly refresh script for ai_endpoints.json.

Usage:
    python scripts/refresh_endpoints.py              # writes JSON in place
    python scripts/refresh_endpoints.py --dry-run    # prints diff only, no write

Wird monatlich via .github/workflows/endpoint-db-update.yml ausgeführt und
erzeugt einen Auto-PR. Der Seed-Katalog in NEW_ENDPOINTS wird manuell gepflegt;
hier ist Platz für zusätzliche Discovery-Quellen (Awesome-AI-Tools, uBlock-Filter,
ASN-Lookups) in späteren Sprints.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

NEW_CATEGORIES = {
    "hr_recruiting_ai": "KI-gestützte HR- und Recruiting-Tools (Interview, Screening, Sourcing)",
    "browser_extension_ai": "KI-Browser-Extensions (Seitenbar-Chatbot, Page-Summary)",
    "customer_support_ai": "KI-gestützte Customer-Support-Plattformen (Ticket-Auto-Resolve, Chatbot)",
}

NEW_ENDPOINTS = [
    {"service": "HireVue", "provider": "HireVue", "category": "hr_recruiting_ai",
     "risk_level": "high", "domains": ["hirevue.com", "app.hirevue.com"],
     "description": "KI-gestütztes Video-Interview-Screening",
     "source": "endpoint-refresh-2026-04"},
    {"service": "Paradox (Olivia)", "provider": "Paradox", "category": "hr_recruiting_ai",
     "risk_level": "medium", "domains": ["paradox.ai", "app.paradox.ai"],
     "description": "Conversational-Recruiting-Assistent",
     "source": "endpoint-refresh-2026-04"},
    {"service": "Sana AI", "provider": "Sana Labs", "category": "hr_recruiting_ai",
     "risk_level": "medium", "domains": ["sana.ai", "app.sana.ai"],
     "description": "Learning & Knowledge-Assistant mit KI-Retrieval",
     "source": "endpoint-refresh-2026-04"},
    {"service": "Eightfold AI", "provider": "Eightfold", "category": "hr_recruiting_ai",
     "risk_level": "high", "domains": ["eightfold.ai", "app.eightfold.ai"],
     "description": "Talent-Intelligence-Plattform mit KI-Matching",
     "source": "endpoint-refresh-2026-04"},
    {"service": "Humanly", "provider": "Humanly", "category": "hr_recruiting_ai",
     "risk_level": "medium", "domains": ["humanly.io", "app.humanly.io"],
     "description": "KI-Chatbot für Candidate-Screening",
     "source": "endpoint-refresh-2026-04"},
    {"service": "SeekOut", "provider": "SeekOut", "category": "hr_recruiting_ai",
     "risk_level": "medium", "domains": ["seekout.com", "app.seekout.com"],
     "description": "KI-gestütztes Talent-Sourcing",
     "source": "endpoint-refresh-2026-04"},
    {"service": "Merlin AI", "provider": "Merlin", "category": "browser_extension_ai",
     "risk_level": "high", "domains": ["getmerlin.in", "api.getmerlin.in"],
     "description": "KI-Browser-Extension (GPT-Zugriff, Page-Summary)",
     "source": "endpoint-refresh-2026-04"},
    {"service": "HARPA AI", "provider": "HARPA", "category": "browser_extension_ai",
     "risk_level": "high", "domains": ["harpa.ai", "api.harpa.ai"],
     "description": "KI-Extension mit Web-Automation und GPT-Zugriff",
     "source": "endpoint-refresh-2026-04"},
    {"service": "Monica AI", "provider": "Monica", "category": "browser_extension_ai",
     "risk_level": "high", "domains": ["monica.im", "api.monica.im"],
     "description": "AI-Assistant-Extension (Chat, Translate, Write)",
     "source": "endpoint-refresh-2026-04"},
    {"service": "MaxAI.me", "provider": "MaxAI", "category": "browser_extension_ai",
     "risk_level": "medium", "domains": ["maxai.me", "api.maxai.me"],
     "description": "One-Click-AI-Browser-Extension",
     "source": "endpoint-refresh-2026-04"},
    {"service": "Sider AI", "provider": "Sider", "category": "browser_extension_ai",
     "risk_level": "medium", "domains": ["sider.ai", "api.sider.ai"],
     "description": "ChatGPT-Sidebar-Extension",
     "source": "endpoint-refresh-2026-04"},
    {"service": "TinaMind", "provider": "TinaMind", "category": "browser_extension_ai",
     "risk_level": "medium", "domains": ["tinamind.com", "api.tinamind.com"],
     "description": "ChatGPT-Extension mit YouTube-Summary",
     "source": "endpoint-refresh-2026-04"},
    {"service": "Intercom Fin", "provider": "Intercom", "category": "customer_support_ai",
     "risk_level": "high", "domains": ["fin.ai", "intercom.io", "api.intercom.io"],
     "description": "KI-Customer-Support-Agent (Fin)",
     "source": "endpoint-refresh-2026-04"},
    {"service": "Forethought", "provider": "Forethought", "category": "customer_support_ai",
     "risk_level": "high", "domains": ["forethought.ai", "app.forethought.ai"],
     "description": "Autonomer Ticket-Resolution-Agent",
     "source": "endpoint-refresh-2026-04"},
    {"service": "Ada", "provider": "Ada Support", "category": "customer_support_ai",
     "risk_level": "medium", "domains": ["ada.cx", "ada.support"],
     "description": "KI-Chatbot für Customer-Service",
     "source": "endpoint-refresh-2026-04"},
    {"service": "Zendesk AI", "provider": "Zendesk", "category": "customer_support_ai",
     "risk_level": "high", "domains": ["zendesk.com", "zdassets.com"],
     "description": "Zendesk Advanced AI (Agent-Copilot, Auto-Reply)",
     "source": "endpoint-refresh-2026-04"},
    {"service": "Cresta", "provider": "Cresta", "category": "customer_support_ai",
     "risk_level": "high", "domains": ["cresta.com", "app.cresta.com"],
     "description": "Real-Time-Agent-Assist für Call-Center",
     "source": "endpoint-refresh-2026-04"},
    {"service": "Decagon", "provider": "Decagon", "category": "customer_support_ai",
     "risk_level": "high", "domains": ["decagon.ai", "app.decagon.ai"],
     "description": "Enterprise-AI-Agent für Customer-Support",
     "source": "endpoint-refresh-2026-04"},
]

NEW_VERSION = "2.1.0"
NEW_DATE = "2026-04-21"


def refresh(path: Path, dry_run: bool = False) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))

    for key, desc in NEW_CATEGORIES.items():
        if key not in data["categories"]:
            data["categories"][key] = desc

    existing = {e["service"] for e in data["endpoints"]}
    added = 0
    for ep in NEW_ENDPOINTS:
        if ep["service"] in existing:
            print(f"SKIP (duplicate): {ep['service']}")
            continue
        data["endpoints"].append(ep)
        added += 1

    data["version"] = NEW_VERSION
    data["last_updated"] = NEW_DATE
    data["endpoints"].sort(key=lambda e: e["service"].lower())

    if dry_run:
        print(f"[dry-run] Würde hinzufügen: {added} Endpoints, "
              f"{len(NEW_CATEGORIES)} neue Kategorien")
        print(f"[dry-run] Total nach Merge: {len(data['endpoints'])} Endpoints")
        return added

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")
    print(f"Added: {added} endpoints")
    print(f"Total endpoints: {len(data['endpoints'])}")
    print(f"Categories: {len(data['categories'])}")
    return added


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true",
                        help="Nur diff zeigen, nichts schreiben")
    parser.add_argument("--path", type=Path,
                        default=Path(__file__).resolve().parent.parent / "data" / "ai_endpoints.json",
                        help="Pfad zur ai_endpoints.json")
    args = parser.parse_args()

    if not args.path.exists():
        print(f"ERROR: {args.path} nicht gefunden", file=sys.stderr)
        return 1

    refresh(args.path, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
