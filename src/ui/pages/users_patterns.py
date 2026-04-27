"""Users & Patterns Page (E2-4).

Zeigt pro Client (pseudonymisiert):
- Top-10-Ranking nach Risk-Max
- Stunden-Heatmap (Client × Stunde des Tages)
- Drill-Down: Services/Findings für einen ausgewählten Client

Privacy:
- Nur pseudonymisierte Client-IDs (client_<hash>), niemals Plaintext.
- k-Anonymitäts-Warnbanner wenn < 5 Clients im Dataset (DSGVO Art. 25/32).
"""

from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.ui.components.badges import risk_badge
from src.ui.components.help import page_intro


def render(report_data: dict[str, Any]) -> None:
    st.title("👥 Users & Patterns")
    page_intro(
        title="Users & Patterns",
        what_you_see=(
            "Per-Client-Sicht (pseudonymisiert): **Top-10-Ranking** nach maximalem "
            "Risk-Score, **Stunden-Heatmap** (Client × Tagesstunde), **Off-Hours-Anteil** "
            "und Drilldown auf Service-Ebene. User-IDs sind durchgängig HMAC-Pseudonyme — "
            "Klartext-Namen erscheinen nur bei explizitem Squid-`%un`-Reveal-Opt-in."
        ),
        key_terms=("pseudonymisierung", "k_anonymitaet", "off_hours_ratio", "heatmap"),
    )

    user_patterns = report_data.get("user_patterns") or {}
    findings = report_data.get("findings", [])
    user_aggregation = report_data.get("user_aggregation") or {}

    _render_k_anonymity_banner(user_patterns.get("k_anonymity") or {})
    _render_username_gating_banner(user_aggregation)

    if user_patterns.get("privacy_redacted"):
        st.error(
            "🛡️ **Redaktion aktiv (DSGVO Art. 25):** Wegen hohen "
            "Re-Identifikations-Risikos (k-Anonymität deutlich unter Minimum) "
            "sind Top-Clients-Ranking und Stunden-Heatmap ausgeblendet. "
            "Erweitere das Dataset auf mindestens die halbe Minimum-k-Grenze "
            "oder dokumentiere eine Rechtsgrundlage, um die Auswertung "
            "wieder freizuschalten."
        )
        return

    top_clients = user_patterns.get("top_clients") or []
    if not top_clients:
        st.info("Keine Client-Daten im Analysezeitraum.")
        return

    _render_top_ranking(top_clients)
    _render_heatmap(user_patterns.get("hourly_heatmap") or {}, top_clients)
    _render_drilldown(top_clients, findings, user_aggregation)


def _render_username_gating_banner(aggregation: dict[str, Any]) -> None:
    """Warnt prominent, wenn Username-Parsing aktiv ist, und steuert den Reveal-Opt-in.

    Zweite Stufe des Double-Opt-in (Issue #22): Selbst wenn der Operator in
    den Einstellungen den Parser-Flag gesetzt hat, bleiben Pseudonyme bis
    zur expliziten Button-Bestätigung maskiert. Der Opt-in gilt nur in der
    aktuellen Streamlit-Session und wird nicht persistiert.
    """
    if not aggregation.get("enabled"):
        return
    unique_users = aggregation.get("unique_users", 0)
    st.warning(
        f"⚠️ **Username-Parsing aktiv** — {unique_users} pseudonymisierte "
        "Usernamen im Dataset. Pseudonyme sind personenbezogene Daten "
        "(DSGVO Art. 4(5)). Die DSFA-Verantwortung nach Art. 35 liegt "
        "beim Betreiber dieser Instanz."
    )
    reveal = st.session_state.get("squid_username_reveal", False)
    col_left, col_right = st.columns([3, 1])
    with col_left:
        st.caption(
            "Standardmäßig werden User-Pseudonyme maskiert (`user_***`). "
            "Der folgende Button hebt die Maskierung nur in dieser Session auf."
        )
    with col_right:
        btn_label = "👁️ Pseudonyme ausblenden" if reveal else "👁 Pseudonyme anzeigen"
        if st.button(btn_label, key="users_username_reveal_btn", use_container_width=True):
            st.session_state.squid_username_reveal = not reveal
            st.rerun()


def _mask_user_pseudonym(pseudo: str) -> str:
    """`user_a3b2c1d4` → `user_a***` (behält 1 Zeichen für Wiedererkennung)."""
    if not pseudo or not pseudo.startswith("user_"):
        return pseudo
    tail = pseudo[5:]
    if len(tail) <= 1:
        return "user_***"
    return f"user_{tail[0]}***"


def _render_k_anonymity_banner(k_info: dict[str, Any]) -> None:
    if not k_info:
        return
    if k_info.get("is_sufficient", True):
        st.caption(
            f"✓ k-Anonymität erfüllt — {k_info.get('observed_k', 0)} Clients "
            f"(Minimum {k_info.get('minimum_k', 5)})."
        )
        return
    risk = (k_info.get("reidentification_risk") or "high").upper()
    st.warning(
        f"⚠️ **k-Anonymität unterschritten:** Nur "
        f"{k_info.get('observed_k', 0)} unterschiedliche Clients im Dataset — "
        f"Re-Identifikations-Risiko: **{risk}**.  \n"
        f"DSGVO Art. 25/32: Bei kleinen Datasets kann Pseudonymisierung das "
        f"Re-Identifikations-Risiko nicht vollständig mitigieren. "
        f"Auswertung nur weiterführen, wenn Rechtsgrundlage und Zweck explizit dokumentiert sind."
    )


def _render_top_ranking(top_clients: list[dict[str, Any]]) -> None:
    st.markdown("### Top-10 Clients nach Risk-Max")
    top10 = top_clients[:10]
    df = pd.DataFrame([
        {
            "Client": c["client_pseudonym"],
            "Services": c["service_count"],
            "Queries": c["total_queries"],
            "Risk-Max": c["risk_max"],
            "Level": c["risk_level_max"],
            "Uploads": c["upload_events"],
            "📄": "✓" if c.get("has_document_upload") else "—",
        }
        for c in top10
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)


def _render_heatmap(
    heatmap_by_client: dict[str, list[int]],
    top_clients: list[dict[str, Any]],
) -> None:
    st.markdown("### Heatmap: Client × Stunde des Tages")
    if not heatmap_by_client:
        st.info("Keine Zeitstempel-Daten für Heatmap verfügbar.")
        return

    # Reihenfolge: Top-Clients zuerst (bis zu 15, sonst unleserlich).
    ordered = [
        c["client_pseudonym"]
        for c in top_clients[:15]
        if c["client_pseudonym"] in heatmap_by_client
    ]
    if not ordered:
        ordered = list(heatmap_by_client.keys())[:15]

    z = [heatmap_by_client[c] for c in ordered]
    hours = list(range(24))
    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=hours,
        y=ordered,
        colorscale="YlOrRd",
        colorbar=dict(title="Queries"),
        hovertemplate="Client: %{y}<br>Stunde: %{x}:00<br>Queries: %{z}<extra></extra>",
    ))
    # Off-Hours-Schattierung (06–22 Uhr = Business; 0–5 & 22–23 = Off-Hours).
    fig.add_vrect(x0=-0.5, x1=5.5, fillcolor="#64748b", opacity=0.10, layer="below", line_width=0)
    fig.add_vrect(x0=21.5, x1=23.5, fillcolor="#64748b", opacity=0.10, layer="below", line_width=0)
    fig.update_layout(
        height=max(300, 40 * len(ordered)),
        xaxis=dict(title="Stunde (UTC) — graue Bereiche = Off-Hours",
                   tickmode="linear", dtick=1, range=[-0.5, 23.5]),
        yaxis=dict(title="Client (pseudonymisiert)"),
        margin=dict(l=20, r=20, t=20, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_drilldown(
    top_clients: list[dict[str, Any]],
    findings: list[dict[str, Any]],
    user_aggregation: dict[str, Any] | None = None,
) -> None:
    st.markdown("### Drilldown")
    client_options = [c["client_pseudonym"] for c in top_clients]
    if not client_options:
        return

    selected = st.selectbox(
        "Client auswählen",
        options=client_options,
        index=0,
        key="users_patterns_selected_client",
    )
    if not selected:
        return

    client_findings = [f for f in findings if f.get("client_pseudonym") == selected]
    st.caption(f"**{len(client_findings)}** Findings für `{selected}`")

    if user_aggregation and user_aggregation.get("enabled"):
        users_for_client = (user_aggregation.get("per_client") or {}).get(selected, [])
        if users_for_client:
            reveal = st.session_state.get("squid_username_reveal", False)
            shown = users_for_client if reveal else [
                _mask_user_pseudonym(u) for u in users_for_client
            ]
            hint = "" if reveal else " (maskiert — Reveal-Button oben)"
            st.markdown(
                f"**Usernamen für `{selected}`{hint}:** "
                + ", ".join(f"`{u}`" for u in shown)
            )

    if not client_findings:
        st.info("Keine Findings für diesen Client.")
        return

    df_f = pd.DataFrame([
        {
            "Service": f["service"],
            "Provider": f["provider"],
            "Risk": f["risk_level"],
            "Score": f["risk_score"],
            "Queries": f["total_queries"],
            "Q/Tag": f["queries_per_day"],
            "Tage": f.get("days_active", 0),
            "Sys.": "✓" if f.get("is_systematic") else "—",
            "Upload": "📄" if f.get("has_document_upload") else "—",
        }
        for f in client_findings
    ])
    st.dataframe(df_f, use_container_width=True, hide_index=True)

    st.markdown("#### Risiko-Übersicht")
    for f in sorted(client_findings, key=lambda x: x.get("risk_score", 0), reverse=True)[:5]:
        st.markdown(
            f"- **{f.get('service', '—')}** "
            f"({f.get('provider', '—')}) — "
            f"{risk_badge(f.get('risk_level', 'low'))} Score **{f.get('risk_score', 0)}** · "
            f"{f.get('queries_per_day', 0)} Queries/Tag"
            + (" · 📄 Upload" if f.get("has_document_upload") else ""),
            unsafe_allow_html=True,
        )
