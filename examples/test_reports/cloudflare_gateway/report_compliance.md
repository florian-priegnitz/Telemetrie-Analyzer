# Compliance Report — Shadow AI Telemetrie

Generiert: **27.04.2026 09:37 UTC**
Zeitraum: **14.04.2026** bis **14.04.2026**
> **DSGVO:** Pseudonymisiert (HMAC-SHA256), Salt-Fingerprint `1bae8080`

## Framework-Übersicht

| Framework | Erfüllt | Triggered/Total | Non-Compliant | Partially | Review |
|---|---|---|---|---|---|
| **EU AI Act** | 0.0% | 3/3 | 3 | 0 | 0 |
| **DSGVO** | 0.0% | 3/3 | 3 | 0 | 0 |
| **EU CRA** | 14.3% | 6/7 | 5 | 1 | 0 |
| **DORA** | 33.3% | 2/3 | 2 | 0 | 0 |
| **ISO/IEC 27001** | 33.3% | 2/3 | 2 | 0 | 0 |
| **ISO/IEC 42001** | 50.0% | 1/2 | 1 | 0 | 0 |

## Severity-Verteilung pro Framework

| Framework | Critical | High | Medium | Low |
|---|---|---|---|---|
| EU AI Act | 0 | 20 | 12 | 0 |
| DSGVO | 0 | 20 | 12 | 0 |
| EU CRA | 0 | 33 | 12 | 0 |
| DORA | 0 | 20 | 1 | 0 |
| ISO/IEC 27001 | 0 | 20 | 2 | 0 |
| ISO/IEC 42001 | 0 | 10 | 1 | 0 |

## Detail: Compliance-Mappings je Finding

### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 70)
- **Client:** `client_e6c0d0df`
- **Queries:** 2 (2.0/Tag)
- **Upload:** 1× Dokument-Upload (869.6 KB)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | non_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | non_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | non_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | non_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 70 ohne Risk-Management-System. |
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
### OpenRouter — OpenRouter

- **Risk:** high (Score 50)
- **Client:** `client_087caacc`
- **Queries:** 2 (2.0/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | partially_compliant | Nicht-inventarisierter KI-Dienst 'OpenRouter' von OpenRouter erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | partially_compliant | Cloud-basierter KI-Dienst 'OpenRouter' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenRouter' (OpenRouter) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | partially_compliant | Hochrisiko-KI-Dienst 'OpenRouter' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | partially_compliant | KI-System 'OpenRouter' (Kategorie: llm_api) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | partially_compliant | KI-Dienst 'OpenRouter' mit Risk-Score 50 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | partially_compliant | GPAI-Modell 'OpenRouter' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | partially_compliant | KI-Dienst 'OpenRouter' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | partially_compliant | Datenverarbeitung durch 'OpenRouter' (OpenRouter) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'OpenRouter' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | partially_compliant | Hochrisiko-KI-Dienst 'OpenRouter' erfordert DSFA (Datentransfer an OpenRouter). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | partially_compliant | KI-Dienst 'OpenRouter' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | partially_compliant | 'OpenRouter' (Kategorie llm_api) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | partially_compliant | 'OpenRouter' (llm_api) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | partially_compliant | Hochrisiko-Dienst 'OpenRouter' (OpenRouter) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'OpenRouter' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 50)
- **Client:** `client_2b75e284`
- **Queries:** 4 (4.0/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | partially_compliant | Nicht-inventarisierter KI-Dienst 'OpenAI ChatGPT' von OpenAI erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | partially_compliant | Cloud-basierter KI-Dienst 'OpenAI ChatGPT' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'OpenAI ChatGPT' (OpenAI) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | partially_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | partially_compliant | KI-System 'OpenAI ChatGPT' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | partially_compliant | KI-Dienst 'OpenAI ChatGPT' mit Risk-Score 50 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | partially_compliant | GPAI-Modell 'OpenAI ChatGPT' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | partially_compliant | KI-Dienst 'OpenAI ChatGPT' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | partially_compliant | Datenverarbeitung durch 'OpenAI ChatGPT' (OpenAI) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'OpenAI ChatGPT' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | partially_compliant | Hochrisiko-KI-Dienst 'OpenAI ChatGPT' erfordert DSFA (Datentransfer an OpenAI). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | partially_compliant | KI-Dienst 'OpenAI ChatGPT' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | partially_compliant | 'OpenAI ChatGPT' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | partially_compliant | Hochrisiko-Dienst 'OpenAI ChatGPT' (OpenAI) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'OpenAI ChatGPT' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 50)
- **Client:** `client_4bb06325`
- **Queries:** 5 (5.0/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | partially_compliant | Nicht-inventarisierter KI-Dienst 'Anthropic Claude' von Anthropic erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | partially_compliant | Cloud-basierter KI-Dienst 'Anthropic Claude' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'Anthropic Claude' (Anthropic) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | partially_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | partially_compliant | KI-System 'Anthropic Claude' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | partially_compliant | KI-Dienst 'Anthropic Claude' mit Risk-Score 50 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | partially_compliant | GPAI-Modell 'Anthropic Claude' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | partially_compliant | KI-Dienst 'Anthropic Claude' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | partially_compliant | Datenverarbeitung durch 'Anthropic Claude' (Anthropic) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'Anthropic Claude' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | partially_compliant | Hochrisiko-KI-Dienst 'Anthropic Claude' erfordert DSFA (Datentransfer an Anthropic). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | partially_compliant | KI-Dienst 'Anthropic Claude' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | partially_compliant | 'Anthropic Claude' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | partially_compliant | Hochrisiko-Dienst 'Anthropic Claude' (Anthropic) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'Anthropic Claude' ohne technische Dokumentation nach CRA-Anhang V. |
### Hugging Face — Hugging Face

- **Risk:** high (Score 50)
- **Client:** `client_5f097b55`
- **Queries:** 1 (1.0/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | partially_compliant | Nicht-inventarisierter KI-Dienst 'Hugging Face' von Hugging Face erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | partially_compliant | Cloud-basierter KI-Dienst 'Hugging Face' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'Hugging Face' (Hugging Face) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | partially_compliant | Hochrisiko-KI-Dienst 'Hugging Face' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | partially_compliant | KI-System 'Hugging Face' (Kategorie: ml_platform) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | partially_compliant | KI-Dienst 'Hugging Face' mit Risk-Score 50 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | partially_compliant | GPAI-Modell 'Hugging Face' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | partially_compliant | KI-Dienst 'Hugging Face' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | partially_compliant | Datenverarbeitung durch 'Hugging Face' (Hugging Face) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'Hugging Face' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | partially_compliant | Hochrisiko-KI-Dienst 'Hugging Face' erfordert DSFA (Datentransfer an Hugging Face). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | partially_compliant | KI-Dienst 'Hugging Face' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | partially_compliant | 'Hugging Face' (Kategorie ml_platform) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | partially_compliant | Hochrisiko-Dienst 'Hugging Face' (Hugging Face) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'Hugging Face' ohne technische Dokumentation nach CRA-Anhang V. |
### Google Gemini — Google

- **Risk:** high (Score 50)
- **Client:** `client_88e8acce`
- **Queries:** 1 (1.0/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | partially_compliant | Nicht-inventarisierter KI-Dienst 'Google Gemini' von Google erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | partially_compliant | Cloud-basierter KI-Dienst 'Google Gemini' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'Google Gemini' (Google) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | partially_compliant | Hochrisiko-KI-Dienst 'Google Gemini' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | partially_compliant | KI-System 'Google Gemini' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | partially_compliant | KI-Dienst 'Google Gemini' mit Risk-Score 50 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | partially_compliant | GPAI-Modell 'Google Gemini' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | partially_compliant | KI-Dienst 'Google Gemini' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | partially_compliant | Datenverarbeitung durch 'Google Gemini' (Google) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'Google Gemini' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | partially_compliant | Hochrisiko-KI-Dienst 'Google Gemini' erfordert DSFA (Datentransfer an Google). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | partially_compliant | KI-Dienst 'Google Gemini' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | partially_compliant | 'Google Gemini' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | partially_compliant | Hochrisiko-Dienst 'Google Gemini' (Google) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'Google Gemini' ohne technische Dokumentation nach CRA-Anhang V. |
### Poe — Quora

- **Risk:** high (Score 50)
- **Client:** `client_9ab5f59a`
- **Queries:** 1 (1.0/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | partially_compliant | Nicht-inventarisierter KI-Dienst 'Poe' von Quora erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | partially_compliant | Cloud-basierter KI-Dienst 'Poe' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'Poe' (Quora) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | partially_compliant | Hochrisiko-KI-Dienst 'Poe' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | partially_compliant | KI-System 'Poe' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | partially_compliant | KI-Dienst 'Poe' mit Risk-Score 50 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | partially_compliant | GPAI-Modell 'Poe' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | partially_compliant | KI-Dienst 'Poe' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | partially_compliant | Datenverarbeitung durch 'Poe' (Quora) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'Poe' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | partially_compliant | Hochrisiko-KI-Dienst 'Poe' erfordert DSFA (Datentransfer an Quora). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | partially_compliant | KI-Dienst 'Poe' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | partially_compliant | 'Poe' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | partially_compliant | Hochrisiko-Dienst 'Poe' (Quora) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'Poe' ohne technische Dokumentation nach CRA-Anhang V. |
### Google Gemini — Google

- **Risk:** high (Score 50)
- **Client:** `client_9ef80f44`
- **Queries:** 1 (1.0/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | partially_compliant | Nicht-inventarisierter KI-Dienst 'Google Gemini' von Google erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | partially_compliant | Cloud-basierter KI-Dienst 'Google Gemini' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'Google Gemini' (Google) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | partially_compliant | Hochrisiko-KI-Dienst 'Google Gemini' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | partially_compliant | KI-System 'Google Gemini' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | partially_compliant | KI-Dienst 'Google Gemini' mit Risk-Score 50 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | partially_compliant | GPAI-Modell 'Google Gemini' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | partially_compliant | KI-Dienst 'Google Gemini' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | partially_compliant | Datenverarbeitung durch 'Google Gemini' (Google) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'Google Gemini' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | partially_compliant | Hochrisiko-KI-Dienst 'Google Gemini' erfordert DSFA (Datentransfer an Google). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | partially_compliant | KI-Dienst 'Google Gemini' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | partially_compliant | 'Google Gemini' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | partially_compliant | Hochrisiko-Dienst 'Google Gemini' (Google) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'Google Gemini' ohne technische Dokumentation nach CRA-Anhang V. |
### Microsoft Copilot — Microsoft

- **Risk:** high (Score 50)
- **Client:** `client_b5a715f7`
- **Queries:** 1 (1.0/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | partially_compliant | Nicht-inventarisierter KI-Dienst 'Microsoft Copilot' von Microsoft erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | partially_compliant | Cloud-basierter KI-Dienst 'Microsoft Copilot' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'Microsoft Copilot' (Microsoft) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | partially_compliant | Hochrisiko-KI-Dienst 'Microsoft Copilot' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | partially_compliant | KI-System 'Microsoft Copilot' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | partially_compliant | KI-Dienst 'Microsoft Copilot' mit Risk-Score 50 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | partially_compliant | GPAI-Modell 'Microsoft Copilot' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | partially_compliant | KI-Dienst 'Microsoft Copilot' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | partially_compliant | Datenverarbeitung durch 'Microsoft Copilot' (Microsoft) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'Microsoft Copilot' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | partially_compliant | Hochrisiko-KI-Dienst 'Microsoft Copilot' erfordert DSFA (Datentransfer an Microsoft). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | partially_compliant | KI-Dienst 'Microsoft Copilot' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | partially_compliant | 'Microsoft Copilot' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | partially_compliant | Hochrisiko-Dienst 'Microsoft Copilot' (Microsoft) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'Microsoft Copilot' ohne technische Dokumentation nach CRA-Anhang V. |
### Perplexity AI — Perplexity

- **Risk:** high (Score 50)
- **Client:** `client_c5bcb8a6`
- **Queries:** 1 (1.0/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | partially_compliant | Nicht-inventarisierter KI-Dienst 'Perplexity AI' von Perplexity erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | partially_compliant | Cloud-basierter KI-Dienst 'Perplexity AI' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'Perplexity AI' (Perplexity) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | partially_compliant | Hochrisiko-KI-Dienst 'Perplexity AI' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | partially_compliant | KI-System 'Perplexity AI' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | partially_compliant | KI-Dienst 'Perplexity AI' mit Risk-Score 50 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | partially_compliant | GPAI-Modell 'Perplexity AI' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | partially_compliant | KI-Dienst 'Perplexity AI' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | partially_compliant | Datenverarbeitung durch 'Perplexity AI' (Perplexity) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'Perplexity AI' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | partially_compliant | Hochrisiko-KI-Dienst 'Perplexity AI' erfordert DSFA (Datentransfer an Perplexity). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | partially_compliant | KI-Dienst 'Perplexity AI' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | partially_compliant | 'Perplexity AI' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | partially_compliant | Hochrisiko-Dienst 'Perplexity AI' (Perplexity) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'Perplexity AI' ohne technische Dokumentation nach CRA-Anhang V. |
### Character.AI — Character Technologies

- **Risk:** medium (Score 30)
- **Client:** `client_d1c0c920`
- **Queries:** 2 (2.0/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | medium | needs_review | Nicht-inventarisierter KI-Dienst 'Character.AI' von Character Technologies erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | medium | needs_review | Cloud-basierter KI-Dienst 'Character.AI' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | medium | needs_review | Nicht-autorisierter ICT-Drittanbieter 'Character.AI' (Character Technologies) im Einsatz. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | medium | needs_review | KI-System 'Character.AI' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | needs_review | GPAI-Modell 'Character.AI' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | medium | needs_review | KI-Dienst 'Character.AI' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | medium | needs_review | Datenverarbeitung durch 'Character.AI' (Character Technologies) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | needs_review | KI-Dienst 'Character.AI' ohne Privacy-by-Design-Bewertung. |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | medium | needs_review | KI-Dienst 'Character.AI' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | needs_review | 'Character.AI' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | needs_review | Cloud-KI-Dienst 'Character.AI' ohne technische Dokumentation nach CRA-Anhang V. |

---
*Generiert von Telemetrie Analyzer · Frameworks: DORA, EU AI Act, ISO 42001, ISO 27001, DSGVO, EU CRA*
*AI Endpoint DB: v2.2.0 (Stand 2026-04-21)*