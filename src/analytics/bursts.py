"""Burst-Detection (E2-3).

Erkennt plötzliche Request-Spitzen (>N Requests in T Minuten), die auf
automatisierte Skripte, Batch-Uploads oder Massen-Abfragen hindeuten.

Compliance-Bezug:
- DORA Art. 17 (ICT-Related Incidents)
- ISO 27001 A.8.16 (Monitoring)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import pandas as pd

BURST_WINDOW_MINUTES = 5
BURST_THRESHOLD = 50
BURST_RISK_BOOST = 10  # Additiv zum Finding-Score bei ≥1 Burst (E2-3)


@dataclass(frozen=True)
class BurstEvent:
    """Ein erkannter Request-Burst."""
    client: str
    service: str | None
    start: datetime
    end: datetime
    query_count: int
    peak_rate: float  # Requests pro Minute zum Burst-Peak

    @property
    def duration_minutes(self) -> float:
        return (self.end - self.start).total_seconds() / 60.0


def detect_bursts(
    df: pd.DataFrame,
    window_minutes: int = BURST_WINDOW_MINUTES,
    threshold: int = BURST_THRESHOLD,
    group_by: tuple[str, ...] = ("client",),
) -> list[BurstEvent]:
    """Findet alle Zeitfenster mit ≥threshold Requests innerhalb window_minutes.

    Args:
        df: DataFrame mit ``timestamp``, ``client`` und optional ``ai_match``
            (aus DetectionEngine) zur Service-Zuordnung.
        window_minutes: Länge des rollenden Fensters (default 5 min).
        threshold: Mindestanzahl Requests im Fenster, um als Burst zu gelten.
        group_by: Tupel der Spalten, über die gruppiert wird. Default nur
            ``client``; ``("client", "service")`` für service-spezifische Bursts.

    Returns:
        Liste von BurstEvent, sortiert nach ``start``. Überlappende Bursts
        werden zu einem Event gemergt.
    """
    if df.empty or "timestamp" not in df.columns:
        return []

    work = df.copy()
    work["timestamp"] = pd.to_datetime(work["timestamp"])

    # Service aus ai_match ableiten falls vorhanden (DetectionEngine-Kontext)
    if "service" not in work.columns and "ai_match" in work.columns:
        work["service"] = work["ai_match"].apply(
            lambda ep: ep.service if ep is not None else None
        )

    group_cols = [c for c in group_by if c in work.columns]
    if not group_cols:
        return []

    bursts: list[BurstEvent] = []
    window = pd.Timedelta(minutes=window_minutes)

    for group_key, group_df in work.groupby(group_cols):
        sorted_df = group_df.sort_values("timestamp").reset_index(drop=True)
        n = len(sorted_df)
        if n < threshold:
            continue

        timestamps = sorted_df["timestamp"].tolist()

        # Sliding window via zwei Pointer über den sortierten Timestamp-Vektor
        active_start_idx: int | None = None
        active_end_idx: int | None = None
        active_peak: int = 0

        left = 0
        for right in range(n):
            while timestamps[right] - timestamps[left] > window:
                left += 1
            count = right - left + 1

            if count >= threshold:
                # Burst aktiv: Grenzen merken/erweitern
                if active_start_idx is None:
                    active_start_idx = left
                active_end_idx = right
                if count > active_peak:
                    active_peak = count
            else:
                # Burst beendet: Event finalisieren, falls einer aktiv war
                if active_start_idx is not None and active_end_idx is not None:
                    bursts.append(_build_event(
                        group_key, group_cols,
                        sorted_df, active_start_idx, active_end_idx,
                        active_peak, window_minutes,
                    ))
                    active_start_idx = active_end_idx = None
                    active_peak = 0

        # Offenen Burst am Ende finalisieren
        if active_start_idx is not None and active_end_idx is not None:
            bursts.append(_build_event(
                group_key, group_cols,
                sorted_df, active_start_idx, active_end_idx,
                active_peak, window_minutes,
            ))

    bursts.sort(key=lambda b: b.start)
    return bursts


def _build_event(
    group_key: object,  # skalarer Wert bei 1 Spalte, Tupel bei mehreren (pandas-GroupBy-Kontrakt)
    group_cols: list[str],
    sorted_df: pd.DataFrame,
    start_idx: int,
    end_idx: int,
    peak: int,
    window_minutes: int,
) -> BurstEvent:
    """Erzeugt einen BurstEvent aus einer erkannten Fenster-Range."""
    key_dict = dict(zip(group_cols, (group_key if isinstance(group_key, tuple) else (group_key,))))
    start = sorted_df.at[start_idx, "timestamp"].to_pydatetime()
    end = sorted_df.at[end_idx, "timestamp"].to_pydatetime()
    query_count = end_idx - start_idx + 1
    peak_rate = peak / window_minutes  # Requests pro Minute
    return BurstEvent(
        client=key_dict.get("client", ""),
        service=key_dict.get("service"),
        start=start,
        end=end,
        query_count=query_count,
        peak_rate=round(peak_rate, 2),
    )
