# Quickstart — In 10 Minuten zur ersten Shadow-AI-Analyse

Diese Anleitung führt Schritt für Schritt vom leeren Projekt zur fertigen Compliance-Analyse.

## 1. Installation (siehe [INSTALLATION.md](../INSTALLATION.md))

Kürzester Pfad (Docker):

```bash
git clone https://github.com/florian-priegnitz/Telemetrie-Analyzer.git
cd Telemetrie-Analyzer
docker compose up --build
```

## 2. Testdaten generieren

Ohne Docker (lokale venv):

```bash
python -m src.testdata.generator --scenario enterprise-mixed --format both --seed 42
# → testdata/scenarios/enterprise-mixed_pihole.log
# → testdata/scenarios/enterprise-mixed_squid.log
```

Verfügbare Szenarien (jedes trifft eine andere Detection-Schwelle):

| Szenario | Zweck | Erwartetes Ergebnis |
|----------|-------|---------------------|
| `clean` | Baseline ohne KI-Nutzung | 0 Findings |
| `low-risk` | Gelegentliche medium-risk Services | Findings, `is_systematic=false`, Score ~30–40 |
| `systematic` | >10 Req/Tag an high/critical Services | `is_systematic=true`, Score 65–85 |
| `upload-leak` | POST-Spikes >500 KB an Claude/ChatGPT | `has_document_upload=true`, Score ≥90 |
| `enterprise-mixed` | ~30 Clients, alle Risk-Level gemischt | Diverse Findings — ideal für Demo |

## 3. UI-Walkthrough

Öffne **http://localhost:8501** (Docker) bzw. starte `streamlit run app.py` lokal.

### Schritt 1 — Upload

```
┌─ Sidebar ──────────────────────────────────┐
│ 🛡️ Telemetrie Analyzer                      │
│ Shadow AI Detection · DORA · EU AI Act…    │
│                                            │
│ 📁 Log-Upload                              │
│   [Browse files]  ← testdata/…/enterprise  │
│   Parser: [🔍 Auto ▾]                      │
│   [▶ Analyse starten]                      │
│                                            │
│ Navigation                                 │
│   ○ 📊 Übersicht                           │
│   ○ 🔍 Findings                            │
│   ○ 👥 Users & Patterns                    │
│   ○ 📋 Compliance                          │
│   ○ ⚙️ Einstellungen                       │
└────────────────────────────────────────────┘
```

Nach Klick auf **Analyse starten** läuft die Pipeline:

1. **Parser** erkennt Format automatisch (Pi-hole / Squid / Zscaler / PAN-OS / …)
2. **Pseudonymisierung** (HMAC-SHA256) auf IPs und Usernames
3. **Detection Engine** berechnet Risk-Score 0–100
4. **Compliance Engine** mappt Findings auf DORA/EU-AI-Act/ISO-42001/ISO-27001/DSGVO
5. **(Optional) Claude-API** annotiert Findings mit Handlungsempfehlungen

Status-Anzeige: `📭 Keine Daten` → `📥 Bereit zur Analyse` → `⏳ Analysiere…` → `✅ Analyse fertig`

### Schritt 2 — Übersicht

Die **Übersicht**-Page zeigt auf einen Blick:

- **KPI-Row:** Anzahl Findings · Clients · Services · Max-Risk-Score
- **Compliance-Ampel:** 5 Frameworks mit Score-Card (🟢 / 🟡 / 🔴)
- **Top-3-Risiken:** größte Findings mit Service, Client-Pseudonym, Score

### Schritt 3 — Findings-Drill-Down

**Findings**-Page: Filterbar nach Risk-Level, Framework, Service. Jede Zeile aufklappbar — zeigt:

- `technical_detail` (was erkannt wurde)
- `compliance_mappings` (welche Artikel/Controls getroffen)
- Empfohlene Mitigation

### Schritt 4 — Users & Patterns

**Users & Patterns**-Page zeigt pseudonymisiertes Verhalten:

- **Top-10-Client-Ranking** nach Max-Risk-Score
- **Stunden-Heatmap** (Client × Stunde) mit Off-Hours-Schattierung (06–22 = Business)
- **Burst-Detection:** >50 Requests in 5 Minuten werden markiert
- **k-Anonymitäts-Banner:** warnt bei Re-Identifikations-Risiko < k=5

### Schritt 5 — Compliance-Report

**Compliance**-Page: 5 Tabs, jeweils mit Score-Card und Mapping-Tabelle. Klick auf einen Artikel/Control zeigt alle Findings, die darauf einzahlen.

### Schritt 6 — Einstellungen

- **Salt-Override:** eigenes Salt setzen (triggert Hard-Reset)
- **Privacy-Self-Check:** prüft manuell, ob Klartext-Leaks im Output
- **Retention-Toggle:** Auto-Delete > Retention-Days aktivieren
- **Schwellwert-Anzeige:** aktuelle `SYSTEMATIC_THRESHOLD`, `UPLOAD_THRESHOLD_BYTES`, `OFF_HOURS_RISK_BOOST`

## 4. Reports exportieren

Aus der UI (geplant: Export-Button auf Übersicht) oder via Python:

```python
from pathlib import Path
from src.reports import ReportGenerator

gen = ReportGenerator(detection, compliance, salt="my-salt")
gen.write(Path("reports/"), audience="executive", format="html")
gen.write(Path("reports/"), audience="it-security", format="markdown")
gen.write(Path("reports/"), audience="compliance", format="html")
gen.write(Path("reports/"), format="json")  # maschinenlesbar
```

**Drei Zielgruppen × drei Formate**:

| Zielgruppe | Fokus |
|------------|-------|
| **Executive / CISO** | Compliance-Ampel, Top-Risiken, Handlungs-Summary |
| **IT-Security** | Technische Details, betroffene Clients, Remediation |
| **Compliance** | Framework-Mappings, Evidenz pro Artikel/Control |

## 5. Eigene Logs analysieren

Unterstützte Formate (v1.0):

- **Pi-hole** (Syslog, FTL-CSV)
- **Squid** (Native + Common Log, konfigurierbar)
- **Zscaler ZIA NSS**
- **Palo Alto PAN-OS URL-Filtering**
- **Cisco Umbrella DNS**
- **Fortinet FortiGate webfilter.log**
- **AWS VPC Flow Logs** (v2 Default + v5 Custom)
- **Azure Entra ID Sign-In** (JSONL)
- **Cloudflare Gateway** (DNS + HTTP NDJSON)
- **Netskope CASB** (JSON NDJSON)

Einfach die Datei hochladen — Auto-Detect erkennt das Format an Header/Struktur.

## 6. Nächste Schritte

- [README.md](../README.md) — Feature-Überblick, Architektur
- [CONTRIBUTING.md](../CONTRIBUTING.md) — eigene Parser beitragen
- [SECURITY.md](../SECURITY.md) — Privacy-Modell, Responsible Disclosure
