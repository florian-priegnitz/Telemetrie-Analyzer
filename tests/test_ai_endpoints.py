"""Tests für die AI Endpoint Database."""

from src.database.ai_endpoints import AIEndpointDatabase


def test_load_default_database():
    db = AIEndpointDatabase()
    assert len(db.endpoints) > 0
    assert len(db.domains) > 0


def test_lookup_exact_match():
    db = AIEndpointDatabase()
    result = db.lookup("chat.openai.com")
    assert result is not None
    assert result.provider == "OpenAI"
    assert result.risk_level == "high"


def test_lookup_case_insensitive():
    db = AIEndpointDatabase()
    result = db.lookup("Chat.OpenAI.com")
    assert result is not None
    assert result.service == "OpenAI ChatGPT"


def test_lookup_unknown_domain():
    db = AIEndpointDatabase()
    assert db.lookup("example.com") is None


def test_lookup_subdomain():
    db = AIEndpointDatabase()
    result = db.lookup_subdomain("cdn.chat.openai.com")
    assert result is not None
    assert result.provider == "OpenAI"


def test_lookup_subdomain_trailing_dot():
    db = AIEndpointDatabase()
    result = db.lookup_subdomain("api.anthropic.com.")
    assert result is not None
    assert result.provider == "Anthropic"


def test_by_category():
    db = AIEndpointDatabase()
    code_assistants = db.by_category("code_assistant")
    assert len(code_assistants) >= 3  # Copilot, Cursor, Replit
    assert all(e.category == "code_assistant" for e in code_assistants)


def test_by_risk_level():
    db = AIEndpointDatabase()
    critical = db.by_risk_level("critical")
    assert len(critical) >= 1
    assert all(e.risk_level == "critical" for e in critical)


def test_deepseek_is_critical():
    """DeepSeek sollte als critical eingestuft sein (Drittland-Transfer)."""
    db = AIEndpointDatabase()
    result = db.lookup("chat.deepseek.com")
    assert result is not None
    assert result.risk_level == "critical"
