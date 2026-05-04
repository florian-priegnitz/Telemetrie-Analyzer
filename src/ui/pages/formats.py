"""Formate-Page — systematische Vorstellung der 12 unterstützten Log-Formate.

Funktionsweise: Liest ``PARSER_METADATA`` aus ``src/parsers/detection.py``
(Single Source of Truth), rendert pro Format einen Expander mit Quelle,
Beispiel-Zeile aus dem Sample, Feld-Mapping auf das Common-Schema und
Risk-Signal-Erklärung. Sample-Download-Button lädt die Datei direkt aus
``testdata/``.

Die Page ist unabhängig vom Pipeline-State navigierbar — auch wenn keine
Analyse läuft, kann man sich über die Formate informieren.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit as st

from src.parsers.detection import PARSER_LABELS, PARSER_METADATA, SUPPORTED_PARSERS
from src.ui.components.help import glossary_block, page_intro

_TESTDATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "testdata"
_MAX_EXAMPLE_LINES = 2
_MAX_EXAMPLE_CHARS = 500


def _load_example(sample_file: str) -> tuple[str, int] | tuple[None, int]:
    """Lädt bis zu ``_MAX_EXAMPLE_LINES`` Zeilen aus testdata/<sample_file>.

    Returns:
        (text, num_lines) wenn Datei gefunden, sonst (None, 0).
    """
    path = _TESTDATA_DIR / sample_file
    if not path.is_file():
        return None, 0
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines: list[str] = []
            for _ in range(_MAX_EXAMPLE_LINES):
                line = fh.readline()
                if not line:
                    break
                lines.append(line.rstrip("\n"))
            total = sum(1 for _ in fh) + len(lines)
    except OSError:
        return None, 0
    text = "\n".join(lines)
    if len(text) > _MAX_EXAMPLE_CHARS:
        text = text[:_MAX_EXAMPLE_CHARS] + " …(gekürzt)"
    return text, total


def _render_field_mapping(mapping: dict[str, str]) -> None:
    cols = st.columns([1, 1])
    cols[0].markdown("**Quelle (Parser-Input)**")
    cols[1].markdown("**Common-Schema (Pipeline-Output)**")
    for src_field, target in mapping.items():
        c_a, c_b = st.columns([1, 1])
        c_a.code(src_field, language="text")
        c_b.code(target, language="text")


def _render_format_card(key: str, meta: dict[str, Any]) -> None:
    label = PARSER_LABELS.get(key, key)
    sample_file = meta.get("sample_file", "")
    with st.expander(f"**{label}**", expanded=False):
        cols = st.columns([3, 1])
        cols[0].markdown(f"**Quelle:** {meta.get('source', '—')}")
        cols[1].markdown(f"**Dateityp:** `{meta.get('file_type', '—')}`")

        st.markdown(f"**Risk-Signal:** {meta.get('risk_signal', '—')}")

        st.markdown("#### 📝 Beispielzeile (aus Testdaten)")
        example, total = _load_example(sample_file)
        if example is None:
            st.info(f"`testdata/{sample_file}` nicht gefunden — "
                    f"Sample regenerieren via Generator oder Commit prüfen.")
        else:
            st.code(example, language="text")
            st.caption(f"Vollständiges Sample: `testdata/{sample_file}` "
                       f"({total} Zeile{'n' if total != 1 else ''})")
            # Download-Button mit Pseudonymisierungs-Hinweis
            path = _TESTDATA_DIR / sample_file
            if path.is_file():
                data = path.read_bytes()
                st.download_button(
                    label=f"⬇ Testdatei herunterladen ({len(data)/1024:.1f} KB)",
                    data=data,
                    file_name=sample_file,
                    mime="text/plain",
                    key=f"dl_{key}",
                )

        st.markdown("#### 🔗 Feld-Mapping")
        st.caption(
            "Welche Eingabe-Felder welche Common-Schema-Spalten füllen. "
            "Downstream-Engines (Detection, Compliance) arbeiten nur auf dem "
            "Common-Schema — Parser sind die einzige Stelle, die Tool-Spezifik kennt."
        )
        mapping = meta.get("field_mapping", {})
        if mapping:
            _render_field_mapping(mapping)
        else:
            st.caption("_(kein Mapping hinterlegt)_")


def render(_report_data: Any | None = None) -> None:
    """Formate-Page-Entry-Point. Signatur wie andere Pages (ignoriert report_data)."""
    st.title("📚 Unterstützte Log-Formate")
    page_intro(
        title="Formate",
        what_you_see=(
            "Katalog aller **12 unterstützten Log-Formate** mit Quelle, Beispiel-Zeile, "
            "Feld-Mapping auf das Common-Schema und Risk-Signal-Hinweisen. Beim Upload "
            "wird das Format automatisch erkannt (Auto-Detect liest die ersten Zeilen). "
            "Die Sample-Dateien sind synthetisch und können direkt heruntergeladen werden."
        ),
        key_terms=("parser_auto_detect", "asn_fallback", "pseudonymisierung"),
    )
    st.markdown(
        "Der Telemetrie Analyzer verarbeitet **12 Telemetrie-Log-Formate** — "
        "von klassischem Pi-hole DNS bis zu modernen Cloud-Security-Plattformen. "
        "Alle Parser erzeugen ein gemeinsames **Common-Schema** "
        "(`timestamp`, `client`, `domain`), auf dem Detection + Compliance arbeiten."
    )
    st.caption(
        "🔒 **Privacy-by-Design:** Alle Client-IPs und Benutzer werden direkt beim "
        "Parsing via HMAC-SHA256 pseudonymisiert (DSGVO Art. 25). Die Testdaten "
        "sind synthetisch (RFC 1918 / Doku-Domains) und enthalten keine realen PII."
    )

    # Überblicks-Tabelle
    st.markdown("### Format-Übersicht")
    rows = []
    for key in SUPPORTED_PARSERS:
        meta = PARSER_METADATA.get(key, {})
        rows.append({
            "Format": PARSER_LABELS.get(key, key),
            "Dateityp": meta.get("file_type", "—"),
            "Sample-Datei": f"testdata/{meta.get('sample_file', '—')}",
        })
    st.dataframe(rows, hide_index=True, use_container_width=True)

    st.markdown("### Details je Format")
    st.caption(
        "Aufklappen für Quelle, Beispielzeile, Feld-Mapping auf das "
        "Common-Schema und Risk-Signal."
    )
    for key in SUPPORTED_PARSERS:
        meta = PARSER_METADATA.get(key)
        if meta is None:
            continue
        _render_format_card(key, meta)

    st.markdown("---")
    st.markdown("### Common-Schema")
    st.markdown(
        """
Jedes Parser-Ergebnis ist ein pandas-DataFrame mit mindestens drei Pflichtspalten:

| Spalte | Typ | Zweck |
|--------|-----|-------|
| `timestamp` | `datetime64[ns]` (tz-naive) | Zeitreihen-Analyse, Off-Hours, Retention |
| `client` | `str` (`ip_<hash>`) | Eindeutiger pseudonymisierter Client |
| `domain` | `str` (lowercase) | Matching gegen AI Endpoint DB |

Optional (parser-abhängig): `user`, `method`, `url_path`, `bytes_uploaded`,
`bytes_downloaded`, `status_code`, `action`, `urlcategory`, `useragent`,
`app`, `activity`, `process`, `asn_org`, `source_file`, `source_type`.

Siehe [`src/parsers/base.py`](https://github.com/florian-priegnitz/Telemetrie-Analyzer/blob/main/src/parsers/base.py)
für den vollständigen Vertrag (`BaseParser` ABC).
        """
    )

    glossary_block([
        "parser_auto_detect",
        "endpoint_db_freshness",
        "drift_guard",
    ])
