"""Tests fuer src/ui/glossary.py + page_intro-Konsistenz (#76, Sprint 11)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from src.ui.glossary import GLOSSARY, GlossaryTerm, get

REPO_ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = REPO_ROOT / "src" / "ui" / "pages"


def test_glossary_has_at_least_20_entries():
    assert len(GLOSSARY) >= 20, (
        f"Glossar muss min. 20 Begriffe haben, hat aktuell {len(GLOSSARY)}"
    )


def test_short_definitions_are_tooltip_sized():
    """`short` muss in einen Streamlit-help=-Tooltip passen (≤140 Zeichen)."""
    too_long: list[tuple[str, int]] = []
    for key, term in GLOSSARY.items():
        assert isinstance(term, GlossaryTerm), f"{key} ist kein GlossaryTerm"
        if len(term.short) > 140:
            too_long.append((key, len(term.short)))
    assert not too_long, (
        "Folgende `short`-Texte sind > 140 Zeichen: "
        + ", ".join(f"{k} ({n})" for k, n in too_long)
    )


def test_see_also_references_are_valid():
    """Jeder `see_also`-Verweis muss ein existierender Glossar-Key sein."""
    invalid: list[tuple[str, str]] = []
    for key, term in GLOSSARY.items():
        for ref in term.see_also:
            if ref not in GLOSSARY:
                invalid.append((key, ref))
    assert not invalid, (
        "Ungueltige see_also-Referenzen: "
        + ", ".join(f"{src} -> {dst}" for src, dst in invalid)
    )


def test_all_page_intro_keys_exist_in_glossary():
    """Alle in `key_terms=(...)`-Argumenten referenzierten Keys muessen im
    Glossar liegen — sonst rendert der Mini-Glossar-Block nichts.

    Wir scannen nicht den vollstaendigen `page_intro(...)`-Aufruf (verschachtelte
    Parens machen Regex unzuverlaessig), sondern direkt das Tuple-Argument
    `key_terms=(...)`.
    """
    key_terms_pattern = re.compile(r"key_terms\s*=\s*\(([^)]*)\)", re.DOTALL)
    referenced: set[str] = set()
    for page_file in PAGES_DIR.glob("*.py"):
        text = page_file.read_text(encoding="utf-8")
        for match in key_terms_pattern.finditer(text):
            inner = match.group(1)
            for raw in inner.split(","):
                key = raw.strip().strip('"').strip("'")
                if key:
                    referenced.add(key)

    missing = referenced - set(GLOSSARY.keys())
    assert not missing, (
        f"Folgende key_terms in page_intro(...)-Aufrufen fehlen im Glossar: {sorted(missing)}"
    )
    # Sanity: mindestens 7 referenzierte Keys ueber alle Pages
    assert len(referenced) >= 7, (
        f"Erwartet >=7 referenzierte Glossar-Keys (eigentlich >=15), gefunden {len(referenced)}"
    )


def test_get_returns_none_for_unknown_key():
    assert get("does_not_exist") is None


@pytest.mark.parametrize("key", list(GLOSSARY.keys()))
def test_each_term_has_label_and_long(key):
    term = GLOSSARY[key]
    assert term.label, f"{key}: leeres Label"
    assert term.long, f"{key}: leeres long"
    assert term.short, f"{key}: leeres short"
