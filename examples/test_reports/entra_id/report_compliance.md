# Compliance Report — Shadow AI Telemetrie

Generiert: **27.04.2026 09:37 UTC**
Zeitraum: **14.04.2026** bis **14.04.2026**
> **DSGVO:** Pseudonymisiert (HMAC-SHA256), Salt-Fingerprint `073ae3b0`

## Framework-Übersicht

| Framework | Erfüllt | Triggered/Total | Non-Compliant | Partially | Review |
|---|---|---|---|---|---|
| **EU AI Act** | 0.0% | 3/3 | 3 | 0 | 0 |
| **DSGVO** | 0.0% | 3/3 | 3 | 0 | 0 |
| **EU CRA** | 28.6% | 5/7 | 5 | 0 | 0 |
| **DORA** | 33.3% | 2/3 | 2 | 0 | 0 |
| **ISO/IEC 27001** | 33.3% | 2/3 | 2 | 0 | 0 |
| **ISO/IEC 42001** | 50.0% | 1/2 | 1 | 0 | 0 |

## Severity-Verteilung pro Framework

| Framework | Critical | High | Medium | Low |
|---|---|---|---|---|
| EU AI Act | 2 | 14 | 7 | 0 |
| DSGVO | 2 | 14 | 8 | 0 |
| EU CRA | 4 | 21 | 8 | 0 |
| DORA | 4 | 12 | 0 | 0 |
| ISO/IEC 27001 | 4 | 12 | 0 | 0 |
| ISO/IEC 42001 | 2 | 6 | 0 | 0 |

## Detail: Compliance-Mappings je Finding

### DeepSeek — DeepSeek

- **Risk:** critical (Score 70)
- **Client:** `client_8ec33aa8`
- **Queries:** 1 (1.0/Tag)
| Framework | Control | Severity | Status | Begründung |
|---|---|---|---|---|
| **ISO_27001** | `A.5.9` (Inventory of Information and Other Associated Assets) | critical | non_compliant | Nicht-inventarisierter KI-Dienst 'DeepSeek' von DeepSeek erkannt. |
| **ISO_27001** | `A.5.23` (Information Security for Use of Cloud Services) | critical | non_compliant | Cloud-basierter KI-Dienst 'DeepSeek' ohne Sicherheitsbewertung genutzt. |
| **DORA** | `Art. 28` (ICT Third-Party Risk) | critical | non_compliant | Nicht-autorisierter ICT-Drittanbieter 'DeepSeek' (DeepSeek) im Einsatz. |
| **DORA** | `Art. 6` (ICT Risk Management Framework) | critical | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' (Risiko: critical) ohne Risikomanagement. |
| **EU_AI_ACT** | `Art. 6` (Classification Rules for High-Risk AI Systems) | critical | non_compliant | KI-System 'DeepSeek' (Kategorie: llm_chatbot) erfordert Risikoklassifizierung. |
| **EU_AI_ACT** | `Art. 9` (Risk Management System) | high | non_compliant | KI-Dienst 'DeepSeek' mit Risk-Score 70 ohne Risk-Management-System. |
| **EU_AI_ACT** | `Art. 53` (Obligations for Providers of General-Purpose AI Models) | medium | non_compliant | GPAI-Modell 'DeepSeek' ohne Transparenz-Dokumentation im Einsatz. |
| **ISO_42001** | `6.1.2` (AI Risk Assessment) | critical | non_compliant | KI-Dienst 'DeepSeek' ohne AI-Risikobewertung im Einsatz. |
| **DSGVO** | `Art. 6` (Rechtmäßigkeit der Verarbeitung) | critical | non_compliant | Datenverarbeitung durch 'DeepSeek' (DeepSeek) ohne Rechtsgrundlage. |
| **DSGVO** | `Art. 25` (Datenschutz durch Technikgestaltung) | medium | non_compliant | KI-Dienst 'DeepSeek' ohne Privacy-by-Design-Bewertung. |
| **DSGVO** | `Art. 35` (Datenschutz-Folgenabschätzung) | high | non_compliant | Hochrisiko-KI-Dienst 'DeepSeek' erfordert DSFA (Datentransfer an DeepSeek). |
| **CRA** | `Art. 6` (Essential Cybersecurity Requirements) | critical | non_compliant | KI-Dienst 'DeepSeek' als Produkt mit digitalen Elementen ohne CE-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 7` (Important and Critical Products with Digital Elements) | high | non_compliant | 'DeepSeek' (Kategorie llm_chatbot) ist als wichtiges Produkt mit digitalen Elementen einzustufen und erfordert Konformitätsbewertung durch Dritte. |
| **CRA** | `Art. 13` (Obligations of Manufacturers) | critical | non_compliant | Hochrisiko-Dienst 'DeepSeek' (DeepSeek) ohne Hersteller-Konformitätserklärung nach CRA. |
| **CRA** | `Art. 24` (Technical Documentation) | medium | non_compliant | Cloud-KI-Dienst 'DeepSeek' ohne technische Dokumentation nach CRA-Anhang V. |
### GitHub Copilot — GitHub / Microsoft

- **Risk:** critical (Score 70)
- **Client:** `client_ec3d41b5`
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
### Microsoft Copilot — Microsoft

- **Risk:** high (Score 50)
- **Client:** `client_070a76d3`
- **Queries:** 2 (2.0/Tag)
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
### Microsoft Copilot — Microsoft

- **Risk:** high (Score 50)
- **Client:** `client_42fa53ae`
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
- **Client:** `client_70f8d55c`
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
- **Client:** `client_a4995561`
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
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 50)
- **Client:** `client_c0da16b5`
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
### OpenAI ChatGPT — OpenAI

- **Risk:** high (Score 50)
- **Client:** `client_327c3419`
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

---
*Generiert von Telemetrie Analyzer · Frameworks: DORA, EU AI Act, ISO 42001, ISO 27001, DSGVO, EU CRA*
*AI Endpoint DB: v2.2.0 (Stand 2026-04-21)*