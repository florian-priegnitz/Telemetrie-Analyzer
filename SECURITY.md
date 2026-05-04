# Security Policy

## Unterstützte Versionen

| Version | Support       |
|---------|---------------|
| 1.x     | ✅ aktiv      |
| 0.1.x   | ⚠️ nur kritische Fixes |
| < 0.1   | ❌            |

## Schwachstellen melden (Responsible Disclosure)

Bitte **keine** öffentlichen Issues für Sicherheitsprobleme öffnen.

**Kontakt:** Bitte einen [Private Vulnerability Report](https://github.com/florian-priegnitz/Telemetrie-Analyzer/security/advisories/new) auf GitHub erstellen.

Bitte im Report mitliefern:
- Kurze Beschreibung der Schwachstelle
- Betroffene Version / Commit-SHA
- Reproduktions-Schritte
- Potenzielle Auswirkung (Datenabfluss, Privilege Escalation, DoS, …)
- Optional: Vorschlag zur Behebung

**Antwort-Zeitrahmen:**
- Bestätigung: 3 Werktage
- Erste Einschätzung: 10 Werktage
- Fix-Release: je nach Schwere 14–60 Tage

## Security-Modell

Der Telemetrie Analyzer verarbeitet **sensible Telemetriedaten** (DNS-, Proxy-, Auth-Logs). Die folgenden Schutzziele sind architektonisch verankert:

### Privacy-by-Design (DSGVO Art. 25 / Art. 32)

- **Pseudonymisierung** aller IPs und Usernames bei Import via HMAC-SHA256 (deterministisch, Salt-basiert)
- **In-Memory-only:** keine persistente Speicherung von Rohdaten, keine Datenbank
- **Session-Clearing:** uploaded bytes werden nach erfolgreicher Pipeline verworfen
- **Salt-Rotation:** Salt-Wechsel triggert Hard-Reset aller Analyse-Daten
- **k-Anonymität** (Default k=5) für UI-Drill-Downs
- **Cache-TTL:** 1h / max. 5 Einträge

### Defense-in-Depth für Reports

- `assert_no_plaintext()` verbietet IPv4/IPv6/MAC/`*.local|.lan|.corp`-Hostnames im Output
- Doppelte Pseudonymisierung (Engine + Report-Generator)
- Salt-Fingerprint (8 Hex) im Disclaimer, kein Salt-Leak

### Third-Party-Integration

- **Claude API (Anthropic):** optional, Skip-Mode ohne API-Key — keine Findings werden ohne explizite Nutzer-Aktion versendet
- **Streamlit:** Telemetrie-Upload deaktiviert (`STREAMLIT_BROWSER_GATHER_USAGE_STATS=false`)

## Bekannte Limitationen

- **Kein Authn/Authz in der UI:** Streamlit-App ist für lokale Nutzung konzipiert. Für Multi-User-Deployments Reverse-Proxy mit Auth vorschalten.
- **Keine TLS-Terminierung im Container:** Docker-Image hört auf Port 8501 ohne TLS — produktiv hinter Reverse-Proxy (Traefik/nginx/Caddy) betreiben.

## Compliance-Referenzen

Der Analyzer adressiert folgende regulatorische Kontrollen (Details siehe [README](README.md)):

- **DORA** Art. 5, 6, 28
- **EU AI Act** Art. 6, 9, 53
- **ISO 42001** 6.1.2, 8.4
- **ISO 27001** A.5.9, A.5.23, A.8.16
- **DSGVO** Art. 5, 6, 25, 32, 35
