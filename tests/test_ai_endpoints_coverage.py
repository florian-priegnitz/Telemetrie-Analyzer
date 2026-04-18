"""Integritätstests für die AI Endpoint Database (E1-8).

Strukturelle Qualitätssicherung: keine Duplikate, Schema-Konformität,
alphabetische Sortierung, nur erlaubte Werte für Kategorien/Risk-Level.
Werden mit jedem neuen Endpoint-Bulk-Import automatisch geprüft.
"""

from collections import Counter, defaultdict
from pathlib import Path

import pytest

from src.database.ai_endpoints import AIEndpointDatabase


DB_PATH = Path(__file__).parent.parent / "data" / "ai_endpoints.json"


@pytest.fixture(scope="module")
def db() -> AIEndpointDatabase:
    return AIEndpointDatabase(validate=True)


# ---------------------------------------------------------------------------
# Integrität: Duplikate, Sortierung, Schema-Konformität
# ---------------------------------------------------------------------------
def test_no_duplicate_domains(db: AIEndpointDatabase):
    """Jede Domain erscheint in höchstens einem Service."""
    domain_map = defaultdict(list)
    for ep in db.endpoints:
        for d in ep.domains:
            domain_map[d.lower()].append(ep.service)
    duplicates = {d: services for d, services in domain_map.items() if len(services) > 1}
    assert not duplicates, f"Duplikate: {duplicates}"


def test_no_duplicate_services(db: AIEndpointDatabase):
    """Kein Service-Name kommt zweimal vor."""
    services = [ep.service for ep in db.endpoints]
    counts = Counter(services)
    dupes = [s for s, n in counts.items() if n > 1]
    assert not dupes, f"Doppelte Services: {dupes}"


def test_services_sorted_case_insensitive(db: AIEndpointDatabase):
    """Einträge alphabetisch sortiert (case-insensitive) — Wartbarkeit."""
    services = [ep.service for ep in db.endpoints]
    expected = sorted(services, key=str.lower)
    if services != expected:
        # Erste Abweichung anzeigen
        for i, (a, b) in enumerate(zip(services, expected)):
            if a != b:
                pytest.fail(
                    f"Sortierung verletzt bei Position {i}: "
                    f"actual={services[max(0,i-1):i+2]}, expected={expected[max(0,i-1):i+2]}"
                )


def test_valid_risk_levels(db: AIEndpointDatabase):
    """Nur Schema-konforme Risk-Levels."""
    allowed = {"critical", "high", "medium", "low"}
    for ep in db.endpoints:
        assert ep.risk_level in allowed, f"{ep.service}: ungültiges risk_level={ep.risk_level}"


def test_valid_categories(db: AIEndpointDatabase):
    """Alle verwendeten Kategorien sind im categories-Block definiert."""
    import json
    data = json.loads(DB_PATH.read_text(encoding="utf-8"))
    declared = set(data["categories"].keys())
    used = {ep.category for ep in db.endpoints}
    missing = used - declared
    assert not missing, f"Verwendete, aber undeklarierte Kategorien: {missing}"


def test_domains_lowercase_in_index(db: AIEndpointDatabase):
    """Der Domain-Index normalisiert auf lowercase (für case-insensitive Lookup)."""
    for d in db.domains:
        assert d == d.lower(), f"Nicht-normalisiert: {d}"


# ---------------------------------------------------------------------------
# Mindestmengen pro Kategorie (E1-2-Akzeptanzkriterium)
# ---------------------------------------------------------------------------
CATEGORY_MINIMA = {
    "llm_chatbot": 15,
    "code_assistant": 12,
    "meeting_ai": 8,
    "presentation_ai": 6,
    "video_ai": 8,
    "image_generation": 12,
    "writing_assistant": 6,
    "data_analysis_ai": 5,
    "ai_agent": 6,
    "enterprise_embedded": 8,
}


def test_category_minima(db: AIEndpointDatabase):
    """Jede Kategorie hat die geforderte Mindestanzahl von Services."""
    counts = Counter(ep.category for ep in db.endpoints)
    for cat, minimum in CATEGORY_MINIMA.items():
        assert counts[cat] >= minimum, (
            f"Kategorie {cat} hat nur {counts[cat]} Services, Minimum {minimum}"
        )


def test_total_endpoint_count(db: AIEndpointDatabase):
    """Mindestanzahl Endpoints insgesamt (E1-2: ≥150)."""
    assert len(db.endpoints) >= 150, f"Nur {len(db.endpoints)} Endpoints, Minimum 150"


# ---------------------------------------------------------------------------
# Sicherstellen, dass existierende kritische Einträge erhalten bleiben
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("service_name,expected_risk", [
    ("OpenAI ChatGPT", "high"),
    ("Anthropic Claude", "high"),
    ("GitHub Copilot", "critical"),
    ("Cursor", "critical"),
    ("DeepSeek", "critical"),
    ("OpenAI Codex / GPT API", "critical"),
])
def test_critical_existing_entries_preserved(db: AIEndpointDatabase, service_name, expected_risk):
    """Bulk-Import darf existierende Einträge nicht verfälschen."""
    match = [e for e in db.endpoints if e.service == service_name]
    assert len(match) == 1, f"{service_name} nicht gefunden"
    assert match[0].risk_level == expected_risk


# ---------------------------------------------------------------------------
# CIDR-Validität (falls ip_ranges gesetzt)
# ---------------------------------------------------------------------------
def test_ip_ranges_are_valid_cidr(db: AIEndpointDatabase):
    """Alle ip_ranges müssen gültige CIDR-Notation haben."""
    import ipaddress
    for ep in db.endpoints:
        for cidr in ep.ip_ranges:
            try:
                ipaddress.ip_network(cidr, strict=False)
            except ValueError as exc:
                pytest.fail(f"{ep.service}: ungültiges CIDR {cidr!r} — {exc}")
