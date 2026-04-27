# Test-Reports — Demo & Audit-Bundle

Dieses Verzeichnis enthält **vorgenerierte Beispiel-Reports** für jeden der 12 unterstützten Parser. Es dient drei Zwecken:

1. **Demo & Vertrieb** — sofort vorzeigbare Reports ohne Pipeline-Lauf.
2. **Audit-Pack** — Compliance-Reports decken alle 6 Frameworks (DORA, EU AI Act, ISO 42001, ISO 27001, DSGVO, CRA).
3. **Regression-Smoke** — sichtbare Auswirkungen von Code-Änderungen sind sofort im PR-Diff sichtbar.

## Struktur

```
examples/test_reports/
├── pihole/                                 # 7 Reports (Standard)
├── squid/                                  # 7 Reports + 7 KRITIS-KMU-Reports + 1 Raw-Log
├── zscaler/                                # 7 Reports
├── paloalto/                               # 7 Reports
├── umbrella/                               # 7 Reports
├── fortinet/                               # 7 Reports
├── aws_vpc_flow/                           # 5 Reports (Compliance MD/JSON entfallen)
├── entra_id/                               # 6 Reports (Exec MD entfällt)
├── cloudflare_gateway/                     # 7 Reports
├── netskope/                               # 7 Reports
├── sysmon/                                 # 6 Reports (Exec MD entfällt)
└── elastic_ecs/                            # 5 Reports (Exec MD + Comp JSON entfallen)
```

**Total:** 85 Reports + 1 KRITIS-KMU-Raw-Log = 86 Files.

## A/B/C/D-Klassifikation (108-Zellen-Matrix)

Jeder Parser hätte 9 mögliche Reports (3 Audiences × 3 Formate). Die Matrix klassifiziert sie:

- **A** *Pflicht* — Demo-/Audit-Standard. Wird committed und in CI verifiziert.
- **B** *Interessant* — sinnvoll für SIEM-/GRC-Integration. Wird committed (`.gitattributes linguist-generated=true`).
- **C** *Redundant* — gleicher Inhalt wie A/B-Variante in anderem Format ohne Stakeholder-Mehrwert. NICHT committed, lokal reproduzierbar.
- **D** *Raus* — Datenlage des Parsers reicht nicht (z. B. Sysmon Exec MD: Endpoint-Daten taugen nicht für Vorstands-Briefing).

Konkret pro Parser siehe Sprint-10-Plan; alle Executive-JSONs sind D (Vorstände konsumieren kein JSON).

## KRITIS-KMU 50-User-Demo (Sonderfall, Squid)

Realistischer KRITIS-KMU-Datensatz mit ausgeprägter Schatten-KI:

- 50 Clients (`10.42.0.10`–`10.42.0.59`)
- 14 Tage × ~800 Queries/Tag/User
- Verteilung: 15 Heavy / 20 Systematic / 10 Casual / 5 Clean
- Upload-Spike-Domains: `chat.openai.com`, `claude.ai`, `api.anthropic.com`
- Alle 9 Reports-Formate (Exec/IT-Sec/Comp × HTML/MD/JSON) sind A — Demo-Story-Wert

Files:
- `squid/kritis_kmu_50users_raw.log` — Squid-Native-Format (1 MB, ~11 200 Zeilen)
- `squid/kritis_kmu_50users_executive.{html,md}`
- `squid/kritis_kmu_50users_it_sec.{html,md}`
- `squid/kritis_kmu_50users_compliance.{html,md}`
- `squid/kritis_kmu_50users_report.json`

## Reproduzieren

```bash
python scripts/generate_example_reports.py            # alle Parser + KRITIS
python scripts/generate_example_reports.py --check    # nur Existenz prüfen
python scripts/generate_example_reports.py --only squid    # nur ein Parser
```

Idempotent (seed=42 für KRITIS-KMU). Static Sample-Logs unter `testdata/<parser>_sample.log` werden nicht überschrieben.

## Privacy-Hinweis

Alle Reports laufen durch `assert_no_plaintext()` → keine Klartext-IPs/Hostnames. Pseudonymisierung via HMAC-SHA256 mit Default-Salt (siehe `docs/PRIVACY.md`). Synthetische Demo-Daten (keine echten Personenbezüge) — trotzdem ist die Pseudonymisierung aktiv.
