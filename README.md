# Telemetrie Analyzer

[![CI](https://github.com/florian-priegnitz/Telemetrie-Analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/florian-priegnitz/Telemetrie-Analyzer/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

KI-gestütztes Analyse-Tool zur Erkennung nicht-autorisierter KI-Nutzung (Shadow AI) in Unternehmensnetzen. Analysiert DNS- und Proxy-Logs, erkennt Muster und erzeugt regulatorisch eingebettete Reports nach **DORA, EU AI Act, ISO 42001, ISO 27001, DSGVO**.

## Get Started in 2 Commands

```bash
git clone https://github.com/florian-priegnitz/Telemetrie-Analyzer.git && cd Telemetrie-Analyzer
docker compose up --build
```

→ UI unter **http://localhost:8501** · Walkthrough: [docs/QUICKSTART.md](docs/QUICKSTART.md) · Alternativen (venv, headless): [INSTALLATION.md](INSTALLATION.md)

## Features

- **10 Parser für DNS- und Proxy-Logs** — Pi-hole, Squid, Zscaler, Palo Alto, Cisco Umbrella, Fortinet, AWS VPC Flow, Azure Entra ID, Cloudflare Gateway, Netskope CASB
- **Detection Engine** mit Risk-Scoring (0–100), systematischer Nutzung, Document-Upload-Erkennung (>500 KB)
- **Behavior Analytics** — Off-Hours-Detection, Burst-Detection, Stunden-Heatmap, k-Anonymitäts-Guard
- **HMAC-SHA256 Pseudonymisierung** (DSGVO Art. 25 — Privacy by Design)
- **Compliance Engine** — 15 Regeln über 5 Frameworks, pro Finding auswertbar je Artikel/Control
- **Claude API Analyzer** (optional, Skip-Mode verfügbar)
- **Report-Generator** (HTML, Markdown, JSON) mit 3 Zielgruppen-Templates: Executive, IT-Security, Compliance
- **Streamlit-Dashboard** — 5 Pages (Übersicht, Findings, Users & Patterns, Compliance, Einstellungen), interaktive Filter, Drill-Down, Privacy-Self-Check
- **Retention Management** — konfigurierbare Auto-Löschung (DSGVO Art. 5)
- **336+ Tests** (pytest, CI-grün)

## Ein-Satz-Architektur

```
Input (DNS/Proxy-Logs) → Parser → AI Endpoint Database (160 Endpoints)
 → Detection Engine → Compliance Engine → (Claude Analyzer opt.)
 → Report Generator (HTML/MD/JSON)  ─┬→  ./reports/
 → Streamlit Dashboard (interaktiv) ─┘
```

Kernprinzip: **Compliance-First** — jedes Finding trägt `compliance_mappings` und ist damit auswertbar pro Framework, pro Kontrolle, pro Zeitraum, pro Risiko.

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

## Compliance-Frameworks

| Framework | Relevante Kontrollen | Auswertung |
|-----------|---------------------|------------|
| **DORA** | Art. 5, 6, 28 | Third-Party-Risiko, Vertragslücken |
| **EU AI Act** | Art. 6, 9, 53 | Risikoklassifizierung pro Tool |
| **ISO 42001** | 6.1.2, 8.4 | KI-Inventar-Vollständigkeit |
| **ISO 27001** | A.5.9, A.5.23, A.8.16 | Asset-Abdeckung, Monitoring-Gaps |
| **DSGVO** | Art. 5, 6, 25, 32, 35 | Datentransfer-Risiko, DSFA-Bedarf |

## Dokumentation

- [docs/QUICKSTART.md](docs/QUICKSTART.md) — 10-Minuten-Walkthrough mit UI
- [INSTALLATION.md](INSTALLATION.md) — Docker / venv / Windows / Python-API
- [CONTRIBUTING.md](CONTRIBUTING.md) — Branch-/PR-Konvention, Privacy-Invarianten
- [SECURITY.md](SECURITY.md) — Responsible Disclosure, Security-Modell
- [CHANGELOG.md](CHANGELOG.md) — Release-Historie
- [CLAUDE.md](CLAUDE.md) — Architektur-Details für Claude-Code-Assistenten

## License

[MIT](LICENSE) · Maintainer: Florian Priegnitz · Issues: [github.com/florian-priegnitz/Telemetrie-Analyzer/issues](https://github.com/florian-priegnitz/Telemetrie-Analyzer/issues)
