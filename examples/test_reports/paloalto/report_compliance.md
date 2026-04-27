# Compliance Report — Shadow AI Telemetrie

Generiert: **27.04.2026 09:37 UTC**
Zeitraum: **14.04.2026** bis **14.04.2026**
> **DSGVO:** Pseudonymisiert (HMAC-SHA256), Salt-Fingerprint `c1d31653`

## Framework-Übersicht

| Framework | Erfüllt | Triggered/Total | Non-Compliant | Partially | Review |
|---|---|---|---|---|---|
| **EU AI Act** | 0.0% | 3/3 | 0 | 3 | 0 |
| **DSGVO** | 0.0% | 3/3 | 0 | 3 | 0 |
| **EU CRA** | 28.6% | 5/7 | 0 | 5 | 0 |
| **DORA** | 33.3% | 2/3 | 0 | 2 | 0 |
| **ISO/IEC 27001** | 33.3% | 2/3 | 0 | 2 | 0 |
| **ISO/IEC 42001** | 50.0% | 1/2 | 0 | 1 | 0 |

## Severity-Verteilung pro Framework

| Framework | Critical | High | Medium | Low |
|---|---|---|---|---|
| EU AI Act | 0 | 24 | 14 | 0 |
| DSGVO | 0 | 24 | 14 | 0 |
| EU CRA | 0 | 38 | 14 | 0 |
| DORA | 0 | 24 | 1 | 0 |
| ISO/IEC 27001 | 0 | 24 | 2 | 0 |
| ISO/IEC 42001 | 0 | 12 | 1 | 0 |

## Detail: Compliance-Mappings je Finding

### Mistral AI — Mistral

- **Risk:** high (Score 50)
- **Client:** `client_34cf85be`
- **Queries:** 1 (1.0/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | partially_compliant | Nicht-inventarisierter KI-Dienst 'Mistral AI' von Mistral erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | partially_compliant | Cloud-basierter KI-Dienst 'Mistral AI' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'Mistral AI' (Mistral) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | partially_compliant | Hochrisiko-KI-Dienst 'Mistral AI' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | partially_compliant | KI-System 'Mistral AI' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | partially_compliant | KI-Dienst 'Mistral AI' mit Risk-Score 50 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | partially_compliant | GPAI-Modell 'Mistral AI' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | partially_compliant | KI-Dienst 'Mistral AI' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | partially_compliant | Datenverarbeitung durch 'Mistral AI' (Mistral) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'Mistral AI' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | partially_compliant | Hochrisiko-KI-Dienst 'Mistral AI' erfordert DSFA (Datentransfer an Mistral). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | partially_compliant | KI-Dienst 'Mistral AI' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | partially_compliant | 'Mistral AI' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | partially_compliant | Hochrisiko-Dienst 'Mistral AI' (Mistral) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'Mistral AI' ohne technische Dokumentation nach CRA-Anhang V. |
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 50)
- **Client:** `client_51f816ef`
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
- **Client:** `client_6ae83dae`
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
### OpenRouter — OpenRouter

- **Risk:** high (Score 50)
- **Client:** `client_6d283c71`
- **Queries:** 1 (1.0/Tag)
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
- **Client:** `client_7308ed49`
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
### Poe — Quora

- **Risk:** high (Score 50)
- **Client:** `client_7fe84c14`
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
### Anthropic Claude — Anthropic

- **Risk:** high (Score 50)
- **Client:** `client_987e2dc9`
- **Queries:** 4 (4.0/Tag)
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
### Replicate — Replicate

- **Risk:** high (Score 50)
- **Client:** `client_bc878c40`
- **Queries:** 1 (1.0/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | high | partially_compliant | Nicht-inventarisierter KI-Dienst 'Replicate' von Replicate erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | high | partially_compliant | Cloud-basierter KI-Dienst 'Replicate' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | high | partially_compliant | Nicht-autorisierter ICT-Drittanbieter 'Replicate' (Replicate) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | high | partially_compliant | Hochrisiko-KI-Dienst 'Replicate' (Risiko: high) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | high | partially_compliant | KI-System 'Replicate' (Kategorie: ml_platform) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | partially_compliant | KI-Dienst 'Replicate' mit Risk-Score 50 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | partially_compliant | GPAI-Modell 'Replicate' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | high | partially_compliant | KI-Dienst 'Replicate' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | high | partially_compliant | Datenverarbeitung durch 'Replicate' (Replicate) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | partially_compliant | KI-Dienst 'Replicate' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | partially_compliant | Hochrisiko-KI-Dienst 'Replicate' erfordert DSFA (Datentransfer an Replicate). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | high | partially_compliant | KI-Dienst 'Replicate' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | partially_compliant | 'Replicate' (Kategorie ml_platform) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | high | partially_compliant | Hochrisiko-Dienst 'Replicate' (Replicate) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | partially_compliant | Cloud-KI-Dienst 'Replicate' ohne technische Dokumentation nach CRA-Anhang V. |
### Microsoft Copilot — Microsoft

- **Risk:** high (Score 50)
- **Client:** `client_dd0d01af`
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
### Google Gemini — Google

- **Risk:** high (Score 50)
- **Client:** `client_e17c78e6`
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
### Perplexity AI — Perplexity

- **Risk:** high (Score 50)
- **Client:** `client_e17c78e6`
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
### Hugging Face — Hugging Face

- **Risk:** high (Score 50)
- **Client:** `client_f389c56e`
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
### Character.AI — Character Technologies

- **Risk:** medium (Score 30)
- **Client:** `client_fbd582e2`
- **Queries:** 1 (1.0/Tag)
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