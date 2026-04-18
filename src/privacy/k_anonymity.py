"""k-Anonymitäts-Guard (E2-7).

Warnt wenn eine Gruppenbildung unter einem Mindestschwellwert (k) liegt —
Re-Identifikations-Risiko trotz Pseudonymisierung bei kleinen Datasets.

DSGVO-Kontext:
- Art. 25 (Privacy by Design): technische Maßnahmen gegen De-Anonymisierung
- Art. 32 (Sicherheit der Verarbeitung): Risikoangemessenheit

Die Funktionen ``assert_k_anonymity`` und ``check_k_anonymity`` werfen KEINE
Exception (User entscheidet selbst — z.B. 3-Personen-Beratung kann legitim
sein), sondern loggen eine Warning und geben einen KAnonymityCheck zurück.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import pandas as pd

logger = logging.getLogger(__name__)

MIN_K_ANONYMITY = 5


@dataclass(frozen=True)
class KAnonymityCheck:
    """Ergebnis einer k-Anonymitäts-Prüfung."""
    field: str
    observed_k: int
    minimum_k: int
    is_sufficient: bool

    @property
    def reidentification_risk(self) -> str:
        """Einstufung des Re-Identifikations-Risikos in drei Stufen."""
        if self.observed_k >= self.minimum_k:
            return "low"
        if self.observed_k >= max(2, self.minimum_k // 2):
            return "medium"
        return "high"


def check_k_anonymity(
    df: pd.DataFrame,
    field: str = "client",
    minimum_k: int = MIN_K_ANONYMITY,
) -> KAnonymityCheck:
    """Prüft, ob ein DataFrame die k-Anonymitäts-Schwelle einhält.

    Args:
        df: DataFrame
        field: Spalte, deren distinct-count geprüft wird (Default: ``client``).
        minimum_k: Mindestschwelle (Default 5).

    Returns:
        KAnonymityCheck (keine Exception, siehe Modul-Docstring).
    """
    observed = int(df[field].nunique()) if not df.empty and field in df.columns else 0
    sufficient = observed >= minimum_k
    if not sufficient:
        logger.warning(
            "k-Anonymität unterschritten: %d %s gefunden (Minimum %d) — "
            "Re-Identifikations-Risiko bei kleinen Datasets",
            observed, field, minimum_k,
        )
    return KAnonymityCheck(
        field=field,
        observed_k=observed,
        minimum_k=minimum_k,
        is_sufficient=sufficient,
    )


def assert_k_anonymity(
    df: pd.DataFrame,
    field: str = "client",
    minimum_k: int = MIN_K_ANONYMITY,
) -> KAnonymityCheck:
    """Alias für check_k_anonymity — semantisch als Assertion gemeint.

    Wirft bewusst KEINE Exception (soft-check, siehe Modul-Docstring).
    """
    return check_k_anonymity(df, field=field, minimum_k=minimum_k)
