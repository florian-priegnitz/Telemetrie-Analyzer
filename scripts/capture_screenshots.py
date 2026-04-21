"""Nimmt Screenshots der 6 Streamlit-Pages für README und Docs.

Erwartet eine bereits laufende Streamlit-Instanz auf ``http://localhost:8501``
(siehe ``make streamlit``). Klickt automatisch das Pi-hole-Demo-Scenario,
wartet auf die Analyse, und navigiert dann durch Übersicht, Findings,
Users & Patterns, Compliance, Formate, Einstellungen.

Output: ``docs/screenshots/<page>.png``.

Usage:
    python scripts/capture_screenshots.py
    python scripts/capture_screenshots.py --url http://localhost:8501
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "docs" / "screenshots"

# Page-Labels wie im Streamlit-Sidebar-Radio
PAGES = [
    ("overview",       "📊 Übersicht"),
    ("findings",       "🔍 Findings"),
    ("users_patterns", "👥 Users & Patterns"),
    ("compliance",     "📋 Compliance"),
    ("formats",        "📚 Formate"),
    ("settings",       "⚙️ Einstellungen"),
]

SCENARIO_BUTTON_TEXT = "🔥 Pi-hole"


async def capture(url: str) -> int:
    """Hauptlogik — startet Browser, navigiert, macht Screenshots."""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("playwright nicht installiert. pip install playwright && "
              "playwright install chromium", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1600, "height": 1100},
            device_scale_factor=2,
        )
        page = await context.new_page()

        print(f"→ Lade {url}")
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)

        await page.screenshot(path=str(OUT_DIR / "00_onboarding.png"), full_page=True)
        print("  ✓ 00_onboarding.png")

        print("→ Klicke Pi-hole-Scenario-Button")
        try:
            btn = page.get_by_role("button", name=SCENARIO_BUTTON_TEXT, exact=False).first
            await btn.click()
            await page.wait_for_timeout(1500)
        except Exception as exc:
            print(f"  ⚠ Scenario-Button nicht gefunden: {exc}", file=sys.stderr)

        print("→ Klicke Analyse starten")
        try:
            analyze_btn = page.get_by_role("button", name="🚀 Analyse starten").first
            await analyze_btn.click()
        except Exception:
            pass

        print("→ Warte auf Analyse-Ende")
        await page.wait_for_selector("text=✅ Analyse fertig", timeout=45000)
        await page.wait_for_timeout(2000)

        for key, label in PAGES:
            print(f"→ Navigiere zu {label}")
            try:
                radio = page.get_by_text(label, exact=True).first
                await radio.click()
                await page.wait_for_timeout(2500)
                out = OUT_DIR / f"{key}.png"
                await page.screenshot(path=str(out), full_page=True)
                print(f"  ✓ {out.name} ({out.stat().st_size/1024:.0f} KB)")
            except Exception as exc:
                print(f"  ⚠ {label} skipped: {exc}", file=sys.stderr)

        await browser.close()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://localhost:8501",
                        help="Streamlit-URL (default: http://localhost:8501)")
    args = parser.parse_args()
    return asyncio.run(capture(args.url))


if __name__ == "__main__":
    sys.exit(main())
