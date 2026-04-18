"""Zeitliche Muster-Analyse (E2-1, E2-2).

- build_hourly_heatmap: Client × Stunde-des-Tages-Matrix
- off_hours_ratio: Anteil der Queries außerhalb Business-Hours

Compliance-Bezug:
- DORA Art. 10 (Anomalie-Erkennung)
- ISO 27001 A.8.16 (Monitoring)
- ISO 27001 A.8.15 (Logging)
"""

from __future__ import annotations

import pandas as pd

# Default Business-Hours (06–22 Uhr). Konfigurierbar in build_hourly_heatmap/off_hours_ratio.
BUSINESS_HOURS_START = 6  # inklusive
BUSINESS_HOURS_END = 22  # exklusiv — ≥22 ist Off-Hours


def build_hourly_heatmap(
    df: pd.DataFrame,
    by_service: bool = False,
) -> pd.DataFrame:
    """Erzeugt eine Stunden-Heatmap (Client × Stunde) aus einem Query-DataFrame.

    Args:
        df: DataFrame mit mindestens den Spalten ``timestamp``, ``client``
            (wie von parse_pihole_log / parse_squid_log erzeugt).
        by_service: Wenn True, wird die Domain (bzw. ``ai_match.service`` falls
            vorhanden) als zusätzliche Dimension aufgenommen; Rückgabe hat dann
            MultiIndex (client, service).

    Returns:
        DataFrame mit Index=Client (oder MultiIndex) und Columns=0..23 (Stunde).
        Werte sind Query-Counts (int).

    Beispiel:
        >>> df = parse_pihole_log("sample.log")
        >>> heatmap = build_hourly_heatmap(df)
        >>> heatmap.shape
        (N, 24)
    """
    if df.empty or "timestamp" not in df.columns or "client" not in df.columns:
        return pd.DataFrame()

    work = df.copy()
    work["hour"] = pd.to_datetime(work["timestamp"]).dt.hour

    if by_service:
        # Bevorzugt den bereits gematchten Service-Namen (falls DetectionEngine
        # die Spalte ``ai_match`` gesetzt hat), sonst fällt zurück auf domain.
        if "ai_match" in work.columns:
            work["_service"] = work["ai_match"].apply(
                lambda ep: ep.service if ep is not None else None
            )
            work = work[work["_service"].notna()]
        elif "domain" in work.columns:
            work["_service"] = work["domain"]
        else:
            return pd.DataFrame()

        heatmap = (
            work.groupby(["client", "_service", "hour"])
            .size()
            .unstack("hour", fill_value=0)
            .reindex(columns=range(24), fill_value=0)
        )
        heatmap.index.names = ["client", "service"]
        return heatmap.astype(int)

    heatmap = (
        work.groupby(["client", "hour"])
        .size()
        .unstack("hour", fill_value=0)
        .reindex(columns=range(24), fill_value=0)
    )
    return heatmap.astype(int)


def off_hours_ratio(
    df: pd.DataFrame,
    business_start: int = BUSINESS_HOURS_START,
    business_end: int = BUSINESS_HOURS_END,
) -> float:
    """Anteil der Queries außerhalb Business-Hours (default 06–22 Uhr).

    KI-Nutzung außerhalb Business-Hours ist anomalie-relevant: Datenexfiltration,
    automatisierte Skripte, Zeitzonen-Unstimmigkeiten.

    Args:
        df: DataFrame mit ``timestamp``
        business_start: Erste Stunde, die als Business-Hour gilt (inklusive)
        business_end: Erste Stunde NACH Business-Hours (exklusiv; ≥end = Off-Hours)

    Returns:
        Float in [0.0, 1.0]; 0.0 = alles während Business-Hours, 1.0 = alles off-hours.
        Bei leerem DataFrame: 0.0.
    """
    if df.empty or "timestamp" not in df.columns:
        return 0.0

    hours = pd.to_datetime(df["timestamp"]).dt.hour
    off_hours_mask = (hours < business_start) | (hours >= business_end)
    return float(off_hours_mask.mean())
