# Privacy Engineering

Der **Telemetrie Analyzer** verarbeitet DNS-, Proxy- und SIEM-Logs. Das sind nach DSGVO Art. 4 personenbezogene Daten (IPs, Usernamen, Domain-Patterns). Dieses Dokument beschreibt die eingebauten Schutzmaßnahmen und die Entscheidungspunkte, an denen der Betreiber bewusst Stellung nehmen muss.

## Pseudonymisierung (Art. 25 DSGVO)

- **Verfahren:** HMAC-SHA256 mit per-Session zufälligem Salt (oder ENV `REPORT_SALT`).
- **Felder:** IPs (Spalte `client` → `ip_<hash>`), Usernamen opt-in (`user_pseudonym` → `user_<hash>`).
- **Deterministik:** Gleicher Salt + gleicher Input → gleicher Hash, damit Korrelation erhalten bleibt.
- **Salt-Wechsel:** invalidiert alle Pseudonyme der Session (Streamlit-Reset-Pipeline) — DSGVO-kompatible "rechtliche Zweckbindung je Analyse".
- **Salt-Entsorgung:** Der Salt selbst ist nicht personenbezogen, wird aber nicht persistiert — Prozess-Restart = neuer Salt, alte Hashes nicht mehr herleitbar.

Pseudonymisierte Daten bleiben nach Art. 4(5) DSGVO personenbezogene Daten. Betreiber sind weiterhin verantwortliche Stelle (Art. 4(7)).

## k-Anonymität (Art. 25)

- **Schwelle:** k ≥ 5 pro Client-Attribut bei UI-Drill-Downs.
- **Harte Redaktion:** Bei beobachtetem k < Minimum/2 werden Top-Ranking, Heatmap und Session-Graph **komplett** unterdrückt; die UI zeigt ein explizites Warnbanner.
- **Heatmap-Zellen-Masking:** Zellen mit Count < 3 werden auf 0 gesetzt (Re-ID-Schutz über 24h-Aktivitätsmuster).

## Retention (Art. 5 (1e))

- **Default:** 90 Tage, konfigurierbar über `config/retention.yaml` oder ENV `RETENTION_DAYS` / `RETENTION_CONFIG`.
- **Wirkmechanik:** nur in-memory — der Analyzer persistiert keine Rohdaten. Retention kappt den Analysezeitraum **vor** der Detection.
- **Dokumentation:** jede Analyse führt eine Retention-Zeile im Settings-Panel mit (Rows before / dropped).

## Runtime-Schutz (`assert_no_plaintext`)

- Vor jedem Report-Write (`src/reports/privacy.py`) prüft ein Regex-Fingerprint, ob Klartext-IPs/MAC/interne Hostnames im Output stehen.
- Ein Fund wirft `PrivacyLeakError` und bricht den Export ab — Defense-in-Depth, unabhängig von Parser-Korrektheit.

## Double-Opt-in Username-Parsing (Squid `%un`, Issue #22)

**Kontext:** Squid kann (bei entsprechendem `logformat`) das Feld `%un` (authentifizierter Username) liefern. Pseudonymisiert gewinnt das erheblich an Aussagekraft gegenüber IP-only-Detection, bleibt aber ein direkt personenbezogenes Datum.

### Warum "Double-Opt-in"?

Der Analyzer ist für den Einsatz in unterschiedlich großen Umgebungen gedacht. In kleinen Subnetzen (< 5 Auth-Nutzer) kann ein Pseudonym 1:1 re-identifizierbar sein. Deshalb gibt es zwei aktive Entscheidungsstufen:

| Stufe | Wirkung | Wer aktiviert? |
|---|---|---|
| **1 — Parser-Flag** | Squid-Parser extrahiert und pseudonymisiert `%un` | Betreiber in Einstellungen → *Squid Username-Parsing* |
| **2 — UI-Reveal** | Pseudonyme in der Users-Page unmaskiert anzeigen | Nutzer per Button "Pseudonyme anzeigen" (nur Session-scoped) |

Ohne Stufe 1 erscheint die Spalte `user_pseudonym` gar nicht im DataFrame. Ohne Stufe 2 zeigt die UI `user_a***` statt `user_a3b2c1d4`.

### Invarianten

- **Raw-Username nie im DataFrame:** Der Parser normalisiert (`DOMAIN\user`, `user@corp.tld`, `CN=user,OU=…` → `user`), hasht sofort und verwirft den Rohwert. Tests sichern das ab (`tests/test_squid_username.py::test_raw_username_never_in_dataframe`).
- **Kein Persist:** Der Reveal-Button-Zustand wird nicht persistiert, er ist Streamlit-Session-scoped.
- **Cache-Trennung:** `squid_username_parsing` ist Teil des `run_pipeline`-Cache-Keys — Flag-Umschaltung erzwingt eine frische Pipeline-Ausführung, keine Vermischung von Modi.
- **k-Anonymität-Gate:** Bei hohem Re-ID-Risiko wird die User-Aggregation analog zu Client-Ranking **komplett** unterdrückt (siehe `_build_user_aggregation`).

### DSFA-Verantwortung des Betreibers

Der Betreiber aktiviert das Feature bewusst und übernimmt damit die Verantwortung für:

- **DSGVO Art. 35 — DSFA** bei hohem Risiko für Betroffene (neue Technologie, Überwachungscharakter)
- **DSGVO Art. 30 — Verzeichnis von Verarbeitungstätigkeiten**
- **Betriebsrats-/MAV-Einbindung** bei Mitbestimmungsrelevanz
- **Information der Betroffenen** (Art. 13/14)

Die UI zeigt bei jedem Analyse-Lauf mit aktivem Username-Parsing einen expliziten Warnbanner. Der Betreiber kann das Feature jederzeit deaktivieren — die nächste Analyse läuft dann wieder im Default-Modus ohne User-Spalte.

### DSFA-Checkliste (kurz)

Vor Aktivierung sollten diese Punkte dokumentiert sein:

- [ ] Zweckbindung (welche Frage beantwortet User-Level-Detection konkret?)
- [ ] Rechtsgrundlage (Art. 6 Abs. 1 lit. f berechtigtes Interesse? Einwilligung? Art. 88 Beschäftigten-Kontext?)
- [ ] Erforderlichkeit (nicht-identifizierende Alternativen geprüft?)
- [ ] Datensparsamkeit (Pseudonym + Löschfrist)
- [ ] Risikobetrachtung (k-Anonymität, Re-ID-Vektoren, Beschäftigten-Überwachung)
- [ ] Technisch-organisatorische Maßnahmen (Zugriff auf UI, Salt-Handling, Log-Handling)
- [ ] Betroffenenrechte (Auskunft, Löschung, Widerspruch — ohne Raw-Username praktisch umsetzbar?)
- [ ] Betriebsrat/MAV einbezogen (falls einschlägig)

## Compliance-Mapping

| Schutzmaßnahme | DSGVO | ISO 27001 | ISO 42001 | EU AI Act |
|---|---|---|---|---|
| HMAC-Pseudonymisierung | Art. 25, Art. 32 | A.8.11 | 8.4 | Art. 10 |
| k-Anonymitäts-Redaktion | Art. 25 | A.8.12 | 8.4 | Art. 10 |
| Runtime-Leak-Assert | Art. 32 | A.8.16 | 8.4 | — |
| Retention-Policy | Art. 5 (1e) | A.8.10 | 8.4 | — |
| Double-Opt-in Username | Art. 25, Art. 35 | A.5.34 | 6.1.2 | Art. 10 |

## Weiterführend

- Architektur: [`README.md#architektur`](../README.md)
- Pseudonymizer-Code: [`src/privacy/pseudonymizer.py`](../src/privacy/pseudonymizer.py)
- k-Anonymität: [`src/privacy/k_anonymity.py`](../src/privacy/k_anonymity.py)
- Leak-Assert: [`src/reports/privacy.py`](../src/reports/privacy.py)
- Verantwortliche Offenlegung: [`SECURITY.md`](../SECURITY.md)
