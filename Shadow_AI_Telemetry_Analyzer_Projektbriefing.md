# Projektbriefing: Shadow-AI Telemetry Analyzer
## KI-gestützte Detektion nicht-autorisierter KI-Nutzung in Unternehmensnetzen

**Projektstatus:** Konzeptphase  
**Autor:** Florian Priegnitz  
**Erstellt:** Februar 2026  
**Repository:** (noch anzulegen)  
**Lizenz:** MIT

---

## 1. Projektvision

Entwicklung eines **KI-gestützten Analyse-Tools**, das Netzwerk-Telemetrie (DNS-Logs, Proxy-Logs) automatisiert auswertet und nicht-autorisierte KI-Tool-Nutzung in Unternehmensumgebungen erkennt, bewertet und dokumentiert.

Shadow-AI – also der unkontrollierte Einsatz von KI-Tools außerhalb des genehmigten Software-Inventars – ist eines der drängendsten Governance-Probleme in Unternehmen 2025/2026. Klassische DLP-Lösungen und URL-Kategorisierungen reichen nicht aus, weil:

- KI-Endpunkte sich schnell ändern (neue Tools, neue Domains)
- Traffic-Volumen und zeitliche Muster relevanter sind als einzelne Aufrufe
- Der regulatorische Kontext (DORA, EU AI Act, ISO 42001) eine strukturierte Dokumentation erfordert

Dieses Tool schließt diese Lücke: Es kombiniert regelbasierte Detektion mit KI-gestützter Kontextualisierung und erzeugt direkt verwertbare, regulatorisch eingebettete Reports.

---

## 2. Hintergrund & Motivation

### Das Problem: Shadow-AI als unkontrolliertes ICT-Risiko

Mitarbeiter nutzen KI-Tools produktiv – oft ohne böse Absicht, aber mit erheblichen Risiken:

- **Datenschutz:** Kundendaten, personenbezogene Daten oder Geschäftsgeheimnisse werden in externe KI-Systeme eingegeben
- **Urheberrecht:** Interne Dokumente, Code oder Designs werden ohne Prüfung als Prompt-Input genutzt
- **Compliance:** Nicht-inventarisierte KI-Systeme können nicht auf Risikoklassen (EU AI Act) geprüft werden
- **DORA:** Jedes externe KI-Tool ist ein unkontrollierter Third-Party ICT Provider

### Warum Telemetrie-Analyse?

Netzwerk-Telemetrie ist der robusteste Detektionsansatz, weil er:
- Nicht umgehbar ist ohne VPN/Proxy (und das ist selbst detektierbar)
- Keine Endpoint-Agents erfordert
- Verhaltensbasierte Analyse ermöglicht (nicht nur Blocklisten)
- In jedem Unternehmen bereits vorhanden ist (Proxy-Logs, DNS-Logs)

### Regulatorische Einbettung

```
Shadow-AI-Nutzung
        ↓
DORA Art. 6:    Nicht-inventarisierte ICT Third-Party Provider
DORA Art. 28:   Kein Contract, kein Risk Assessment, kein Exit-Plan
EU AI Act:      Unbekannte Risikoklasse, kein Conformity Assessment
ISO 42001:      Nicht im KI-Inventar (Asset Register)
ISO 27001:      A.5.9 Inventory of Assets – unvollständig
```

Jeder dieser Punkte ist nicht nur ein theoretisches Risiko, sondern bei regulierten Unternehmen (Banken, Versicherungen, kritische Infrastruktur) ein Audit-Finding.

---

## 3. Technische Architektur

### Übersicht

```
┌─────────────────────────────────────────────────┐
│              Input Layer                        │
│  DNS-Logs     Proxy-Logs     Synthet. Testdaten │
│  (Pi-hole)    (mitmproxy)    (Generator)        │
└──────────────────┬──────────────────────────────┘
                   │ Raw Log Files (CSV/JSON/CLF)
┌──────────────────▼──────────────────────────────┐
│              Parser & Normalizer                │
│  - Format-Erkennung (auto-detect)               │
│  - Timestamp-Normalisierung (UTC)               │
│  - User/IP-Pseudonymisierung (DSGVO)            │
│  - Strukturierter Output: pandas DataFrame      │
└──────────────────┬──────────────────────────────┘
                   │ Normalized DataFrame
┌──────────────────▼──────────────────────────────┐
│         AI Endpoint Database                    │
│  - Kuratierte Liste bekannter KI-Endpunkte      │
│  - Kategorisierung (LLM, Image, Code, etc.)     │
│  - Risk-Level (High/Medium/Low)                 │
│  - Wöchentliches Update via GitHub              │
└──────────────────┬──────────────────────────────┘
                   │ Matched Hits + Risk Metadata
┌──────────────────▼──────────────────────────────┐
│           Detection Engine                      │
│  - Frequenz-Analyse (wie oft, wann)             │
│  - Volumen-Analyse (Upload-Spikes = Dokumente)  │
│  - User-Cluster (wer nutzt was systematisch)    │
│  - Zeitliche Muster (Arbeitszeit vs. nachts)    │
│  - Anomalie-Score pro User-Gruppe               │
└──────────────────┬──────────────────────────────┘
                   │ Findings + Scores
┌──────────────────▼──────────────────────────────┐
│           Claude API Analyzer                   │
│  - Kontextualisierung der Findings              │
│  - Risikopriorisierung (was ist wirklich kritisch?)│
│  - Natürlichsprachliche Erklärungen             │
│  - Regulatorisches Mapping (DORA/AI Act)        │
└──────────────────┬──────────────────────────────┘
                   │ Analyzed Report Data
┌──────────────────▼──────────────────────────────┐
│           Report Generator                      │
│  - Executive Summary (für Management)           │
│  - Technical Findings (für IT-Security)         │
│  - Regulatorisches Mapping (für Compliance)     │
│  - Empfehlungsmaßnahmen                         │
│  - Output: HTML / Markdown / JSON               │
└─────────────────────────────────────────────────┘
```

---

## 4. Kernkomponenten im Detail

### 4.1 AI Endpoint Database

Das wertwertvollste eigenständige Asset des Projekts – eine gepflegte, strukturierte Datenbank bekannter KI-Endpunkte:

```json
{
  "endpoints": [
    {
      "host": "api.openai.com",
      "service": "OpenAI API",
      "category": "LLM",
      "risk_level": "high",
      "data_residency": "US",
      "gdpr_compliant": false,
      "dora_relevant": true,
      "notes": "Trainingsdaten-Opt-out möglich, aber kein DPA standard"
    },
    {
      "host": "claude.ai",
      "service": "Claude (Anthropic)",
      "category": "LLM",
      "risk_level": "high",
      "data_residency": "US",
      "gdpr_compliant": false,
      "dora_relevant": true,
      "notes": "API-Zugriff separat bewertbar"
    },
    {
      "host": "copilot.microsoft.com",
      "service": "Microsoft Copilot",
      "category": "LLM",
      "risk_level": "medium",
      "data_residency": "EU (M365-Tenant abhängig)",
      "gdpr_compliant": true,
      "dora_relevant": true,
      "notes": "Oft bereits lizenziert – prüfen ob autorisiert"
    },
    {
      "host": "midjourney.com",
      "service": "Midjourney",
      "category": "Image Generation",
      "risk_level": "high",
      "data_residency": "US",
      "gdpr_compliant": false,
      "dora_relevant": false,
      "notes": "Urheberrecht-Risiko bei generierten Assets"
    }
  ]
}
```

Diese Datenbank wird als eigenständiges Open-Source-Projekt gepflegt und versioniert. Community-Contributions via Pull Request.

### 4.2 Detection Engine

```python
class ShadowAIDetectionEngine:
    
    def analyze_frequency(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Berechnet Zugriffshäufigkeit pro User/IP und Endpunkt.
        Schwellenwerte: >10 Requests/Tag = systematische Nutzung
        """
    
    def analyze_volume(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analysiert Upload-Volumen zu KI-Endpunkten.
        Spike >500KB = wahrscheinlich Dokument-Upload
        Kontext: Welche Uhrzeit? Welcher User-Cluster?
        """
    
    def detect_temporal_patterns(self, df: pd.DataFrame) -> dict:
        """
        Zeitliche Musteranalyse:
        - Außerhalb Arbeitszeiten (evtl. Umgehungsversuch)
        - Regelmäßige tägliche Nutzung (systematischer Einsatz)
        - Burst-Muster (einmalig großer Upload)
        """
    
    def cluster_users(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Gruppierung nach Verhaltensmustern (nicht nach Name/ID).
        DSGVO-konform: Pseudonymisiert bis zur HR-Eskalation.
        Output: Cluster A (Heavy User), B (Gelegenheitsnutzer), 
                C (Einmalig), D (Verdächtig)
        """
    
    def calculate_risk_score(self, findings: dict) -> int:
        """
        0-100 Score basierend auf:
        - Anzahl verschiedener KI-Tools (Diversität)
        - Datenvolumen (Sensitivität)
        - Regelmäßigkeit (Systematik)
        - Risk-Level der genutzten Endpunkte
        """
```

### 4.3 Claude API Integration

```python
class AIAnalyzer:
    
    def __init__(self):
        self.client = anthropic.Anthropic()
    
    def analyze_findings(self, findings: dict) -> AnalysisResult:
        
        prompt = f"""
        Du bist ein Information Security Analyst spezialisiert auf 
        KI-Governance und DORA-Compliance.
        
        Analysiere folgende Shadow-AI-Nutzungsmuster in einem Unternehmen:
        
        {json.dumps(findings, indent=2)}
        
        Erstelle eine strukturierte Analyse mit:
        1. Executive Summary (3 Sätze, für CISO-Level)
        2. Top 3 Risiken nach Priorität (mit DORA/AI Act Referenz)
        3. Sofortmaßnahmen (was muss diese Woche passieren?)
        4. Mittelfristige Empfehlungen (Governance-Struktur)
        5. Welche Findings erfordern eine DORA-Meldung?
        
        Sprache: Deutsch, professionell, keine Marketing-Sprache.
        """
        
        response = self.client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return self._parse_response(response)
    
    def classify_tool_risk(self, tool_name: str, 
                           usage_context: str) -> RiskClassification:
        """
        Klassifiziert ein unbekanntes KI-Tool nach EU AI Act Risikoklassen.
        Für Tools, die noch nicht in der Endpoint-Database sind.
        """
```

---

## 5. DSGVO-Konzept

Da Netzwerk-Telemetrie personenbezogene Daten enthält (IP-Adressen = personenbezogen nach DSGVO), braucht das Tool ein sauberes Datenschutzkonzept:

### Pseudonymisierung

```python
class DataPrivacyHandler:
    
    def pseudonymize_log(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        IP-Adressen und Usernamen werden beim Import 
        mit HMAC-SHA256 pseudonymisiert.
        Salt wird lokal gespeichert, nie im Report.
        De-Pseudonymisierung nur durch berechtigte Personen (ISB/HR).
        """
        
    def apply_retention_policy(self, df: pd.DataFrame, 
                                days: int = 90) -> pd.DataFrame:
        """
        Logs älter als 90 Tage werden automatisch gelöscht.
        Konfigurierbar nach Unternehmens-Retention-Policy.
        """
```

### Rechtliche Grundlage

Das Tool ist so konzipiert, dass es auf Basis von **Art. 6 Abs. 1 lit. f DSGVO** (berechtigtes Interesse) oder einer **Betriebsvereinbarung** betrieben werden kann. Die Dokumentation enthält einen Vorschlag für den DSFA-Kurzcheck.

---

## 6. Testinfrastruktur

### Lokales Testbed (ohne Unternehmens-Infrastruktur)

**Pi-hole als DNS-Sensor:**
```bash
# Pi-hole Query-Log als Basis
# Format: timestamp | domain | client | status
# Dein eigener Traffic als realistische Testdaten
tail -f /var/log/pihole.log | python parser/pihole_parser.py
```

**mitmproxy als Proxy-Sensor:**
```bash
# HTTPS-Traffic deiner eigenen Geräte
# Zeigt: welche AI-Tools du selbst täglich nutzt
mitmproxy --save-stream-file=../testdata/proxy_$(date +%Y%m%d).log
```

**Synthetischer Datengenerator:**
```python
class TestDataGenerator:
    """
    Generiert realistische Log-Dateien mit:
    - Normaler Hintergrund-Traffic (90%)
    - Verschiedene Shadow-AI-Muster (10%):
      * Einzelner Heavy-User (OpenAI API täglich)
      * Abteilungsweite ChatGPT-Nutzung
      * Einmaliger Massen-Upload zu Midjourney
      * Verdächtiger nächtlicher Zugriff
    """
```

---

## 7. Report-Beispiel (Output)

```markdown
# Shadow-AI Security Report
**Analysezeitraum:** 01.02.2026 – 28.02.2026  
**Erstellt:** 2026-02-26  
**Risk Score:** 73/100 🔴 HOCH

## Executive Summary
Im Analysezeitraum wurden 847 Zugriffe auf 12 verschiedene 
nicht-autorisierte KI-Endpunkte detektiert. Besonders kritisch: 
Regelmäßige Upload-Aktivität zu api.openai.com mit durchschnittlich 
340KB pro Session deutet auf systematische Verarbeitung interner 
Dokumente hin. Sofortmaßnahmen werden empfohlen.

## Top Findings

### Finding 1 – KRITISCH
**Endpunkt:** api.openai.com  
**Muster:** 23 User, täglich, Ø 340KB Upload  
**Bewertung:** Hohe Wahrscheinlichkeit für Verarbeitung 
              interner Geschäftsdokumente  
**DORA-Referenz:** Art. 28 – Nicht-vertraglicher Third-Party Provider  
**AI Act:** Risikoklasse unklar – kein Conformity Assessment vorhanden  
**Empfehlung:** Sofortiger Block + Policy-Kommunikation

### Finding 2 – MITTEL
**Endpunkt:** copilot.microsoft.com  
**Muster:** 156 User, unregelmäßig  
**Bewertung:** Vermutlich M365 Copilot (ggf. bereits lizenziert)  
**Empfehlung:** Klärung ob autorisiert – wenn ja: ins KI-Inventar

## Regulatorisches Mapping
| Finding | DORA | EU AI Act | ISO 42001 | ISO 27001 |
|---------|------|-----------|-----------|-----------|
| OpenAI API | Art. 6, 28 | Art. 6 (GPAI) | 6.1.2 | A.5.9 |
| Midjourney | Art. 28 | Art. 6 | 6.1.2 | A.5.9 |

## Empfohlene Maßnahmen
1. **Diese Woche:** DNS-Block für High-Risk Endpunkte
2. **Dieser Monat:** Shadow-AI-Policy kommunizieren
3. **Dieses Quartal:** KI-Inventar aufbauen, Freigabeprozess definieren
```

---

## 8. Roadmap

### Phase 1 – MVP (3–4 Wochen)
- [ ] Log-Parser: Pi-hole DNS-Format
- [ ] AI Endpoint Database: 50 wichtigste Endpunkte
- [ ] Basis-Detection: Frequenz + Volumen
- [ ] Claude API: Findings analysieren
- [ ] Report-Generator: Markdown-Output
- [ ] README + Demo mit synthetischen Daten

### Phase 2 – Erweiterung (4 Wochen)
- [ ] Proxy-Log-Parser (Squid, BlueCoat, mitmproxy)
- [ ] Zeitliche Musteranalyse
- [ ] User-Cluster-Analyse
- [ ] DSGVO-Pseudonymisierung
- [ ] HTML-Report mit Visualisierungen (matplotlib/plotly)
- [ ] AI Endpoint Database: 200+ Endpunkte

### Phase 3 – Governance Integration (parallel)
- [ ] DORA-Mapping in Reports automatisieren
- [ ] EU AI Act Risikoklassen-Check für unbekannte Tools
- [ ] ISO 42001 KI-Inventar-Export (CSV/JSON)
- [ ] Kurzcheck DSFA-Dokumentation

---

## 9. Technologie-Stack

| Komponente | Technologie | Version |
|---|---|---|
| Core | Python | 3.11+ |
| Datenverarbeitung | pandas | 2.x |
| Visualisierung | plotly | 5.x |
| KI-Analyse | Claude API (Anthropic) | aktuell |
| Report | Jinja2 | 3.x |
| Testing | pytest | 7.x |
| Pseudonymisierung | hashlib (HMAC-SHA256) | stdlib |
| DNS-Testbed | Pi-hole | 5.x |
| Proxy-Testbed | mitmproxy | 10.x |
| CI | GitHub Actions | – |

---

## 10. Lernziele & Kompetenznachweis

Dieses Projekt demonstriert:

**Technisch:**
- Log-Parsing und -Normalisierung verschiedener Formate
- Verhaltensbasierte Anomalie-Detektion (regelbasiert)
- Statistische Analyse von Zeitreihendaten
- Claude API Integration für Security-Analyse
- DSGVO-konforme Datenverarbeitung (Pseudonymisierung)

**Security Engineering:**
- Detection Engineering (von Rohdaten zu verwertbaren Findings)
- Threat Intelligence (AI Endpoint Database als eigenständiges Asset)
- Security Reporting für verschiedene Zielgruppen (CISO vs. IT vs. Compliance)

**Governance & Compliance:**
- DORA Third-Party Risk in der Praxis
- EU AI Act Risikoklassifizierung operativ angewandt
- ISO 42001 KI-Inventar-Aufbau automatisiert
- ISO 27001 Asset Management (A.5.9)

**Direkter Bewerbungsnachweis:**
Das Projekt verbindet technische Security-Kompetenz (Log-Analyse, Detektion) mit Governance-Expertise (DORA, EU AI Act, ISO 42001) – eine Kombination, die für Stellen im Bereich AI Security & Governance in regulierten Unternehmen (Banken, Versicherungen, KRITIS) direkt verwertbar ist.

---

## 11. Abgrenzung zu bestehenden Tools

| Tool | Ansatz | Lücke die dieses Projekt füllt |
|---|---|---|
| Netskope / Zscaler | CASB, regelbasierter Block | Kein Governance-Reporting, kein AI-Act-Mapping |
| Darktrace | ML-basierte Anomalie | Zu komplex, kein Governance-Output |
| Pi-hole | DNS-Block | Keine Analyse, kein Reporting |
| Manuelles Log-Review | Analyst-Zeit | Nicht skalierbar |

**Positionierung:** Leichtgewichtiges, open-source, governance-fokussiertes Detection-Tool für Unternehmen ohne Enterprise-CASB-Budget.

---

## 12. Referenzen

- [DORA – Regulation (EU) 2022/2554](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX:32022R2554)
- [EU AI Act – Regulation (EU) 2024/1689](https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=OJ:L_202401689)
- [ISO/IEC 42001:2023 – AI Management Systems](https://www.iso.org/standard/81230.html)
- [ISO/IEC 27001:2022 – Information Security](https://www.iso.org/standard/27001)
- [MITRE ATLAS – Adversarial Threat Landscape for AI Systems](https://atlas.mitre.org)
- [BSI – KI-Einsatz in Unternehmen](https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Kuenstliche-Intelligenz/kuenstliche-intelligenz_node.html)

---

*Dieses Dokument ist Teil eines Portfolio-Projekts zur Demonstration von AI-Security-Kompetenz im regulierten Unternehmensumfeld.*  
*Verwandtes Projekt: MCP Hub – Security Tool Integration via Model Context Protocol*
