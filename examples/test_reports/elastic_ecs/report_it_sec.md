# IT-Security Report — Shadow AI Telemetrie

Generiert: **27.04.2026 09:37 UTC**
Zeitraum: **18.04.2026** bis **18.04.2026**
> **DSGVO:** Pseudonymisiert (HMAC-SHA256), Salt-Fingerprint `2e2965bc`

## Kennzahlen

| Metrik | Wert |
|---|---|
| Gesamt-Queries | 11 |
| AI-Queries | 11 (100.0%) |
| Non-AI-Queries | 0 |
| Unique Clients | 11 |
| Unique AI-Dienste | 10 |
| Document-Uploads (>500 KB) | 2 |
| Upload-Volumen total | 2.45 MB |

## Risiko-Verteilung

| Risk-Level | Findings |
|---|---|
| critical | 3 |
| high | 7 |
| medium | 1 |
| low | 0 |

## Findings (sortiert nach Risk-Score)

| Service | Provider | Risk | Score | Client | Q/Tag | Systematic | Upload |
|---|---|---|---|---|---|---|---|
| DeepSeek | DeepSeek | critical | **90** | `client_8aa0df9c` | 1.0 | — | 1× (512.0 KB) |
| GitHub Copilot | GitHub / Microsoft | critical | **70** | `client_2baaf624` | 1.0 | — | — |
| Anthropic Claude | Anthropic | high | **70** | `client_54a9fd16` | 1.0 | — | 1× (2000.0 KB) |
| Cursor | Anysphere | critical | **70** | `client_f3b1b8f0` | 1.0 | — | — |
| Mistral AI | Mistral | high | **50** | `client_3ee3122f` | 1.0 | — | — |
| Google Gemini | Google | high | **50** | `client_4a446bb7` | 1.0 | — | — |
| OpenAI ChatGPT | OpenAI | high | **50** | `client_83988976` | 1.0 | — | — |
| Anthropic Claude | Anthropic | high | **50** | `client_bd8dfd1c` | 1.0 | — | — |
| Perplexity AI | Perplexity | high | **50** | `client_c426a00c` | 1.0 | — | — |
| Hugging Face | Hugging Face | high | **50** | `client_ca54d336` | 1.0 | — | — |
| Midjourney | Midjourney | medium | **30** | `client_8a8df2b7` | 1.0 | — | — |

---
*Generiert von Telemetrie Analyzer v0.1.0*