"""Einstellungen-Page: Salt-Override, Privacy-Self-Check, Schwellwert-Anzeige."""

from __future__ import annotations

import json
import secrets
from typing import Any

import streamlit as st

from src.detection.engine import SYSTEMATIC_THRESHOLD, UPLOAD_THRESHOLD_BYTES
from src.privacy.retention import load_policy
from src.reports.privacy import PrivacyLeakError, assert_no_plaintext
from src.ui.state import reset_pipeline


def render(report_data: dict[str, Any] | None) -> None:
    st.title("⚙️ Einstellungen")

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
