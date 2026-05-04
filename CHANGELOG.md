# Changelog

Alle nennenswerten Änderungen am Telemetrie Analyzer werden in dieser Datei dokumentiert.

Format orientiert sich an [Keep a Changelog](https://keepachangelog.com/de/1.1.0/),
Versionierung folgt [Semantic Versioning](https://semver.org/lang/de/).

## [Unreleased]

## [1.4.0] — 2026-05-04

### Hinzugefügt

- **CI-Branding Streamlit-UI (#78, Sprint 13a)** — Bauhaus-Branding aus `florian-priegnitz.de` auf das Streamlit-Dashboard übertragen. Neu:
  - `.streamlit/config.toml` — Theme-Mapping (Rostrot `#9B4A2F` als Primary).
  - `src/ui/static/branding.css` — globales CSS mit allen 9 Farb-Tokens (`--c-acc`, `--c-gold`, `--c-green`, `--c-ink`, `--c-bright`, `--c-bg`, `--c-layer`, `--c-mid`, `--c-line`), Schriften (DM Sans 400/700/900 + Share Tech Mono via Google-Fonts-Import), Spacing-Skala `--s-1`..`--s-10`, 10×2 Rostrot-Bullets, Button-Hover-Invert, Streamlit-Tabs als Mono-Chips, Severity-/Compliance-Status-Farb-Klassen.
  - `src/ui/static/favicon.svg` — Bauhaus-Lineal als Bildmarke (3 Rechtecke: 6 px Rostrot · 2 px Ink · 16 px Gold).
  - `src/ui/static/plotly_telemetrie_theme.json` — CI-konforme Plotly-Layout-Sequenz (`colorway` startet mit Rostrot/Gold/Grün, Mono-Achsen-Ticks).
  - `src/ui/branding.py` — `inject_global_css()` (idempotent über Session-Flag), `render_lineal()` (Sidebar + Page-Top), `severity_color(level)`, `compliance_status_color(status)`, `get_plotly_template()`.
  - `app.py` — Favicon via `page_config(page_icon=str(FAVICON_PATH))`, `inject_global_css()` einmalig pro Run, Lineal in Sidebar + vor Page-Dispatch.
- **15 neue Tests** (`tests/test_branding.py`) — Severity-/Status-Farb-Mapping (parametrisiert), CSS-Token-Vollständigkeit, Favicon-Geometrie, Plotly-Template-JSON-Round-Trip, AppTest-Smoke.

### Hinweis zu Sprint 13b/c

Sprint 13a deckt die Streamlit-UI ab. Folge-PRs:
- **13b** HTML-Reports (Jinja2-Templates `_base.html.j2` + 3 Audience-Templates, self-contained CSS für Mail-Versand).
- **13c** Markdown-Reports + `docs/style/CI_GUIDE.md` (Beitragenden-Kurzreferenz).
- 21 Demo-Screenshots werden erst nach 13a/b/c neu erzeugt (siehe `docs/screenshots/CHECKLIST.md` Z.74).

### Risk-Severity-Farb-Schema (Entscheidung)

4-stufig auf Akzent + Sättigung (CI-konsistent ohne Konflikt mit Lineal-Gold):

| Level    | Hex                        |
|----------|----------------------------|
| critical | `#9B4A2F` (Rostrot voll)   |
| high     | `#C26B4A` (helleres Rost)  |
| medium   | `#B07A10` (Gold)           |
| low      | `rgba(12,26,50,0.40)`      |

## [1.4.0] — 2026-04-27

### Hinzugefügt

- **Pluggable LLM-Backend (#72, Sprint 10A)** — `src/analyzer/backends/` mit `LLMBackend`-Protocol, `AnthropicBackend` (Cloud-Default) und `OllamaBackend` (Offline, stdlib `urllib`). Backend-Selection via env `LLM_BACKEND ∈ {anthropic, ollama, skip}`, Default = `anthropic` wenn `ANTHROPIC_API_KEY`, sonst `skip`. `ClaudeAnalyzer` ist jetzt Fassade über das Backend; bestehende Tests + Aufrufe funktionieren unverändert. Settings-Page enthält neuen Block "KI-Backend" mit Radio-Auswahl + Verbindungs-Test für Ollama. Voraussetzung für KRITIS-/DSGVO-Argumentation: KI-Analyse komplett offline möglich.
- **27 neue Tests** (`tests/test_llm_backends.py` + `tests/test_analyzer_backend_dispatch.py`) — Protocol-Konformität, AnthropicBackend, OllamaBackend (mit `urlopen`-Mock), Factory `select_backend`, Backend-Injection, Backwards-Compat-Pfad.

- **Demo & Audit-Bundle: 85 Beispiel-Reports + KRITIS-KMU-Datensatz (#73, Sprint 10B)** — Neues `scripts/generate_example_reports.py` orchestriert pro Parser den vollen Pipeline-Lauf (Parse → Detection → Compliance → ReportGenerator) und erzeugt unter `examples/test_reports/<parser>/` ein A+B-Klassifiziertes Report-Bundle. Klassifikation lt. 108-Zellen-Matrix aus dem Sprint-10-Plan (A=Pflicht, B=Interessant, C=Redundant nicht-committed, D=keine Daten). KRITIS-KMU-Sonderfall für Squid: neues Szenario `kritis-kmu-shadow-ai` (50 User in `10.42.0.10`–`10.42.0.59`, 15 Heavy / 20 Systematic / 10 Casual / 5 Clean, 14 Tage × 800 Queries) erzeugt 7 Reports + 1 Raw-Log unter `examples/test_reports/squid/kritis_kmu_50users_*`. `.gitattributes` markiert das gesamte Bundle als `linguist-generated=true`.
- **Sample-Logs angereichert** — `testdata/sysmon_sample.log` (5 → 11 unique User) und `testdata/elastic_ecs_sample.log` (6 → 11 unique User) auf ≥10 User erweitert, um die Anforderung "Testreport pro Tool mit 10 verschiedenen Usern" auch ohne KRITIS-Generator-Lauf abzudecken.
- **+2 Tests** (`test_kritis_kmu_scenario_has_50_clients_and_strong_shadow_ai`, aktualisierter `test_all_scenarios_are_tested`).

- **Offline-Stack via Docker-Compose-Profile (#75, Sprint 10D)** — `docker-compose.offline.yml` definiert Telemetrie-Analyzer + Ollama als Sidecar (Compose-Profile `offline`, Standard-Compose bleibt unbeeinflusst). Ollama-Image gepinnt auf `0.4.7`, Healthcheck via `ollama list`, named volume `telemetrie-ollama-data`. `docker-compose.yml` erhält Pass-through für `LLM_BACKEND`, `OLLAMA_HOST`, `OLLAMA_MODEL`, `OLLAMA_TIMEOUT`. `.gitignore` ergänzt `ollama-data/` für lokale Bind-Mount-Varianten.
- **`scripts/verify_screenshots.py` (#75, Sprint 10D)** — parst `docs/screenshots/CHECKLIST.md`, extrahiert Filenames aus `- [ ] NN_*.png`-Zeilen und prüft `Path.exists()` pro PNG. Default `--warn` (Exit 0 bei fehlenden Files), `--strict` (Exit 1) für Release-CI. 8 Unit-Tests in `tests/test_verify_screenshots.py`.
- **Makefile-Targets:** `offline-up`, `offline-down`, `offline-pull`, `verify-screenshots`, `generate-examples`, `check-all`.

- **AI-Endpoint-DB-Freshness-Sichtbarkeit + monatlicher Review-Issue (#77, Sprint 12)** — Neue Komponente `src/ui/components/db_status.py` zeigt DB-Version, Endpoint-/Provider-/Kategorie-Anzahl und ein Frische-Signal (🟢 ≤35d / 🟡 ≤70d / 🔴 darüber) auf Settings-Page (voll) und Overview-Page (kompakt im Footer). `scripts/db_coverage_report.py` generiert `docs/AI_COVERAGE.md` mit vollständigem Katalog gruppiert nach Kategorie + Top-10-Provider; ein Sync-Test bricht, wenn die Datei vom DB-Stand drifted. `.github/workflows/db-review-issue.yml` (cron `0 7 2 * *`) erzeugt monatlich ein Review-Issue gemäß `.github/ISSUE_TEMPLATE/db_review.yml` (Checkliste über Discovery, Bestandspflege, Privacy-Bewertung, DB-Bump). Glossar-Eintrag `endpoint_db_freshness` ergänzt.

- **Squid Username-Parsing mit Double-Opt-in Privacy-Gating (#22)** — Zwei aktive Entscheidungsstufen entkoppeln die Fähigkeit von der Wirksamkeit. Stufe 1: Parser-Flag `parse_username` aktiviert `%un`/RFC931-Extraktion, normalisiert AD-Down-Level-/UPN-/LDAP-CN-Formate (`DOMAIN\user`, `user@corp.tld`, `CN=user,...` → `user`) und schreibt nur das HMAC-Pseudonym in eine neue optionale Spalte `user_pseudonym`. Stufe 2: UI-Reveal-Button in der Users-Page hebt die Maskierung (`user_a***`) session-scoped auf. Default für beides: off. Der Raw-Username wird zu keinem Zeitpunkt persistiert.
- **Settings-Toggle "Squid Username-Parsing (DSFA-pflichtig)"** mit explizitem Warnbanner und Pipeline-Reset beim Umschalten (analog Salt-Wechsel). DSFA-Verantwortung bleibt dokumentiert beim Betreiber (DSGVO Art. 35).
- **`docs/PRIVACY.md`** — zentrale Dokumentation der Privacy-Engineering-Entscheidungen inkl. DSFA-Kurz-Checkliste für den Username-Parsing-Opt-in.

### Privacy-Invariante

- Neue Invariante 7 in [`CONTRIBUTING.md`](CONTRIBUTING.md): Raw-Usernamen dürfen in keinem DataFrame, Cache-Entry oder Report erscheinen. Test `test_raw_username_never_in_dataframe` sichert das für den Squid-Parser gegen Regressionen ab.
- Cache-Trennung: `squid_username_parsing` ist Teil des `run_pipeline`-Cache-Keys, Flag-Umschaltung erzwingt frische Pipeline-Ausführung.
- Bei hohem Re-Identifikations-Risiko (k < k_min / 2) wird die User-Aggregation analog zum Top-Clients-Ranking komplett unterdrückt.

### Behoben

- **Docker-Release-Workflow** (`templates/` Copy) wurde als eigener Fix außerhalb dieses Features gemerged und entsperrt den GHCR-Image-Publish für zukünftige Tag-Pushes. (Siehe PR fix/dockerfile-templates-path.)

### Interna

- **Test-Suite** 597 → **650** (+17 #22 + **+27 #72** Backend + **+1 #73** KRITIS + **+8 #75** Verifier).
- **Issue #22** geschlossen — Epic E2 damit auch inhaltlich abgeschlossen (vorher DSFA-blockiert deferred).
- **Issue #72** (Sprint 10A LLMBackend) — abgeschlossen, entkoppelt KI-Analyse von Anthropic-Cloud.
- **Issue #73** (Sprint 10B Generator + Reports) — abgeschlossen, 85 Beispiel-Reports + KRITIS-KMU-Bundle.
- **Issue #75** (Sprint 10D DevOps) — abgeschlossen, Offline-Compose-Stack + Verifier + Makefile-Targets.
- **Issue #77** (Sprint 12 DB-Freshness) — abgeschlossen, UI-Sichtbarkeit + Coverage-Report + Monthly-Review-Workflow.
- **Test-Suite jetzt 692** (650 + 27 #76 + 15 #77).

## [1.3.0] — 2026-04-22

Minor-Release mit dem Abschluss des Epic E2 Behavior Analytics: Service-Co-Occurrence-Graphen erkennen Tool-Kombinationen wie *ChatGPT + Cursor + Claude* als zusammengehörige Nutzungsmuster — risikorelevanter als die Einzelservices. Backlog auf **1 offenes Issue** reduziert (#22 bleibt DSFA-blockiert).

### Hinzugefügt

- **Session-Korrelation (#23)** — Neues Modul `src/analytics/sessions.py` mit `build_session_graph(df, window_minutes=30) → networkx.Graph` als Kern-API. Two-Pointer-Sliding-Window-Pattern (O(N·E)) analog zu `bursts.py`. Output: gewichtete Service-Co-Occurrence-Kanten + Per-User-Top-5-Paare (pseudonymisiert).
- **Streamlit-Page 🔗 Sessions** (`src/ui/pages/sessions.py`) — Plotly-Netzwerk-Visualisierung mit `networkx.spring_layout(seed=42)` für deterministische Layouts, Top-20-Paare-Tabelle, Per-Client-Drilldown. Bei `privacy_redacted=True` wird der Drilldown unterdrückt, der globale Graph (Service-zentriert) bleibt sichtbar.
- **`networkx>=3.0` als Dependency** — keine Transitive, <50 KB reine Python.

### Privacy-Invariante

Graph-Nodes tragen ausschließlich Service-Namen — **keine Client-Keys**. Per-User-Top-N-Keys werden mit `pseudonymize_client()` maskiert (analog zu `_build_user_patterns`). Dedizierter Test `test_no_plaintext_client_in_graph_nodes` verifiziert die Invariante gegen Regressionen.

### Interna

- **Test-Suite** 580 → **597** (+17: 16 Unit + 1 End-to-End-Pipeline).
- **Epic E2 abgeschlossen** — Behavior Analytics ist damit komplett (E2-1 Heatmap, E2-2 Off-Hours, E2-3 Bursts, E2-4 Users-&-Patterns, E2-6 Sessions; E2-5 Squid %un bleibt deferred mit DSFA-Pflicht).

## [1.2.0] — 2026-04-22

Minor-Release mit zwei neuen Detection-Erweiterungen: ASN-Provider-Fallback für unbekannte IPs und formale Versionierung der AI-Endpoint-Datenbank mit Audit-Disclaimer in Reports. Backlog auf **2 offene Issues** reduziert (beide deferred mit DSFA-Bedarf).

### Hinzugefügt

- **ASN-Fallback (#15)** — Opt-in-Detection-Pfad. Wenn Domain-, Alias- und Service-IP-Lookup alle fehlschlagen und der Wert wie eine IP aussieht, wird gegen eine neue kuratierte Provider-CIDR-DB (`data/ai_ip_ranges.json` — Anthropic, OpenAI, Google Vertex AI, AWS Bedrock, Azure OpenAI) geprüft. Treffer tragen `detection_confidence="low"` (false-positive-anfällig). Aktivierung über `DetectionEngine(enable_asn_fallback=True)`. Neues Modul `src/detection/asn_fallback.py`. Keine externen WHOIS-/ASN-Abfragen zur Laufzeit (DSGVO).
- **AI Endpoint DB Versioning (#14)** — Semver-Konvention (MAJOR=Kategorie/Entfernung, MINOR=neue Endpoints, PATCH=Metadaten), vollständige Snapshots unter `data/versions/<semver>.json`, formales `data/CHANGELOG_AI_ENDPOINTS.md`. Neues Modul `src/database/versioning.py` mit `DiffReport` + `compute_diff`. Drift-Guard-Test stellt sicher, dass Snapshot und Live-DB synchron bleiben.
- **CLI-Subcommand `diff-db`** — `telemetrie-analyzer diff-db <from> <to>` erzeugt lesbaren Delta-Report (Added/Removed/Changed). Ohne Argumente listet er verfügbare Snapshots.
- **Audit-Disclaimer in Reports** — `AIEndpointDatabase.version` und `.last_updated` werden automatisch in Report-Footer (HTML/Markdown) und in den JSON-Output (`report_meta.ai_endpoint_db`) injiziert. Basis für auditierbare Reproduzierbarkeit: ein Report verweist eindeutig auf die Endpoint-DB-Version, mit der er erzeugt wurde.

### Interna

- **Test-Suite** 544 → **580** (+36): 12 ASN-Fallback, 24 DB-Versioning.
- **Issue-Cleanup** — #50 und #52 (beide als zombie erkannt und geschlossen) + #15 und #14 erledigt.

## [1.1.0] — 2026-04-22

Minor-Release mit dem 6. Compliance-Framework (CRA) und konsequentem Privacy-Enforcement auf der Users-&-Patterns-Page. Board von 21 auf 4 offene Issues reduziert (7 Zombies geschlossen).

### Hinzugefügt

- **CRA Phase 2a (#42)** — 6. Compliance-Framework **EU Cyber Resilience Act** (Verordnung (EU) 2024/2847) produktiv. 7 Kontrollen (Art. 6, 7, 10, 11, 13, 14, 24) werden auf Shadow-AI-Findings gemappt. Neue `mappings/cra.yaml` als deklarative Control-Registry mit Framework-Metadaten, Artikel-Titeln und Beschreibungen. Engine-Regeln in `src/compliance/engine.py`, UI-Tab in Compliance-Page, Reports (Executive/IT-Security/Compliance × HTML/Markdown/JSON) führen CRA-Spalten/Mappings. CRA-Volle-Compliance-Deadline: 2027-12-11, Meldepflichten ab 2026-09-11.
- **Heatmap Cell-Masking (DSGVO Art. 25, #43)** — Neue Funktion `mask_low_count_cells(heatmap, min_count=3)` in `src/analytics/temporal.py` maskiert Heatmap-Zellen mit niedrigem Count auf 0, um Re-Identifikation über 24h-Aktivitätsmuster zu verhindern.
- **k-Anonymity Redaktion (DSGVO Art. 25, #43)** — Bei `reidentification_risk == "high"` (beobachtetes k < `minimum_k / 2`) werden Top-Clients-Ranking und Stunden-Heatmap automatisch redigiert (`top_clients=[]`, `hourly_heatmap={}`), neues Flag `privacy_redacted=True` steuert Error-Banner in Users-&-Patterns-Page. Konservativer Default ohne Opt-out.

### Geändert

- **Overnight-Shift in `off_hours_ratio` (#43)** — Wrap-around-Logik: bei `business_start > business_end` (z. B. 22–06 Nachtschicht) wird Business-Fenster als `[start, 24) ∪ [0, end)` interpretiert, Off-Hours liegt in `[end, start)`. Vorher zählte bei Nachtschicht alles als off-hours.
- **Framework-Zählung in UI/Reports** — Alle Freitext-Listen und hardcoded "5 Frameworks"-Strings auf 6 erweitert (Templates, Traffic-Light-Komponente, Claude-API-System-Prompt).
- **`_build_user_patterns` Output** — ungenutzte `services`-Liste aus `top_clients` entfernt (Privacy-Konservativ, nur `service_count` bleibt).

### Behoben

- `_build_event` in `src/analytics/bursts.py` hatte keinen Type-Hint auf `group_key` — jetzt `object` + Kontrakt-Kommentar.
- Expliziter `del df, df_trimmed` nach `_build_user_patterns` in `src/ui/state.py` (Intent-Klarheit analog zum `uploaded_bytes=None`-Pattern).

### Interna

- **Test-Suite** 516 → **544** (+28): 20 neu für CRA, 8 neu für #43 (3 Heatmap-Masking, 2 Overnight-Shift, 3 Redaktions-Logik).
- **Issue-Cleanup** — 7 Zombie-Issues geschlossen (#12, #19, #20, #24, #35, #50, #52) + 3 echte Issues erledigt (#42, #43 + v1.0.0-Arbeit).

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
