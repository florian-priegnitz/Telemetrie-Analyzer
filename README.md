# Telemetrie Analyzer

[![CI](https://github.com/florian-priegnitz/Telemetrie-Analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/florian-priegnitz/Telemetrie-Analyzer/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

KI-gestütztes Analyse-Tool zur Erkennung nicht-autorisierter KI-Nutzung (Shadow AI) in Unternehmensnetzen. Analysiert DNS- und Proxy-Logs, erkennt Muster und erzeugt regulatorisch eingebettete Reports nach **DORA, EU AI Act, ISO 42001, ISO 27001, DSGVO, EU CRA**.

## Was ist Schatten-KI?

**Schatten-KI** (Shadow AI) bezeichnet die Nutzung generativer KI-Dienste — ChatGPT, Claude, Gemini, Copilot, Cursor, Perplexity, Hugging Face und weitere — *ohne* freigegebenen Vertrag, ohne Auftragsverarbeitung und außerhalb des etablierten IT-Prozesses. Mitarbeitende laden Code, Kundendaten oder Konzepte in Drittsysteme — meist gut gemeint, regulatorisch aber riskant: **DORA Art. 28** (Third-Party-Risiko), **EU AI Act Art. 6** (Risikoklassen), **DSGVO Art. 6** (Rechtsgrundlage) und **ISO 27001 A.5.23** (Cloud-Services) fordern eine belastbare Aussage darüber, *welche* KI-Dienste im Unternehmen aktiv sind.

Der Telemetrie Analyzer beantwortet diese Frage **ohne Endpoint-Agent** — rein aus DNS-, Proxy- und SIEM-Telemetrie, die in Enterprise-Umgebungen ohnehin anfällt. Pseudonymisierung greift bereits im Parser (DSGVO Art. 25 — Privacy by Design), nicht erst im Report.

## Get Started in 2 Commands

```bash
git clone https://github.com/florian-priegnitz/Telemetrie-Analyzer.git && cd Telemetrie-Analyzer
docker compose up --build
```

→ UI unter **http://localhost:8501** · Walkthrough: [docs/QUICKSTART.md](docs/QUICKSTART.md) · Alternativen (venv, headless): [INSTALLATION.md](INSTALLATION.md)

## UI-Tour

Der Analyzer bietet 6 Pages im Streamlit-Dashboard. **Ein-Klick-Demo**: einer der 12 Scenario-Buttons auf der Willkommensseite lädt ein synthetisches Sample und startet die Pipeline.

```
┌─────────────────────────────────┐   ┌──────────────────────────────────────────┐
│ 🛡️ Telemetrie Analyzer           │   │ 👋 Willkommen beim Telemetrie Analyzer   │
│ Shadow AI Detection · DORA · …  │   │                                          │
│                                 │   │ 🎬 Direkt mit einem Demo starten         │
│ 📁 Log-Upload                   │   │                                          │
│   [Browse files]                │   │ [🔥 Pi-hole (größtes Sample)        ]   │
│   Pi-hole · Squid · Zscaler ·   │   │ [Squid Proxy (~1700 Events)         ]   │
│   PAN-OS · Umbrella · FortiGate │   │ [Netskope CASB — angereichert (100) ]   │
│   AWS VPC · Entra · Cloudflare  │   │ [Windows Sysmon — angereichert (80) ]   │
│   · Netskope · Sysmon · ECS     │   │ [Elastic ECS — angereichert (80)    ]   │
│                                 │   │ … (12 Scenarios total)                   │
│ ▾ 🎬 Demo-Scenario              │   │                                          │
│                                 │   │ 📖 Oder eigenes Log hochladen            │
│ Navigation                      │   │ • Upload links, 12 Formate Auto-Detect   │
│   ○ 📊 Übersicht                │   │ • .log / .csv / .json / .jsonl / .ndjson │
│   ○ 🔍 Findings                 │   │ • Pseudonymisierung schon im Parser      │
│   ○ 👥 Users & Patterns          │   │                                          │
│   ○ 📋 Compliance                │   │ Siehe 📚 Formate für Feld-Mapping        │
│   ○ 📚 Formate                   │   └──────────────────────────────────────────┘
│   ○ ⚙️ Einstellungen             │
│                                 │
│ Status: ✅ Analyse fertig        │
│ Pseudonym: ✓ AKTIV · Salt-FP    │
└─────────────────────────────────┘
```

### Die 6 Pages

| Page | Zweck |
|------|-------|
| **📊 Übersicht** | KPI-Row, Compliance-Ampel über 5 Frameworks, Score-Bar pro Framework, Top-3-Risiken. Enthält den **📥 Report-Export-Button** (HTML/Markdown/JSON pro Zielgruppe) |
| **🔍 Findings** | Filterbare Tabelle aller Findings mit Drill-Down-Expandern (Domains, Compliance-Mappings, Upload-Events) |
| **👥 Users & Patterns** | Top-10-Client-Ranking, pseudonymisierte Stunden-Heatmap (24×N) mit Off-Hours-Schattierung, k-Anonymitäts-Banner |
| **📋 Compliance** | 5 Tabs (DORA / EU AI Act / ISO 42001 / ISO 27001 / DSGVO) mit Score-Cards und Mapping-Tabellen pro Artikel/Control |
| **📚 Formate** | Systematische Vorstellung der 12 Log-Formate — Quelle, Beispiel-Zeile, Feld-Mapping Input→Common-Schema, Sample-Downloads |
| **⚙️ Einstellungen** | Salt-Override (triggert Hard-Reset), Retention-Policy-Anzeige, Privacy-Self-Check, Detection-Schwellwerte |

Screenshots werden via [Playwright](scripts/capture_screenshots.py) generiert — siehe [docs/screenshots/README.md](docs/screenshots/README.md).

## Features

- **12 Parser für DNS- / Proxy- / Identity-Logs** — Pi-hole, Squid, Zscaler, Palo Alto, Cisco Umbrella, Fortinet, AWS VPC Flow, Azure Entra ID, Cloudflare Gateway, Netskope CASB, Windows Sysmon, Elastic ECS
- **Detection Engine** mit Risk-Scoring (0–100), systematischer Nutzung, Document-Upload-Erkennung (>500 KB), 4-Stufen-Matching (Subdomain → Alias → Service-IP → ASN-Provider-CIDR opt-in)
- **Behavior Analytics** — Off-Hours-Detection, Burst-Detection, Stunden-Heatmap, k-Anonymitäts-Guard, Session-Korrelations-Graph (networkx)
- **HMAC-SHA256 Pseudonymisierung** (DSGVO Art. 25 — Privacy by Design), Squid-`%un`-Username-Parsing als DSFA-Double-Opt-in
- **Compliance Engine** — 22 Regeln über **6 Frameworks**, pro Finding auswertbar je Artikel/Control
- **Pluggable LLM-Backend** — Anthropic Cloud oder **Ollama Offline** (`LLM_BACKEND ∈ {anthropic, ollama, skip}`); Skip-Mode für Air-Gap-Setups. Siehe [docs/OFFLINE_AI.md](docs/OFFLINE_AI.md)
- **Report-Generator** (HTML, Markdown, JSON) mit 3 Zielgruppen-Templates: Executive, IT-Security, Compliance
- **Streamlit-Dashboard** — 7 Pages (Übersicht, Findings, Users & Patterns, Sessions, Compliance, Formate, Einstellungen), interaktive Filter, Drill-Down, Privacy-Self-Check
- **Retention Management** — konfigurierbare Auto-Löschung (DSGVO Art. 5)
- **692+ Tests** (pytest, CI-grün auf Python 3.11 + 3.12)

### Unterstützte Logformate

12 Parser mit Auto-Detect — Upload-Dialog erkennt das Format an Header, Token-Layout oder Schlüsselwörtern:

| Quelle | Typ | Endung | Auto-Detect-Hinweis |
|---|---|---|---|
| Pi-hole | DNS | `.log` (Syslog) / `.csv` (FTL) | Token `dnsmasq[` |
| Squid | Web-Proxy | `.log` (Native + Common) | Whitespace-Token-Layout |
| Zscaler ZIA | Web-Proxy | `.log` (NSS) | LEEF-Header |
| Palo Alto PAN-OS | URL-Filtering | `.log` (Syslog) | `PAN-OS,` Position 1–3 |
| Cisco Umbrella | DNS-Security | `.csv` | `identity_type`-Spalte |
| Fortinet FortiGate | Webfilter | `.log` (key=value) | `eventtime=` |
| AWS VPC Flow | Network | `.log` (v2/v5) | Spalten-Header v2/v5 |
| Azure Entra ID | Sign-In | `.json` / `.jsonl` | `appDisplayName` |
| Cloudflare Gateway | DNS + HTTP | `.ndjson` (Logpush) | `EventTimestamp` |
| Netskope CASB | CASB | `.json` (NDJSON) | `activity` |
| Windows Sysmon | Endpoint | `.log` / `.json` | EventID 22 (DNS) |
| Elastic ECS | SIEM | `.json` | `@timestamp` + `event.module` |

Feld-Mapping pro Parser zeigt die UI-Page **📚 Formate** (Quelle → Common-Schema). Sample-Dateien für jeden Parser liegen unter [testdata/](testdata/).

### Was wird konkret erkannt?

| Erkennung | Schwelle / Logik | Output-Flag |
|---|---|---|
| **Systematische Nutzung** | `>10 Requests/Tag` pro Client × Service | `is_systematic=true` |
| **Dokument-Upload** | `>500 KB` pro Request an KI-Endpoint | `has_document_upload=true` |
| **Off-Hours-Aktivität** | Anteil außerhalb 08–18 Uhr (Wochentag konfigurierbar) | `off_hours_ratio` (0–1) |
| **Bursts** | kurzfristige Frequenz-Spitzen, Sliding-Window | `burst_count` |
| **Service-Kombinationen** | Co-Occurrence-Graph in 30-Min-Window (z. B. *ChatGPT + Cursor + Claude*) | `session_pairs[]` |
| **Provider-Fallback** | Domain unbekannt, IP in Provider-CIDR (Anthropic / OpenAI / Google / AWS / Azure) — opt-in | `detection_confidence=low` |
| **Risk-Score** | aggregiert obige Signale + Service-Risikoklasse | `risk_score` (0–100) |

## Funktionsweise

Die Pipeline läuft in fünf strikt getrennten Stages — gleichzeitig die Verantwortungs-Grenzen für Tests und Privacy-Invarianten:

```
Input (DNS/Proxy/SIEM) → Parser → AI Endpoint DB → Detection → Compliance
                                                                    ↓
                              Report Generator + LLM Analyzer (Anthropic | Ollama | Skip)
                                       ↓
                          ./reports/  •  Streamlit-Dashboard
```

1. **Parser** — 12 Format-Adapter normalisieren auf ein Common-Schema (`timestamp, client, domain, …`). IPs und (opt-in) Usernames werden hier mit HMAC-SHA256 pseudonymisiert; Rohwerte erreichen nie ein DataFrame.
2. **AI Endpoint Database** — 178 Endpoints, versioniert unter `data/versions/`. 4-Stufen-Matching: exact → subdomain → service-IP → ASN-Provider-CIDR (opt-in).
3. **Detection Engine** — berechnet Risk-Score 0–100 pro `client × service`, taggt systematische Nutzung, Dokument-Upload, Off-Hours, Bursts und Service-Co-Occurrence.
4. **Compliance Engine** — 22 Regeln über 6 Frameworks; jedes Finding trägt `compliance_mappings[]` mit `framework`, `control_id`, `severity`, `assessment_status`.
5. **Report Generator + LLM Analyzer** — Jinja2-Templates für 3 Zielgruppen × 3 Formate (HTML/Markdown/JSON). LLM-Analyse pluggable: **Anthropic Cloud** (Default mit `ANTHROPIC_API_KEY`), **Ollama Offline** (KRITIS / Air-Gap), **Skip** (kein LLM-Aufruf). Vor jedem Report-Write greift `assert_no_plaintext()` als Defense-in-Depth.

Kernprinzip: **Compliance-First** — Findings sind auswertbar pro Framework, Kontrolle, Zeitraum und Risiko, nicht nur als technische Liste.

## Tools × Reports

Pro Parser ist ein vorgeneriertes Beispiel-Bundle unter [examples/test_reports/](examples/test_reports/) committed. Die Klassifikation legt fest, welche Reports pro Parser sinnvoll sind:

- **A** *Pflicht* — Demo-/Audit-Standard (committed + CI-verifiziert)
- **B** *Interessant* — SIEM-/GRC-Integration (committed, `.gitattributes linguist-generated=true`)
- **C** *Redundant* — gleicher Inhalt wie A/B in anderem Format (NICHT committed, lokal reproduzierbar)
- **D** *Raus* — Datenlage des Parsers reicht nicht für sinnvollen Report

| Parser | Exec HTML | Exec MD | Exec JSON | ITSec HTML | ITSec MD | ITSec JSON | Comp HTML | Comp MD | Comp JSON |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| [pihole](examples/test_reports/pihole/) | A | B | D | A | B | B | A | A | B |
| [squid](examples/test_reports/squid/) | A | B | D | A | B | B | A | A | B |
| [zscaler](examples/test_reports/zscaler/) | A | B | D | A | B | B | A | A | B |
| [paloalto](examples/test_reports/paloalto/) | A | B | D | A | B | B | A | A | B |
| [umbrella](examples/test_reports/umbrella/) | A | B | D | A | B | B | A | A | B |
| [fortinet](examples/test_reports/fortinet/) | A | B | D | A | B | B | A | A | B |
| [aws_vpc_flow](examples/test_reports/aws_vpc_flow/) | A | B | D | A | B | B | B | C | C |
| [entra_id](examples/test_reports/entra_id/) | A | C | D | A | B | B | A | A | B |
| [cloudflare_gateway](examples/test_reports/cloudflare_gateway/) | A | B | D | A | B | B | A | A | B |
| [netskope](examples/test_reports/netskope/) | A | B | D | A | B | B | A | A | B |
| [sysmon](examples/test_reports/sysmon/) | B | D | D | A | B | B | A | A | B |
| [elastic_ecs](examples/test_reports/elastic_ecs/) | A | C | D | A | B | B | A | A | C |

**Hinweis Exec JSON:** Alle 12 Parser haben hier `D` — Vorstände konsumieren keine maschinenlesbaren Reports. JSON-Bedarf liegt bei IT-Security (SIEM/SOAR) und Compliance (GRC-Tools).

**KRITIS-KMU 50-User-Sonderfall (Squid):** Vollständiges Demo-Set unter [examples/test_reports/squid/kritis_kmu_50users_*](examples/test_reports/squid/) — alle 9 Zellen sind A. Realistischer KRITIS-KMU-Datensatz (15 Heavy / 20 Systematic / 10 Casual / 5 Clean User über 14 Tage). Reproduzierbar via:

```bash
python scripts/generate_example_reports.py            # alle 86 Files
python scripts/generate_example_reports.py --check    # nur Existenz prüfen
```

## Python-API (headless)

```python
from pathlib import Path
from src.parsers.pihole import parse_pihole_log
from src.privacy.pseudonymizer import Pseudonymizer
from src.detection.engine import DetectionEngine
from src.compliance.engine import ComplianceEngine
from src.reports import ReportGenerator

df = parse_pihole_log(Path("testdata/pihole_sample.log"),
                      pseudonymizer=Pseudonymizer(key=b"my-salt"))
detection = DetectionEngine().analyze(df)
compliance = ComplianceEngine().analyze(detection)

gen = ReportGenerator(detection, compliance, salt="my-salt")
gen.write(Path("reports/"), audience="all", format="html")
gen.write(Path("reports/"), format="json")
```

## Testdaten

```bash
python -m src.testdata.generator --scenario enterprise-mixed --format both --seed 42
python -m src.testdata.generator --scenario all --format both          # alle 5 Szenarien
```

Szenario-Profile: `clean`, `low-risk`, `systematic`, `upload-leak`, `enterprise-mixed` — jedes trifft eine andere Detection-Schwelle. Details: [docs/QUICKSTART.md](docs/QUICKSTART.md).

Alle Profile sind seed-reproduzierbar und rein synthetisch (RFC1918-IPs).

## Privacy by Design

- **HMAC-SHA256-Pseudonymisierung** aller IPs/User beim Parsing
- **Defense-in-Depth:** Engine pseudonymisiert + Generator pseudonymisiert (separater Salt) + Post-Render-Check `assert_no_plaintext()` verbietet IPv4/IPv6/MAC/`*.local|.lan|.corp`-Hostnames im Output
- **Salt-Konfiguration** via `REPORT_SALT` / `PSEUDONYM_SALT` ENV-Var (siehe [.env.example](.env.example))
- **Disclaimer-Block** in jedem Report mit Salt-Fingerprint (8 Hex), kein Salt-Leak
- **Retention:** Standard 90 Tage, konfigurierbar via `config/retention.yaml`
- **Uploaded Bytes** werden nach erfolgreicher Pipeline aus dem Session-State verworfen

### Warum Salt?

Pseudonymisierung mit einem geheimen, je Auftrag wechselnden Salt ist die rechtlich tragende Variante (DSGVO Art. 25 / Art. 32) — nicht reines Hashing.

- **Deterministik innerhalb einer Analyse** — gleicher Client erscheint als gleiches Pseudonym, sodass Verhaltens-Korrelation (systematische Nutzung, Bursts, Sessions) erhalten bleibt.
- **Trennung zwischen Analysen** — neuer Salt = nicht mehr herleitbare Hashes. Das setzt die DSGVO-Zweckbindung (Art. 5 Abs. 1 lit. b) technisch um: Pseudonyme aus Auftrag A sind in Auftrag B unbrauchbar.
- **HMAC statt einfaches SHA-256** — IP-Bereiche sind klein und vorhersagbar (`10.0.0.0/8`, `192.168.0.0/16`). Ohne Salt würde eine Rainbow-Table aller IPv4-Adressen jedes Pseudonym binnen Sekunden brechen. HMAC mit geheimem Salt verhindert das.
- **Salt-Wechsel als Notbremse** — die Settings-Page erzwingt bei Salt-Override einen Pipeline-Hard-Reset. Alte Pseudonyme der Session sind danach nicht mehr herleitbar.

Vollständig: [docs/PRIVACY.md](docs/PRIVACY.md) (Pseudonymisierung, k-Anonymität, DSFA-Checkliste für Squid-`%un`-Username-Parsing).

## Compliance-Frameworks

| Framework | Relevante Kontrollen | Auswertung |
|-----------|---------------------|------------|
| **DORA** | Art. 5, 6, 28 | Third-Party-Risiko, Vertragslücken |
| **EU AI Act** | Art. 6, 9, 53 | Risikoklassifizierung pro Tool |
| **ISO 42001** | 6.1.2, 8.4 | KI-Inventar-Vollständigkeit |
| **ISO 27001** | A.5.9, A.5.23, A.8.16 | Asset-Abdeckung, Monitoring-Gaps |
| **DSGVO** | Art. 5, 6, 25, 32, 35 | Datentransfer-Risiko, DSFA-Bedarf |
| **EU CRA** (Reg. 2024/2847) | 7 Controls (`mappings/cra.yaml`) | Cyber Resilience, Vulnerability Disclosure |

## Dokumentation

- [docs/QUICKSTART.md](docs/QUICKSTART.md) — 10-Minuten-Walkthrough mit UI
- [docs/OFFLINE_AI.md](docs/OFFLINE_AI.md) — Ollama-Setup für Air-Gap- / KRITIS- / DSGVO-Szenarien
- [docs/PRIVACY.md](docs/PRIVACY.md) — Privacy-Engineering, DSFA, Pseudonymisierung
- [docs/screenshots/CHECKLIST.md](docs/screenshots/CHECKLIST.md) — 21 PNGs für Demo-Doku
- [INSTALLATION.md](INSTALLATION.md) — Docker / venv / Windows / Python-API
- [CONTRIBUTING.md](CONTRIBUTING.md) — Branch-/PR-Konvention, Privacy-Invarianten
- [SECURITY.md](SECURITY.md) — Responsible Disclosure, Security-Modell
- [CHANGELOG.md](CHANGELOG.md) — Release-Historie
- [CLAUDE.md](CLAUDE.md) — Architektur-Details für Claude-Code-Assistenten
- [BACKLOG.md](BACKLOG.md) — Sprint-Plan + offene Items

## License

[MIT](LICENSE) · Maintainer: Florian Priegnitz · Issues: [github.com/florian-priegnitz/Telemetrie-Analyzer/issues](https://github.com/florian-priegnitz/Telemetrie-Analyzer/issues)
