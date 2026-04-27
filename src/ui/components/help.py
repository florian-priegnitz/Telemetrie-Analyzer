"""UI-Helper fuer Per-Page-Erklaerungen + Streamlit-Tooltipps (Issue #76).

Drei Funktionen:
- `page_intro(title, what_you_see, key_terms)` rendert einen Expander direkt
  unter dem Page-Titel mit Erklaer-Text + Mini-Glossar.
- `term_help(key)` liefert die Kurz-Definition (`short`) als String — direkt
  als `help=`-Parameter an `st.metric`, `st.slider`, `st.toggle` etc. uebergeben.
- `glossary_block(keys)` rendert eine kleine Definitions-Liste, z. B. unterhalb
  einer Tabelle.

Konsumiert `src.ui.glossary.GLOSSARY`.
"""

from __future__ import annotations

from collections.abc import Iterable

import streamlit as st

from src.ui.glossary import GLOSSARY


def page_intro(
    title: str,
    what_you_see: str,
    key_terms: Iterable[str] = (),
    *,
    expanded: bool = False,
) -> None:
    """Rendert einen 'Was sehe ich hier?'-Expander direkt unter `st.title()`.

    Args:
        title: Page-Titel ohne Emoji (z. B. "Übersicht", "Findings").
        what_you_see: Markdown-Text, der den Inhalt der Page beschreibt.
        key_terms: Liste der Glossar-Keys, die als Mini-Glossar angehaengt werden.
        expanded: Default geschlossen, damit die Page nicht visuell ueberlastet wird.
    """
    label = f"ℹ️ Was zeigt mir die Seite '{title}'?"
    with st.expander(label, expanded=expanded):
        st.markdown(what_you_see)
        glossary_block(key_terms)


def term_help(key: str) -> str:
    """Liefert die Kurz-Definition als String fuer `help=`-Parameter.

    Bei unbekanntem Key fallback auf den Key selbst — keine Exception, damit eine
    UI-Aenderung nicht den Streamlit-Render bricht.
    """
    term = GLOSSARY.get(key)
    return term.short if term is not None else key


def glossary_block(keys: Iterable[str]) -> None:
    """Mini-Glossar-Liste fuer eine Sektion (z. B. unter einer Tabelle)."""
    keys = [k for k in keys if k in GLOSSARY]
    if not keys:
        return
    st.markdown("**Begriffe auf dieser Seite:**")
    for key in keys:
        term = GLOSSARY[key]
        st.markdown(f"- **{term.label}** — {term.short}")


__all__ = ["page_intro", "term_help", "glossary_block"]
