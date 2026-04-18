"""Streamlit UI Layer für den Telemetrie Analyzer.

Strikte Layer-Trennung:
- `state.py` ist der einzige Wrapper, der die Pipeline (Parser → Detection → Compliance) aufruft.
- `pages/` und `components/` importieren NIE direkt aus `src/parsers`, `src/detection`, `src/compliance`.
"""
