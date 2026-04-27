"""Erzeugt docs/AI_COVERAGE.md — Uebersicht aller bekannten KI-Anbieter.

Liest die AI-Endpoint-DB (`data/ai_endpoints.json`) und generiert einen
strukturierten Report fuer Audit-/Demo-Zwecke. Sprint 12 / #77.

Aufruf:
    python scripts/db_coverage_report.py            # schreibt docs/AI_COVERAGE.md
    python scripts/db_coverage_report.py --check    # vergleicht ohne Schreiben
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.database.ai_endpoints import AIEndpointDatabase  # noqa: E402

OUTPUT_PATH = REPO_ROOT / "docs" / "AI_COVERAGE.md"

# Lesbare Labels fuer die Kategorie-Slugs aus der DB.
CATEGORY_LABELS: dict[str, str] = {
    "ai_agent": "Autonome AI-Agenten",
    "audio_generation": "Audio-Generierung",
    "browser_extension_ai": "Browser-Extensions",
    "code_assistant": "Code-Assistenten",
    "content_generation": "Content-Generierung",
    "customer_support_ai": "Customer-Support-AI",
    "data_analysis_ai": "Daten-Analyse",
    "enterprise_embedded": "Enterprise-Embedded",
    "hr_recruiting_ai": "HR & Recruiting",
    "image_generation": "Bild-Generierung",
    "llm_api": "LLM-APIs",
    "llm_chatbot": "LLM-Chatbots",
    "meeting_ai": "Meeting-AI",
    "ml_platform": "ML-Plattformen",
    "presentation_ai": "Präsentations-AI",
    "productivity_ai": "Produktivitäts-AI",
    "speech_to_text": "Sprach-zu-Text",
    "text_to_speech": "Text-zu-Sprache",
    "translation": "Übersetzung",
    "video_ai": "Video-AI",
    "writing_assistant": "Schreib-Assistenten",
}


def render_markdown(db: AIEndpointDatabase) -> str:
    """Liefert den Markdown-Body fuer docs/AI_COVERAGE.md."""
    endpoints = db.endpoints
    providers = Counter(e.provider for e in endpoints)
    categories = Counter(e.category for e in endpoints)
    risk_levels = Counter(e.risk_level for e in endpoints)

    by_category: dict[str, list] = defaultdict(list)
    for endpoint in endpoints:
        by_category[endpoint.category].append(endpoint)

    today = date.today().isoformat()
    last_updated = db.last_updated or "—"
    age_days = _age_days(last_updated)
    age_str = f"{age_days} Tage alt" if age_days is not None else "Stand unbekannt"
    freshness = _freshness_emoji(age_days)

    lines: list[str] = []
    lines.append("# AI-Coverage-Report")
    lines.append("")
    lines.append(
        f"**DB-Version:** v{db.version} · **Stand:** {last_updated} ({age_str}) · "
        f"{freshness}"
    )
    lines.append("")
    lines.append(
        f"_Auto-generiert via `scripts/db_coverage_report.py` am {today}. "
        "Manuelle Bearbeitung wird beim naechsten Skript-Lauf ueberschrieben._"
    )
    lines.append("")

    lines.append("## Kennzahlen")
    lines.append("")
    lines.append(f"- **Endpoints:** {len(endpoints)}")
    lines.append(f"- **Provider:** {len(providers)}")
    lines.append(f"- **Kategorien:** {len(categories)}")
    if endpoints:
        lines.append(
            "- **Risk-Verteilung:** "
            + " · ".join(
                f"{level}: {risk_levels.get(level, 0)}"
                for level in ("critical", "high", "medium", "low")
                if risk_levels.get(level, 0)
            )
        )
    lines.append("")

    lines.append("## Per Kategorie")
    lines.append("")
    lines.append("| Kategorie | Endpoints | Anteil |")
    lines.append("|-----------|----------:|-------:|")
    for category, count in categories.most_common():
        label = CATEGORY_LABELS.get(category, category)
        share = count / len(endpoints) * 100 if endpoints else 0
        lines.append(f"| {label} (`{category}`) | {count} | {share:.1f}% |")
    lines.append("")

    lines.append("## Top-10-Provider nach Endpoints")
    lines.append("")
    lines.append("| Provider | Endpoints |")
    lines.append("|----------|----------:|")
    for provider, count in providers.most_common(10):
        lines.append(f"| {provider} | {count} |")
    lines.append("")

    lines.append("## Vollständiger Katalog (gruppiert nach Kategorie)")
    lines.append("")
    for category in sorted(by_category.keys()):
        label = CATEGORY_LABELS.get(category, category)
        lines.append(f"### {label} (`{category}`)")
        lines.append("")
        lines.append("| Service | Provider | Risk | Domains |")
        lines.append("|---------|----------|------|---------|")
        for ep in sorted(by_category[category], key=lambda e: e.service.lower()):
            domains = ", ".join(f"`{d}`" for d in ep.domains[:3])
            if len(ep.domains) > 3:
                domains += f" _(+{len(ep.domains) - 3} weitere)_"
            lines.append(
                f"| {ep.service} | {ep.provider} | {ep.risk_level} | {domains} |"
            )
        lines.append("")

    lines.append("## Frische-Hinweis")
    lines.append("")
    lines.append(
        "Die DB wird monatlich aktualisiert via "
        "`.github/workflows/endpoint-db-update.yml` (cron `0 6 1 * *`). "
        "Ein zusätzlicher Review-Issue wird via "
        "`.github/workflows/db-review-issue.yml` erzeugt. Bei Frische-Signal "
        "🟡/🔴 in der Settings-Page sollte ein DB-Review prioritisiert werden."
    )
    lines.append("")

    return "\n".join(lines) + "\n"


def _age_days(last_updated: str) -> int | None:
    try:
        parsed = datetime.strptime(last_updated, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None
    return (date.today() - parsed).days


def _freshness_emoji(age_days: int | None) -> str:
    if age_days is None:
        return "❓ Stand unbekannt"
    if age_days <= 35:
        return f"🟢 Aktuell ({age_days} Tage)"
    if age_days <= 70:
        return f"🟡 Review fällig ({age_days} Tage)"
    return f"🔴 Veraltet ({age_days} Tage)"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument(
        "--check", action="store_true",
        help="Vergleicht aktuellen Inhalt mit dem berechneten Report (Exit 1 bei Diff).",
    )
    parser.add_argument(
        "--output", type=Path, default=OUTPUT_PATH,
        help="Output-Pfad (default: docs/AI_COVERAGE.md)",
    )
    args = parser.parse_args()

    db = AIEndpointDatabase()
    body = render_markdown(db)

    if args.check:
        if not args.output.exists():
            print(f"FEHLT: {args.output} existiert nicht.", file=sys.stderr)
            return 1
        current = args.output.read_text(encoding="utf-8")
        # Datum-Zeile ist erwartungsgemäß tagesabhängig — ignorieren.
        if _strip_today_line(current) != _strip_today_line(body):
            print(
                f"DRIFT: {args.output} ist nicht synchron mit der DB. "
                "Bitte `python scripts/db_coverage_report.py` ausführen.",
                file=sys.stderr,
            )
            return 1
        print(f"OK: {args.output} synchron mit DB v{db.version}.")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(body, encoding="utf-8")
    print(f"Geschrieben: {args.output} ({len(body)} Zeichen, DB v{db.version})")
    return 0


def _strip_today_line(text: str) -> str:
    """Entfernt die 'Auto-generiert ... am YYYY-MM-DD'-Zeile fuer stabile Diffs."""
    return "\n".join(
        line for line in text.splitlines()
        if not line.startswith("_Auto-generiert via")
    )


if __name__ == "__main__":
    raise SystemExit(main())
