"""Tests für das Privacy-Modul (Pseudonymisierung)."""

from src.privacy.pseudonymizer import Pseudonymizer


def test_deterministic_output():
    """Gleicher Input + gleicher Key = gleicher Output."""
    key = b"test-key-12345"
    p = Pseudonymizer(key=key)
    assert p.pseudonymize_ip("192.168.1.1") == p.pseudonymize_ip("192.168.1.1")


def test_different_ips_different_output():
    p = Pseudonymizer(key=b"test")
    assert p.pseudonymize_ip("192.168.1.1") != p.pseudonymize_ip("192.168.1.2")


def test_different_keys_different_output():
    p1 = Pseudonymizer(key=b"key1")
    p2 = Pseudonymizer(key=b"key2")
    assert p1.pseudonymize_ip("192.168.1.1") != p2.pseudonymize_ip("192.168.1.1")


def test_ip_prefix():
    p = Pseudonymizer(key=b"test")
    result = p.pseudonymize_ip("10.0.0.1")
    assert result.startswith("ip_")
    assert len(result) == 11  # "ip_" + 8 hex chars


def test_user_prefix():
    p = Pseudonymizer(key=b"test")
    result = p.pseudonymize_user("john.doe")
    assert result.startswith("user_")


def test_no_plaintext_in_output():
    """Sicherstellen, dass keine Klartextdaten im Pseudonym enthalten sind."""
    p = Pseudonymizer(key=b"test")
    result = p.pseudonymize_ip("192.168.1.100")
    assert "192" not in result
    assert "168" not in result


def test_auto_key_generation():
    """Ohne expliziten Key wird ein zufälliger generiert."""
    p1 = Pseudonymizer()
    p2 = Pseudonymizer()
    # Verschiedene Instanzen ohne Key sollten verschiedene Keys haben
    assert p1.key != p2.key
