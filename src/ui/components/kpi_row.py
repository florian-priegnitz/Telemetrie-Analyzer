"""KPI-Übersichts-Reihe mit st.metric (4 Kennzahlen)."""

from __future__ import annotations

from typing import Any

import streamlit as st

from src.ui.components.help import term_help


def _format_bytes(num_bytes: int) -> str:
    if num_bytes < 1024:
        return f"{num_bytes} B"
    if num_bytes < 1024 ** 2:
        return f"{num_bytes / 1024:.1f} KB"
    if num_bytes < 1024 ** 3:
        return f"{num_bytes / 1024 ** 2:.1f} MB"
    return f"{num_bytes / 1024 ** 3:.2f} GB"


def render_kpi_row(report_data: dict[str, Any]) -> None:
    """Vier Kennzahlen-Karten oben auf der Übersichts-Page."""
    summary = report_data.get("summary", {})
    cols = st.columns(4)
    cols[0].metric(
        label="Gesamt-Queries",
        value=f"{summary.get('total_queries', 0):,}".replace(",", "."),
        help="Alle Anfragen im Analysezeitraum (DNS-Lookups, HTTP-Requests etc.) — KI- und Nicht-KI-Traffic zusammen.",
    )
    cols[1].metric(
        label="AI-Queries",
        value=f"{summary.get('ai_queries', 0):,}".replace(",", "."),
        delta=f"{summary.get('ai_query_ratio', 0) * 100:.1f}% Anteil",
        delta_color="off",
        help="Anfragen an bekannte KI-Services aus der AI Endpoint Database. Der Anteil zeigt die Schatten-KI-Dichte.",
    )
    cols[2].metric(
        label="Unique Clients",
        value=summary.get("unique_clients", 0),
        delta=f"{summary.get('unique_ai_services', 0)} AI-Dienste",
        delta_color="off",
        help="Anzahl pseudonymisierter Clients (IP-Hashes). Die Sub-Metrik zeigt wie viele verschiedene KI-Dienste insgesamt erkannt wurden.",
    )
    cols[3].metric(
        label="Document-Uploads",
        value=summary.get("upload_events_total", 0),
        delta=_format_bytes(summary.get("total_bytes_uploaded", 0)),
        delta_color="off",
        help=term_help("upload_threshold"),
    )
