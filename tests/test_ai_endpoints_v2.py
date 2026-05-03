"""Tests für Schema v2 der AI Endpoint Database (E1-1).

Neue Felder: aliases, ip_ranges, sni_patterns, detection_confidence,
last_verified, source. Backward-kompatibel zu v1.
"""

import json
from pathlib import Path

import pytest

from src.database.ai_endpoints import AIEndpoint, AIEndpointDatabase


# ---------------------------------------------------------------------------
# Schema-Validierung
# ---------------------------------------------------------------------------
def test_default_db_passes_schema_validation():
    """Die ausgelieferte ai_endpoints.json muss schema-valide sein."""
    db = AIEndpointDatabase(validate=True)
    assert len(db.endpoints) > 0


def test_schema_file_exists():
    """ai_endpoints_schema.json existiert neben ai_endpoints.json."""
    schema = Path(__file__).parent.parent / "data" / "ai_endpoints_schema.json"
    assert schema.exists(), f"Schema fehlt: {schema}"
    with open(schema) as f:
        data = json.load(f)
    assert data["$schema"].startswith("https://json-schema.org/")


def test_schema_rejects_invalid_risk_level(tmp_path: Path):
    """Ein DB mit unbekanntem risk_level muss bei validate=True rejected werden."""
    bad_db = tmp_path / "bad.json"
    bad_db.write_text(json.dumps({
        "version": "1.0.0",
        "endpoints": [{
            "service": "Test", "provider": "Test", "category": "llm_chatbot",
            "risk_level": "ultra-critical",  # ungültig
            "domains": ["test.com"],
        }]
    }), encoding="utf-8")
    # Schema liegt im Projekt — wir müssen es mitkopieren oder den Pfad angeben
    schema_src = Path(__file__).parent.parent / "data" / "ai_endpoints_schema.json"
    (tmp_path / "ai_endpoints_schema.json").write_text(
        schema_src.read_text(encoding="utf-8"), encoding="utf-8"
    )
    with pytest.raises(ValueError, match="Schema"):
        AIEndpointDatabase(db_path=bad_db, validate=True)


def test_schema_accepts_v1_entries_without_v2_fields(tmp_path: Path):
    """v1-Einträge ohne optionale v2-Felder müssen mit Defaults geladen werden.

    Nutzt synthetische DB in tmp_path (statt der Live-DB), damit der Test
    unabhaengig von DB-Bumps weiterlaeuft. Vor v2.3.0 verwies dieser Test
    auf den Codex-Eintrag in der Live-DB; seit dem Codex-Merge (Issue #88)
    pruefen wir das Schema-Verhalten kontrolliert auf einer Mini-DB.
    """
    db_json = tmp_path / "db.json"
    db_json.write_text(json.dumps({
        "version": "1.0.0",
        "endpoints": [{
            "service": "MinimalV1",
            "provider": "P",
            "category": "llm_chatbot",
            "risk_level": "high",
            "domains": ["minimal-v1.example.test"],
            "description": "v1-style entry, no v2 fields",
        }],
    }), encoding="utf-8")
    schema_src = Path(__file__).parent.parent / "data" / "ai_endpoints_schema.json"
    (tmp_path / "ai_endpoints_schema.json").write_text(
        schema_src.read_text(encoding="utf-8"), encoding="utf-8"
    )
    db = AIEndpointDatabase(db_path=db_json, validate=True)
    ep = db.lookup("minimal-v1.example.test")
    assert ep is not None
    assert ep.aliases == ()
    assert ep.ip_ranges == ()
    assert ep.sni_patterns == ()
    assert ep.detection_confidence == "high"  # Default
    assert ep.source == "manual"  # Default für Einträge ohne expliziten source


# ---------------------------------------------------------------------------
# Alias-Matching
# ---------------------------------------------------------------------------
def test_alias_lookup(tmp_path: Path):
    """Alias-Lookup findet Service über alternative Namen."""
    db_json = tmp_path / "db.json"
    db_json.write_text(json.dumps({
        "version": "2.0.0",
        "endpoints": [{
            "service": "OpenAI ChatGPT", "provider": "OpenAI",
            "category": "llm_chatbot", "risk_level": "high",
            "domains": ["chat.openai.com"],
            "aliases": ["ChatGPT", "GPT", "gpt-4"],
        }]
    }), encoding="utf-8")
    db = AIEndpointDatabase(db_path=db_json)

    assert db.lookup_alias("ChatGPT") is not None
    assert db.lookup_alias("chatgpt").service == "OpenAI ChatGPT"  # case-insensitive
    assert db.lookup_alias("gpt-4") is not None
    assert db.lookup_alias("unknown-ai") is None


# ---------------------------------------------------------------------------
# SNI-Pattern-Matching (Wildcard-Fallback in lookup_subdomain)
# ---------------------------------------------------------------------------
def test_sni_pattern_matches_as_subdomain_fallback(tmp_path: Path):
    """Wenn Domain nicht direkt bekannt, greift sni_patterns (Wildcard)."""
    db_json = tmp_path / "db.json"
    db_json.write_text(json.dumps({
        "version": "2.0.0",
        "endpoints": [{
            "service": "OpenAI", "provider": "OpenAI",
            "category": "llm_chatbot", "risk_level": "high",
            "domains": ["api.openai.com"],  # chat.openai.com NICHT gelistet
            "sni_patterns": ["*.openai.com"],
        }]
    }), encoding="utf-8")
    db = AIEndpointDatabase(db_path=db_json)

    # Direct-Match trotz Wildcard verfügbar
    assert db.lookup_subdomain("api.openai.com") is not None
    # SNI-Fallback: chat.openai.com matcht *.openai.com
    result = db.lookup_subdomain("chat.openai.com")
    assert result is not None, "SNI-Wildcard-Fallback greift nicht"
    assert result.service == "OpenAI"


# ---------------------------------------------------------------------------
# IP-Range-Lookup (für Parser ohne Domain, z.B. VPC Flow Logs)
# ---------------------------------------------------------------------------
def test_ip_range_lookup_ipv4(tmp_path: Path):
    """IP-Lookup matcht eine Adresse gegen CIDR-Ranges."""
    db_json = tmp_path / "db.json"
    db_json.write_text(json.dumps({
        "version": "2.0.0",
        "endpoints": [{
            "service": "Anthropic", "provider": "Anthropic",
            "category": "llm_chatbot", "risk_level": "high",
            "domains": ["api.anthropic.com"],
            "ip_ranges": ["160.79.104.0/23", "2607:6bc0::/32"],
        }]
    }), encoding="utf-8")
    db = AIEndpointDatabase(db_path=db_json)

    assert db.lookup_ip("160.79.104.5") is not None
    assert db.lookup_ip("160.79.105.200") is not None  # noch im /23
    assert db.lookup_ip("8.8.8.8") is None  # Google DNS, nicht AI
    assert db.lookup_ip("invalid-ip") is None  # Parser-Fehler


def test_ip_range_lookup_ipv6(tmp_path: Path):
    """IPv6 wird korrekt gegen IPv6-CIDR gematcht."""
    db_json = tmp_path / "db.json"
    db_json.write_text(json.dumps({
        "version": "2.0.0",
        "endpoints": [{
            "service": "Anthropic", "provider": "Anthropic",
            "category": "llm_chatbot", "risk_level": "high",
            "domains": ["api.anthropic.com"],
            "ip_ranges": ["2607:6bc0::/32"],
        }]
    }), encoding="utf-8")
    db = AIEndpointDatabase(db_path=db_json)

    assert db.lookup_ip("2607:6bc0::1") is not None


# ---------------------------------------------------------------------------
# v2-Metadaten-Felder werden korrekt geladen
# ---------------------------------------------------------------------------
def test_v2_metadata_loaded(tmp_path: Path):
    """Alle v2-Felder erreichen das AIEndpoint-Dataclass."""
    db_json = tmp_path / "db.json"
    db_json.write_text(json.dumps({
        "version": "2.0.0",
        "endpoints": [{
            "service": "Test", "provider": "Test",
            "category": "llm_chatbot", "risk_level": "medium",
            "domains": ["test.com"],
            "aliases": ["T"],
            "ip_ranges": ["10.0.0.0/8"],
            "sni_patterns": ["*.test.com"],
            "detection_confidence": "low",
            "last_verified": "2026-04-18",
            "source": "awesome-ai-tools",
        }]
    }), encoding="utf-8")
    db = AIEndpointDatabase(db_path=db_json)

    ep: AIEndpoint = db.endpoints[0]
    assert ep.aliases == ("T",)
    assert ep.ip_ranges == ("10.0.0.0/8",)
    assert ep.sni_patterns == ("*.test.com",)
    assert ep.detection_confidence == "low"
    assert ep.last_verified == "2026-04-18"
    assert ep.source == "awesome-ai-tools"
