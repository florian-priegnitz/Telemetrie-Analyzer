"""Tests für das opt-in Squid-Username-Parsing (Issue #22).

Double-Opt-in Privacy-Gating:
- Parser-Flag ``parse_username`` (Default False) muss aktiv gesetzt werden.
- Selbst bei aktivem Flag ist der Raw-Username nie im DataFrame sichtbar,
  nur der HMAC-Pseudonym in Spalte ``user_pseudonym``.
- AD-Down-Level- und UPN-Formate werden auf denselben Hash normalisiert.
"""

import tempfile
from pathlib import Path

from src.parsers.squid import SquidParser, parse_squid_log
from src.privacy.pseudonymizer import Pseudonymizer, normalize_username

SAMPLE_WITH_USERNAMES = (
    "1709971200.000 100 192.168.1.10 TCP_MISS/200 512 GET "
    "https://api.openai.com/v1 jdoe HIER_DIRECT/1.2.3.4 application/json\n"
    "1709971210.000 80 192.168.1.11 TCP_MISS/200 900 POST "
    "https://claude.ai/api alice HIER_DIRECT/1.2.3.5 application/json\n"
    "1709971220.000 70 192.168.1.12 TCP_MISS/200 300 GET "
    "https://example.com/ - HIER_DIRECT/1.2.3.6 text/html\n"
)


def _write_temp_log(content: str) -> Path:
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False, encoding="utf-8")
    f.write(content)
    f.close()
    return Path(f.name)


def test_default_off_no_user_column():
    """Privacy-by-Default: ohne Flag gibt es keine user_pseudonym-Spalte."""
    path = _write_temp_log(SAMPLE_WITH_USERNAMES)
    df = parse_squid_log(path, pseudonymizer=Pseudonymizer(key=b"k"))
    assert "user_pseudonym" not in df.columns


def test_opt_in_adds_user_column():
    path = _write_temp_log(SAMPLE_WITH_USERNAMES)
    df = parse_squid_log(
        path, pseudonymizer=Pseudonymizer(key=b"k"), parse_username=True,
    )
    assert "user_pseudonym" in df.columns
    assert len(df) == 3


def test_opt_in_pseudonyms_prefixed():
    path = _write_temp_log(SAMPLE_WITH_USERNAMES)
    df = parse_squid_log(
        path, pseudonymizer=Pseudonymizer(key=b"k"), parse_username=True,
    )
    pseudonyms = [u for u in df["user_pseudonym"] if u]
    assert len(pseudonyms) == 2
    assert all(p.startswith("user_") for p in pseudonyms)


def test_dash_rfc931_yields_empty_pseudonym():
    """Squid ``-`` markiert 'kein Username' — muss leer bleiben."""
    path = _write_temp_log(SAMPLE_WITH_USERNAMES)
    df = parse_squid_log(
        path, pseudonymizer=Pseudonymizer(key=b"k"), parse_username=True,
    )
    empty_rows = df[df["user_pseudonym"] == ""]
    assert len(empty_rows) == 1
    assert empty_rows.iloc[0]["domain"] == "example.com"


def test_raw_username_never_in_dataframe():
    """Raw-Username darf in keinem Feld leaken — nur der Hash."""
    path = _write_temp_log(SAMPLE_WITH_USERNAMES)
    df = parse_squid_log(
        path, pseudonymizer=Pseudonymizer(key=b"k"), parse_username=True,
    )
    as_str = df.to_json()
    for raw in ("jdoe", "alice"):
        assert raw not in as_str, f"Klartext-Username {raw!r} im DataFrame"


def test_same_user_same_pseudonym_different_salt():
    """Deterministisch bei gleichem Salt, unterschiedlich bei anderem Salt."""
    path = _write_temp_log(SAMPLE_WITH_USERNAMES)
    df_a = parse_squid_log(
        path, pseudonymizer=Pseudonymizer(key=b"salt-a"), parse_username=True,
    )
    df_b = parse_squid_log(
        path, pseudonymizer=Pseudonymizer(key=b"salt-b"), parse_username=True,
    )
    jdoe_a = df_a.iloc[0]["user_pseudonym"]
    jdoe_b = df_b.iloc[0]["user_pseudonym"]
    assert jdoe_a and jdoe_b
    assert jdoe_a != jdoe_b


def test_ad_and_upn_and_plain_collapse_to_same_pseudonym():
    """``DOMAIN\\jdoe``, ``jdoe@corp.tld`` und ``jdoe`` → identisches Pseudonym."""
    p = Pseudonymizer(key=b"k")
    assert (
        p.pseudonymize_user("CORP\\jdoe")
        == p.pseudonymize_user("jdoe@corp.tld")
        == p.pseudonymize_user("jdoe")
        == p.pseudonymize_user("JDoe")  # Case-insensitive
    )


def test_ldap_cn_dn_stripped():
    p = Pseudonymizer(key=b"k")
    assert p.pseudonymize_user("CN=jdoe,OU=Sales,DC=corp,DC=tld") == p.pseudonymize_user("jdoe")


def test_empty_username_returns_empty():
    p = Pseudonymizer(key=b"k")
    assert p.pseudonymize_user("") == ""
    assert p.pseudonymize_user("   ") == ""
    assert p.pseudonymize_user("\\") == ""  # nur Trennzeichen


def test_normalize_username_helpers():
    assert normalize_username("CORP\\jdoe") == "jdoe"
    assert normalize_username("jdoe@corp.tld") == "jdoe"
    assert normalize_username("jdoe") == "jdoe"
    assert normalize_username("") == ""
    assert normalize_username("  JDOE  ") == "jdoe"


def test_parser_class_passes_flag_through():
    path = _write_temp_log(SAMPLE_WITH_USERNAMES)
    parser = SquidParser(
        pseudonymizer=Pseudonymizer(key=b"k"), parse_username=True,
    )
    df = parser.parse(path)
    assert "user_pseudonym" in df.columns


def test_parser_class_default_off():
    path = _write_temp_log(SAMPLE_WITH_USERNAMES)
    parser = SquidParser(pseudonymizer=Pseudonymizer(key=b"k"))
    df = parser.parse(path)
    assert "user_pseudonym" not in df.columns


def test_empty_log_with_username_flag():
    path = _write_temp_log("")
    df = parse_squid_log(
        path, pseudonymizer=Pseudonymizer(key=b"k"), parse_username=True,
    )
    assert len(df) == 0
    assert "user_pseudonym" in df.columns


# --- UI-Helper: user_aggregation + masking ---------------------------------

def test_build_user_aggregation_disabled_without_column():
    """Ohne ``user_pseudonym``-Spalte: disabled + leere Aggregation."""
    from src.ui.state import _build_user_aggregation

    path = _write_temp_log(SAMPLE_WITH_USERNAMES)
    df = parse_squid_log(path, pseudonymizer=Pseudonymizer(key=b"k"))  # Flag off
    agg = _build_user_aggregation(df, salt="test-salt", redacted=False)
    assert agg["enabled"] is False
    assert agg["per_client"] == {}
    assert agg["unique_users"] == 0


def test_build_user_aggregation_enabled_with_users():
    from src.ui.state import _build_user_aggregation

    path = _write_temp_log(SAMPLE_WITH_USERNAMES)
    df = parse_squid_log(
        path, pseudonymizer=Pseudonymizer(key=b"k"), parse_username=True,
    )
    agg = _build_user_aggregation(df, salt="test-salt", redacted=False)
    assert agg["enabled"] is True
    assert agg["unique_users"] == 2  # jdoe + alice (dash=kein user)
    # Clients werden über pseudonymize_client normalisiert — Mapping muss Usernamen pro Client liefern.
    assert sum(len(users) for users in agg["per_client"].values()) == 2


def test_build_user_aggregation_suppressed_when_redacted():
    """Bei hohem Re-ID-Risiko: Aggregation komplett unterdrückt (DSGVO Art. 25)."""
    from src.ui.state import _build_user_aggregation

    path = _write_temp_log(SAMPLE_WITH_USERNAMES)
    df = parse_squid_log(
        path, pseudonymizer=Pseudonymizer(key=b"k"), parse_username=True,
    )
    agg = _build_user_aggregation(df, salt="test-salt", redacted=True)
    assert agg["enabled"] is False
    assert agg["per_client"] == {}


def test_mask_user_pseudonym():
    from src.ui.pages.users_patterns import _mask_user_pseudonym

    assert _mask_user_pseudonym("user_a3b2c1d4") == "user_a***"
    assert _mask_user_pseudonym("user_") == "user_***"
    assert _mask_user_pseudonym("") == ""
    # Fremdes Pseudonym-Format bleibt unverändert
    assert _mask_user_pseudonym("ip_a3b2") == "ip_a3b2"
