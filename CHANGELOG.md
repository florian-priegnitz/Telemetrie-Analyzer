# Changelog

Alle nennenswerten Änderungen am Telemetrie Analyzer werden in dieser Datei dokumentiert.

Format orientiert sich an [Keep a Changelog](https://keepachangelog.com/de/1.1.0/),
Versionierung folgt [Semantic Versioning](https://semver.org/lang/de/).

## [1.0.0] — 2026-04-21

Erste stabile Produktiv-Version. Fokus dieser Finalisierung: **Ops + Onboarding** — der Analyzer ist jetzt in 2 Kommandos per Docker Compose startbar, vollständig CI/CD-abgesichert und DSGVO-Retention-konform. Das Parser-Epic E3 ist mit 12/12 Parsern komplett abgeschlossen, inkl. Windows-Sysmon und dem vendor-agnostischen Elastic-Common-Schema-Parser als universeller Fallback.

### Hinzugefügt

- **12 Log-Parser (Epic E3, Sprint 7 komplett)** — Pi-hole, Squid, Zscaler ZIA, Palo Alto PAN-OS, Cisco Umbrella, Fortinet, AWS VPC Flow (v2+v5), Azure Entra ID, Cloudflare Gateway, Netskope CASB, **Windows Sysmon Event 22** (E3-9, #34), **Elastic Common Schema** (E3-10, #35) als vendor-agnostischer Fallback. Alle Parser erfüllen den `BaseParser`-Contract (E3-0) und pseudonymisieren Identitäten bereits beim Import.
- **CLI Entry Point (#3)** — `telemetrie-analyzer analyze <log> --format html|markdown|json --audience …` mit Auto-Detect für alle 12 Formate, `--stdout` für Pipe-Nutzung, `--no-retention` für Tests, separates `validate-db`-Subkommando. Headless-Automation für Cron/CI/SIEM.
- **Multi-Fallback-Lookup in Detection Engine (#50, #52)** — Endpoint-Match erkennt jetzt dreistufig: Subdomain → Alias (Entra `AppDisplayName`) → IP-Range (AWS VPC Flow ohne Domain). Deckt heterogene Log-Formate ab. 12 kritische Services haben Entra-Aliases (ChatGPT, Claude, Gemini, Copilot, …), 3 haben dokumentierte IP-Ranges als Mechanism-Demo.
- **Retention Management (#38)** — `src/privacy/retention.py` trimmt Parser-Output auf konfigurierbaren Horizont (Default 90 Tage, per Log-Typ überschreibbar via `config/retention.yaml`). ENV-Overrides: `RETENTION_DAYS`, `RETENTION_CONFIG`. Settings-Page zeigt aktive Policy + Audit-Report der letzten Analyse (DSGVO Art. 5 (1e)).
- **AI Endpoint Database v2.2** — 178 Endpoints (+18 in 3 neuen Kategorien): HR/Recruiting-AI (HireVue, Paradox, Eightfold, …), Browser-Extensions-AI (Merlin, HARPA, Monica, …), Customer-Support-AI (Intercom Fin, Forethought, Zendesk AI, …). Monthly Auto-Refresh via GitHub Actions (#11, #12).
- **CI/CD Pipeline (#37)** — GitHub Actions mit Python-3.11/3.12-Matrix, `pytest`, `ruff`, `bandit`, Schema-Validator. Auto-Release on Tag `v*` mit Wheel + SBOM.
- **GHCR Docker-Publish** — Multi-Arch-Image (amd64+arm64) wird bei Tag `v*` automatisch nach `ghcr.io/florian-priegnitz/telemetrie-analyzer` gepusht. User ziehen das fertige Image statt lokal zu bauen.
- **Docker-Image + docker-compose.yml** — 1-Command-Deployment (`docker compose up --build`), Multi-Stage Build, Non-Root-User, HEALTHCHECK auf Streamlit `/_stcore/health`.
- **Makefile + pre-commit** — 14 Developer-Targets (`make test/lint/docker/streamlit/analyze-sample`), `.pre-commit-config.yaml` mit ruff/bandit/Schema-Validator.
- **End-to-End Integration Tests** — `tests/test_e2e_pipeline.py` (11 Tests) schützt die Pipeline Parser → Retention → Detection → Compliance → Report gegen Regressions-Brüche.
- **Dokumentation für End-User** — [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), [INSTALLATION.md](INSTALLATION.md), [docs/QUICKSTART.md](docs/QUICKSTART.md) mit 10-Minuten-Walkthrough + UI-Mockup.
- **Packaging-Metadaten** — pyproject.toml mit authors, classifiers, URLs, keywords (PyPI-ready), Hatchling-Build-System.
- **SBOM-Script** (`scripts/generate_sbom.sh`) — CycloneDX-JSON für CRA-Vorbereitung (VO EU 2024/2847).
- **Endpoint-DB-CLI** — `python -m src.database.ai_endpoints --validate` für Schema-Checks in CI.
- **GitHub-Metadaten** — `.github/dependabot.yml` (monthly pip + actions), Pull-Request-Template mit DSGVO-Checkliste.

### Geändert

- **pyproject.toml** auf Hatchling umgestellt, SemVer-Version 0.1.0 → 1.0.0, Dev-Status 5 (Production/Stable).
- **README.md** überarbeitet mit CI-Badge, „Get Started in 2 Commands"-Sektion, aktualisierter Feature-Liste (10 Parser, 359 Tests).
- **Ruff-Config** aktiviert (E/F/W/I/UP/B/SIM) mit pragmatischer Ignore-Liste für pre-existing Style-Issues.

### Sicherheit

- **Retention** wirkt rein In-Memory (keine Persistenz von Rohdaten), `apply_retention` ist idempotent und respektiert existierende Pseudonymisierung.
- **Bandit-Scan** als CI-Gate: 0 High, 0 Medium Findings beim Release.
- **SBOM** als Release-Asset (CycloneDX) dokumentiert Dependencies für Supply-Chain-Audits.
- `.env.example` + `.gitignore`-Eintrag für `.env` verhindern Secret-Leaks.

### Tests

- **441 Tests grün** (von 161 in v0.1.0) — +17 Retention, +6 Endpoint-DB-v2.1, +24 Sysmon, +27 Elastic ECS, +9 CLI, +11 E2E-Pipeline, +11 Multi-Fallback-Detection.

### Known Limitations / v1.1 Roadmap

Folgende Items sind bewusst für v1.0 deferred:

- **#22 Squid `%un`-Username-Parsing** (P1) — braucht DSFA-Review vor Reaktivierung
- **#23 Session-Korrelation** (P1) — E3-0 BaseParser-Foundation bereits vorhanden, für Sprint 8
- **#42 CRA Phase 2a** — separates Projekt `cra-compliance`, Deadline 2026-09-11
- **#14, #15, #16, #43** — Endpoint-DB-Housekeeping, ASN-Fallback, Coverage-Details

## [0.1.0] — 2026-04-19

Erstes öffentliches Release. MVP für Shadow-AI-Detection via DNS/Proxy-Log-Analyse
mit Compliance-Mapping auf DORA, EU AI Act, ISO 42001, ISO 27001 und DSGVO.

### Hinzugefügt

- **AI Endpoint Database** — 26 KI-Dienste in `data/ai_endpoints.json` mit
  Domains, Kategorien und vier Risikostufen. Python-Klasse mit exaktem
  Matching und Subdomain-Matching (`src/database/ai_endpoints.py`).
- **Pi-hole DNS-Parser** — Syslog- und FTL-CSV-Format (`src/parsers/pihole.py`).
  Domains werden normalisiert, IPs bei Import pseudonymisiert.
- **Squid Proxy-Parser** — Native- und Common-Log-Format, konfigurierbar via
  `config/squid_logformat.conf` (`src/parsers/squid.py`).
  Volumen-Detection: Uploads ab 500 KB werden als Dokument-Upload markiert.
- **Pseudonymisierung** — HMAC-SHA256, deterministisch
  (`src/privacy/pseudonymizer.py`). Pseudonyme mit `ip_`/`user_`-Prefix.
- **Detection Engine** — Domain-Matching (exakt + Subdomain),
  Frequenz-Analyse, Risk-Scoring 0-100, Gruppierung Client × Service
  (`src/detection/engine.py`).
- **Compliance Engine** — 15 Regeln über 5 Frameworks (DORA, EU AI Act,
  ISO 42001, ISO 27001, DSGVO), framework- und kontroll-basiertes Scoring,
  Finding-Modell mit `compliance_mappings` (`src/compliance/`).
- **Claude API Integration** — KI-gestützte Finding-Analyse über Anthropic SDK
  (`src/analyzer/`). Skip-Mode ohne API-Key, strukturierter Prompt,
  JSON-Parsing.
- **Report-Generator** — Jinja2-basiert, drei Zielgruppen (Executive/CISO,
  IT-Security, Compliance) × zwei Formate (HTML + Markdown) + JSON-Schnittstelle
  (`src/reports/`). DSGVO-Schutzschicht prüft Klartext-Leaks vor dem Ausspielen
  (`src/reports/privacy.py`).
- **Streamlit-Dashboard** — Interaktive UI mit fünf Pages (Übersicht, Findings,
  Users & Patterns, Compliance, Einstellungen) und sechs wiederverwendbaren
  Komponenten (`app.py`, `src/ui/`). Strikte Layer-Trennung: `src/ui/` spricht
  nur über `src/ui/state.py` mit der Analyse-Pipeline.
- **Behavior Analytics** (Epic E2) — Zeitliche Muster- und Anomalie-Erkennung
  (`src/analytics/`): Hourly-Heatmap (Client × Stunde), Off-Hours-Detection
  mit +15 Risk-Boost (Business-Default 06–22 Uhr), Burst-Detection (>50
  Requests in 5 Minuten via Sliding-Window).
- **k-Anonymitäts-Guard** — Soft-Check in `src/privacy/k_anonymity.py`
  (Default Minimum k=5). UI-Banner warnt bei Re-Identifikations-Risiko
  unterhalb der Schwelle (DSGVO Art. 25/32).
- **Users & Patterns Page** — Top-10-Client-Ranking nach Risk-Max,
  pseudonymisierte Stunden-Heatmap mit Off-Hours-Schattierung und
  Drill-Down pro Client (`src/ui/pages/users_patterns.py`).
- **Synthetische Testdaten** — Generator mit 5 Szenario-Profilen (clean,
  low-risk, systematic, upload-leak, enterprise-mixed) und reproduzierbarem
  Seed (`src/testdata/generator.py`).

### Sicherheit

- HMAC-SHA256-Pseudonymisierung als Privacy-by-Design-Default
  (DSGVO Art. 25).
- Klartext-Bytes werden nach erfolgreicher Pipeline aus dem Streamlit-
  Session-State verworfen (DSGVO Art. 32).
- Salt-Wechsel in der UI invalidiert alte Analyse-Daten automatisch
  (Hard-Reset mit Warnbanner).
- Pipeline-Cache mit TTL (max. 5 Einträge, 1 Stunde).
- Assertion `assert_no_plaintext()` verhindert unbemerkte Klartext-Leaks
  in Reports.

### Tests

- 161 Tests, alle grün (inkl. 18 Analytics-Tests und 3 Users-&-Patterns-UI-Tests).

[1.0.0]: https://github.com/florian-priegnitz/Telemetrie-Analyzer/releases/tag/v1.0.0
[0.1.0]: https://github.com/florian-priegnitz/Telemetrie-Analyzer/releases/tag/v0.1.0
