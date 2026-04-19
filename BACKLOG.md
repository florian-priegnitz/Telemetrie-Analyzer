# Backlog — Telemetrie Analyzer

**Stand:** 2026-04-19
**Status:** Sprint 1+2+4+6 implementiert + 5 Review-Blocker gefixt. 161 Tests grün. v0.1.0 release-bereit.

---

## Sprint 0: MVP / Grundgerüst ✔

| # | Aufgabe | Beschreibung | Status |
|---|---------|--------------|--------|
| 1 | Projektstruktur anlegen | `src/`, `tests/`, `testdata/`, `config/`, `data/`, `templates/` + `pyproject.toml` | erledigt |
| 2 | AI Endpoint Database | 26 KI-Dienste in `data/ai_endpoints.json` – Domains, Kategorien, 4 Risikostufen. Python-Klasse mit exaktem/Subdomain-Matching (`src/database/ai_endpoints.py`) | erledigt |
| 3 | Log-Parser (Pi-hole DNS) | `src/parsers/pihole.py` – Syslog + FTL-CSV → pandas DataFrame, Domains normalisiert, IPs bei Import pseudonymisiert | erledigt |
| 4 | Privacy-Modul | `src/privacy/pseudonymizer.py` – HMAC-SHA256, deterministische Pseudonyme (`ip_`/`user_`-Prefix) | erledigt |
| 5 | Detection Engine (Basis) | `src/detection/engine.py` – Domain-Matching inkl. Subdomains, Frequenz-Analyse, Risk-Scoring (0-100), Gruppierung Client×Service | erledigt |
| 6 | Synthetische Testdaten | `src/testdata/generator.py` – Client-Profile, reproduzierbar via Seed. Sample: `testdata/pihole_sample.log` (207 KB) | erledigt |
| 7 | Tests (MVP) | 37 pytest-Tests für Endpoints, Parser, Privacy, Detection, Generator | erledigt |

## Phase 2: Compliance & Analyse ✔

| # | Aufgabe | Beschreibung | Status |
|---|---------|--------------|--------|
| 8 | Compliance Engine | Framework-Mapping (DORA, EU AI Act, ISO 42001, ISO 27001, DSGVO), Scoring, Finding-Modell mit `compliance_mappings`. 15 Regeln, 5 Frameworks, 21 Tests. | erledigt |
| 9 | Claude API Integration | KI-gestützte Analyse der Findings via Anthropic SDK. Skip-Mode, strukturierter Prompt, JSON-Parsing. 10 Tests. | erledigt |

## Sprint 1: Proxy-Parser ✔

| # | Aufgabe | Beschreibung | Status |
|---|---------|--------------|--------|
| 10 | Log-Parser (Proxy) | `src/parsers/squid.py` – Squid Native + Common Log Format, konfigurierbar via `config/squid_logformat.conf`, Volumen-Detection >500KB = Dokument-Upload. Commit `f8afe90` (PR #4). | erledigt |

## Sprint 2: Reporting ✔

| # | Aufgabe | Beschreibung | Status |
|---|---------|--------------|--------|
| 11 | Report Generator | `src/reports/generator.py` – Jinja2-basierte Reports (HTML/Markdown/JSON), DSGVO-Schutzschicht (`src/reports/privacy.py`). Commit `51b89b6` (PR #6). | erledigt |
| 12 | Report Templates | 12 Jinja2-Templates in `src/reports/templates/`: 3 Zielgruppen (Executive/CISO, IT-Security, Compliance) × 2 Formate (HTML + Markdown) + Partials (Header, Footer, Disclaimer, Finding-Table, Framework-Card). | erledigt |

## Sprint 3: CLI Entry Point ⏸ zurückgestellt

| # | Aufgabe | Beschreibung | Status |
|---|---------|--------------|--------|
| 13 | CLI Entry Point | `python -m src.main --input <log> --format pihole --output report.html` — Issue #3. **Zurückgestellt** zugunsten UI-First-Strategie (Sprint 4 Streamlit-UI). Reaktivierung als Sprint-5-Kandidat. | zurückgestellt |

## Sprint 4: Streamlit-UI ✔

| # | Aufgabe | Beschreibung | Status |
|---|---------|--------------|--------|
| 17 | Streamlit-Dashboard | `app.py` + `src/ui/pages/` (4 Pages: Overview, Findings, Compliance, Settings) + `src/ui/components/` (6 Components: Traffic-Light, KPI-Row, Badges, Upload-Widget, Framework-Card, Finding-Row). Commit `16c64f4` (PR #5). | erledigt |

## Sprint 6: Behavior Analytics (Epic E2) — 4/7 erledigt

| # | Aufgabe | Beschreibung | Status |
|---|---------|--------------|--------|
| E2-1 | Hourly-Heatmap-Analyzer | `src/analytics/temporal.py` — `build_hourly_heatmap(df, by_service=False)` (Client × Stunde-Matrix). Issue #18. Commit `c98dde6`. | erledigt |
| E2-2 | Off-Hours-Detection + Risk-Boost | `off_hours_ratio()` + `+15` Boost in Detection-Engine bei `off_hours_ratio > 0.3`. Default Business-Hours 06–22 Uhr. Issue #19. | erledigt |
| E2-3 | Burst-Detection | `src/analytics/bursts.py` — `detect_bursts(df, window_minutes=5, threshold=50)` via Sliding-Window, mergt überlappende Bursts. Issue #20. | erledigt |
| E2-4 | Streamlit-Page 'Users & Patterns' | `src/ui/pages/users_patterns.py` — Top-10-Ranking, pseudonymisierte Heatmap mit Off-Hours-Schattierung, Drill-Down pro Client, k-Anonymitäts-Banner. Issue #21. | erledigt |
| E2-5 | Squid Username-Parsing (`%un`) | Privacy-sensibel. **Verschoben** bis echter Squid-Parser `%un`-Feld konsumiert; DSFA-Review bei Reaktivierung. Issue #22. | verschoben |
| E2-6 | Session-Korrelation | Parallel genutzte Services pro Client. Eigenständiges Item für Sprint 7. Issue #23. | verschoben |
| E2-7 | k-Anonymitäts-Guard | `src/privacy/k_anonymity.py` — Soft-Check mit `KAnonymityCheck` + `reidentification_risk`-Stufen (low/medium/high). UI-Banner in E2-4. Issue #24. | erledigt |

## Offener Backlog (Sprint 7+)

| # | Aufgabe | Beschreibung | Status |
|---|---------|--------------|--------|
| 14 | Retention Management | Automatische Datenlöschung nach 90 Tagen (konfigurierbar). DSGVO Art. 5 (Speicherbegrenzung). | offen |
| 15 | CI/CD Pipeline | GitHub Actions für Tests & Linting auf jedem PR. | offen |
| 16 | Visualisierung (erweitert) | Plotly-Dashboards für Trends & Compliance-Scores über Zeit (ergänzend zu Sprint 4). | offen |
| 13 | CLI Entry Point (Reaktivierung) | Siehe Sprint 3. | offen |
| E2-5 | Squid Username-Parsing (`%un`) | Privacy-Review nötig, blockiert bis Squid-Parser `%un`-Feld konsumiert. | verschoben |
| E2-6 | Session-Korrelation | Parallel genutzte Services pro Client (eigener Epic-Chunk). | verschoben |
| — | **Epic E1-3** AI Endpoint DB v3 | HR/Recruiting, Browser-Extensions, Customer-Support-AI + Copilot-Familie. Ziel: DB von 160 → ~360. Siehe Plan `erweiterung-backlog-telemetrie-analyzer`. | geplant |

---

## Test-Stand

**161 Tests grün** (Stand 2026-04-19), aufgeteilt u.a. in:
- MVP (Endpoints, Parser, Privacy, Detection, Generator): 37
- Compliance Engine: 21
- Claude API Analyzer: 10
- Squid Parser + Reports: ~29
- Streamlit-UI-Smoketests: 9 (inkl. 3 Users-&-Patterns-Tests)
- Behavior Analytics (Heatmap, Off-Hours, Bursts, k-Anon): 18
- Testdata-Szenarien + weitere: Rest

Ausführung: `pytest tests/ -v` bzw. `wsl -e bash -c "cd /home/flowing1978/projects/telemetrie-analyzer && python3 -m pytest tests/ -v"`

---

## Nächster Schritt

1. **Sprint 6 Merge** — Branch `sprint-6/behavior-analytics` nach `main`, anschließend v0.1.0 taggen.
2. **Sprint 7 planen** — Optionen:
   - Epic E1-3: AI Endpoint DB v3 (HR/Recruiting, Browser-Extensions, Customer-Support) → `plans/erweiterung-backlog-telemetrie-analyzer…`
   - CI/CD Pipeline (Issue #37)
   - Retention Management (Issue #38)
   - E2-6 Session-Korrelation (Issue #23)
