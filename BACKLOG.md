# Backlog — Telemetrie Analyzer

**Stand:** 2026-04-18
**Status:** Sprint 1+2+4 erledigt. 109 Tests grün. v0.1.0 in Vorbereitung.

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

## Sprint 4: Streamlit-UI ✔ (Branch, Merge steht aus)

| # | Aufgabe | Beschreibung | Status |
|---|---------|--------------|--------|
| 17 | Streamlit-Dashboard | `app.py` + `src/ui/pages/` (4 Pages: Overview, Findings, Compliance, Settings) + `src/ui/components/` (6 Components: Traffic-Light, KPI-Row, Badges, Upload-Widget, Framework-Card, Finding-Row). Commit `16c64f4` — Issue #5, noch nicht nach main gemerged. | in Branch |

## Offener Backlog (Sprint 5+)

| # | Aufgabe | Beschreibung | Status |
|---|---------|--------------|--------|
| 14 | Retention Management | Automatische Datenlöschung nach 90 Tagen (konfigurierbar). DSGVO Art. 5 (Speicherbegrenzung). | offen |
| 15 | CI/CD Pipeline | GitHub Actions für Tests & Linting auf jedem PR. | offen |
| 16 | Visualisierung (erweitert) | Plotly-Dashboards für Trends & Compliance-Scores über Zeit (ergänzend zu Sprint 4). | offen |
| 13 | CLI Entry Point (Reaktivierung) | Siehe Sprint 3. | offen |

---

## Test-Stand

**109 Tests grün** (Stand 2026-04-18), aufgeteilt in:
- MVP (Endpoints, Parser, Privacy, Detection, Generator): 37
- Compliance Engine: 21
- Claude API Analyzer: 10
- Squid Parser + Reports + UI: 41 (Summe)

Ausführung: `pytest tests/ -v` bzw. `wsl -e bash -c "cd /home/flowing1978/projects/telemetrie-analyzer && python3 -m pytest tests/ -v"`

---

## Nächster Schritt

1. **Release v0.1.0** — Sprint 4 (`sprint-4/streamlit-ui`) nach `main` mergen, CHANGELOG anlegen, Tag `v0.1.0` setzen, GitHub Release erstellen.
2. **Sprint 5 planen** — Priorisierung unter: CI/CD (GitHub Actions), Retention Management (DSGVO), CLI-Reaktivierung. Entscheidung nach Release.
