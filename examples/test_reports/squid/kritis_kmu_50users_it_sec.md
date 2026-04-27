# IT-Security Report — Shadow AI Telemetrie

Generiert: **27.04.2026 09:37 UTC**
Zeitraum: **12.04.2026** bis **26.04.2026**
> **DSGVO:** Pseudonymisiert (HMAC-SHA256), Salt-Fingerprint `c338ca09`

## Kennzahlen

| Metrik | Wert |
|---|---|
| Gesamt-Queries | 9064 |
| AI-Queries | 1984 (21.89%) |
| Non-AI-Queries | 7080 |
| Unique Clients | 50 |
| Unique AI-Dienste | 12 |
| Document-Uploads (>500 KB) | 281 |
| Upload-Volumen total | 563.11 MB |

## Risiko-Verteilung

| Risk-Level | Findings |
|---|---|
| critical | 34 |
| high | 50 |
| medium | 6 |
| low | 0 |

## Findings (sortiert nach Risk-Score)

| Service | Provider | Risk | Score | Client | Q/Tag | Systematic | Upload |
|---|---|---|---|---|---|---|---|
| DeepSeek | DeepSeek | critical | **100** | `client_144be7d3` | 2.2 | — | 5× (6854.5 KB) |
| DeepSeek | DeepSeek | critical | **100** | `client_1dc78685` | 1.2 | — | 2× (6974.1 KB) |
| GitHub Copilot | GitHub / Microsoft | critical | **100** | `client_1ddad6a1` | 3.0 | — | 3× (6745.9 KB) |
| DeepSeek | DeepSeek | critical | **100** | `client_2632e438` | 1.3 | — | 2× (2133.5 KB) |
| GitHub Copilot | GitHub / Microsoft | critical | **100** | `client_40d7d667` | 2.4 | — | 1× (992.0 KB) |
| Cursor | Anysphere | critical | **100** | `client_5cac0f7a` | 2.7 | — | 4× (3060.8 KB) |
| DeepSeek | DeepSeek | critical | **100** | `client_5cac0f7a` | 1.4 | — | 1× (2127.9 KB) |
| DeepSeek | DeepSeek | critical | **100** | `client_6318295c` | 1.6 | — | 3× (4285.7 KB) |
| Cursor | Anysphere | critical | **100** | `client_64f36f5f` | 2.9 | — | 1× (880.4 KB) |
| DeepSeek | DeepSeek | critical | **100** | `client_64f36f5f` | 1.2 | — | 1× (807.0 KB) |
| Cursor | Anysphere | critical | **100** | `client_75babc12` | 2.9 | — | 1× (5155.1 KB) |
| DeepSeek | DeepSeek | critical | **100** | `client_75babc12` | 1.0 | — | 2× (5768.1 KB) |
| Cursor | Anysphere | critical | **100** | `client_8ef5b6c7` | 2.6 | — | 1× (3029.1 KB) |
| DeepSeek | DeepSeek | critical | **100** | `client_8ef5b6c7` | 0.8 | — | 1× (1046.5 KB) |
| Cursor | Anysphere | critical | **100** | `client_a141fb06` | 2.8 | — | 3× (2828.0 KB) |
| DeepSeek | DeepSeek | critical | **100** | `client_a141fb06` | 1.0 | — | 2× (5332.6 KB) |
| Cursor | Anysphere | critical | **100** | `client_a62207c2` | 2.3 | — | 2× (3926.0 KB) |
| DeepSeek | DeepSeek | critical | **100** | `client_a62207c2` | 1.0 | — | 2× (4073.0 KB) |
| Cursor | Anysphere | critical | **100** | `client_ab152d79` | 2.4 | — | 3× (6108.5 KB) |
| DeepSeek | DeepSeek | critical | **100** | `client_ab152d79` | 1.2 | — | 1× (2472.8 KB) |
| GitHub Copilot | GitHub / Microsoft | critical | **100** | `client_bec9d25a` | 2.2 | — | 2× (2718.4 KB) |
| DeepSeek | DeepSeek | critical | **100** | `client_bfc4bed7` | 1.1 | — | 3× (4415.3 KB) |
| GitHub Copilot | GitHub / Microsoft | critical | **100** | `client_ccde70e1` | 2.5 | — | 3× (4314.0 KB) |
| Cursor | Anysphere | critical | **100** | `client_ce22278c` | 2.5 | — | 1× (2684.0 KB) |
| DeepSeek | DeepSeek | critical | **100** | `client_ce22278c` | 1.6 | — | 3× (10481.4 KB) |
| Cursor | Anysphere | critical | **100** | `client_e0bf80f6` | 3.6 | — | 2× (2678.3 KB) |
| DeepSeek | DeepSeek | critical | **100** | `client_e0bf80f6` | 1.5 | — | 1× (1745.6 KB) |
| Cursor | Anysphere | critical | **100** | `client_faca11e2` | 1.8 | — | 1× (1567.4 KB) |
| DeepSeek | DeepSeek | critical | **100** | `client_faca11e2` | 1.8 | — | 3× (9494.4 KB) |
| Perplexity AI | Perplexity | high | **80** | `client_0ee5d804` | 2.6 | — | 1× (1618.3 KB) |
| Anthropic Claude | Anthropic | high | **80** | `client_144be7d3` | 1.7 | — | 6× (10773.3 KB) |
| Cursor | Anysphere | critical | **80** | `client_144be7d3` | 3.2 | — | — |
| OpenAI ChatGPT | OpenAI | high | **80** | `client_144be7d3` | 1.2 | — | 5× (8282.0 KB) |
| OpenAI ChatGPT | OpenAI | high | **80** | `client_159a17cd` | 3.5 | — | 7× (11716.1 KB) |
| Anthropic Claude | Anthropic | high | **80** | `client_1dc78685` | 1.0 | — | 2× (5686.5 KB) |
| Cursor | Anysphere | critical | **80** | `client_1dc78685` | 2.1 | — | — |
| OpenAI ChatGPT | OpenAI | high | **80** | `client_1dc78685` | 2.3 | — | 8× (17866.8 KB) |
| Google Gemini | Google | high | **80** | `client_22672cb7` | 2.5 | — | 7× (9579.0 KB) |
| Anthropic Claude | Anthropic | high | **80** | `client_2632e438` | 1.8 | — | 4× (6669.6 KB) |
| Cursor | Anysphere | critical | **80** | `client_2632e438` | 3.5 | — | — |
| Google Gemini | Google | high | **80** | `client_2a1cb879` | 2.3 | — | 5× (14075.7 KB) |
| Anthropic Claude | Anthropic | high | **80** | `client_3a0b2034` | 2.8 | — | 11× (16358.5 KB) |
| OpenAI ChatGPT | OpenAI | high | **80** | `client_4dd00205` | 2.5 | — | 6× (12736.3 KB) |
| Anthropic Claude | Anthropic | high | **80** | `client_5cac0f7a` | 1.9 | — | 8× (16567.8 KB) |
| OpenAI ChatGPT | OpenAI | high | **80** | `client_5cac0f7a` | 1.4 | — | 2× (6149.9 KB) |
| Anthropic Claude | Anthropic | high | **80** | `client_6318295c` | 2.0 | — | 3× (14715.6 KB) |
| Cursor | Anysphere | critical | **80** | `client_6318295c` | 2.8 | — | — |
| OpenAI ChatGPT | OpenAI | high | **80** | `client_6318295c` | 1.1 | — | 3× (4304.6 KB) |
| Anthropic Claude | Anthropic | high | **80** | `client_64f36f5f` | 1.7 | — | 5× (11238.6 KB) |
| OpenAI ChatGPT | OpenAI | high | **80** | `client_64f36f5f` | 1.0 | — | 1× (1095.5 KB) |
| OpenAI ChatGPT | OpenAI | high | **80** | `client_661b9a57` | 3.5 | — | 9× (19272.9 KB) |
| Anthropic Claude | Anthropic | high | **80** | `client_75babc12` | 1.5 | — | 3× (9675.2 KB) |
| OpenAI ChatGPT | OpenAI | high | **80** | `client_75babc12` | 1.5 | — | 4× (12956.9 KB) |
| Anthropic Claude | Anthropic | high | **80** | `client_7eade85b` | 2.2 | — | 8× (21122.9 KB) |
| Anthropic Claude | Anthropic | high | **80** | `client_8807a2b8` | 2.7 | — | 9× (10888.0 KB) |
| Anthropic Claude | Anthropic | high | **80** | `client_8ef5b6c7` | 1.3 | — | 5× (17971.8 KB) |
| OpenAI ChatGPT | OpenAI | high | **80** | `client_8ef5b6c7` | 2.0 | — | 6× (7288.1 KB) |
| OpenAI ChatGPT | OpenAI | high | **80** | `client_9be49256` | 2.4 | — | 6× (11292.9 KB) |
| Anthropic Claude | Anthropic | high | **80** | `client_a141fb06` | 1.5 | — | 2× (2030.7 KB) |
| OpenAI ChatGPT | OpenAI | high | **80** | `client_a141fb06` | 1.5 | — | 3× (8437.3 KB) |
| Anthropic Claude | Anthropic | high | **80** | `client_a62207c2` | 1.6 | — | 5× (5807.9 KB) |
| OpenAI ChatGPT | OpenAI | high | **80** | `client_a62207c2` | 1.6 | — | 4× (5414.4 KB) |
| Anthropic Claude | Anthropic | high | **80** | `client_ab152d79` | 2.1 | — | 9× (17846.2 KB) |
| OpenAI ChatGPT | OpenAI | high | **80** | `client_ab152d79` | 1.7 | — | 5× (13793.3 KB) |
| Anthropic Claude | Anthropic | high | **80** | `client_b60d1ba2` | 3.0 | — | 7× (11671.0 KB) |
| Anthropic Claude | Anthropic | high | **80** | `client_bfc4bed7` | 1.0 | — | 1× (6076.4 KB) |
| Cursor | Anysphere | critical | **80** | `client_bfc4bed7` | 2.5 | — | — |
| OpenAI ChatGPT | OpenAI | high | **80** | `client_bfc4bed7` | 1.2 | — | 6× (12321.2 KB) |
| Perplexity AI | Perplexity | high | **80** | `client_c0252d7e` | 1.6 | — | 1× (3499.7 KB) |
| Google Gemini | Google | high | **80** | `client_c04b3ab5` | 3.8 | — | 9× (16808.7 KB) |
| Anthropic Claude | Anthropic | high | **80** | `client_ce22278c` | 1.4 | — | 3× (8271.7 KB) |
| OpenAI ChatGPT | OpenAI | high | **80** | `client_ce22278c` | 1.2 | — | 2× (1567.7 KB) |
| Perplexity AI | Perplexity | high | **80** | `client_d3c76b46` | 2.2 | — | 2× (3344.5 KB) |
| Anthropic Claude | Anthropic | high | **80** | `client_e0bf80f6` | 1.9 | — | 6× (21537.4 KB) |
| OpenAI ChatGPT | OpenAI | high | **80** | `client_e0bf80f6` | 1.2 | — | 4× (9216.9 KB) |
| Google Gemini | Google | high | **80** | `client_ed14a61a` | 3.0 | — | 6× (9882.6 KB) |
| Perplexity AI | Perplexity | high | **80** | `client_f5fcbe33` | 3.2 | — | 3× (6464.7 KB) |
| Anthropic Claude | Anthropic | high | **80** | `client_faca11e2` | 1.5 | — | 6× (11135.0 KB) |
| OpenAI ChatGPT | OpenAI | high | **80** | `client_faca11e2` | 1.1 | — | 2× (2938.1 KB) |
| OpenAI ChatGPT | OpenAI | high | **60** | `client_2632e438` | 1.2 | — | — |
| Hugging Face | Hugging Face | high | **60** | `client_2dfdf2f7` | 1.0 | — | — |
| Mistral AI | Mistral | high | **60** | `client_48d7c436` | 0.7 | — | — |
| Grammarly AI | Grammarly | medium | **60** | `client_d5b8476f` | 0.5 | — | 1× (1275.0 KB) |
| Mistral AI | Mistral | high | **55** | `client_7d688da0` | 0.9 | — | — |
| Hugging Face | Hugging Face | high | **55** | `client_ed11768c` | 0.9 | — | — |
| Midjourney | Midjourney | medium | **40** | `client_6ad2f1c8` | 0.8 | — | — |
| DeepL | DeepL | medium | **40** | `client_7c6a8790` | 0.5 | — | — |
| DeepL | DeepL | medium | **40** | `client_a4541cb3` | 0.9 | — | — |
| Midjourney | Midjourney | medium | **40** | `client_c2e6f2a0` | 1.4 | — | — |
| Grammarly AI | Grammarly | medium | **40** | `client_d06f2a13` | 0.2 | — | — |

---
*Generiert von Telemetrie Analyzer v0.1.0*