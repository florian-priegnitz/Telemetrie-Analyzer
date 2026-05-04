# Telemetrie Analyzer v1.0.0 — Release Notes

**Release-Datum:** 2026-04-24
**Kurz:** Erste produktionsreife Version nach dem v0.1.0-MVP vom 2026-04-19. Fokus: 12 Log-Formate, 5 Compliance-Frameworks, nutzbar in 2 Kommandos.

---

## Was der Analyzer tut

Erkennt unautorisierte KI-Nutzung (**Shadow AI**) in Unternehmensnetzen durch Analyse von DNS- und Proxy-Logs. Jedes erkannte Finding trägt ein **Compliance-Mapping** auf Artikel/Controls aus DORA · EU AI Act · ISO 42001 · ISO 27001 · DSGVO — damit Security-Findings direkt für Audits und Framework-Scoring nutzbar sind.

**Privacy-by-Design:** Alle IPs und Benutzernamen werden beim Import via HMAC-SHA256 pseudonymisiert (DSGVO Art. 25). Rohdaten werden nicht persistiert. Retention-Policy (Default 90 Tage, konfigurierbar) schneidet ältere Events bevor Detection läuft.

---

## Installation in 2 Kommandos

```bash
git clone https://github.com/florian-priegnitz/Telemetrie-Analyzer.git
cd Telemetrie-Analyzer && docker compose up --build
```

→ UI auf **http://localhost:8501** · 12 Demo-Scenario-Buttons im Willkommen-Screen

**Alternativen:**
- **GHCR-Image:** `docker run -p 8501:8501 ghcr.io/florian-priegnitz/telemetrie-analyzer:v1.0.0`
- **venv + pip:** siehe [INSTALLATION.md](../INSTALLATION.md)
- **Headless CLI:** `telemetrie-analyzer analyze <log> --format html --out reports/`

---

## Key-Features

### 12 Log-Format-Parser (Epic E3 komplett)

| Kategorie | Parser |
|-----------|--------|
| **DNS** | Pi-hole · Cisco Umbrella · Cloudflare Gateway · Windows Sysmon |
| **Web-Proxy** | Squid · Zscaler ZIA NSS · Palo Alto PAN-OS · FortiGate UTM |
| **Cloud** | AWS VPC Flow (v2 + v5 Custom) · Azure Entra ID Sign-In · Netskope CASB |
| **Generic** | Elastic Common Schema (Fallback für alles ECS-konforme) |

Alle Parser erzeugen ein gemeinsames Common-Schema (`timestamp`, `client`, `domain` + optionale Felder). Auto-Detect erkennt das Format an den ersten Bytes; manueller Override möglich.

### 5 Compliance-Frameworks, 15 Regel-Klassen

Jedes Finding trägt eine Liste `compliance_mappings[]` mit Framework + Control-ID + Severity + Assessment-Status. Score-Aggregation pro Framework (0–100 %), Cross-Framework-Summary auf der Compliance-Page.

### Multi-Fallback-Matching

Die Detection-Engine erkennt AI-Services über drei Wege:
1. **Subdomain-Match** gegen `domains`-Liste (`chat.openai.com`)
2. **Alias-Match** (Entra `AppDisplayName` wie "GitHub Copilot")
3. **IP-Range-Match** (AWS VPC Flow ohne Domain)

178 KI-Endpoints in 21 Kategorien, inklusive HR/Recruiting, Browser-Extensions und Customer-Support-AI (v2.2.0).

### UI-Dashboard mit 6 Pages

- **📊 Übersicht** — KPIs, Compliance-Ampel, Top-3-Risiken, **Report-Export** (HTML/Markdown/JSON × 3 Zielgruppen)
- **🔍 Findings** — filterbare Tabelle, Drill-Down mit Compliance-Mappings
- **👥 Users & Patterns** — Top-10-Client-Ranking, Stunden-Heatmap mit Off-Hours-Schattierung
- **📋 Compliance** — 5 Framework-Tabs mit Score-Cards und Mapping-Tabellen
- **📚 Formate** — systematische Format-Präsentation mit Feld-Mapping und Sample-Downloads
- **⚙️ Einstellungen** — Salt-Override, Retention-Anzeige, Privacy-Self-Check

### Demo-Onboarding

12 Ein-Klick-Demo-Scenarios aus der Willkommens-Page. Realistische synthetische Samples (RFC 1918 IPs, seed-reproduzierbar) für Pi-hole, Squid, Netskope, Sysmon, Elastic ECS und AWS VPC Flow v5.

### Headless-Automation

`telemetrie-analyzer`-CLI mit Subcommands (`analyze`, `validate-db`), Auto-Detect für alle 12 Formate, stdout-Pipe-Mode, Retention-Override für Tests.

### CI/CD + Release-Automation

- GitHub Actions mit Python 3.11/3.12 Matrix (pytest + ruff + bandit)
- Monthly Endpoint-DB-Refresh-Workflow
- Tag-basierter Release-Workflow: baut Wheel + SBOM (CycloneDX) + Multi-Arch-Docker-Image (`linux/amd64`, `linux/arm64`)

---

## Getestet & validiert

- **516 Tests grün** (von 161 in v0.1.0)
- **ruff** clean · **bandit** 0 High/Medium Findings
- End-to-End-Roundtrips für alle 13 Demo-Samples
- Parser-Contract-Tests (BaseParser-ABC) parametrized über alle 12 Parser
- DSGVO-Invarianten als Laufzeit-Assertions (`assert_no_plaintext`)

---

## Upgrade von v0.1.0

**v1.0.0 ist ein Major-Release mit neuen Features — kein Breaking Change für die bestehende Python-API.**

Neu erforderliche Dependencies: `pyyaml` (für `config/retention.yaml`), `ruff`/`bandit` im Dev-Extra. Automatisch via `pip install -e .` gezogen.

**Wer vorher mit v0.1.0 gearbeitet hat:**
- Bestehende Python-Scripts mit `parse_pihole_log()` / `parse_squid_log()` laufen unverändert
- Report-Output-Schema ist erweitert um `retention` und `_exports`-Blöcke (optional, ignorierbar)
- Default-Retention-Policy (90 Tage) kann via `RETENTION_DAYS=0` oder `config/retention.yaml` `enabled: false` deaktiviert werden

---

## Known Limitations

- **Multi-File-Upload / Korrelation:** aktuell 1 File pro Session (Sprint 8)
- **Kein Multi-User-Authn in der UI:** lokale Nutzung; für Multi-User hinter Reverse-Proxy mit Auth betreiben
- **Sysmon XML-Format:** nur JSONL unterstützt (evtx2json / Winlogbeat als Konverter dokumentiert)
- **Keine TLS-Terminierung im Container:** hinter Reverse-Proxy (Traefik, Caddy) betreiben
- **CRA-Framework:** noch nicht integriert, separates Projekt `cra-compliance` (Deadline 2026-09-11 — kommt mit v1.1)

---

## Deferred für v1.1

- `#22` Squid `%un`-Username-Parsing (braucht DSFA-Review vor Reaktivierung)
- `#23` Session-Korrelation (parallel genutzte Services pro Client)
- `#42` CRA Phase 2a (6. Compliance-Framework)
- Claude-API-End-to-End-Test mit echtem Key (aktuell nur Skip-Mode dokumentiert)

---

## Contributor-Credits

**Maintainer:** Florian Priegnitz ([@florian-priegnitz](https://github.com/florian-priegnitz))

**Pair-Programming:** Claude Opus (Anthropic) — strukturierte Implementierung der 12 Parser, UI-Page-Architektur, Multi-Fallback-Detection, Release-Workflows.

Dieses Release basiert auf **7 Sprints**, **56 gemergten PRs** und **~16 Wochen** Ausarbeitung. Dank an alle, die geteilt, getestet und Feedback gegeben haben — besonders für die Real-World-Feedback-Runden, die die Demo-Reife und das Format-Audit möglich gemacht haben.

---

## Referenzen

- Repository: https://github.com/florian-priegnitz/Telemetrie-Analyzer
- GHCR-Image: `ghcr.io/florian-priegnitz/telemetrie-analyzer:v1.0.0`
- CHANGELOG: [CHANGELOG.md](../CHANGELOG.md)
- Issues & Roadmap: [GitHub Issues](https://github.com/florian-priegnitz/Telemetrie-Analyzer/issues)
- Quickstart: [docs/QUICKSTART.md](QUICKSTART.md)
- Installation: [INSTALLATION.md](../INSTALLATION.md)
- Security: [SECURITY.md](../SECURITY.md)
- Contributor-Guide: [CONTRIBUTING.md](../CONTRIBUTING.md)
