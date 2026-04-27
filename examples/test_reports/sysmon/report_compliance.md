# Compliance Report — Shadow AI Telemetrie

Generiert: **27.04.2026 09:37 UTC**
Zeitraum: **18.04.2026** bis **18.04.2026**
> **DSGVO:** Pseudonymisiert (HMAC-SHA256), Salt-Fingerprint `7aa57391`

## Framework-Übersicht

| Framework | Erfüllt | Triggered/Total | Non-Compliant | Partially | Review |
|---|---|---|---|---|---|
| **EU AI Act** | 0.0% | 3/3 | 2 | 1 | 0 |
| **DSGVO** | 0.0% | 3/3 | 3 | 0 | 0 |
| **EU CRA** | 28.6% | 5/7 | 5 | 0 | 0 |
| **DORA** | 33.3% | 2/3 | 2 | 0 | 0 |
| **ISO/IEC 27001** | 33.3% | 2/3 | 2 | 0 | 0 |
| **ISO/IEC 42001** | 50.0% | 1/2 | 1 | 0 | 0 |

## Severity-Verteilung pro Framework

| Framework | Critical | High | Medium | Low |
|---|---|---|---|---|
| EU AI Act | 1 | 25 | 12 | 0 |
| DSGVO | 1 | 25 | 13 | 0 |
| EU CRA | 2 | 38 | 13 | 0 |
| DORA | 2 | 24 | 0 | 0 |
| ISO/IEC 27001 | 2 | 24 | 0 | 0 |
| ISO/IEC 42001 | 1 | 12 | 0 | 0 |

## Detail: Compliance-Mappings je Finding

### GitHub Copilot — GitHub / Microsoft

- **Risk:** critical (Score 70)
- **Client:** `client_b4a309c0`
- **Queries:** 1 (1.0/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'GitHub Copilot' von GitHub / Microsoft erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'GitHub Copilot' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'GitHub Copilot' (GitHub / Microsoft) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'GitHub Copilot' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'GitHub Copilot' (Kategorie: code_assistant) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'GitHub Copilot' mit Risk-Score 70 ohne Risk-Management-System. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'GitHub Copilot' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'GitHub Copilot' (GitHub / Microsoft) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'GitHub Copilot' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'GitHub Copilot' erfordert DSFA (Datentransfer an GitHub / Microsoft). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'GitHub Copilot' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'GitHub Copilot' (Kategorie code_assistant) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 10` (Security Requirements during Product Lifecycle) | high | non_compliant | 'GitHub Copilot' (code_assistant) — Supply-Chain-Risiko ohne Lifecycle-Security-Nachweis und Patch-Pipeline. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'GitHub Copilot' (GitHub / Microsoft) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'GitHub Copilot' ohne technische Dokumentation nach CRA-Anhang V. |
### Anthropic Claude — Anthropic

- **Risk:** high (Score 50)
- **Client:** `client_4990a83a`
- **Queries:** 1 (1.0/Tag)
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
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 50)
- **Client:** `client_4990a83a`
- **Queries:** 1 (1.0/Tag)
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
### Google Gemini — Google

- **Risk:** high (Score 50)
- **Client:** `client_5a4105a0`
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
### Anthropic Claude — Anthropic

- **Risk:** high (Score 50)
- **Client:** `client_601e772f`
- **Queries:** 1 (1.0/Tag)
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
### Google Gemini — Google

- **Risk:** high (Score 50)
- **Client:** `client_601e772f`
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
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 50)
- **Client:** `client_7e3e4712`
- **Queries:** 1 (1.0/Tag)
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
### Perplexity AI — Perplexity

- **Risk:** high (Score 50)
- **Client:** `client_91c137fb`
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
### Microsoft Copilot — Microsoft

- **Risk:** high (Score 50)
- **Client:** `client_a152952d`
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
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 50)
- **Client:** `client_ae356785`
- **Queries:** 1 (1.0/Tag)
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
### Hugging Face — Hugging Face

- **Risk:** high (Score 50)
- **Client:** `client_bc01a42a`
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
### Anthropic Claude — Anthropic

- **Risk:** high (Score 50)
- **Client:** `client_c33ac717`
- **Queries:** 1 (1.0/Tag)
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
### Perplexity AI — Perplexity

- **Risk:** high (Score 50)
- **Client:** `client_ef0859bf`
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

---
*Generiert von Telemetrie Analyzer · Frameworks: DORA, EU AI Act, ISO 42001, ISO 27001, DSGVO, EU CRA*
*AI Endpoint DB: v2.2.0 (Stand 2026-04-21)*