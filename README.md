# Telemetrie Analyzer

KI-gestütztes Analyse-Tool zur Erkennung nicht-autorisierter KI-Nutzung (Shadow AI) in Unternehmensnetzen. Analysiert DNS- und Proxy-Logs, erkennt Muster und erzeugt regulatorisch eingebettete Reports nach **DORA, EU AI Act, ISO 42001, ISO 27001, DSGVO**.

**Repo:** https://github.com/florian-priegnitz/Telemetrie-Analyzer

## Features

- **Pi-hole DNS-Parser** (Syslog + FTL-CSV)
- **Squid Proxy-Parser** (native + common log) mit **Volumen-Detection** (>500 KB Upload = `document_upload`)
- **Detection Engine** mit Risk-Scoring (0-100), systematische Nutzung, Document-Upload-Erkennung
- **HMAC-SHA256 Pseudonymisierung** (DSGVO Art. 25 — Privacy by Design)
- **Compliance Engine** mit 15 Regeln über 5 Frameworks
- **Claude API Analyzer** (optional, Skip-Mode verfügbar)
- **Report-Generator** (HTML, Markdown, JSON) mit 3 Zielgruppen-Templates: Executive, IT-Security, Compliance
- **Streamlit-Dashboard** — interaktive UI mit Filter, Drill-Down, Privacy-Self-Check
- **109 Tests** (pytest, alle grün)

## Quickstart

### Setup

```bash
git clone https://github.com/florian-priegnitz/Telemetrie-Analyzer.git
cd Telemetrie-Analyzer
pip install -e .
```

### Synthetische Testdaten generieren

```bash
# Legacy-Default (gemischter Traffic):
python -m src.testdata.generator --format both --days 7 --queries-per-day 500
# → testdata/pihole_sample.log + testdata/squid_sample.log

# Szenario-basiert (gezielt für Detection-Schwellen):
python -m src.testdata.generator --scenario enterprise-mixed --format both
python -m src.testdata.generator --scenario all --format both
# → testdata/scenarios/{name}_pihole.log + {name}_squid.log
```

**Szenario-Profile** — jedes trifft eine andere Detection-Schwelle
(`SYSTEMATIC_THRESHOLD=10` Req/Tag, `UPLOAD_THRESHOLD_BYTES=500 KB`):

| Szenario | Zweck | Erwartetes Ergebnis |
|----------|-------|---------------------|
| `clean` | Baseline ohne KI-Nutzung | 0 Findings |
| `low-risk` | Gelegentliche medium-risk Services (DeepL, Grammarly) | Findings, aber `is_systematic=false`, Score ~30–40 |
| `systematic` | >10 Req/Tag an high/critical Services | `is_systematic=true`, Score 65–85 |
| `upload-leak` | POST-Spikes >500 KB an Claude/ChatGPT | `has_document_upload=true`, Score ≥90 |
| `enterprise-mixed` | ~30 Clients, alle Risk-Level gemischt | Diverse Findings für UI/Report-Demo |

Alle Profile sind seed-reproduzierbar (`--seed 42`) und rein synthetisch (RFC1918-IPs).

### Streamlit-Dashboard starten

```bash
streamlit run app.py
# → http://localhost:8501
```

In der Sidebar Log-Datei hochladen, "Analyse starten", durch die 4 Pages klicken:
- **📊 Übersicht** — KPIs, Compliance-Ampel, Score-Bars über alle Frameworks, Top-3-Risiken
- **🔍 Findings** — Filter nach Risk/Framework/Service, Tabelle, Detail-Expander mit Compliance-Mappings
- **📋 Compliance** — 5 Tabs (DORA / EU AI Act / ISO 42001 / ISO 27001 / DSGVO) mit Score-Cards + Mapping-Tabellen
- **⚙️ Einstellungen** — Salt-Override, Privacy-Self-Check, Schwellwert-Anzeige

### Reports CLI-frei (Python)

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

### Tests

```bash
python -m pytest tests/ -v
```

## Privacy by Design

- **HMAC-SHA256-Pseudonymisierung** aller IPs/User beim Parsing
- **Defense-in-Depth:** Engine pseudonymisiert + Generator pseudonymisiert (separater Salt) + Post-Render-Check `assert_no_plaintext()` verbietet IPv4/IPv6/MAC/`*.local|.lan|.corp`-Hostnames im Output
- **Salt-Konfiguration** via `REPORT_SALT` ENV-Var (Default: random pro Process)
- **Disclaimer-Block** in jedem Report mit Salt-Fingerprint (8 Hex), kein Salt-Leak
- **Retention:** Standard 90 Tage, konfigurierbar

## Architektur

```
Input (DNS/Proxy-Logs) → Parser → AI Endpoint Database
→ Detection Engine → Compliance Engine → (Claude Analyzer opt.)
→ Report Generator (HTML/MD/JSON)  ─┬→  ./reports/
→ Streamlit Dashboard (interaktiv) ─┘
```

## License

Siehe [LICENSE](LICENSE).
