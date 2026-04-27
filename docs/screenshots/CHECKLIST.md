# Screenshot-Checkliste

Diese Liste ist die **Single Source of Truth** für alle Demo- und Doku-Screenshots des Telemetrie-Analyzers. Sie wird maschinell ausgewertet von [`scripts/verify_screenshots.py`](../../scripts/verify_screenshots.py) (kommt mit Sprint 10D / [#75](https://github.com/florian-priegnitz/Telemetrie-Analyzer/issues/75)).

## Konventionen

- **Naming-Schema:** `NN_<page>_<state>.png` (`NN` = zweistellig, beginnend bei `00`)
- **Resolution:** 1920 × 1080 (Full-Page für Streamlit, sichtbarer Viewport bei Browser-Reports)
- **Format:** PNG, ohne Browser-Chrome (Adressleiste etc.) wo möglich
- **Ablage:** Alle PNGs liegen direkt in `docs/screenshots/` (keine Sub-Verzeichnisse)
- **Sample-Datensatz:** Soweit nicht anders vermerkt → KRITIS-KMU-Demo (50 User Squid)

## Verifikation

Der Verifier parst dieses Dokument und prüft pro `- [ ]`-Zeile, ob die genannte `.png`-Datei existiert:

```bash
python scripts/verify_screenshots.py            # Default: --warn (Exit 0, listet fehlende)
python scripts/verify_screenshots.py --strict   # Exit 1 bei fehlenden (für Release-CI)
```

## Liste

### Onboarding & Übersicht (5 PNGs)

- [ ] 00_onboarding.png — Willkommens-Screen mit Demo-Buttons (Pi-hole, Squid, KRITIS, …)
- [ ] 01_overview_kritis_loaded.png — Übersicht nach KRITIS-KMU-Demo, KPIs sichtbar (Total Queries, AI Queries, Unique Clients, Compliance-Ampel)
- [ ] 02_findings_filter_critical.png — Findings gefiltert auf Risk=critical, sichtbare Tabelle mit ≥3 Einträgen
- [ ] 03_findings_detail_expanded.png — Ein Finding mit Compliance-Mappings expanded (DORA Art. 28 + EU AI Act Art. 9 sichtbar)
- [ ] 04_users_patterns_top10.png — Top-10-User-Ranking, KRITIS-Datensatz (Pseudonyme `user_*`)

### Analytics (2 PNGs)

- [ ] 05_users_patterns_heatmap.png — Stunden-Heatmap mit Off-Hours-Schattierung, k-Anonymitäts-Banner sichtbar
- [ ] 06_sessions_graph.png — Session-Korrelations-Graph (networkx-Plot mit ≥3 Knoten und ≥2 Kanten)

### Compliance — alle 6 Frameworks (6 PNGs)

- [ ] 07_compliance_dora.png — DORA-Tab mit Score-Card und Mapping-Tabelle
- [ ] 08_compliance_eu_ai_act.png — EU AI Act-Tab mit Risikoklassifizierung
- [ ] 09_compliance_iso_42001.png — ISO 42001-Tab mit AI-Inventar-Status
- [ ] 10_compliance_iso_27001.png — ISO 27001-Tab mit Asset-Coverage
- [ ] 11_compliance_dsgvo.png — DSGVO-Tab mit DSFA-Hinweisen
- [ ] 12_compliance_cra.png — CRA-Tab (6. Framework, 7 Controls aus `mappings/cra.yaml`)

### Settings & Formate (4 PNGs)

- [ ] 13_formats_catalog.png — 12-Formate-Liste mit Feld-Mapping (Pi-hole bis Elastic ECS)
- [ ] 14_settings_backend_ollama.png — Settings mit aktiviertem Ollama-Backend, Verbindungs-Test ✅
- [ ] 15_settings_privacy_selfcheck.png — Salt-Fingerprint + Retention-Policy + Privacy-Self-Check OK
- [ ] 16_settings_squid_username_dsfa.png — Squid-Username-Toggle mit DSFA-Banner ([#22](https://github.com/florian-priegnitz/Telemetrie-Analyzer/pull/70))

### Reports im Browser (2 PNGs)

- [ ] 17_report_executive_kritis.png — Executive-HTML-Report (KRITIS-KMU) Browser-View, sichtbare Risk-Section
- [ ] 18_report_compliance_cra.png — Compliance-HTML-Report mit aufgeklappter CRA-Sektion

### Offline-Stack (2 PNGs)

- [ ] 19_offline_docker_compose_up.png — Terminal: `docker compose --profile offline up` mit gestartetem `ollama`-Service
- [ ] 20_offline_ollama_chat_response.png — Settings-Page zeigt erfolgreichen Verbindungs-Test (Modell `llama3.1:8b`)

## Workflow

1. Streamlit lokal starten: `streamlit run app.py` → http://localhost:8501
2. KRITIS-Demo-Button klicken (oder eigenes Sample hochladen)
3. Pro Page einen Screenshot erstellen — Naming exakt wie oben
4. PNGs nach `docs/screenshots/` kopieren
5. `python scripts/verify_screenshots.py` ausführen — prüft Vollständigkeit
6. Optional: Playwright-Variante via `scripts/capture_screenshots.py` (existiert für Pi-hole-Standard-Demo, KRITIS-/Offline-Screenshots derzeit manuell)

## Hinweis

Nach **CI-Branding-Rollout** ([#78](https://github.com/florian-priegnitz/Telemetrie-Analyzer/issues/78)) müssen alle Screenshots neu erstellt werden — neue Farben, Schriften, Lineal-Bildmarke. Der Verifier markiert das nicht automatisch; bitte CHECKLIST nach dem Branding-Merge erneut durchgehen.
