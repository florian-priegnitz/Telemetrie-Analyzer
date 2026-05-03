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
])
def test_critical_existing_entries_preserved(db: AIEndpointDatabase, service_name, expected_risk):
    """Bulk-Import darf existierende Einträge nicht verfälschen."""
    match = [e for e in db.endpoints if e.service == service_name]
    assert len(match) == 1, f"{service_name} nicht gefunden"
    assert match[0].risk_level == expected_risk


def test_v2_3_0_alias_mergers(db: AIEndpointDatabase):
    """v2.3.0 (#88): Codex/DALL-E unter OpenAI ChatGPT, Duet unter Google Gemini."""
    chatgpt = next((e for e in db.endpoints if e.service == "OpenAI ChatGPT"), None)
    assert chatgpt is not None
    assert "Codex" in chatgpt.aliases
    assert "DALL-E" in chatgpt.aliases

    gemini = next((e for e in db.endpoints if e.service == "Google Gemini"), None)
    assert gemini is not None
    assert "Duet" in gemini.aliases


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


# ---------------------------------------------------------------------------
# v2.1 Refresh (2026-04): neue Kategorien HR/Browser-Ext/Customer-Support
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("category,min_count", [
    ("hr_recruiting_ai", 5),
    ("browser_extension_ai", 5),
    ("customer_support_ai", 5),
])
def test_v21_new_categories_populated(db: AIEndpointDatabase, category, min_count):
    """v2.1-Refresh: neue Kategorien haben mindestens je min_count Services."""
    counts = Counter(ep.category for ep in db.endpoints)
    assert counts[category] >= min_count, (
        f"Kategorie {category} hat nur {counts[category]} Services, Minimum {min_count}"
    )


@pytest.mark.parametrize("service_name", [
    "HireVue",
    "Merlin AI",
    "Intercom Fin",
])
def test_v21_refresh_keystone_entries(db: AIEndpointDatabase, service_name):
    """v2.1-Refresh: Keystone-Einträge pro neuer Kategorie vorhanden."""
    assert any(e.service == service_name for e in db.endpoints), (
        f"{service_name} fehlt — refresh_endpoints.py lief nicht"
    )


# ---------------------------------------------------------------------------
# W4-C (#16) — Schema-Edge-Cases
# ---------------------------------------------------------------------------
def test_no_duplicate_aliases_across_services(db: AIEndpointDatabase):
    """Ein Alias darf nur einem Service gehören — sonst ambiger lookup_alias."""
    import json

    data = json.loads(DB_PATH.read_text(encoding="utf-8"))
    alias_to_services: dict[str, list[str]] = defaultdict(list)
    for ep in data["endpoints"]:
        for alias in ep.get("aliases", []) or []:
            alias_to_services[alias.lower()].append(ep["service"])
    duplicates = {a: svcs for a, svcs in alias_to_services.items() if len(svcs) > 1}
    assert not duplicates, (
        f"Aliases treten bei mehreren Services auf (ambig für lookup_alias): {duplicates}"
    )


def test_ip_ranges_are_either_ipv4_or_ipv6(db: AIEndpointDatabase):
    """Jedes CIDR muss reines IPv4 oder reines IPv6 sein (keine Mischform)."""
    import ipaddress

    for ep in db.endpoints:
        for cidr in ep.ip_ranges:
            net = ipaddress.ip_network(cidr, strict=False)
            assert isinstance(net, (ipaddress.IPv4Network, ipaddress.IPv6Network)), (
                f"{ep.service}: {cidr} ist weder v4 noch v6 — {type(net)}"
            )


def test_category_descriptions_non_empty(db: AIEndpointDatabase):
    """Jede Kategorie hat eine Beschreibung ≥ 10 Zeichen (kein leerer Stub)."""
    import json

    data = json.loads(DB_PATH.read_text(encoding="utf-8"))
    short = {k: v for k, v in data.get("categories", {}).items()
             if len(v.strip()) < 10}
    assert not short, f"Kategorie-Beschreibungen zu kurz (<10 chars): {short}"


def test_all_categories_have_at_least_one_endpoint(db: AIEndpointDatabase):
    """Deklarierte Kategorie muss tatsächlich verwendet werden — sonst tote Kategorie."""
    import json

    data = json.loads(DB_PATH.read_text(encoding="utf-8"))
    declared = set(data["categories"].keys())
    used = {ep.category for ep in db.endpoints}
    unused = declared - used
    assert not unused, f"Kategorien deklariert aber ungenutzt: {unused}"


def test_detection_confidence_values_in_enum(db: AIEndpointDatabase):
    """v2-Feld detection_confidence: nur {high, medium, low} erlaubt (Schema-Enum)."""
    allowed = {"high", "medium", "low"}
    for ep in db.endpoints:
        assert ep.detection_confidence in allowed, (
            f"{ep.service}: ungültiges detection_confidence={ep.detection_confidence!r}"
        )


def test_domains_list_never_empty(db: AIEndpointDatabase):
    """Schema verlangt minItems=1 — sicherstellen, dass kein Endpoint durchrutscht."""
    for ep in db.endpoints:
        assert len(ep.domains) >= 1, f"{ep.service}: domains-Liste ist leer"
        assert all(d.strip() for d in ep.domains), f"{ep.service}: leerer Domain-Eintrag"


def test_domains_lowercase_and_no_trailing_dot(db: AIEndpointDatabase):
    """Domain-Konvention: lowercase, kein trailing dot (konsistent mit Parser-Output)."""
    for ep in db.endpoints:
        for d in ep.domains:
            assert d == d.lower(), f"{ep.service}: {d!r} nicht lowercase"
            assert not d.endswith("."), f"{ep.service}: {d!r} hat trailing dot"


def test_sni_patterns_contain_wildcards(db: AIEndpointDatabase):
    """v2 sni_patterns sind Wildcard-Patterns — reine exakte Strings gehören zu domains."""
    for ep in db.endpoints:
        for pattern in ep.sni_patterns:
            assert "*" in pattern or "?" in pattern, (
                f"{ep.service}: sni_pattern {pattern!r} ohne Wildcard — gehört in domains"
            )


def test_providers_non_empty(db: AIEndpointDatabase):
    """Jeder Endpoint hat einen provider — wichtig für das Finding-Reporting."""
    for ep in db.endpoints:
        assert ep.provider and ep.provider.strip(), (
            f"{ep.service}: provider ist leer"
        )
