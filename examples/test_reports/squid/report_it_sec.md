# IT-Security Report — Shadow AI Telemetrie

Generiert: **27.04.2026 09:37 UTC**
Zeitraum: **13.04.2026** bis **20.04.2026**
> **DSGVO:** Pseudonymisiert (HMAC-SHA256), Salt-Fingerprint `ec6255ea`

## Kennzahlen

| Metrik | Wert |
|---|---|
| Gesamt-Queries | 1700 |
| AI-Queries | 126 (7.41%) |
| Non-AI-Queries | 1574 |
| Unique Clients | 11 |
| Unique AI-Dienste | 9 |
| Document-Uploads (>500 KB) | 11 |
| Upload-Volumen total | 17.41 MB |

## Risiko-Verteilung

| Risk-Level | Findings |
|---|---|
| critical | 3 |
| high | 6 |
| medium | 2 |
| low | 0 |

## Findings (sortiert nach Risk-Score)

| Service | Provider | Risk | Score | Client | Q/Tag | Systematic | Upload |
|---|---|---|---|---|---|---|---|
| Cursor | Anysphere | critical | **95** | `client_b2076b41` | 3.0 | — | 1× (1144.3 KB) |
| Google Gemini | Google | high | **75** | `client_46c0b28c` | 0.8 | — | 2× (2623.3 KB) |
| DeepSeek | DeepSeek | critical | **75** | `client_b2076b41` | 3.5 | — | — |
| OpenAI ChatGPT | OpenAI | high | **75** | `client_b2076b41` | 1.3 | — | 2× (3596.0 KB) |
| Perplexity AI | Perplexity | high | **75** | `client_b2076b41` | 2.8 | — | 1× (2316.2 KB) |
| GitHub Copilot | GitHub / Microsoft | critical | **75** | `client_ef483e4a` | 6.3 | — | — |
| OpenAI ChatGPT | OpenAI | high | **75** | `client_ef483e4a` | 2.0 | — | 3× (4904.3 KB) |
| Anthropic Claude | Anthropic | high | **70** | `client_b2076b41` | 4.0 | — | 2× (2850.5 KB) |
| OpenAI ChatGPT | OpenAI | high | **55** | `client_2c4f1e69` | 2.0 | — | — |
| DeepL | DeepL | medium | **35** | `client_2c4f1e69` | 1.2 | — | — |
| Grammarly AI | Grammarly | medium | **35** | `client_46c0b28c` | 1.2 | — | — |

---
*Generiert von Telemetrie Analyzer v0.1.0*