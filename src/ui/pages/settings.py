"""Einstellungen-Page: Salt-Override, Privacy-Self-Check, Schwellwert-Anzeige."""

from __future__ import annotations

import json
import secrets
from typing import Any

import streamlit as st

from src.detection.engine import SYSTEMATIC_THRESHOLD, UPLOAD_THRESHOLD_BYTES
from src.reports.privacy import PrivacyLeakError, assert_no_plaintext


def render(report_data: dict[str, Any] | None) -> None:
    st.title("⚙️ Einstellungen")

    st.markdown("### Pseudonymisierung")
    st.success("Pseudonymisierung ist **immer aktiv** (HMAC-SHA256, DSGVO Art. 25).")

    current_salt = st.session_state.get("report_salt", "")
    fingerprint = report_data.get("report_meta", {}).get("salt_fingerprint", "—") if report_data else "—"
    st.markdown(
        f"**Aktiver Salt-Fingerprint:** `{fingerprint}` "
        f"(reproduzierbare Pseudonyme bei gleichem Salt)"
    )

    with st.expander("Salt überschreiben (für reproduzierbare Reports)"):
        new_salt = st.text_input(
            "Neuer Salt (mind. 16 Zeichen empfohlen)",
            value="",
            type="password",
        )
        col1, col2 = st.columns(2)
        if col1.button("Salt setzen", disabled=not new_salt or len(new_salt) < 8):
            st.session_state.report_salt = new_salt
            st.success("Salt aktualisiert. Bitte Analyse neu starten (Reset → erneuter Upload).")
        if col2.button("Zufälligen Salt generieren"):
            st.session_state.report_salt = secrets.token_hex(16)
            st.success("Neuer zufälliger Salt gesetzt.")

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
