# Compliance Report — Shadow AI Telemetrie

Generiert: **27.04.2026 09:37 UTC**
Zeitraum: **12.04.2026** bis **26.04.2026**
> **DSGVO:** Pseudonymisiert (HMAC-SHA256), Salt-Fingerprint `c338ca09`

## Framework-Übersicht

| Framework | Erfüllt | Triggered/Total | Non-Compliant | Partially | Review |
|---|---|---|---|---|---|
| **EU AI Act** | 0.0% | 3/3 | 3 | 0 | 0 |
| **DSGVO** | 0.0% | 3/3 | 3 | 0 | 0 |
| **EU CRA** | 14.3% | 6/7 | 6 | 0 | 0 |
| **DORA** | 33.3% | 2/3 | 2 | 0 | 0 |
| **ISO/IEC 27001** | 33.3% | 2/3 | 2 | 0 | 0 |
| **ISO/IEC 42001** | 50.0% | 1/2 | 1 | 0 | 0 |

## Severity-Verteilung pro Framework

| Framework | Critical | High | Medium | Low |
|---|---|---|---|---|
| EU AI Act | 34 | 135 | 65 | 0 |
| DSGVO | 34 | 134 | 96 | 0 |
| EU CRA | 68 | 278 | 96 | 0 |
| DORA | 68 | 100 | 6 | 0 |
| ISO/IEC 27001 | 68 | 100 | 12 | 0 |
| ISO/IEC 42001 | 34 | 50 | 6 | 0 |

## Detail: Compliance-Mappings je Finding

### DeepSeek — DeepSeek

- **Risk:** critical (Score 100)
- **Client:** `client_144be7d3`
- **Queries:** 27 (2.2/Tag)
- **Upload:** 5× Dokument-Upload (6854.5 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'DeepSeek' von DeepSeek erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'DeepSeek' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'DeepSeek' (DeepSeek) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'DeepSeek' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'DeepSeek' mit Risk-Score 100 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'DeepSeek' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'DeepSeek' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'DeepSeek' (DeepSeek) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'DeepSeek' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' erfordert DSFA (Datentransfer an DeepSeek). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'DeepSeek' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'DeepSeek' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'DeepSeek' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'DeepSeek' (DeepSeek) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'DeepSeek' ohne technische Dokumentation nach CRA-Anhang V. |
### DeepSeek — DeepSeek

- **Risk:** critical (Score 100)
- **Client:** `client_1dc78685`
- **Queries:** 11 (1.2/Tag)
- **Upload:** 2× Dokument-Upload (6974.1 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'DeepSeek' von DeepSeek erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'DeepSeek' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'DeepSeek' (DeepSeek) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'DeepSeek' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'DeepSeek' mit Risk-Score 100 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'DeepSeek' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'DeepSeek' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'DeepSeek' (DeepSeek) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'DeepSeek' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' erfordert DSFA (Datentransfer an DeepSeek). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'DeepSeek' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'DeepSeek' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'DeepSeek' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'DeepSeek' (DeepSeek) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'DeepSeek' ohne technische Dokumentation nach CRA-Anhang V. |
### GitHub Copilot — GitHub / Microsoft

- **Risk:** critical (Score 100)
- **Client:** `client_1ddad6a1`
- **Queries:** 36 (3.0/Tag)
- **Upload:** 3× Dokument-Upload (6745.9 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'GitHub Copilot' von GitHub / Microsoft erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'GitHub Copilot' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'GitHub Copilot' (GitHub / Microsoft) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'GitHub Copilot' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'GitHub Copilot' (Kategorie: code_assistant) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'GitHub Copilot' mit Risk-Score 100 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'GitHub Copilot' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'GitHub Copilot' (GitHub / Microsoft) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'GitHub Copilot' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'GitHub Copilot' erfordert DSFA (Datentransfer an GitHub / Microsoft). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'GitHub Copilot' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'GitHub Copilot' (Kategorie code_assistant) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | non_compliant | 'GitHub Copilot' (code_assistant) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'GitHub Copilot' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'GitHub Copilot' (GitHub / Microsoft) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'GitHub Copilot' ohne technische Dokumentation nach CRA-Anhang V. |
### DeepSeek — DeepSeek

- **Risk:** critical (Score 100)
- **Client:** `client_2632e438`
- **Queries:** 14 (1.3/Tag)
- **Upload:** 2× Dokument-Upload (2133.5 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'DeepSeek' von DeepSeek erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'DeepSeek' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'DeepSeek' (DeepSeek) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'DeepSeek' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'DeepSeek' mit Risk-Score 100 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'DeepSeek' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'DeepSeek' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'DeepSeek' (DeepSeek) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'DeepSeek' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' erfordert DSFA (Datentransfer an DeepSeek). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'DeepSeek' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'DeepSeek' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'DeepSeek' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'DeepSeek' (DeepSeek) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'DeepSeek' ohne technische Dokumentation nach CRA-Anhang V. |
### GitHub Copilot — GitHub / Microsoft

- **Risk:** critical (Score 100)
- **Client:** `client_40d7d667`
- **Queries:** 29 (2.4/Tag)
- **Upload:** 1× Dokument-Upload (992.0 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'GitHub Copilot' von GitHub / Microsoft erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'GitHub Copilot' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'GitHub Copilot' (GitHub / Microsoft) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'GitHub Copilot' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'GitHub Copilot' (Kategorie: code_assistant) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'GitHub Copilot' mit Risk-Score 100 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'GitHub Copilot' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'GitHub Copilot' (GitHub / Microsoft) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'GitHub Copilot' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'GitHub Copilot' erfordert DSFA (Datentransfer an GitHub / Microsoft). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'GitHub Copilot' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'GitHub Copilot' (Kategorie code_assistant) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | non_compliant | 'GitHub Copilot' (code_assistant) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'GitHub Copilot' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'GitHub Copilot' (GitHub / Microsoft) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'GitHub Copilot' ohne technische Dokumentation nach CRA-Anhang V. |
### Cursor — Anysphere

- **Risk:** critical (Score 100)
- **Client:** `client_5cac0f7a`
- **Queries:** 35 (2.7/Tag)
- **Upload:** 4× Dokument-Upload (3060.8 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'Cursor' von Anysphere erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'Cursor' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Cursor' (Anysphere) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'Cursor' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'Cursor' (Kategorie: code_assistant) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Cursor' mit Risk-Score 100 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'Cursor' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'Cursor' (Anysphere) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Cursor' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Cursor' erfordert DSFA (Datentransfer an Anysphere). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'Cursor' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Cursor' (Kategorie code_assistant) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | non_compliant | 'Cursor' (code_assistant) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Cursor' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'Cursor' (Anysphere) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Cursor' ohne technische Dokumentation nach CRA-Anhang V. |
### DeepSeek — DeepSeek

- **Risk:** critical (Score 100)
- **Client:** `client_5cac0f7a`
- **Queries:** 15 (1.4/Tag)
- **Upload:** 1× Dokument-Upload (2127.9 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'DeepSeek' von DeepSeek erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'DeepSeek' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'DeepSeek' (DeepSeek) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'DeepSeek' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'DeepSeek' mit Risk-Score 100 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'DeepSeek' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'DeepSeek' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'DeepSeek' (DeepSeek) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'DeepSeek' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' erfordert DSFA (Datentransfer an DeepSeek). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'DeepSeek' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'DeepSeek' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'DeepSeek' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'DeepSeek' (DeepSeek) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'DeepSeek' ohne technische Dokumentation nach CRA-Anhang V. |
### DeepSeek — DeepSeek

- **Risk:** critical (Score 100)
- **Client:** `client_6318295c`
- **Queries:** 19 (1.6/Tag)
- **Upload:** 3× Dokument-Upload (4285.7 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'DeepSeek' von DeepSeek erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'DeepSeek' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'DeepSeek' (DeepSeek) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'DeepSeek' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'DeepSeek' mit Risk-Score 100 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'DeepSeek' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'DeepSeek' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'DeepSeek' (DeepSeek) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'DeepSeek' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' erfordert DSFA (Datentransfer an DeepSeek). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'DeepSeek' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'DeepSeek' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'DeepSeek' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'DeepSeek' (DeepSeek) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'DeepSeek' ohne technische Dokumentation nach CRA-Anhang V. |
### Cursor — Anysphere

- **Risk:** critical (Score 100)
- **Client:** `client_64f36f5f`
- **Queries:** 35 (2.9/Tag)
- **Upload:** 1× Dokument-Upload (880.4 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'Cursor' von Anysphere erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'Cursor' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Cursor' (Anysphere) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'Cursor' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'Cursor' (Kategorie: code_assistant) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Cursor' mit Risk-Score 100 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'Cursor' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'Cursor' (Anysphere) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Cursor' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Cursor' erfordert DSFA (Datentransfer an Anysphere). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'Cursor' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Cursor' (Kategorie code_assistant) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | non_compliant | 'Cursor' (code_assistant) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Cursor' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'Cursor' (Anysphere) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Cursor' ohne technische Dokumentation nach CRA-Anhang V. |
### DeepSeek — DeepSeek

- **Risk:** critical (Score 100)
- **Client:** `client_64f36f5f`
- **Queries:** 11 (1.2/Tag)
- **Upload:** 1× Dokument-Upload (807.0 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'DeepSeek' von DeepSeek erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'DeepSeek' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'DeepSeek' (DeepSeek) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'DeepSeek' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'DeepSeek' mit Risk-Score 100 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'DeepSeek' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'DeepSeek' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'DeepSeek' (DeepSeek) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'DeepSeek' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' erfordert DSFA (Datentransfer an DeepSeek). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'DeepSeek' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'DeepSeek' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'DeepSeek' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'DeepSeek' (DeepSeek) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'DeepSeek' ohne technische Dokumentation nach CRA-Anhang V. |
### Cursor — Anysphere

- **Risk:** critical (Score 100)
- **Client:** `client_75babc12`
- **Queries:** 38 (2.9/Tag)
- **Upload:** 1× Dokument-Upload (5155.1 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'Cursor' von Anysphere erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'Cursor' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Cursor' (Anysphere) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'Cursor' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'Cursor' (Kategorie: code_assistant) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Cursor' mit Risk-Score 100 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'Cursor' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'Cursor' (Anysphere) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Cursor' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Cursor' erfordert DSFA (Datentransfer an Anysphere). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'Cursor' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Cursor' (Kategorie code_assistant) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | non_compliant | 'Cursor' (code_assistant) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Cursor' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'Cursor' (Anysphere) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Cursor' ohne technische Dokumentation nach CRA-Anhang V. |
### DeepSeek — DeepSeek

- **Risk:** critical (Score 100)
- **Client:** `client_75babc12`
- **Queries:** 12 (1.0/Tag)
- **Upload:** 2× Dokument-Upload (5768.1 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'DeepSeek' von DeepSeek erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'DeepSeek' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'DeepSeek' (DeepSeek) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'DeepSeek' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'DeepSeek' mit Risk-Score 100 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'DeepSeek' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'DeepSeek' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'DeepSeek' (DeepSeek) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'DeepSeek' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' erfordert DSFA (Datentransfer an DeepSeek). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'DeepSeek' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'DeepSeek' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'DeepSeek' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'DeepSeek' (DeepSeek) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'DeepSeek' ohne technische Dokumentation nach CRA-Anhang V. |
### Cursor — Anysphere

- **Risk:** critical (Score 100)
- **Client:** `client_8ef5b6c7`
- **Queries:** 31 (2.6/Tag)
- **Upload:** 1× Dokument-Upload (3029.1 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'Cursor' von Anysphere erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'Cursor' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Cursor' (Anysphere) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'Cursor' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'Cursor' (Kategorie: code_assistant) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Cursor' mit Risk-Score 100 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'Cursor' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'Cursor' (Anysphere) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Cursor' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Cursor' erfordert DSFA (Datentransfer an Anysphere). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'Cursor' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Cursor' (Kategorie code_assistant) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | non_compliant | 'Cursor' (code_assistant) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Cursor' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'Cursor' (Anysphere) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Cursor' ohne technische Dokumentation nach CRA-Anhang V. |
### DeepSeek — DeepSeek

- **Risk:** critical (Score 100)
- **Client:** `client_8ef5b6c7`
- **Queries:** 9 (0.8/Tag)
- **Upload:** 1× Dokument-Upload (1046.5 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'DeepSeek' von DeepSeek erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'DeepSeek' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'DeepSeek' (DeepSeek) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'DeepSeek' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'DeepSeek' mit Risk-Score 100 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'DeepSeek' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'DeepSeek' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'DeepSeek' (DeepSeek) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'DeepSeek' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' erfordert DSFA (Datentransfer an DeepSeek). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'DeepSeek' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'DeepSeek' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'DeepSeek' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'DeepSeek' (DeepSeek) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'DeepSeek' ohne technische Dokumentation nach CRA-Anhang V. |
### Cursor — Anysphere

- **Risk:** critical (Score 100)
- **Client:** `client_a141fb06`
- **Queries:** 37 (2.8/Tag)
- **Upload:** 3× Dokument-Upload (2828.0 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'Cursor' von Anysphere erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'Cursor' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Cursor' (Anysphere) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'Cursor' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'Cursor' (Kategorie: code_assistant) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Cursor' mit Risk-Score 100 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'Cursor' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'Cursor' (Anysphere) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Cursor' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Cursor' erfordert DSFA (Datentransfer an Anysphere). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'Cursor' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Cursor' (Kategorie code_assistant) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | non_compliant | 'Cursor' (code_assistant) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Cursor' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'Cursor' (Anysphere) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Cursor' ohne technische Dokumentation nach CRA-Anhang V. |
### DeepSeek — DeepSeek

- **Risk:** critical (Score 100)
- **Client:** `client_a141fb06`
- **Queries:** 11 (1.0/Tag)
- **Upload:** 2× Dokument-Upload (5332.6 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'DeepSeek' von DeepSeek erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'DeepSeek' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'DeepSeek' (DeepSeek) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'DeepSeek' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'DeepSeek' mit Risk-Score 100 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'DeepSeek' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'DeepSeek' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'DeepSeek' (DeepSeek) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'DeepSeek' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' erfordert DSFA (Datentransfer an DeepSeek). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'DeepSeek' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'DeepSeek' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'DeepSeek' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'DeepSeek' (DeepSeek) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'DeepSeek' ohne technische Dokumentation nach CRA-Anhang V. |
### Cursor — Anysphere

- **Risk:** critical (Score 100)
- **Client:** `client_a62207c2`
- **Queries:** 30 (2.3/Tag)
- **Upload:** 2× Dokument-Upload (3926.0 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'Cursor' von Anysphere erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'Cursor' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Cursor' (Anysphere) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'Cursor' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'Cursor' (Kategorie: code_assistant) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Cursor' mit Risk-Score 100 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'Cursor' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'Cursor' (Anysphere) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Cursor' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Cursor' erfordert DSFA (Datentransfer an Anysphere). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'Cursor' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Cursor' (Kategorie code_assistant) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | non_compliant | 'Cursor' (code_assistant) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Cursor' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'Cursor' (Anysphere) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Cursor' ohne technische Dokumentation nach CRA-Anhang V. |
### DeepSeek — DeepSeek

- **Risk:** critical (Score 100)
- **Client:** `client_a62207c2`
- **Queries:** 13 (1.0/Tag)
- **Upload:** 2× Dokument-Upload (4073.0 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'DeepSeek' von DeepSeek erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'DeepSeek' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'DeepSeek' (DeepSeek) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'DeepSeek' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'DeepSeek' mit Risk-Score 100 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'DeepSeek' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'DeepSeek' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'DeepSeek' (DeepSeek) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'DeepSeek' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' erfordert DSFA (Datentransfer an DeepSeek). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'DeepSeek' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'DeepSeek' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'DeepSeek' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'DeepSeek' (DeepSeek) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'DeepSeek' ohne technische Dokumentation nach CRA-Anhang V. |
### Cursor — Anysphere

- **Risk:** critical (Score 100)
- **Client:** `client_ab152d79`
- **Queries:** 29 (2.4/Tag)
- **Upload:** 3× Dokument-Upload (6108.5 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'Cursor' von Anysphere erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'Cursor' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Cursor' (Anysphere) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'Cursor' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'Cursor' (Kategorie: code_assistant) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Cursor' mit Risk-Score 100 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'Cursor' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'Cursor' (Anysphere) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Cursor' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Cursor' erfordert DSFA (Datentransfer an Anysphere). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'Cursor' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Cursor' (Kategorie code_assistant) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | non_compliant | 'Cursor' (code_assistant) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Cursor' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'Cursor' (Anysphere) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Cursor' ohne technische Dokumentation nach CRA-Anhang V. |
### DeepSeek — DeepSeek

- **Risk:** critical (Score 100)
- **Client:** `client_ab152d79`
- **Queries:** 13 (1.2/Tag)
- **Upload:** 1× Dokument-Upload (2472.8 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'DeepSeek' von DeepSeek erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'DeepSeek' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'DeepSeek' (DeepSeek) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'DeepSeek' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'DeepSeek' mit Risk-Score 100 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'DeepSeek' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'DeepSeek' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'DeepSeek' (DeepSeek) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'DeepSeek' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' erfordert DSFA (Datentransfer an DeepSeek). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'DeepSeek' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'DeepSeek' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'DeepSeek' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'DeepSeek' (DeepSeek) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'DeepSeek' ohne technische Dokumentation nach CRA-Anhang V. |
### GitHub Copilot — GitHub / Microsoft

- **Risk:** critical (Score 100)
- **Client:** `client_bec9d25a`
- **Queries:** 27 (2.2/Tag)
- **Upload:** 2× Dokument-Upload (2718.4 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'GitHub Copilot' von GitHub / Microsoft erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'GitHub Copilot' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'GitHub Copilot' (GitHub / Microsoft) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'GitHub Copilot' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'GitHub Copilot' (Kategorie: code_assistant) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'GitHub Copilot' mit Risk-Score 100 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'GitHub Copilot' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'GitHub Copilot' (GitHub / Microsoft) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'GitHub Copilot' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'GitHub Copilot' erfordert DSFA (Datentransfer an GitHub / Microsoft). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'GitHub Copilot' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'GitHub Copilot' (Kategorie code_assistant) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | non_compliant | 'GitHub Copilot' (code_assistant) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'GitHub Copilot' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'GitHub Copilot' (GitHub / Microsoft) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'GitHub Copilot' ohne technische Dokumentation nach CRA-Anhang V. |
### DeepSeek — DeepSeek

- **Risk:** critical (Score 100)
- **Client:** `client_bfc4bed7`
- **Queries:** 12 (1.1/Tag)
- **Upload:** 3× Dokument-Upload (4415.3 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'DeepSeek' von DeepSeek erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'DeepSeek' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'DeepSeek' (DeepSeek) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'DeepSeek' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'DeepSeek' mit Risk-Score 100 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'DeepSeek' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'DeepSeek' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'DeepSeek' (DeepSeek) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'DeepSeek' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' erfordert DSFA (Datentransfer an DeepSeek). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'DeepSeek' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'DeepSeek' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'DeepSeek' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'DeepSeek' (DeepSeek) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'DeepSeek' ohne technische Dokumentation nach CRA-Anhang V. |
### GitHub Copilot — GitHub / Microsoft

- **Risk:** critical (Score 100)
- **Client:** `client_ccde70e1`
- **Queries:** 30 (2.5/Tag)
- **Upload:** 3× Dokument-Upload (4314.0 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'GitHub Copilot' von GitHub / Microsoft erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'GitHub Copilot' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'GitHub Copilot' (GitHub / Microsoft) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'GitHub Copilot' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'GitHub Copilot' (Kategorie: code_assistant) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'GitHub Copilot' mit Risk-Score 100 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'GitHub Copilot' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'GitHub Copilot' (GitHub / Microsoft) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'GitHub Copilot' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'GitHub Copilot' erfordert DSFA (Datentransfer an GitHub / Microsoft). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'GitHub Copilot' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'GitHub Copilot' (Kategorie code_assistant) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | non_compliant | 'GitHub Copilot' (code_assistant) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'GitHub Copilot' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'GitHub Copilot' (GitHub / Microsoft) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'GitHub Copilot' ohne technische Dokumentation nach CRA-Anhang V. |
### Cursor — Anysphere

- **Risk:** critical (Score 100)
- **Client:** `client_ce22278c`
- **Queries:** 30 (2.5/Tag)
- **Upload:** 1× Dokument-Upload (2684.0 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'Cursor' von Anysphere erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'Cursor' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Cursor' (Anysphere) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'Cursor' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'Cursor' (Kategorie: code_assistant) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Cursor' mit Risk-Score 100 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'Cursor' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'Cursor' (Anysphere) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Cursor' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Cursor' erfordert DSFA (Datentransfer an Anysphere). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'Cursor' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Cursor' (Kategorie code_assistant) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | non_compliant | 'Cursor' (code_assistant) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Cursor' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'Cursor' (Anysphere) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Cursor' ohne technische Dokumentation nach CRA-Anhang V. |
### DeepSeek — DeepSeek

- **Risk:** critical (Score 100)
- **Client:** `client_ce22278c`
- **Queries:** 19 (1.6/Tag)
- **Upload:** 3× Dokument-Upload (10481.4 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'DeepSeek' von DeepSeek erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'DeepSeek' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'DeepSeek' (DeepSeek) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'DeepSeek' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'DeepSeek' mit Risk-Score 100 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'DeepSeek' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'DeepSeek' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'DeepSeek' (DeepSeek) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'DeepSeek' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' erfordert DSFA (Datentransfer an DeepSeek). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'DeepSeek' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'DeepSeek' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'DeepSeek' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'DeepSeek' (DeepSeek) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'DeepSeek' ohne technische Dokumentation nach CRA-Anhang V. |
### Cursor — Anysphere

- **Risk:** critical (Score 100)
- **Client:** `client_e0bf80f6`
- **Queries:** 47 (3.6/Tag)
- **Upload:** 2× Dokument-Upload (2678.3 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'Cursor' von Anysphere erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'Cursor' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Cursor' (Anysphere) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'Cursor' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'Cursor' (Kategorie: code_assistant) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Cursor' mit Risk-Score 100 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'Cursor' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'Cursor' (Anysphere) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Cursor' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Cursor' erfordert DSFA (Datentransfer an Anysphere). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'Cursor' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Cursor' (Kategorie code_assistant) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | non_compliant | 'Cursor' (code_assistant) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Cursor' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'Cursor' (Anysphere) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Cursor' ohne technische Dokumentation nach CRA-Anhang V. |
### DeepSeek — DeepSeek

- **Risk:** critical (Score 100)
- **Client:** `client_e0bf80f6`
- **Queries:** 18 (1.5/Tag)
- **Upload:** 1× Dokument-Upload (1745.6 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'DeepSeek' von DeepSeek erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'DeepSeek' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'DeepSeek' (DeepSeek) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'DeepSeek' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'DeepSeek' mit Risk-Score 100 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'DeepSeek' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'DeepSeek' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'DeepSeek' (DeepSeek) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'DeepSeek' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' erfordert DSFA (Datentransfer an DeepSeek). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'DeepSeek' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'DeepSeek' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'DeepSeek' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'DeepSeek' (DeepSeek) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'DeepSeek' ohne technische Dokumentation nach CRA-Anhang V. |
### Cursor — Anysphere

- **Risk:** critical (Score 100)
- **Client:** `client_faca11e2`
- **Queries:** 18 (1.8/Tag)
- **Upload:** 1× Dokument-Upload (1567.4 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'Cursor' von Anysphere erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'Cursor' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Cursor' (Anysphere) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'Cursor' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'Cursor' (Kategorie: code_assistant) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Cursor' mit Risk-Score 100 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'Cursor' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'Cursor' (Anysphere) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Cursor' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Cursor' erfordert DSFA (Datentransfer an Anysphere). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'Cursor' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Cursor' (Kategorie code_assistant) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | non_compliant | 'Cursor' (code_assistant) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Cursor' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'Cursor' (Anysphere) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Cursor' ohne technische Dokumentation nach CRA-Anhang V. |
### DeepSeek — DeepSeek

- **Risk:** critical (Score 100)
- **Client:** `client_faca11e2`
- **Queries:** 23 (1.8/Tag)
- **Upload:** 3× Dokument-Upload (9494.4 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'DeepSeek' von DeepSeek erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'DeepSeek' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'DeepSeek' (DeepSeek) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'DeepSeek' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'DeepSeek' mit Risk-Score 100 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'DeepSeek' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'DeepSeek' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'DeepSeek' (DeepSeek) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'DeepSeek' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' erfordert DSFA (Datentransfer an DeepSeek). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'DeepSeek' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'DeepSeek' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'DeepSeek' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'DeepSeek' (DeepSeek) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'DeepSeek' ohne technische Dokumentation nach CRA-Anhang V. |
### Perplexity AI — Perplexity

- **Risk:** high (Score 80)
- **Client:** `client_0ee5d804`
- **Queries:** 31 (2.6/Tag)
- **Upload:** 1× Dokument-Upload (1618.3 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Perplexity AI' von Perplexity erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Perplexity AI' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Perplexity AI' (Perplexity) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Perplexity AI' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Perplexity AI' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Perplexity AI' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Perplexity AI' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Perplexity AI' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Perplexity AI' (Perplexity) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Perplexity AI' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Perplexity AI' erfordert DSFA (Datentransfer an Perplexity). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Perplexity AI' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Perplexity AI' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Perplexity AI' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Perplexity AI' (Perplexity) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Perplexity AI' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 80)
- **Client:** `client_144be7d3`
- **Queries:** 22 (1.7/Tag)
- **Upload:** 6× Dokument-Upload (10773.3 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Anthropic Claude' von Anthropic erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Anthropic Claude' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Anthropic Claude' (Anthropic) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Anthropic Claude' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Anthropic Claude' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Anthropic Claude' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Anthropic Claude' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Anthropic Claude' (Anthropic) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Anthropic Claude' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' erfordert DSFA (Datentransfer an Anthropic). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Anthropic Claude' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Anthropic Claude' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Anthropic Claude' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Anthropic Claude' (Anthropic) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Anthropic Claude' ohne technische Dokumentation nach CRA-Anhang V. |
### Cursor — Anysphere

- **Risk:** critical (Score 80)
- **Client:** `client_144be7d3`
- **Queries:** 41 (3.2/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'Cursor' von Anysphere erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'Cursor' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Cursor' (Anysphere) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'Cursor' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'Cursor' (Kategorie: code_assistant) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Cursor' mit Risk-Score 80 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'Cursor' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'Cursor' (Anysphere) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Cursor' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Cursor' erfordert DSFA (Datentransfer an Anysphere). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'Cursor' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Cursor' (Kategorie code_assistant) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | non_compliant | 'Cursor' (code_assistant) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'Cursor' (Anysphere) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Cursor' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 80)
- **Client:** `client_144be7d3`
- **Queries:** 11 (1.2/Tag)
- **Upload:** 5× Dokument-Upload (8282.0 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'OpenAI ChatGPT' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'OpenAI ChatGPT' (OpenAI) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' erfordert DSFA (Datentransfer an OpenAI). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'OpenAI ChatGPT' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'OpenAI ChatGPT' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'OpenAI ChatGPT' (OpenAI) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'OpenAI ChatGPT' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 80)
- **Client:** `client_159a17cd`
- **Queries:** 42 (3.5/Tag)
- **Upload:** 7× Dokument-Upload (11716.1 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'OpenAI ChatGPT' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'OpenAI ChatGPT' (OpenAI) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' erfordert DSFA (Datentransfer an OpenAI). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'OpenAI ChatGPT' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'OpenAI ChatGPT' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'OpenAI ChatGPT' (OpenAI) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'OpenAI ChatGPT' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 80)
- **Client:** `client_1dc78685`
- **Queries:** 12 (1.0/Tag)
- **Upload:** 2× Dokument-Upload (5686.5 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Anthropic Claude' von Anthropic erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Anthropic Claude' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Anthropic Claude' (Anthropic) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Anthropic Claude' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Anthropic Claude' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Anthropic Claude' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Anthropic Claude' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Anthropic Claude' (Anthropic) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Anthropic Claude' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' erfordert DSFA (Datentransfer an Anthropic). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Anthropic Claude' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Anthropic Claude' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Anthropic Claude' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Anthropic Claude' (Anthropic) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Anthropic Claude' ohne technische Dokumentation nach CRA-Anhang V. |
### Cursor — Anysphere

- **Risk:** critical (Score 80)
- **Client:** `client_1dc78685`
- **Queries:** 25 (2.1/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'Cursor' von Anysphere erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'Cursor' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Cursor' (Anysphere) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'Cursor' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'Cursor' (Kategorie: code_assistant) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Cursor' mit Risk-Score 80 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'Cursor' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'Cursor' (Anysphere) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Cursor' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Cursor' erfordert DSFA (Datentransfer an Anysphere). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'Cursor' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Cursor' (Kategorie code_assistant) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | non_compliant | 'Cursor' (code_assistant) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'Cursor' (Anysphere) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Cursor' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 80)
- **Client:** `client_1dc78685`
- **Queries:** 30 (2.3/Tag)
- **Upload:** 8× Dokument-Upload (17866.8 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'OpenAI ChatGPT' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'OpenAI ChatGPT' (OpenAI) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' erfordert DSFA (Datentransfer an OpenAI). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'OpenAI ChatGPT' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'OpenAI ChatGPT' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'OpenAI ChatGPT' (OpenAI) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'OpenAI ChatGPT' ohne technische Dokumentation nach CRA-Anhang V. |
### Google Gemini — Google

- **Risk:** high (Score 80)
- **Client:** `client_22672cb7`
- **Queries:** 30 (2.5/Tag)
- **Upload:** 7× Dokument-Upload (9579.0 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Google Gemini' von Google erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Google Gemini' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Google Gemini' (Google) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Google Gemini' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Google Gemini' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Google Gemini' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Google Gemini' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Google Gemini' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Google Gemini' (Google) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Google Gemini' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Google Gemini' erfordert DSFA (Datentransfer an Google). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Google Gemini' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Google Gemini' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Google Gemini' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Google Gemini' (Google) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Google Gemini' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 80)
- **Client:** `client_2632e438`
- **Queries:** 22 (1.8/Tag)
- **Upload:** 4× Dokument-Upload (6669.6 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Anthropic Claude' von Anthropic erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Anthropic Claude' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Anthropic Claude' (Anthropic) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Anthropic Claude' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Anthropic Claude' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Anthropic Claude' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Anthropic Claude' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Anthropic Claude' (Anthropic) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Anthropic Claude' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' erfordert DSFA (Datentransfer an Anthropic). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Anthropic Claude' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Anthropic Claude' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Anthropic Claude' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Anthropic Claude' (Anthropic) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Anthropic Claude' ohne technische Dokumentation nach CRA-Anhang V. |
### Cursor — Anysphere

- **Risk:** critical (Score 80)
- **Client:** `client_2632e438`
- **Queries:** 35 (3.5/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'Cursor' von Anysphere erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'Cursor' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Cursor' (Anysphere) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'Cursor' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'Cursor' (Kategorie: code_assistant) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Cursor' mit Risk-Score 80 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'Cursor' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'Cursor' (Anysphere) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Cursor' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Cursor' erfordert DSFA (Datentransfer an Anysphere). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'Cursor' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Cursor' (Kategorie code_assistant) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | non_compliant | 'Cursor' (code_assistant) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'Cursor' (Anysphere) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Cursor' ohne technische Dokumentation nach CRA-Anhang V. |
### Google Gemini — Google

- **Risk:** high (Score 80)
- **Client:** `client_2a1cb879`
- **Queries:** 28 (2.3/Tag)
- **Upload:** 5× Dokument-Upload (14075.7 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Google Gemini' von Google erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Google Gemini' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Google Gemini' (Google) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Google Gemini' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Google Gemini' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Google Gemini' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Google Gemini' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Google Gemini' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Google Gemini' (Google) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Google Gemini' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Google Gemini' erfordert DSFA (Datentransfer an Google). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Google Gemini' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Google Gemini' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Google Gemini' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Google Gemini' (Google) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Google Gemini' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 80)
- **Client:** `client_3a0b2034`
- **Queries:** 33 (2.8/Tag)
- **Upload:** 11× Dokument-Upload (16358.5 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Anthropic Claude' von Anthropic erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Anthropic Claude' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Anthropic Claude' (Anthropic) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Anthropic Claude' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Anthropic Claude' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Anthropic Claude' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Anthropic Claude' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Anthropic Claude' (Anthropic) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Anthropic Claude' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' erfordert DSFA (Datentransfer an Anthropic). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Anthropic Claude' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Anthropic Claude' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Anthropic Claude' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Anthropic Claude' (Anthropic) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Anthropic Claude' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 80)
- **Client:** `client_4dd00205`
- **Queries:** 32 (2.5/Tag)
- **Upload:** 6× Dokument-Upload (12736.3 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'OpenAI ChatGPT' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'OpenAI ChatGPT' (OpenAI) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' erfordert DSFA (Datentransfer an OpenAI). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'OpenAI ChatGPT' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'OpenAI ChatGPT' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'OpenAI ChatGPT' (OpenAI) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'OpenAI ChatGPT' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 80)
- **Client:** `client_5cac0f7a`
- **Queries:** 23 (1.9/Tag)
- **Upload:** 8× Dokument-Upload (16567.8 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Anthropic Claude' von Anthropic erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Anthropic Claude' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Anthropic Claude' (Anthropic) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Anthropic Claude' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Anthropic Claude' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Anthropic Claude' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Anthropic Claude' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Anthropic Claude' (Anthropic) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Anthropic Claude' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' erfordert DSFA (Datentransfer an Anthropic). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Anthropic Claude' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Anthropic Claude' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Anthropic Claude' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Anthropic Claude' (Anthropic) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Anthropic Claude' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 80)
- **Client:** `client_5cac0f7a`
- **Queries:** 15 (1.4/Tag)
- **Upload:** 2× Dokument-Upload (6149.9 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'OpenAI ChatGPT' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'OpenAI ChatGPT' (OpenAI) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' erfordert DSFA (Datentransfer an OpenAI). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'OpenAI ChatGPT' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'OpenAI ChatGPT' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'OpenAI ChatGPT' (OpenAI) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'OpenAI ChatGPT' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 80)
- **Client:** `client_6318295c`
- **Queries:** 20 (2.0/Tag)
- **Upload:** 3× Dokument-Upload (14715.6 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Anthropic Claude' von Anthropic erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Anthropic Claude' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Anthropic Claude' (Anthropic) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Anthropic Claude' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Anthropic Claude' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Anthropic Claude' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Anthropic Claude' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Anthropic Claude' (Anthropic) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Anthropic Claude' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' erfordert DSFA (Datentransfer an Anthropic). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Anthropic Claude' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Anthropic Claude' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Anthropic Claude' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Anthropic Claude' (Anthropic) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Anthropic Claude' ohne technische Dokumentation nach CRA-Anhang V. |
### Cursor — Anysphere

- **Risk:** critical (Score 80)
- **Client:** `client_6318295c`
- **Queries:** 37 (2.8/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'Cursor' von Anysphere erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'Cursor' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Cursor' (Anysphere) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'Cursor' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'Cursor' (Kategorie: code_assistant) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Cursor' mit Risk-Score 80 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'Cursor' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'Cursor' (Anysphere) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Cursor' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Cursor' erfordert DSFA (Datentransfer an Anysphere). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'Cursor' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Cursor' (Kategorie code_assistant) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | non_compliant | 'Cursor' (code_assistant) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'Cursor' (Anysphere) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Cursor' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 80)
- **Client:** `client_6318295c`
- **Queries:** 13 (1.1/Tag)
- **Upload:** 3× Dokument-Upload (4304.6 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'OpenAI ChatGPT' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'OpenAI ChatGPT' (OpenAI) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' erfordert DSFA (Datentransfer an OpenAI). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'OpenAI ChatGPT' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'OpenAI ChatGPT' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'OpenAI ChatGPT' (OpenAI) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'OpenAI ChatGPT' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 80)
- **Client:** `client_64f36f5f`
- **Queries:** 22 (1.7/Tag)
- **Upload:** 5× Dokument-Upload (11238.6 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Anthropic Claude' von Anthropic erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Anthropic Claude' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Anthropic Claude' (Anthropic) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Anthropic Claude' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Anthropic Claude' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Anthropic Claude' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Anthropic Claude' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Anthropic Claude' (Anthropic) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Anthropic Claude' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' erfordert DSFA (Datentransfer an Anthropic). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Anthropic Claude' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Anthropic Claude' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Anthropic Claude' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Anthropic Claude' (Anthropic) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Anthropic Claude' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 80)
- **Client:** `client_64f36f5f`
- **Queries:** 11 (1.0/Tag)
- **Upload:** 1× Dokument-Upload (1095.5 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'OpenAI ChatGPT' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'OpenAI ChatGPT' (OpenAI) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' erfordert DSFA (Datentransfer an OpenAI). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'OpenAI ChatGPT' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'OpenAI ChatGPT' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'OpenAI ChatGPT' (OpenAI) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'OpenAI ChatGPT' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 80)
- **Client:** `client_661b9a57`
- **Queries:** 45 (3.5/Tag)
- **Upload:** 9× Dokument-Upload (19272.9 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'OpenAI ChatGPT' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'OpenAI ChatGPT' (OpenAI) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' erfordert DSFA (Datentransfer an OpenAI). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'OpenAI ChatGPT' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'OpenAI ChatGPT' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'OpenAI ChatGPT' (OpenAI) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'OpenAI ChatGPT' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 80)
- **Client:** `client_75babc12`
- **Queries:** 17 (1.5/Tag)
- **Upload:** 3× Dokument-Upload (9675.2 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Anthropic Claude' von Anthropic erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Anthropic Claude' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Anthropic Claude' (Anthropic) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Anthropic Claude' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Anthropic Claude' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Anthropic Claude' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Anthropic Claude' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Anthropic Claude' (Anthropic) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Anthropic Claude' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' erfordert DSFA (Datentransfer an Anthropic). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Anthropic Claude' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Anthropic Claude' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Anthropic Claude' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Anthropic Claude' (Anthropic) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Anthropic Claude' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 80)
- **Client:** `client_75babc12`
- **Queries:** 16 (1.5/Tag)
- **Upload:** 4× Dokument-Upload (12956.9 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'OpenAI ChatGPT' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'OpenAI ChatGPT' (OpenAI) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' erfordert DSFA (Datentransfer an OpenAI). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'OpenAI ChatGPT' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'OpenAI ChatGPT' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'OpenAI ChatGPT' (OpenAI) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'OpenAI ChatGPT' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 80)
- **Client:** `client_7eade85b`
- **Queries:** 28 (2.2/Tag)
- **Upload:** 8× Dokument-Upload (21122.9 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Anthropic Claude' von Anthropic erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Anthropic Claude' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Anthropic Claude' (Anthropic) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Anthropic Claude' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Anthropic Claude' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Anthropic Claude' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Anthropic Claude' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Anthropic Claude' (Anthropic) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Anthropic Claude' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' erfordert DSFA (Datentransfer an Anthropic). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Anthropic Claude' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Anthropic Claude' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Anthropic Claude' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Anthropic Claude' (Anthropic) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Anthropic Claude' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 80)
- **Client:** `client_8807a2b8`
- **Queries:** 35 (2.7/Tag)
- **Upload:** 9× Dokument-Upload (10888.0 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Anthropic Claude' von Anthropic erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Anthropic Claude' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Anthropic Claude' (Anthropic) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Anthropic Claude' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Anthropic Claude' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Anthropic Claude' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Anthropic Claude' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Anthropic Claude' (Anthropic) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Anthropic Claude' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' erfordert DSFA (Datentransfer an Anthropic). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Anthropic Claude' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Anthropic Claude' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Anthropic Claude' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Anthropic Claude' (Anthropic) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Anthropic Claude' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 80)
- **Client:** `client_8ef5b6c7`
- **Queries:** 16 (1.3/Tag)
- **Upload:** 5× Dokument-Upload (17971.8 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Anthropic Claude' von Anthropic erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Anthropic Claude' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Anthropic Claude' (Anthropic) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Anthropic Claude' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Anthropic Claude' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Anthropic Claude' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Anthropic Claude' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Anthropic Claude' (Anthropic) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Anthropic Claude' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' erfordert DSFA (Datentransfer an Anthropic). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Anthropic Claude' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Anthropic Claude' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Anthropic Claude' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Anthropic Claude' (Anthropic) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Anthropic Claude' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 80)
- **Client:** `client_8ef5b6c7`
- **Queries:** 20 (2.0/Tag)
- **Upload:** 6× Dokument-Upload (7288.1 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'OpenAI ChatGPT' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'OpenAI ChatGPT' (OpenAI) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' erfordert DSFA (Datentransfer an OpenAI). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'OpenAI ChatGPT' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'OpenAI ChatGPT' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'OpenAI ChatGPT' (OpenAI) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'OpenAI ChatGPT' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 80)
- **Client:** `client_9be49256`
- **Queries:** 31 (2.4/Tag)
- **Upload:** 6× Dokument-Upload (11292.9 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'OpenAI ChatGPT' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'OpenAI ChatGPT' (OpenAI) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' erfordert DSFA (Datentransfer an OpenAI). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'OpenAI ChatGPT' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'OpenAI ChatGPT' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'OpenAI ChatGPT' (OpenAI) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'OpenAI ChatGPT' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 80)
- **Client:** `client_a141fb06`
- **Queries:** 16 (1.5/Tag)
- **Upload:** 2× Dokument-Upload (2030.7 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Anthropic Claude' von Anthropic erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Anthropic Claude' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Anthropic Claude' (Anthropic) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Anthropic Claude' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Anthropic Claude' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Anthropic Claude' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Anthropic Claude' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Anthropic Claude' (Anthropic) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Anthropic Claude' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' erfordert DSFA (Datentransfer an Anthropic). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Anthropic Claude' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Anthropic Claude' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Anthropic Claude' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Anthropic Claude' (Anthropic) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Anthropic Claude' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 80)
- **Client:** `client_a141fb06`
- **Queries:** 19 (1.5/Tag)
- **Upload:** 3× Dokument-Upload (8437.3 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'OpenAI ChatGPT' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'OpenAI ChatGPT' (OpenAI) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' erfordert DSFA (Datentransfer an OpenAI). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'OpenAI ChatGPT' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'OpenAI ChatGPT' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'OpenAI ChatGPT' (OpenAI) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'OpenAI ChatGPT' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 80)
- **Client:** `client_a62207c2`
- **Queries:** 18 (1.6/Tag)
- **Upload:** 5× Dokument-Upload (5807.9 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Anthropic Claude' von Anthropic erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Anthropic Claude' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Anthropic Claude' (Anthropic) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Anthropic Claude' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Anthropic Claude' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Anthropic Claude' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Anthropic Claude' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Anthropic Claude' (Anthropic) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Anthropic Claude' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' erfordert DSFA (Datentransfer an Anthropic). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Anthropic Claude' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Anthropic Claude' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Anthropic Claude' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Anthropic Claude' (Anthropic) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Anthropic Claude' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 80)
- **Client:** `client_a62207c2`
- **Queries:** 19 (1.6/Tag)
- **Upload:** 4× Dokument-Upload (5414.4 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'OpenAI ChatGPT' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'OpenAI ChatGPT' (OpenAI) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' erfordert DSFA (Datentransfer an OpenAI). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'OpenAI ChatGPT' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'OpenAI ChatGPT' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'OpenAI ChatGPT' (OpenAI) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'OpenAI ChatGPT' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 80)
- **Client:** `client_ab152d79`
- **Queries:** 21 (2.1/Tag)
- **Upload:** 9× Dokument-Upload (17846.2 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Anthropic Claude' von Anthropic erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Anthropic Claude' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Anthropic Claude' (Anthropic) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Anthropic Claude' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Anthropic Claude' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Anthropic Claude' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Anthropic Claude' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Anthropic Claude' (Anthropic) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Anthropic Claude' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' erfordert DSFA (Datentransfer an Anthropic). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Anthropic Claude' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Anthropic Claude' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Anthropic Claude' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Anthropic Claude' (Anthropic) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Anthropic Claude' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 80)
- **Client:** `client_ab152d79`
- **Queries:** 20 (1.7/Tag)
- **Upload:** 5× Dokument-Upload (13793.3 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'OpenAI ChatGPT' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'OpenAI ChatGPT' (OpenAI) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' erfordert DSFA (Datentransfer an OpenAI). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'OpenAI ChatGPT' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'OpenAI ChatGPT' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'OpenAI ChatGPT' (OpenAI) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'OpenAI ChatGPT' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 80)
- **Client:** `client_b60d1ba2`
- **Queries:** 33 (3.0/Tag)
- **Upload:** 7× Dokument-Upload (11671.0 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Anthropic Claude' von Anthropic erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Anthropic Claude' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Anthropic Claude' (Anthropic) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Anthropic Claude' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Anthropic Claude' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Anthropic Claude' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Anthropic Claude' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Anthropic Claude' (Anthropic) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Anthropic Claude' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' erfordert DSFA (Datentransfer an Anthropic). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Anthropic Claude' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Anthropic Claude' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Anthropic Claude' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Anthropic Claude' (Anthropic) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Anthropic Claude' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 80)
- **Client:** `client_bfc4bed7`
- **Queries:** 10 (1.0/Tag)
- **Upload:** 1× Dokument-Upload (6076.4 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Anthropic Claude' von Anthropic erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Anthropic Claude' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Anthropic Claude' (Anthropic) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Anthropic Claude' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Anthropic Claude' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Anthropic Claude' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Anthropic Claude' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Anthropic Claude' (Anthropic) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Anthropic Claude' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' erfordert DSFA (Datentransfer an Anthropic). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Anthropic Claude' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Anthropic Claude' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Anthropic Claude' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Anthropic Claude' (Anthropic) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Anthropic Claude' ohne technische Dokumentation nach CRA-Anhang V. |
### Cursor — Anysphere

- **Risk:** critical (Score 80)
- **Client:** `client_bfc4bed7`
- **Queries:** 32 (2.5/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'Cursor' von Anysphere erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'Cursor' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Cursor' (Anysphere) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'Cursor' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'Cursor' (Kategorie: code_assistant) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Cursor' mit Risk-Score 80 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'Cursor' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'Cursor' (Anysphere) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Cursor' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Cursor' erfordert DSFA (Datentransfer an Anysphere). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'Cursor' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Cursor' (Kategorie code_assistant) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | non_compliant | 'Cursor' (code_assistant) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'Cursor' (Anysphere) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Cursor' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 80)
- **Client:** `client_bfc4bed7`
- **Queries:** 12 (1.2/Tag)
- **Upload:** 6× Dokument-Upload (12321.2 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'OpenAI ChatGPT' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'OpenAI ChatGPT' (OpenAI) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' erfordert DSFA (Datentransfer an OpenAI). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'OpenAI ChatGPT' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'OpenAI ChatGPT' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'OpenAI ChatGPT' (OpenAI) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'OpenAI ChatGPT' ohne technische Dokumentation nach CRA-Anhang V. |
### Perplexity AI — Perplexity

- **Risk:** high (Score 80)
- **Client:** `client_c0252d7e`
- **Queries:** 21 (1.6/Tag)
- **Upload:** 1× Dokument-Upload (3499.7 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Perplexity AI' von Perplexity erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Perplexity AI' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Perplexity AI' (Perplexity) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Perplexity AI' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Perplexity AI' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Perplexity AI' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Perplexity AI' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Perplexity AI' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Perplexity AI' (Perplexity) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Perplexity AI' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Perplexity AI' erfordert DSFA (Datentransfer an Perplexity). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Perplexity AI' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Perplexity AI' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Perplexity AI' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Perplexity AI' (Perplexity) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Perplexity AI' ohne technische Dokumentation nach CRA-Anhang V. |
### Google Gemini — Google

- **Risk:** high (Score 80)
- **Client:** `client_c04b3ab5`
- **Queries:** 50 (3.8/Tag)
- **Upload:** 9× Dokument-Upload (16808.7 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Google Gemini' von Google erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Google Gemini' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Google Gemini' (Google) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Google Gemini' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Google Gemini' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Google Gemini' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Google Gemini' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Google Gemini' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Google Gemini' (Google) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Google Gemini' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Google Gemini' erfordert DSFA (Datentransfer an Google). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Google Gemini' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Google Gemini' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Google Gemini' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Google Gemini' (Google) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Google Gemini' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 80)
- **Client:** `client_ce22278c`
- **Queries:** 15 (1.4/Tag)
- **Upload:** 3× Dokument-Upload (8271.7 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Anthropic Claude' von Anthropic erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Anthropic Claude' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Anthropic Claude' (Anthropic) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Anthropic Claude' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Anthropic Claude' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Anthropic Claude' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Anthropic Claude' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Anthropic Claude' (Anthropic) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Anthropic Claude' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' erfordert DSFA (Datentransfer an Anthropic). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Anthropic Claude' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Anthropic Claude' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Anthropic Claude' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Anthropic Claude' (Anthropic) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Anthropic Claude' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 80)
- **Client:** `client_ce22278c`
- **Queries:** 15 (1.2/Tag)
- **Upload:** 2× Dokument-Upload (1567.7 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'OpenAI ChatGPT' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'OpenAI ChatGPT' (OpenAI) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' erfordert DSFA (Datentransfer an OpenAI). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'OpenAI ChatGPT' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'OpenAI ChatGPT' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'OpenAI ChatGPT' (OpenAI) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'OpenAI ChatGPT' ohne technische Dokumentation nach CRA-Anhang V. |
### Perplexity AI — Perplexity

- **Risk:** high (Score 80)
- **Client:** `client_d3c76b46`
- **Queries:** 26 (2.2/Tag)
- **Upload:** 2× Dokument-Upload (3344.5 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Perplexity AI' von Perplexity erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Perplexity AI' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Perplexity AI' (Perplexity) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Perplexity AI' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Perplexity AI' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Perplexity AI' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Perplexity AI' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Perplexity AI' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Perplexity AI' (Perplexity) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Perplexity AI' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Perplexity AI' erfordert DSFA (Datentransfer an Perplexity). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Perplexity AI' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Perplexity AI' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Perplexity AI' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Perplexity AI' (Perplexity) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Perplexity AI' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 80)
- **Client:** `client_e0bf80f6`
- **Queries:** 23 (1.9/Tag)
- **Upload:** 6× Dokument-Upload (21537.4 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Anthropic Claude' von Anthropic erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Anthropic Claude' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Anthropic Claude' (Anthropic) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Anthropic Claude' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Anthropic Claude' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Anthropic Claude' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Anthropic Claude' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Anthropic Claude' (Anthropic) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Anthropic Claude' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' erfordert DSFA (Datentransfer an Anthropic). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Anthropic Claude' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Anthropic Claude' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Anthropic Claude' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Anthropic Claude' (Anthropic) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Anthropic Claude' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 80)
- **Client:** `client_e0bf80f6`
- **Queries:** 15 (1.2/Tag)
- **Upload:** 4× Dokument-Upload (9216.9 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'OpenAI ChatGPT' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'OpenAI ChatGPT' (OpenAI) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' erfordert DSFA (Datentransfer an OpenAI). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'OpenAI ChatGPT' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'OpenAI ChatGPT' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'OpenAI ChatGPT' (OpenAI) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'OpenAI ChatGPT' ohne technische Dokumentation nach CRA-Anhang V. |
### Google Gemini — Google

- **Risk:** high (Score 80)
- **Client:** `client_ed14a61a`
- **Queries:** 39 (3.0/Tag)
- **Upload:** 6× Dokument-Upload (9882.6 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Google Gemini' von Google erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Google Gemini' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Google Gemini' (Google) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Google Gemini' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Google Gemini' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Google Gemini' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Google Gemini' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Google Gemini' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Google Gemini' (Google) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Google Gemini' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Google Gemini' erfordert DSFA (Datentransfer an Google). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Google Gemini' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Google Gemini' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Google Gemini' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Google Gemini' (Google) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Google Gemini' ohne technische Dokumentation nach CRA-Anhang V. |
### Perplexity AI — Perplexity

- **Risk:** high (Score 80)
- **Client:** `client_f5fcbe33`
- **Queries:** 41 (3.2/Tag)
- **Upload:** 3× Dokument-Upload (6464.7 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Perplexity AI' von Perplexity erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Perplexity AI' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Perplexity AI' (Perplexity) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Perplexity AI' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Perplexity AI' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Perplexity AI' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Perplexity AI' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Perplexity AI' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Perplexity AI' (Perplexity) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Perplexity AI' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Perplexity AI' erfordert DSFA (Datentransfer an Perplexity). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Perplexity AI' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Perplexity AI' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Perplexity AI' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Perplexity AI' (Perplexity) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Perplexity AI' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 80)
- **Client:** `client_faca11e2`
- **Queries:** 19 (1.5/Tag)
- **Upload:** 6× Dokument-Upload (11135.0 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'Anthropic Claude' von Anthropic erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'Anthropic Claude' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'Anthropic Claude' (Anthropic) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'Anthropic Claude' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'Anthropic Claude' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'Anthropic Claude' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'Anthropic Claude' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'Anthropic Claude' (Anthropic) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'Anthropic Claude' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' erfordert DSFA (Datentransfer an Anthropic). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'Anthropic Claude' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'Anthropic Claude' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'Anthropic Claude' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'Anthropic Claude' (Anthropic) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'Anthropic Claude' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 80)
- **Client:** `client_faca11e2`
- **Queries:** 13 (1.1/Tag)
- **Upload:** 2× Dokument-Upload (2938.1 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 80 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'OpenAI ChatGPT' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | non_compliant | Datenverarbeitung durch 'OpenAI ChatGPT' (OpenAI) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'OpenAI ChatGPT' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' erfordert DSFA (Datentransfer an OpenAI). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'OpenAI ChatGPT' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | non_compliant | Dokument-Uploads an 'OpenAI ChatGPT' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | non_compliant | Hochrisiko-Dienst 'OpenAI ChatGPT' (OpenAI) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'OpenAI ChatGPT' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 60)
- **Client:** `client_2632e438`
- **Queries:** 13 (1.2/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | partially_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | partially_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | partially_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | partially_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | partially_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 60 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | partially_compliant | GPAI-Modell 'OpenAI ChatGPT' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | partially_compliant | KI-Dienst 'OpenAI ChatGPT' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | partially_compliant | Datenverarbeitung durch 'OpenAI ChatGPT' (OpenAI) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'OpenAI ChatGPT' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | partially_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' erfordert DSFA (Datentransfer an OpenAI). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | partially_compliant | KI-Dienst 'OpenAI ChatGPT' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | partially_compliant | 'OpenAI ChatGPT' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | partially_compliant | Hochrisiko-Dienst 'OpenAI ChatGPT' (OpenAI) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'OpenAI ChatGPT' ohne technische Dokumentation nach CRA-Anhang V. |
### Hugging Face — Hugging Face

- **Risk:** high (Score 60)
- **Client:** `client_2dfdf2f7`
- **Queries:** 8 (1.0/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | partially_compliant | Nicht-inventarisierter KI-Dienst 'Hugging Face' von Hugging Face erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | partially_compliant | Cloud-basierter KI-Dienst 'Hugging Face' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'Hugging Face' (Hugging Face) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | partially_compliant | Hochrisiko-KI-Dienst 'Hugging Face' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | partially_compliant | KI-System 'Hugging Face' (Kategorie: ml_platform) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | partially_compliant | KI-Dienst 'Hugging Face' mit Risk-Score 60 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | partially_compliant | GPAI-Modell 'Hugging Face' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | partially_compliant | KI-Dienst 'Hugging Face' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | partially_compliant | Datenverarbeitung durch 'Hugging Face' (Hugging Face) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'Hugging Face' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | partially_compliant | Hochrisiko-KI-Dienst 'Hugging Face' erfordert DSFA (Datentransfer an Hugging Face). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | partially_compliant | KI-Dienst 'Hugging Face' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | partially_compliant | 'Hugging Face' (Kategorie ml_platform) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | partially_compliant | Hochrisiko-Dienst 'Hugging Face' (Hugging Face) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'Hugging Face' ohne technische Dokumentation nach CRA-Anhang V. |
### Mistral AI — Mistral

- **Risk:** high (Score 60)
- **Client:** `client_48d7c436`
- **Queries:** 8 (0.7/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | partially_compliant | Nicht-inventarisierter KI-Dienst 'Mistral AI' von Mistral erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | partially_compliant | Cloud-basierter KI-Dienst 'Mistral AI' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'Mistral AI' (Mistral) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | partially_compliant | Hochrisiko-KI-Dienst 'Mistral AI' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | partially_compliant | KI-System 'Mistral AI' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | partially_compliant | KI-Dienst 'Mistral AI' mit Risk-Score 60 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | partially_compliant | GPAI-Modell 'Mistral AI' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | partially_compliant | KI-Dienst 'Mistral AI' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | partially_compliant | Datenverarbeitung durch 'Mistral AI' (Mistral) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'Mistral AI' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | partially_compliant | Hochrisiko-KI-Dienst 'Mistral AI' erfordert DSFA (Datentransfer an Mistral). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | partially_compliant | KI-Dienst 'Mistral AI' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | partially_compliant | 'Mistral AI' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | partially_compliant | Hochrisiko-Dienst 'Mistral AI' (Mistral) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'Mistral AI' ohne technische Dokumentation nach CRA-Anhang V. |
### Grammarly AI — Grammarly

- **Risk:** medium (Score 60)
- **Client:** `client_d5b8476f`
- **Queries:** 5 (0.5/Tag)
- **Upload:** 1× Dokument-Upload (1275.0 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | medium | partially_compliant | Nicht-inventarisierter KI-Dienst 'Grammarly AI' von Grammarly erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | medium | partially_compliant | Cloud-basierter KI-Dienst 'Grammarly AI' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | medium | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'Grammarly AI' (Grammarly) im Einsatz. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | partially_compliant | KI-Dienst 'Grammarly AI' mit Risk-Score 60 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | medium | partially_compliant | KI-Dienst 'Grammarly AI' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | medium | partially_compliant | Datenverarbeitung durch 'Grammarly AI' (Grammarly) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'Grammarly AI' ohne Privacy-by-Design-Bewertung. |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | medium | partially_compliant | KI-Dienst 'Grammarly AI' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 11` (Obligations for Manufacturers — Vulnerability Handling) | high | partially_compliant | Dokument-Uploads an 'Grammarly AI' ohne nachgewiesenes Vulnerability-Handling-Verfahren. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'Grammarly AI' ohne technische Dokumentation nach CRA-Anhang V. |
### Mistral AI — Mistral

- **Risk:** high (Score 55)
- **Client:** `client_7d688da0`
- **Queries:** 6 (0.9/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | partially_compliant | Nicht-inventarisierter KI-Dienst 'Mistral AI' von Mistral erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | partially_compliant | Cloud-basierter KI-Dienst 'Mistral AI' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'Mistral AI' (Mistral) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | partially_compliant | Hochrisiko-KI-Dienst 'Mistral AI' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | partially_compliant | KI-System 'Mistral AI' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | partially_compliant | KI-Dienst 'Mistral AI' mit Risk-Score 55 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | partially_compliant | GPAI-Modell 'Mistral AI' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | partially_compliant | KI-Dienst 'Mistral AI' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | partially_compliant | Datenverarbeitung durch 'Mistral AI' (Mistral) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'Mistral AI' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | partially_compliant | Hochrisiko-KI-Dienst 'Mistral AI' erfordert DSFA (Datentransfer an Mistral). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | partially_compliant | KI-Dienst 'Mistral AI' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | partially_compliant | 'Mistral AI' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | partially_compliant | Hochrisiko-Dienst 'Mistral AI' (Mistral) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'Mistral AI' ohne technische Dokumentation nach CRA-Anhang V. |
### Hugging Face — Hugging Face

- **Risk:** high (Score 55)
- **Client:** `client_ed11768c`
- **Queries:** 6 (0.9/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | partially_compliant | Nicht-inventarisierter KI-Dienst 'Hugging Face' von Hugging Face erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | partially_compliant | Cloud-basierter KI-Dienst 'Hugging Face' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'Hugging Face' (Hugging Face) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | partially_compliant | Hochrisiko-KI-Dienst 'Hugging Face' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | partially_compliant | KI-System 'Hugging Face' (Kategorie: ml_platform) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | partially_compliant | KI-Dienst 'Hugging Face' mit Risk-Score 55 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | partially_compliant | GPAI-Modell 'Hugging Face' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | partially_compliant | KI-Dienst 'Hugging Face' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | partially_compliant | Datenverarbeitung durch 'Hugging Face' (Hugging Face) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'Hugging Face' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | partially_compliant | Hochrisiko-KI-Dienst 'Hugging Face' erfordert DSFA (Datentransfer an Hugging Face). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | partially_compliant | KI-Dienst 'Hugging Face' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | partially_compliant | 'Hugging Face' (Kategorie ml_platform) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | partially_compliant | Hochrisiko-Dienst 'Hugging Face' (Hugging Face) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'Hugging Face' ohne technische Dokumentation nach CRA-Anhang V. |
### Midjourney — Midjourney

- **Risk:** medium (Score 40)
- **Client:** `client_6ad2f1c8`
- **Queries:** 8 (0.8/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | medium | partially_compliant | Nicht-inventarisierter KI-Dienst 'Midjourney' von Midjourney erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | medium | partially_compliant | Cloud-basierter KI-Dienst 'Midjourney' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | medium | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'Midjourney' (Midjourney) im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | medium | partially_compliant | KI-Dienst 'Midjourney' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | medium | partially_compliant | Datenverarbeitung durch 'Midjourney' (Midjourney) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'Midjourney' ohne Privacy-by-Design-Bewertung. |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | medium | partially_compliant | KI-Dienst 'Midjourney' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'Midjourney' ohne technische Dokumentation nach CRA-Anhang V. |
### DeepL — DeepL

- **Risk:** medium (Score 40)
- **Client:** `client_7c6a8790`
- **Queries:** 5 (0.5/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | medium | partially_compliant | Nicht-inventarisierter KI-Dienst 'DeepL' von DeepL erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | medium | partially_compliant | Cloud-basierter KI-Dienst 'DeepL' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | medium | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'DeepL' (DeepL) im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | medium | partially_compliant | KI-Dienst 'DeepL' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | medium | partially_compliant | Datenverarbeitung durch 'DeepL' (DeepL) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'DeepL' ohne Privacy-by-Design-Bewertung. |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | medium | partially_compliant | KI-Dienst 'DeepL' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'DeepL' ohne technische Dokumentation nach CRA-Anhang V. |
### DeepL — DeepL

- **Risk:** medium (Score 40)
- **Client:** `client_a4541cb3`
- **Queries:** 10 (0.9/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | medium | partially_compliant | Nicht-inventarisierter KI-Dienst 'DeepL' von DeepL erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | medium | partially_compliant | Cloud-basierter KI-Dienst 'DeepL' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | medium | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'DeepL' (DeepL) im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | medium | partially_compliant | KI-Dienst 'DeepL' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | medium | partially_compliant | Datenverarbeitung durch 'DeepL' (DeepL) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'DeepL' ohne Privacy-by-Design-Bewertung. |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | medium | partially_compliant | KI-Dienst 'DeepL' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'DeepL' ohne technische Dokumentation nach CRA-Anhang V. |
### Midjourney — Midjourney

- **Risk:** medium (Score 40)
- **Client:** `client_c2e6f2a0`
- **Queries:** 13 (1.4/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | medium | partially_compliant | Nicht-inventarisierter KI-Dienst 'Midjourney' von Midjourney erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | medium | partially_compliant | Cloud-basierter KI-Dienst 'Midjourney' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | medium | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'Midjourney' (Midjourney) im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | medium | partially_compliant | KI-Dienst 'Midjourney' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | medium | partially_compliant | Datenverarbeitung durch 'Midjourney' (Midjourney) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'Midjourney' ohne Privacy-by-Design-Bewertung. |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | medium | partially_compliant | KI-Dienst 'Midjourney' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'Midjourney' ohne technische Dokumentation nach CRA-Anhang V. |
### Grammarly AI — Grammarly

- **Risk:** medium (Score 40)
- **Client:** `client_d06f2a13`
- **Queries:** 3 (0.2/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | medium | partially_compliant | Nicht-inventarisierter KI-Dienst 'Grammarly AI' von Grammarly erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | medium | partially_compliant | Cloud-basierter KI-Dienst 'Grammarly AI' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | medium | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'Grammarly AI' (Grammarly) im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | medium | partially_compliant | KI-Dienst 'Grammarly AI' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | medium | partially_compliant | Datenverarbeitung durch 'Grammarly AI' (Grammarly) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'Grammarly AI' ohne Privacy-by-Design-Bewertung. |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | medium | partially_compliant | KI-Dienst 'Grammarly AI' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'Grammarly AI' ohne technische Dokumentation nach CRA-Anhang V. |

---
*Generiert von Telemetrie Analyzer · Frameworks: DORA, EU AI Act, ISO 42001, ISO 27001, DSGVO, EU CRA*
*AI Endpoint DB: v2.2.0 (Stand 2026-04-21)*