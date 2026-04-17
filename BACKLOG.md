# Backlog — Telemetrie Analyzer

**Stand:** 2026-03-16
**Status:** Phase 2 teilweise abgeschlossen (Compliance Engine + Claude API) – Proxy-Parser offen, Phase 3 steht an.

---

## Phase 1: MVP / Grundgerüst ✔

| # | Aufgabe | Beschreibung | Status |
|---|---------|--------------|--------|
| 1 | Projektstruktur anlegen | `src/`, `tests/`, `testdata/`, `config/`, `data/`, `templates/` + `pyproject.toml` | erledigt |
| 2 | AI Endpoint Database | 26 KI-Dienste in `data/ai_endpoints.json` – Domains, Kategorien, 4 Risikostufen. Python-Klasse mit exaktem/Subdomain-Matching (`src/database/ai_endpoints.py`) | erledigt |
| 3 | Log-Parser (Pi-hole DNS) | `src/parsers/pihole.py` – Syslog + FTL-CSV → pandas DataFrame, Domains normalisiert, IPs bei Import pseudonymisiert | erledigt |
| 4 | Privacy-Modul | `src/privacy/pseudonymizer.py` – HMAC-SHA256, deterministische Pseudonyme (`ip_`/`user_`-Prefix) | erledigt |
| 5 | Detection Engine (Basis) | `src/detection/engine.py` – Domain-Matching inkl. Subdomains, Frequenz-Analyse, Risk-Scoring (0-100), Gruppierung Client×Service | erledigt |
| 6 | Synthetische Testdaten | `src/testdata/generator.py` – Client-Profile, reproduzierbar via Seed. Sample: `testdata/pihole_sample.log` (207 KB) | erledigt |
| 7 | Tests (Phase 1) | 37 pytest-Tests für Endpoints, Parser, Privacy, Detection, Generator | erledigt |

## Phase 2: Compliance & Analyse

| # | Aufgabe | Beschreibung | Status |
|---|---------|--------------|--------|
| 8 | Compliance Engine | Framework-Mapping (DORA, EU AI Act, ISO 42001, ISO 27001, DSGVO), Scoring, Finding-Modell mit compliance_mappings. 15 Regeln, 5 Frameworks, 21 Tests. | erledigt |
| 9 | Claude API Integration | KI-gestützte Analyse der Findings via Anthropic SDK. Skip-Mode, strukturierter Prompt, JSON-Parsing. 10 Tests. | erledigt |
| 10 | Log-Parser (Proxy) | Squid / mitmproxy Parser, Volumen-Analyse (>500KB Upload = Dokument-Upload) | offen |

## Phase 3: Reporting

| # | Aufgabe | Beschreibung | Status |
|---|---------|--------------|--------|
| 11 | Report Generator | Jinja2-basierte Reports (HTML/Markdown/JSON) | offen |
| 12 | Report Templates | Drei Zielgruppen: Executive/CISO, IT-Security, Compliance | offen |
| 13 | CLI Entry Point | `python -m src.main --input <log> --format pihole --output report.html` | offen |

## Phase 4: Erweiterung

| # | Aufgabe | Beschreibung | Status |
|---|---------|--------------|--------|
| 14 | Retention Management | Automatische Datenlöschung nach 90 Tagen (konfigurierbar) | offen |
| 15 | CI/CD Pipeline | GitHub Actions für Tests & Linting | offen |
| 16 | Visualisierung | Plotly-Dashboards für Trends & Compliance-Scores | offen |

---

## Nächster Schritt

Phase 2 abschließen: Proxy-Parser (#10), dann Phase 3 (Reporting).
