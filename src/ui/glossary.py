"""Zentrales Glossar fuer UI-Tooltipps + Per-Page-Erklaerungen (Issue #76).

Single Source of Truth fuer Compliance- und Security-Fachbegriffe, die in der
Streamlit-UI auftauchen. Konsumiert via `src.ui.components.help.page_intro()`
und `term_help()`.

Konvention:
- `short`: max. 140 Zeichen, wird in Streamlit `help=`-Tooltipps angezeigt
- `long`: ausfuehrlicher Markdown-Text fuer den `page_intro`-Expander
- `see_also`: Verweis auf weitere Glossar-Keys (Test pruet dass Keys existieren)
"""

from __future__ import annotations

from typing import NamedTuple


class GlossaryTerm(NamedTuple):
    """Ein einzelner Glossar-Eintrag."""
    label: str
    short: str
    long: str
    see_also: tuple[str, ...] = ()


GLOSSARY: dict[str, GlossaryTerm] = {
    "erfuellungsgrad": GlossaryTerm(
        label="Erfüllungsgrad",
        short=(
            "Anteil der Compliance-Controls eines Frameworks ohne offene Findings. "
            "100 % = alle Controls grün, 0 % = alle non_compliant."
        ),
        long=(
            "Der **Erfüllungsgrad** wird pro Framework (DORA, EU AI Act, ISO 42001, ISO 27001, "
            "DSGVO, CRA) berechnet als `(compliante Controls) / (gesamte Controls)`. "
            "Ein Control gilt als compliant, wenn keine Findings mit Status `non_compliant` "
            "oder `partially_compliant` darauf zeigen. Die Aggregation erfolgt im `ComplianceEngine`."
        ),
        see_also=("compliance_mapping", "non_compliant_status"),
    ),
    "risk_score": GlossaryTerm(
        label="Risk-Score",
        short=(
            "0–100, kombiniert Service-Risikostufe + Frequenz + Upload-Volumen + Off-Hours. "
            "≥ 80 = critical, 60–79 = high."
        ),
        long=(
            "Pro Finding (Client × Service) berechnet die Detection-Engine einen "
            "**Risk-Score 0–100**:\n"
            "- Basis aus `risk_level` des Services (low=20 / medium=40 / high=60 / critical=80)\n"
            "- `+15`, wenn `is_systematic` (`> 10` Requests/Tag)\n"
            "- `+ days_active / 7 * 10`, max. `+10` für anhaltende Nutzung\n"
            "- `+20`, wenn ein Document-Upload (>500 KB) erkannt wurde\n"
            "- `+15`, wenn `off_hours_ratio > 0.3`"
        ),
        see_also=("systematic_threshold", "upload_threshold", "off_hours_ratio"),
    ),
    "compliance_ampel": GlossaryTerm(
        label="Compliance-Ampel",
        short="Visuelle Darstellung der Erfüllungsgrade über alle 6 Frameworks (rot/gelb/grün).",
        long=(
            "Die **Compliance-Ampel** auf der Übersicht zeigt pro Framework eine "
            "Drei-Stufen-Indikation:\n"
            "- 🟢 grün ≥ 80 % Erfüllungsgrad\n"
            "- 🟡 gelb 50 – 79 %\n"
            "- 🔴 rot < 50 %\n"
            "Die Schwellen sind in `src/ui/components/traffic_light.py` definiert."
        ),
        see_also=("erfuellungsgrad",),
    ),
    "compliance_mapping": GlossaryTerm(
        label="Compliance-Mapping",
        short=(
            "Verknüpfung eines technischen Findings mit konkretem Framework-Control "
            "(z. B. DORA Art. 28, ISO 27001 A.5.23)."
        ),
        long=(
            "Jedes Finding trägt eine Liste von **Compliance-Mappings**. Pro Mapping:\n"
            "- `framework` (DORA / EU_AI_ACT / ISO_42001 / ISO_27001 / DSGVO / CRA)\n"
            "- `control_id` (z. B. `Art. 28`, `A.5.9`, `6.1.2`)\n"
            "- `severity` (critical / high / medium / low)\n"
            "- `assessment_status` (non_compliant / partially_compliant / needs_review)\n"
            "Die 22 Mapping-Regeln liegen in `src/compliance/engine.py`."
        ),
        see_also=("erfuellungsgrad", "non_compliant_status"),
    ),
    "non_compliant_status": GlossaryTerm(
        label="Compliance-Status",
        short=(
            "non_compliant = klare Verletzung; partially_compliant = teilweise erfüllt; "
            "needs_review = Sachverhalt unklar."
        ),
        long=(
            "Pro Compliance-Mapping wird ein **Status** vergeben:\n"
            "- `non_compliant` — Control klar verletzt (z. B. nicht-registrierter Drittanbieter)\n"
            "- `partially_compliant` — Control teilweise erfüllt (z. B. Anbieter bekannt, "
            "aber kein AVV)\n"
            "- `needs_review` — Sachverhalt erfordert manuelle Bewertung "
            "(z. B. Browser-Extensions ohne Vendor-Info)"
        ),
        see_also=("compliance_mapping",),
    ),
    "pseudonymisierung": GlossaryTerm(
        label="Pseudonymisierung",
        short=(
            "HMAC-SHA256 von IP/Username, Salt-basiert. Pseudonyme bleiben nach DSGVO Art. 4(5) "
            "personenbezogene Daten."
        ),
        long=(
            "**Pseudonymisierung** ersetzt Klartext-Identifikatoren (IPs, Usernamen) durch "
            "deterministische Hashes (`HMAC-SHA256(key=salt, msg=value)`).\n"
            "- Default-Salt aus `REPORT_SALT`/`PSEUDONYM_SALT` Env oder zufällig\n"
            "- Wechsel des Salts invalidiert alle alten Pseudonyme (Hard-Reset)\n"
            "- Pseudonyme bleiben **personenbezogen** (Wiederherstellung mit Salt möglich) "
            "→ DSGVO bleibt anwendbar"
        ),
        see_also=("salt_override", "k_anonymitaet", "dsfa"),
    ),
    "k_anonymitaet": GlossaryTerm(
        label="k-Anonymität",
        short=(
            "Datenschutz-Garantie: jede sichtbare Gruppe hat mindestens k Mitglieder. "
            "Default k=5; bei k<5 erfolgt Hard-Redaktion."
        ),
        long=(
            "**k-Anonymität** sorgt dafür, dass bei kleinen Gruppen keine Re-Identifikation "
            "möglich ist:\n"
            "- Default `k=5` (`KAnonymityCheck.k_min=5`)\n"
            "- Risikostufen: `low` (k ≥ k_min), `medium` (k_min/2 ≤ k < k_min), "
            "`high` (k < k_min/2)\n"
            "- Bei `high reidentification_risk`: User-Aggregation komplett unterdrückt "
            "(Hard-Redaktion)\n"
            "Bezug: DSGVO Art. 25 Privacy by Design + Art. 32 Schutzmaßnahmen."
        ),
        see_also=("pseudonymisierung", "dsfa"),
    ),
    "dsfa": GlossaryTerm(
        label="DSFA — Datenschutz-Folgenabschätzung",
        short=(
            "DSGVO Art. 35: Pflicht-Risikoanalyse bei voraussichtlich hohem Risiko für "
            "Betroffene (z. B. Squid-Username-Parsing)."
        ),
        long=(
            "Eine **Datenschutz-Folgenabschätzung (DSFA)** nach DSGVO Art. 35 ist Pflicht, "
            "wenn die Verarbeitung voraussichtlich ein hohes Risiko für die Rechte und "
            "Freiheiten der Betroffenen darstellt — z. B. systematische Überwachung von "
            "Mitarbeitenden.\n"
            "Im Telemetrie-Analyzer ist das Squid-Username-Parsing (`%un`) DSFA-pflichtig: "
            "Aktivierung nur über expliziten Double-Opt-in (Settings + Reveal-Button). "
            "Details: [docs/PRIVACY.md](../../../docs/PRIVACY.md)."
        ),
        see_also=("pseudonymisierung",),
    ),
    "salt_override": GlossaryTerm(
        label="Salt-Override",
        short=(
            "Manueller Salt-Wechsel: invalidiert alle bisher generierten Pseudonyme; "
            "Analyse-Daten werden verworfen."
        ),
        long=(
            "Mit dem **Salt-Override** wird der HMAC-Key für die Pseudonymisierung "
            "geändert. Konsequenz:\n"
            "- Alle bisher generierten Pseudonyme sind nicht mehr reproduzierbar\n"
            "- Die Pipeline wird zurückgesetzt (`reset_pipeline()`), Daten müssen neu "
            "hochgeladen werden\n"
            "- Sinnvoll bei Salt-Leak-Verdacht oder zum Vor-/Nach-Vergleich von Audit-Reports"
        ),
        see_also=("pseudonymisierung",),
    ),
    "privacy_self_check": GlossaryTerm(
        label="Privacy-Self-Check",
        short=(
            "Runtime-Test gegen Klartext-Leaks: prüft Reports auf IPv4/IPv6/MAC/interne "
            "Hostnames vor Auslieferung."
        ),
        long=(
            "Der **Privacy-Self-Check** ruft `assert_no_plaintext()` über das gerenderte "
            "Report-JSON. Erkannt werden:\n"
            "- IPv4 / IPv6-Adressen (außer Loopback und RFC1918-Templating)\n"
            "- MAC-Adressen\n"
            "- Interne Hostnamen `*.local`, `*.lan`, `*.corp`, `*.intern`\n"
            "Bei Treffer wird ein `PrivacyLeakError` geworfen und der Report nicht "
            "zurückgegeben. Defense-in-Depth gegen vergessene Pseudonymisierungen."
        ),
        see_also=("pseudonymisierung",),
    ),
    "off_hours_ratio": GlossaryTerm(
        label="Off-Hours-Anteil",
        short=(
            "Anteil der Aktivität außerhalb Bürozeiten (Default 06–22 Uhr). > 0.3 löst "
            "Risk-Score-Boost aus."
        ),
        long=(
            "**Off-Hours-Ratio** = Anteil der Requests außerhalb der konfigurierten "
            "Business-Hours (Default 06:00 – 22:00 lokale Zeit) am Gesamtvolumen "
            "pro Client.\n"
            "Schwelle 0.3 (= 30 %) löst einen `+15`-Boost im Risk-Score aus, weil "
            "nächtliche/Wochenend-Aktivität typisch ist für Daten-Exfiltration oder "
            "Bot-Verhalten. Implementation: `src/analytics/temporal.py`."
        ),
        see_also=("risk_score", "heatmap"),
    ),
    "burst": GlossaryTerm(
        label="Burst",
        short=(
            "Plötzliche Häufung > 50 Requests in 5-Min-Fenster — typisch für Datenabfluss "
            "oder automatisierte Tools."
        ),
        long=(
            "**Bursts** werden via Sliding-Window-Algorithmus erkannt: ≥ 50 Requests "
            "innerhalb eines 5-Minuten-Fensters lösen ein Burst-Finding aus. Überlappende "
            "Bursts werden gemerged. Indiziert oft:\n"
            "- automatisierte API-Calls (Skripte, SDKs)\n"
            "- Daten-Exfiltration in Schüben\n"
            "Implementation: `src/analytics/bursts.py`."
        ),
        see_also=("risk_score",),
    ),
    "co_occurrence_fenster": GlossaryTerm(
        label="Co-Occurrence-Fenster",
        short=(
            "30-Minuten-Zeitfenster, in dem ein User zwei oder mehr KI-Services nutzt — "
            "indiziert Workflow-Kopplung."
        ),
        long=(
            "Das **Co-Occurrence-Fenster** ist die Zeitspanne (Default 30 min), innerhalb "
            "derer parallel genutzte KI-Services als zusammengehörig gewertet werden.\n"
            "Beispiel: ChatGPT + Cursor + Claude binnen 30 min indizieren einen typischen "
            "Code-Kontext-Workflow — risikorelevanter als die Einzelservices, weil "
            "Daten zwischen Tools fließen können (Kontextabfluss).\n"
            "Implementation: `src/analytics/sessions.py:build_session_graph()`."
        ),
        see_also=("session_graph",),
    ),
    "session_graph": GlossaryTerm(
        label="Session-Korrelations-Graph",
        short=(
            "Networkx-Graph mit Services als Knoten und Co-Occurrence-Häufigkeit als "
            "Kantengewicht."
        ),
        long=(
            "Der **Session-Graph** visualisiert KI-Service-Kombinationen pro User über das "
            "30-Min-Fenster:\n"
            "- Knoten = KI-Service (Größe ≈ Nutzungsfrequenz)\n"
            "- Kante = gemeinsame Nutzung im Co-Occurrence-Fenster\n"
            "- Kantengewicht = Häufigkeit\n"
            "- Layout: `networkx.spring_layout(seed=42)` für deterministische Reproduktion\n"
            "Per-User-Drilldown nur sichtbar bei k-Anonymität low risk."
        ),
        see_also=("co_occurrence_fenster", "k_anonymitaet"),
    ),
    "heatmap": GlossaryTerm(
        label="Stunden-Heatmap",
        short=(
            "24×N-Matrix Stunde × Client mit Aktivitätsdichte. Off-Hours sind visuell "
            "schattiert."
        ),
        long=(
            "Die **Heatmap** zeigt Aktivität pro Stunde (Y-Achse) × Client (X-Achse). "
            "Farbintensität = Anzahl Events. Off-Hours-Stunden sind farblich abgesetzt, um "
            "Anomalien sofort sichtbar zu machen.\n"
            "Bei `mask_low_count_cells=True` werden Zellen mit weniger als k=5 Events maskiert, "
            "um keine Re-Identifikation zu ermöglichen."
        ),
        see_also=("off_hours_ratio", "k_anonymitaet"),
    ),
    "asn_fallback": GlossaryTerm(
        label="ASN-Fallback",
        short=(
            "4-Stufen-Matching: wenn Domain unbekannt → IP+Port via ASN-Provider-CIDR-Mapping "
            "auflösen (opt-in)."
        ),
        long=(
            "Wenn ein Log keine Domain enthält (z. B. AWS VPC Flow), greift der **ASN-Fallback**:\n"
            "1. Subdomain-Match → exakter Service\n"
            "2. Alias-Match → Service-Variante\n"
            "3. Service-IP-Match → bekannte direkte IPs\n"
            "4. ASN-Provider-CIDR → Match per AS-Number (opt-in via `enable_asn_fallback=True`)\n"
            "Liefert geringere Confidence — Findings tragen ein `match_method`-Feld."
        ),
        see_also=("parser_auto_detect",),
    ),
    "drift_guard": GlossaryTerm(
        label="Drift-Guard",
        short=(
            "Test, der Schema-Abweichungen zwischen AI-Endpoint-DB-Versionen erkennt und "
            "Datenverlust verhindert."
        ),
        long=(
            "Der **Drift-Guard** in `tests/test_db_versioning.py` lädt jede versionierte "
            "DB unter `data/versions/` und prüft:\n"
            "- Schema-Konformität (`mappings/ai_endpoints_schema.json`)\n"
            "- Keine entfernten Endpoints zwischen Versionen ohne Deprecation-Marker\n"
            "- Konsistente Risk-Levels für gleiche Domains\n"
            "Bricht den Test, wenn ein Bump zu Detection-Lücken führen würde."
        ),
        see_also=(),
    ),
    "systematic_threshold": GlossaryTerm(
        label="Systematik-Schwelle",
        short=(
            "> 10 Requests/Tag/Client/Service = systematische Nutzung. Trigger für Risk-Score-Boost."
        ),
        long=(
            "Ein Finding gilt als **systematisch**, wenn ein Client > 10 Requests/Tag an "
            "einen einzelnen KI-Service sendet. Schwelle in "
            "`src/detection/engine.py:SYSTEMATIC_THRESHOLD = 10`. Konsequenz im Risk-Score: "
            "`+15` Punkte und Markierung `is_systematic=True`. Begründung: gelegentliche "
            "Nutzung ist Recherche, regelmäßige Nutzung ist Workflow-Integration mit "
            "höherem Datenfluss."
        ),
        see_also=("risk_score",),
    ),
    "upload_threshold": GlossaryTerm(
        label="Upload-Schwelle",
        short=(
            "> 500 KB pro Request = Document-Upload-Verdacht. Trigger für +20 Risk-Boost."
        ),
        long=(
            "Squid- und Proxy-Logs liefern `bytes_uploaded`. Ab "
            "`UPLOAD_THRESHOLD_BYTES = 500_000` (= 500 KB) wird ein Request als "
            "**Document-Upload** klassifiziert. Konsequenz: `+20` Risk-Score-Boost und "
            "ein eigenes `upload_event`-Flag im Finding. Indiziert Datei-Anhänge an "
            "ChatGPT/Claude/Gemini."
        ),
        see_also=("risk_score",),
    ),
    "parser_auto_detect": GlossaryTerm(
        label="Parser Auto-Detect",
        short=(
            "Heuristik liest erste Zeilen einer Log-Datei und wählt automatisch den "
            "passenden der 12 Parser."
        ),
        long=(
            "Beim Upload wird die Datei via `detect_log_format()` analysiert: "
            "Header-Zeilen, JSON-Schlüssel oder Syslog-Pattern bestimmen, welcher der "
            "12 Parser zum Einsatz kommt (Pi-hole, Squid, Zscaler, …). Bei Mehrdeutigkeit "
            "kann der Nutzer manuell überschreiben. Implementierung: `src/parsers/detect.py`."
        ),
        see_also=(),
    ),
    "retention_policy": GlossaryTerm(
        label="Retention-Policy",
        short=(
            "Automatische Auto-Löschung nach Default 90 Tagen (DSGVO Art. 5(1e) "
            "Speicherbegrenzung)."
        ),
        long=(
            "Die **Retention-Policy** verwirft Log-Einträge älter als das konfigurierte "
            "Fenster bereits **vor** der Detection — die Daten werden nicht persistiert.\n"
            "- Default: 90 Tage (`RETENTION_DAYS`)\n"
            "- Per-Log-Typ-Overrides via `config/retention.yaml`\n"
            "- Bezug: DSGVO Art. 5(1e) Speicherbegrenzung\n"
            "- Anzeige: Letzte Analyse zeigt `rows_dropped` durch Retention"
        ),
        see_also=(),
    ),
    "llm_backend": GlossaryTerm(
        label="LLM-Backend",
        short=(
            "Anthropic (Cloud) | Ollama (Offline) | Skip (keine KI-Analyse). Auswahl via "
            "Settings oder env LLM_BACKEND."
        ),
        long=(
            "Der **LLM-Backend** entscheidet, womit die KI-gestützte Analyse-Stufe läuft:\n"
            "- `anthropic` — Claude API (Standard, wenn `ANTHROPIC_API_KEY` gesetzt)\n"
            "- `ollama` — lokaler Ollama-Server (z. B. `http://localhost:11434`, Modell "
            "`llama3.1:8b`)\n"
            "- `skip` — keine KI-Analyse, Reports kommen ohne LLM-Empfehlungen\n"
            "Setup-Guide: [docs/OFFLINE_AI.md](../../../docs/OFFLINE_AI.md)."
        ),
        see_also=(),
    ),
}


def get(key: str) -> GlossaryTerm | None:
    """Sicherer Lookup, gibt None statt KeyError."""
    return GLOSSARY.get(key)


__all__ = ["GLOSSARY", "GlossaryTerm", "get"]
