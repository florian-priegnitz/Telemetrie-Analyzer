"""BaseParser — gemeinsames Interface für alle Log-Parser.

Issue #25 (E3-0). Definiert den DataFrame-Vertrag, den Downstream-Konsumenten
(Detection Engine, Behavior Analytics, UI) von jedem Parser erwarten. Neue
Enterprise-Parser (Zscaler, Palo Alto, ...) erben von BaseParser und müssen
nur `parse()` + optional `OPTIONAL_COLUMNS` implementieren.

Vertrag (siehe REQUIRED_COLUMNS): jedes zurückgegebene DataFrame enthält
`timestamp`, `client`, `domain`. Pseudonymisierung passiert im Parser,
nicht im Caller.
"""

from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd

from src.privacy.pseudonymizer import Pseudonymizer


def coerce_timestamp_ns(df: pd.DataFrame) -> pd.DataFrame:
    """Erzwingt ``datetime64[ns]`` für die ``timestamp``-Spalte.

    pandas ≥ 2.2 kann je nach Input-Quelle ``datetime64[us]`` liefern
    (z.B. aus ISO-Strings mit Microsekunden, oder aus numpy-Defaults).
    Unser BaseParser-Contract verlangt strikt ``[ns]`` — dieser Helper
    wird am Ende jeder ``parse_*_log()``-Funktion gerufen UND im
    ``_finalize()``-Hook der Klassen, sodass beide Aufrufpfade (direkte
    Funktion + Klassen-parse()) den dtype-Vertrag erfüllen.
    """
    if df.empty or "timestamp" not in df.columns:
        return df
    if str(df["timestamp"].dtype) != "datetime64[ns]":
        df = df.copy()
        df["timestamp"] = df["timestamp"].astype("datetime64[ns]")
    return df


class BaseParser(ABC):
    """Abstrakte Basisklasse für Log-Parser mit gemeinsamem DataFrame-Schema."""

    REQUIRED_COLUMNS: set[str] = {"timestamp", "client", "domain"}
    OPTIONAL_COLUMNS: set[str] = set()

    def __init__(self, pseudonymizer: Pseudonymizer | None = None):
        self.pseudonymizer = pseudonymizer or Pseudonymizer()

    @abstractmethod
    def parse(self, path: str | Path) -> pd.DataFrame:
        """Parst eine Log-Datei und gibt ein schema-konformes DataFrame zurück.

        Postconditions:
        - Alle `REQUIRED_COLUMNS` sind present
        - `timestamp` ist `datetime64[ns]` (tz-naive), aufsteigend sortiert
        - `client` ist pseudonymisiert (Präfix `ip_*` oder `user_*`)
        - `domain` ist lowercase, ohne trailing `.`
        - Leeres DataFrame ist erlaubt (z.B. bei leerer Log-Datei)
        """
        ...

    def validate_schema(self, df: pd.DataFrame, strict: bool = False) -> None:
        """Prüft, ob das DataFrame den Parser-Vertrag erfüllt.

        Args:
            df: Zu prüfendes DataFrame.
            strict: Wenn True, werden auch unerwartete Spalten abgelehnt.

        Raises:
            ValueError: Pflicht-Spalten fehlen, Timestamp-Typ falsch oder
                unsortiert, oder unerwartete Spalten in strict mode.
        """
        if df.empty:
            return

        missing = self.REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"Fehlende Pflicht-Spalten: {sorted(missing)}")

        if df["timestamp"].dtype != "datetime64[ns]":
            raise ValueError(
                f"timestamp muss datetime64[ns] sein, ist {df['timestamp'].dtype}"
            )
        if not df["timestamp"].is_monotonic_increasing:
            raise ValueError("timestamp ist nicht aufsteigend sortiert")

        if strict:
            allowed = self.REQUIRED_COLUMNS | self.OPTIONAL_COLUMNS
            extra = set(df.columns) - allowed
            if extra:
                raise ValueError(f"Unerwartete Spalten: {sorted(extra)}")

    def _finalize(self, df: pd.DataFrame) -> pd.DataFrame:
        """Sortiert nach timestamp, coerce auf [ns], validiert.

        Der `.astype("datetime64[ns]")`-Coerce fängt pandas-≥2.2-Fälle ab,
        in denen der Timestamp als `[us]` aus Parse-Operationen kommt.
        """
        if not df.empty and "timestamp" in df.columns:
            df = df.sort_values("timestamp").reset_index(drop=True)
            df = coerce_timestamp_ns(df)
        self.validate_schema(df)
        return df
