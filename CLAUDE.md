# Telemetrie Analyzer

> **Repo:** https://github.com/florian-priegnitz/Telemetrie-Analyzer
>
> **Relevante PKB-Skills** (bei Bedarf laden aus `//wsl$/Ubuntu/home/flowing1978/projects/my-ai-os/skills/`):
> security-engineer, backend-dev, qa-engineer, software-architect, technical-writer

KI-gestütztes Analyse-Tool zur Erkennung nicht-autorisierter KI-Nutzung (Shadow AI) in Unternehmensnetzen. Analysiert DNS- und Proxy-Logs, erkennt Muster und erzeugt regulatorisch eingebettete Reports (DORA, EU AI Act, ISO 42001).

**Status:** Phase 1 (MVP) abgeschlossen – Phase 2 (Compliance & Analyse) steht an.

## Tech-Stack

- **Sprache:** Python 3.11+
- **Datenverarbeitung:** pandas 2.x
- **Visualisierung:** plotly 5.x
- **KI-Analyse:** Claude API (Anthropic SDK)
- **Reports:** Jinja2 Templates (HTML/Markdown/JSON)
- **Testing:** pytest
- **Pseudonymisierung:** HMAC-SHA256 (hashlib)
- **CI:** GitHub Actions

## Architektur (Pipeline)

```
Input (DNS/Proxy-Logs) → Parser & Normalizer → AI Endpoint Database
→ Detection Engine → Compliance Engine → Claude API Analyzer → Report Generator
```

### Compliance-First Design

Alle Findings werden über ein zentrales **Compliance-Modell** strukturiert. Jedes Finding referenziert konkrete Kontrollen und Artikel – das ermöglicht spätere Auswertungen entlang einzelner Frameworks.

```
Finding
 ├── technical_detail     (was wurde erkannt)
 ├── risk_score            (0-100)
 └── compliance_mappings[] (Liste von Framework-Referenzen)
       ├── framework        (DORA | EU_AI_ACT | ISO_42001 | ISO_27001 | DSGVO)
       ├── control_id       (z.B. "Art. 28", "A.5.9", "6.1.2")
       ├── severity          (critical | high | medium | low)
       └── assessment_status (non_compliant | partially_compliant | needs_review)
```

**Auswertungsdimensionen:**
- **Per Framework:** Alle Findings zu DORA, EU AI Act etc. aggregiert
- **Per Kontrolle:** Erfüllungsgrad einzelner Artikel/Controls
- **Per Zeitraum:** Compliance-Trend über Analysezeiträume
- **Per Risiko:** Findings nach Severity/Risk-Score sortiert
- **Compliance-Score:** Prozentualer Erfüllungsgrad je Framework

## Konventionen

- **Sprache im Code:** Englisch (Variablen, Funktionen, Klassen)
- **Dokumentation/Reports:** Deutsch
- **Datenformat intern:** pandas DataFrame
- **Privacy by Design:** Alle personenbezogenen Daten (IPs, Usernamen) werden bei Import mit HMAC-SHA256 pseudonymisiert
- **Retention:** Standard 90 Tage, konfigurierbar

## Projektstruktur

```
telemetrie-analyzer/
├── src/
│   ├── parsers/
│   │   └── pihole.py         # Pi-hole DNS-Parser (Syslog + FTL-CSV)
│   ├── database/
│   │   └── ai_endpoints.py   # AIEndpointDatabase (Laden, Lookup, Subdomain-Matching)
│   ├── detection/
│   │   └── engine.py         # DetectionEngine (Matching, Frequenz, Risk-Scoring)
│   ├── compliance/           # (Phase 2) Compliance Engine
│   ├── analyzer/             # (Phase 2) Claude API Integration
│   ├── privacy/
│   │   └── pseudonymizer.py  # HMAC-SHA256 Pseudonymisierung
│   ├── reports/              # (Phase 3) Jinja2 Report-Generator
│   └── testdata/
│       └── generator.py      # Synthetische Testdaten-Generator
├── templates/                # (Phase 3) Report-Templates
├── tests/                    # 37 pytest-Tests
├── testdata/
│   └── pihole_sample.log     # Generiertes 7-Tage-Sample (207 KB)
├── config/                   # Konfigurationsdateien
├── data/
│   └── ai_endpoints.json     # 26 KI-Dienste mit Domains & Risikostufen
└── pyproject.toml
```

## Wichtige Befehle

```bash
# Tests ausführen
pytest

# Synthetische Testdaten generieren
python -m src.testdata.generator

# Analyse starten (geplant)
python -m src.main --input <logfile> --format pihole --output report.html
```

## Compliance Frameworks

Jedes Framework hat ein eigenes Kontroll-Set mit auswertbaren Controls:

| Framework | Relevante Kontrollen | Auswertung |
|-----------|---------------------|------------|
| **DORA** | Art. 5 (ICT-Governance), Art. 6 (ICT-Risikomanagement), Art. 28 (Third-Party) | Third-Party-Risiko-Score, Vertragslücken |
| **EU AI Act** | Art. 6 (Risikoklassen), Art. 9 (Risk Management), Art. 53 (GPAI) | Risikoklassifizierung pro Tool, Conformity-Status |
| **ISO 42001** | 6.1.2 (AI Risk Assessment), 8.4 (AI System Operation) | KI-Inventar-Vollständigkeit, Assessment-Abdeckung |
| **ISO 27001** | A.5.9 (Asset Inventory), A.5.23 (Cloud Services), A.8.16 (Monitoring) | Asset-Abdeckungsgrad, Monitoring-Gaps |
| **DSGVO** | Art. 6 (Rechtsgrundlage), Art. 25 (Privacy by Design), Art. 35 (DSFA) | Datentransfer-Risiko, DSFA-Bedarf |

Reports können nach einzelnen Frameworks oder framework-übergreifend generiert werden.

## Hinweise für Claude

- Bei Code-Änderungen immer DSGVO-Konformität beachten (keine Klartextdaten in Logs/Reports)
- AI Endpoint Database ist ein eigenständiges Asset – Änderungen sorgfältig versionieren
- Reports haben drei Zielgruppen: Executive/CISO, IT-Security, Compliance
- Detection-Schwellenwerte: >10 Requests/Tag = systematisch, >500KB Upload = Dokument-Upload
