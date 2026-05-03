# Changelog — AI Endpoint Database

Alle Änderungen an der `data/ai_endpoints.json`-Datenbank werden hier dokumentiert.

Format orientiert sich an [Keep a Changelog](https://keepachangelog.com/de/1.1.0/),
Versionierung folgt [Semantic Versioning](https://semver.org/lang/de/).

## Semver-Konvention für die Endpoint-DB

| Änderung | Versions-Stufe |
|----------|----------------|
| Neue Kategorie, Entfernen eines Endpoints, Risk-Level-Änderung eines produktiv genutzten Services | **Major** (X.0.0) |
| Neue Endpoints, neue Aliases/IP-Ranges, neue optionale Felder im Schema | **Minor** (2.X.0) |
| Beschreibungs-/Metadaten-Korrekturen, Typo-Fixes, Source-Attribution, `last_verified`-Updates | **Patch** (2.2.X) |

Jedes Release wird als vollständiger Snapshot unter `data/versions/<semver>.json` abgelegt.
Das CLI-Werkzeug `telemetrie-analyzer diff-db <from> <to>` erzeugt einen lesbaren
Delta-Report (Added / Removed / Changed) zwischen zwei Versionen.

## [2.3.0] — 2026-05-03

Monatlicher Review (Issue #88) — Mergers + Schema-Hygiene.

### Removed (3 Mergers)

- **OpenAI Codex / GPT API** — Codex wurde 2023 deprecated und in die ChatGPT-API
  gemerged. Endpoint `codex.openai.com` ist tot (DNS-NXDOMAIN). Aliases
  (`Codex`, `OpenAI Codex`, `Codex API`) auf "OpenAI ChatGPT" uebertragen.
- **DALL-E** — In ChatGPT integriert. Endpoint `labs.openai.com` ist tot.
  Aliases (`DALL-E`, `DALL-E 2`, `DALL-E 3`) auf "OpenAI ChatGPT" uebertragen.
- **Google Workspace Duet** — 2024 zu "Gemini for Workspace" umbenannt. Eigene
  Domain `duet.google.com` existiert nicht mehr. Aliases (`Duet`, `Workspace Duet`,
  `Google Duet`) auf "Google Gemini" uebertragen.

### Changed

- **Veo** (Google DeepMind) — Domain `veo.google` → `labs.google` (Google Labs
  hostet Veo-Demos; eigene `.google`-TLD existiert nicht).
- **OpenAI ChatGPT** — Aliases ergaenzt: Codex, OpenAI Codex, Codex API, DALL-E,
  DALL-E 2, DALL-E 3 (siehe Removed).
- **Google Gemini** — Aliases ergaenzt: Duet, Workspace Duet, Google Duet.

### Schema Hygiene

- 24 Endpoints (urspruenglich aus dem v1.0-Q1-2026-Initialset) erhalten
  `source: "initial-import-2026-q1"` (vorher fehlend; entdeckt im Stufe-2-DB-
  Health-Check via `scripts/db_health_check.py`).

### Outstanding (re-verify naechster Monat)

DNS-Aufloesung schlug an meinem Resolver fehl, koennte regional sein —
Eintraege bleiben drin und werden im naechsten Review erneut geprueft:

- **Amazon Q Developer** (`q.aws.amazon.com`)
- **Salesforce Einstein** (`einstein.salesforce.com`)
- **Play.ht** (`play.ht`, `api.play.ht`)

### Status

- **175 Endpoints** (von 178; -3 Mergers) in 21 Kategorien.
- Source-Attribution: 100 % (nach Schema-Cleanup).

### Migration

```
python -m telemetrie_analyzer diff-db 2.2.0 2.3.0
```

## [2.2.0] — 2026-04-21

Snapshot-Basislinie. Erste dokumentierte Version im neuen Versioning-Schema.

### Status

- **178 Endpoints** in 15 Kategorien (llm_chatbot, code_assistant, image_generation,
  ml_platform, content_generation, writing_assistant, translation, productivity_ai,
  speech_to_text, text_to_speech, video_generation, llm_api, audio_generation,
  hr_ai, browser_extension_ai, customer_support_ai).
- 15 Endpoints tragen `aliases` (z. B. "ChatGPT Enterprise" für OpenAI, "Bard" für
  Gemini), 3 Endpoints tragen `ip_ranges` als Mechanism-Demo für AWS-VPC-Fallback.
- Schema v2 (seit Sprint 5): optionale Felder `aliases`, `ip_ranges`, `sni_patterns`,
  `detection_confidence`, `last_verified`, `source`.
- Auto-Refresh-Pipeline via `.github/workflows/endpoint-db-update.yml` (monatlich)
  und `scripts/refresh_endpoints.py`.

### Vorgeschichte (vor Versioning-Schema)

Die nachstehenden Änderungen haben keinen formalen Release-Tag, sind aber im
git-log dokumentiert. Sie sind hier der Vollständigkeit halber aufgeführt.

- **v2.1 (April 2026, Sprint 6/7)** — Erweiterung um HR/Recruiting-AI, Browser-
  Extensions-AI, Customer-Support-AI; Monthly Auto-Refresh produktiv;
  Alias-/IP-Range-Schema v2 finalisiert.
- **v2.0 (April 2026, Sprint 5)** — 160 Endpoints (von 26), 6 neue Kategorien,
  Schema-Validator, Subdomain-/Alias-/IP-Range-Lookup.
- **v1.0 (Q1 2026)** — 26 KI-Dienste, flaches Schema (service/provider/category/
  risk_level/domains/description), Basis für Detection Engine.
