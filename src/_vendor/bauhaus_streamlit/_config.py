"""Streamlit-Config-Helper: schreibt CI-Theme in `.streamlit/config.toml`."""

from __future__ import annotations

from pathlib import Path

CONFIG_TOML_TEMPLATE = '''[theme]
primaryColor = "#9B4A2F"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F6F8FC"
textColor = "#0C1A32"
font = "sans serif"
'''


def install_config(target_dir: Path, *, overwrite: bool = False) -> Path:
    """Schreibt `config.toml` mit Bauhaus-CI-Theme in `target_dir`.

    Args:
        target_dir: Streamlit-Config-Verzeichnis (typischerweise `Path('.streamlit')`).
        overwrite: Wenn `False` (Default) und die Datei bereits existiert,
            wird `FileExistsError` geworfen.

    Returns:
        Pfad zur geschriebenen `config.toml`.
    """
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "config.toml"
    if target.exists() and not overwrite:
        raise FileExistsError(
            f"{target} existiert bereits. Setze overwrite=True zum Ueberschreiben."
        )
    target.write_text(CONFIG_TOML_TEMPLATE, encoding="utf-8")
    return target
