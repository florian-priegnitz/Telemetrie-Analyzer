# Screenshots

Screenshots werden über Playwright headless automatisiert erzeugt:

```bash
# Einmalig: Chromium-System-Libs installieren
sudo apt install -y libnspr4 libnss3 libasound2 libatk-bridge2.0-0 libxss1 libgtk-3-0

# Streamlit starten (separater Terminal)
make streamlit

# Screenshots generieren
python scripts/capture_screenshots.py
```

Das Skript klickt automatisch das Pi-hole-Demo-Scenario, wartet auf die
Analyse und macht pro Page einen Full-Page-Screenshot:

- `00_onboarding.png` — Willkommens-Screen mit Demo-Buttons
- `overview.png` — Übersicht mit KPIs + Compliance-Ampel + Export-Panel
- `findings.png` — Findings-Tabelle + Filter-Sidebar + Detail-Expander
- `users_patterns.png` — Top-10-Ranking + Stunden-Heatmap
- `compliance.png` — 5 Framework-Tabs mit Score-Cards
- `formats.png` — Format-Katalog mit Feld-Mapping
- `settings.png` — Salt-Override + Retention-Policy + Privacy-Self-Check

**In CI** (GitHub Actions) kann `xvfb-run python scripts/capture_screenshots.py`
genutzt werden (siehe `.github/workflows/docs.yml` als TODO für v1.1).
