# Changelog

Alle nennenswerten Änderungen am Telemetrie Analyzer werden in dieser Datei dokumentiert.

Format orientiert sich an [Keep a Changelog](https://keepachangelog.com/de/1.1.0/),
Versionierung folgt [Semantic Versioning](https://semver.org/lang/de/).

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
- **Streamlit-Dashboard** — Interaktive UI mit vier Pages (Übersicht, Findings,
  Compliance, Einstellungen) und sechs wiederverwendbaren Komponenten
  (`app.py`, `src/ui/`). Strikte Layer-Trennung: `src/ui/` spricht nur über
  `src/ui/state.py` mit der Analyse-Pipeline.
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

- 140 Tests, alle grün.

[0.1.0]: https://github.com/florian-priegnitz/Telemetrie-Analyzer/releases/tag/v0.1.0
