"""UI-Komponente: AI-Endpoint-DB-Stand sichtbar machen (#77).

Zeigt Version, last_updated, Anzahl Endpoints/Provider/Kategorien
sowie ein Frische-Signal (gruen/gelb/rot) basierend auf dem Alter
der DB. Wird auf Settings (voll) und Overview (kompakt) eingehaengt.
"""

from __future__ import annotations

from collections import Counter
from datetime import date, datetime

import streamlit as st

from src.database.ai_endpoints import AIEndpointDatabase

# Schwellen fuer Frische-Signale (Tage seit last_updated).
FRESHNESS_FRESH_DAYS = 35
FRESHNESS_AGING_DAYS = 70


def _parse_date(raw: str) -> date | None:
    if not raw:
        return None
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        return None


def _freshness_signal(last_updated: str) -> tuple[str, str, int | None]:
    """Liefert (Emoji, Label, Tage seit Update) basierend auf Alter."""
    parsed = _parse_date(last_updated)
    if parsed is None:
        return "❓", "Stand unbekannt", None
    age = (date.today() - parsed).days
    if age <= FRESHNESS_FRESH_DAYS:
        return "🟢", "Aktuell", age
    if age <= FRESHNESS_AGING_DAYS:
        return "🟡", "Review fällig", age
    return "🔴", "Veraltet", age


def _collect_stats(db: AIEndpointDatabase) -> dict[str, object]:
    endpoints = db.endpoints
    providers = Counter(e.provider for e in endpoints)
    categories = Counter(e.category for e in endpoints)
    risk_levels = Counter(e.risk_level for e in endpoints)
    return {
        "endpoint_count": len(endpoints),
        "provider_count": len(providers),
        "category_count": len(categories),
        "risk_levels": dict(risk_levels),
        "top_categories": providers.most_common(5),
    }


def render_db_status(*, compact: bool = False) -> None:
    """Rendert einen DB-Stand-Block.

    Args:
        compact: Wenn True, nur eine kompakte Caption (fuer Overview-Footer).
                 Wenn False, voller Block mit Stats + Frische-Signal (fuer Settings).
    """
    db = AIEndpointDatabase()
    emoji, label, age = _freshness_signal(db.last_updated)
    age_str = f"{age} Tage" if age is not None else "—"

    if compact:
        st.caption(
            f"AI-Endpoint-DB **v{db.version}** · {len(db.endpoints)} Endpoints · "
            f"Stand {db.last_updated or '—'} ({age_str}) · {emoji} {label}"
        )
        return

    stats = _collect_stats(db)
    st.markdown("### AI-Endpoint-Datenbank")
    st.caption(
        "Datenbank der bekannten KI-Dienste, gegen die Detection läuft. Wird "
        "monatlich aktualisiert (siehe `.github/workflows/endpoint-db-update.yml`). "
        "Bei Frische-Signal 🟡/🔴 sollte ein DB-Review angestoßen werden."
    )

    cols = st.columns(4)
    cols[0].metric(
        "DB-Version",
        f"v{db.version}",
        help="Schema- und Inhalts-Version. Major-Bump bei Schema-Änderungen.",
    )
    cols[1].metric(
        "Endpoints",
        stats["endpoint_count"],
        delta=f"{stats['provider_count']} Provider",
        delta_color="off",
        help="Anzahl bekannter KI-Service-Endpunkte (Service × Provider × Domain-Set).",
    )
    cols[2].metric(
        "Kategorien",
        stats["category_count"],
        help="Anzahl unterschiedlicher AI-Kategorien (z.B. llm_chatbot, code_assistant, hr_recruiting_ai).",
    )
    cols[3].metric(
        "Letzte Aktualisierung",
        db.last_updated or "—",
        delta=f"{emoji} {label} · {age_str}",
        delta_color="off",
        help=(
            f"Frische-Signal: 🟢 ≤{FRESHNESS_FRESH_DAYS}d aktuell, "
            f"🟡 ≤{FRESHNESS_AGING_DAYS}d Review fällig, 🔴 darüber veraltet."
        ),
    )

    risk_dist = stats["risk_levels"]
    risk_str = " · ".join(
        f"{level}: **{risk_dist.get(level, 0)}**"
        for level in ("critical", "high", "medium", "low")
        if level in risk_dist
    )
    if risk_str:
        st.caption(f"Risk-Verteilung: {risk_str}")

    st.caption(
        "Coverage-Report: [`docs/AI_COVERAGE.md`](docs/AI_COVERAGE.md) — automatisch "
        "via `scripts/db_coverage_report.py` generiert."
    )


__all__ = ["render_db_status", "FRESHNESS_FRESH_DAYS", "FRESHNESS_AGING_DAYS"]
