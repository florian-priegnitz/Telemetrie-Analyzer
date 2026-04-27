"""Einstellungen-Page: Salt-Override, Privacy-Self-Check, Schwellwert-Anzeige."""

from __future__ import annotations

import json
import os
import secrets
from typing import Any

import streamlit as st

from src.analyzer.backends import OllamaBackend, select_backend
from src.detection.engine import SYSTEMATIC_THRESHOLD, UPLOAD_THRESHOLD_BYTES
from src.privacy.retention import load_policy
from src.reports.privacy import PrivacyLeakError, assert_no_plaintext
from src.ui.components.db_status import render_db_status
from src.ui.components.help import page_intro
from src.ui.state import reset_pipeline


def render(report_data: dict[str, Any] | None) -> None:
    st.title("⚙️ Einstellungen")
    page_intro(
        title="Einstellungen",
        what_you_see=(
            "Konfigurations-Hub für die Analyse:\n\n"
            "- **KI-Backend** wählen (Anthropic Cloud / Ollama Offline / Skip)\n"
            "- **Pseudonymisierungs-Salt** überschreiben (mit Hard-Reset)\n"
            "- **Squid-Username-Parsing** als DSFA-Double-Opt-in (DSGVO Art. 35)\n"
            "- **Retention-Policy** anzeigen (Auto-Löschung nach Default 90 Tagen)\n"
            "- **Privacy-Self-Check** über das letzte Report-Datenset\n"
            "- **Detection-Schwellwerte** (Read-Only zur Reproduzierbarkeit)\n\n"
            "Änderungen am Salt oder Username-Toggle verwerfen vorhandene Analyse-Daten."
        ),
        key_terms=(
            "llm_backend", "salt_override", "pseudonymisierung", "dsfa",
            "retention_policy", "privacy_self_check",
            "systematic_threshold", "upload_threshold", "endpoint_db_freshness",
        ),
    )

    _render_backend_section()

    st.markdown("### Pseudonymisierung")
    st.success("Pseudonymisierung ist **immer aktiv** (HMAC-SHA256, DSGVO Art. 25).")

    fingerprint = report_data.get("report_meta", {}).get("salt_fingerprint", "—") if report_data else "—"
    st.markdown(
        f"**Aktiver Salt-Fingerprint:** `{fingerprint}` "
        f"(reproduzierbare Pseudonyme bei gleichem Salt)"
    )

    with st.expander("Salt überschreiben (für reproduzierbare Reports)"):
        st.warning(
            "⚠️ Salt-Wechsel invalidiert alle bisher generierten Pseudonyme. "
            "Vorhandene Analyse-Daten werden verworfen, danach bitte erneut hochladen."
        )
        new_salt = st.text_input(
            "Neuer Salt (mind. 16 Zeichen empfohlen)",
            value="",
            type="password",
        )
        col1, col2 = st.columns(2)
        if col1.button("Salt setzen", disabled=not new_salt or len(new_salt) < 8):
            st.session_state.report_salt = new_salt
            reset_pipeline()
            st.success("Salt aktualisiert. Analyse-Daten verworfen, bitte Datei erneut hochladen.")
        if col2.button("Zufälligen Salt generieren"):
            st.session_state.report_salt = secrets.token_hex(16)
            reset_pipeline()
            st.success("Neuer zufälliger Salt gesetzt. Analyse-Daten verworfen.")

    st.markdown("### Squid Username-Parsing (Double-Opt-in, DSFA-pflichtig)")
    st.caption(
        "Optional: aktiviert das Auslesen des `%un`/`rfc931`-Feldes aus Squid-"
        "Access-Logs und macht User-Level-Korrelation möglich. Der Raw-Username "
        "wird nie persistiert — nur ein deterministisches HMAC-Pseudonym. "
        "Trotzdem bleiben pseudonymisierte Usernamen nach DSGVO Art. 4(5) "
        "personenbezogene Daten und erfordern eine DSFA (Art. 35) durch den "
        "Betreiber vor der Aktivierung."
    )
    username_enabled = st.session_state.get("squid_username_parsing_enabled", False)
    new_state = st.toggle(
        "Username-Parsing aktivieren (DSFA-Verantwortung beim Betreiber)",
        value=username_enabled,
        key="squid_username_toggle",
        help=(
            "Wenn aktiv, extrahiert der Squid-Parser das `%un`-Feld und "
            "pseudonymisiert es. Die Users-Page zeigt dann Pseudonyme "
            "standardmäßig maskiert; ein zweiter Opt-in-Button in der "
            "Users-Page hebt die Maskierung session-weit auf."
        ),
    )
    if new_state != username_enabled:
        st.session_state.squid_username_parsing_enabled = new_state
        # Reveal-Opt-in verliert mit Toggle seine Grundlage, zurücksetzen.
        st.session_state.squid_username_reveal = False
        reset_pipeline()
        if new_state:
            st.warning(
                "✅ Username-Parsing aktiviert. Bitte eine neue Analyse starten. "
                "**Hinweis:** Die DSFA-Dokumentation liegt in Ihrer Verantwortung "
                "als Betreiber (DSGVO Art. 35, Verzeichnis von "
                "Verarbeitungstätigkeiten nach Art. 30)."
            )
        else:
            st.success("Username-Parsing deaktiviert. Analyse-Daten verworfen.")

    with st.expander("Analyse-Session beenden (alle Daten löschen)"):
        st.caption(
            "Löscht hochgeladene Bytes, Pipeline-Cache und Report-Daten aus der "
            "Browser-Session. DSGVO Art. 5 (1e) Speicherbegrenzung."
        )
        if st.button("🗑 Alle Analyse-Daten jetzt löschen", use_container_width=True):
            reset_pipeline()
            st.success("Alle Analyse-Daten gelöscht.")

    st.markdown("### Retention (DSGVO Art. 5 (1e) — Speicherbegrenzung)")
    policy = load_policy()
    if policy.enabled:
        st.success(
            f"Aktiv: Default **{policy.default_days} Tage**. Einträge außerhalb des "
            f"Retention-Horizonts werden vor der Detection verworfen."
        )
    else:
        st.warning("Retention ist **deaktiviert**. Bitte `config/retention.yaml` prüfen.")

    per_type = " · ".join(
        f"`{k}`: **{v}d**" for k, v in sorted(policy.policies.items())
    ) or "—"
    st.caption(f"Per-Log-Typ-Overrides: {per_type}")

    if report_data and "retention" in report_data:
        ret = report_data["retention"]
        st.markdown(
            f"**Letzte Analyse:** {ret['rows_before']} Einträge geparst, "
            f"{ret['rows_dropped']} durch Retention verworfen "
            f"(Log-Typ `{ret['log_type']}`, Fenster {ret['days']} Tage)."
        )
    st.caption(
        "Override via ENV `RETENTION_DAYS` / `RETENTION_CONFIG`. Der Analyzer "
        "persistiert keine Rohdaten — Retention wirkt rein in-memory."
    )

    render_db_status(compact=False)

    st.markdown("### Detection-Schwellwerte (read-only)")
    st.markdown(
        f"- **Systematische Nutzung:** > {SYSTEMATIC_THRESHOLD} Requests/Tag\n"
        f"- **Document-Upload-Schwelle:** > {UPLOAD_THRESHOLD_BYTES / 1024:.0f} KB pro Request"
    )
    st.caption(
        "Schwellwerte werden in `src/detection/engine.py` definiert und gelten für alle Analysen. "
        "Eine Laufzeit-Anpassung ist aktuell nicht implementiert (bewusst, für Reproduzierbarkeit)."
    )

    st.markdown("### Privacy Self-Check")
    if not report_data:
        st.info("Bitte zuerst eine Analyse durchführen, bevor der Self-Check ausgeführt wird.")
        return

    if st.button("🔒 Auf Klartext-Daten prüfen"):
        try:
            payload = json.dumps(report_data, default=str)
            assert_no_plaintext(payload)
            st.success(
                "✅ **Bestanden** — keine Klartext-IPs/MAC/internen Hostnames im Report-Datensatz."
            )
        except PrivacyLeakError as exc:
            st.error(f"❌ **Privacy-Leak gefunden:** {exc}")


def _render_backend_section() -> None:
    """KI-Backend-Auswahl (Anthropic Cloud / Ollama Offline / Skip)."""
    st.markdown("### KI-Backend")
    st.caption(
        "Wählt das LLM-Backend für die Analyse. **Ollama** läuft komplett offline "
        "(z.B. via `docker compose --profile offline up`) und ist für KRITIS-/DSGVO-"
        "Argumentation relevant. **Skip** deaktiviert die KI-Analyse — Detection, "
        "Compliance-Mapping und Reports laufen weiter."
    )

    current = (
        st.session_state.get("llm_backend_choice")
        or os.environ.get("LLM_BACKEND", "").strip().lower()
        or ("anthropic" if os.environ.get("ANTHROPIC_API_KEY") else "skip")
    )
    options = ["anthropic", "ollama", "skip"]
    labels = {
        "anthropic": "Anthropic (Cloud)",
        "ollama": "Ollama (Offline)",
        "skip": "Skip (keine KI-Analyse)",
    }
    choice = st.radio(
        "Backend",
        options,
        index=options.index(current) if current in options else 2,
        format_func=lambda key: labels[key],
        horizontal=True,
        key="llm_backend_choice_radio",
        help=(
            "Wechsel wirkt für die nächste Analyse. Anthropic benötigt "
            "`ANTHROPIC_API_KEY`; Ollama benötigt einen erreichbaren "
            "Ollama-Server (Default `http://localhost:11434`)."
        ),
    )
    if choice != current:
        st.session_state.llm_backend_choice = choice

    # Backend-spezifische Statusanzeige
    if choice == "anthropic":
        has_key = bool(os.environ.get("ANTHROPIC_API_KEY"))
        if has_key:
            st.success("✅ `ANTHROPIC_API_KEY` ist gesetzt.")
        else:
            st.warning(
                "⚠️ `ANTHROPIC_API_KEY` ist nicht gesetzt. "
                "Backend bleibt im Skip-Modus."
            )
    elif choice == "ollama":
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
        model = os.environ.get("OLLAMA_MODEL", "llama3.1:8b")
        st.markdown(f"**Host:** `{host}` · **Modell:** `{model}`")
        if st.button("🔌 Verbindung testen"):
            backend = OllamaBackend()
            if backend.is_available:
                st.success(f"✅ Ollama erreichbar unter `{backend.host}` (Modell `{backend.model}`).")
            else:
                st.error(
                    f"❌ Ollama nicht erreichbar unter `{backend.host}`. "
                    "Server starten via `docker compose --profile offline up` "
                    "oder `ollama serve`."
                )
    else:  # skip
        st.info("KI-Analyse deaktiviert. Reports werden ohne LLM-generierte Empfehlungen erstellt.")

    # Aktive Auflösung anzeigen (was würde `select_backend` faktisch zurückgeben?)
    resolved = select_backend(name=choice)
    resolved_label = resolved.name if resolved is not None else "skip"
    st.caption(f"Effektiv aktives Backend bei nächster Analyse: **{resolved_label}**")
