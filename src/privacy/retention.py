"""Retention-Management (DSGVO Art. 5 (1e) — Speicherbegrenzung).

Zweck: Aus einem parsed-DataFrame alle Zeilen entfernen, die älter als die
konfigurierte Retention-Periode sind. Rein in-memory — der Analyzer persistiert
keine Rohdaten. Retention wirkt als Pipeline-Hook nach dem Parser und vor
der Detection-Engine.

Konfiguration: `config/retention.yaml` — Default 90 Tage, per Log-Typ
überschreibbar. ENV-Overrides: `RETENTION_DAYS`, `RETENTION_CONFIG`.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import yaml


DEFAULT_CONFIG_PATH = (
    Path(__file__).resolve().parent.parent.parent / "config" / "retention.yaml"
)
DEFAULT_DAYS = 90


@dataclass(frozen=True)
class RetentionPolicy:
    """Retention-Konfiguration pro Log-Typ.

    Attributes:
        enabled: Master-Switch. False = DataFrame unverändert durchreichen.
        default_days: Fallback-Fenster wenn kein log_type-spezifischer Eintrag.
        policies: Dict log_type -> days (überschreibt default).
    """

    enabled: bool = True
    default_days: int = DEFAULT_DAYS
    policies: dict[str, int] = field(default_factory=dict)

    def days_for(self, log_type: str | None) -> int:
        if log_type and log_type in self.policies:
            return int(self.policies[log_type])
        return int(self.default_days)


def load_policy(path: Path | None = None) -> RetentionPolicy:
    """Lädt Retention-Konfiguration aus YAML.

    Resolver-Reihenfolge:
    1. Explizites `path`-Argument
    2. ENV `RETENTION_CONFIG`
    3. `config/retention.yaml` im Projekt-Root
    4. Hardcoded-Defaults (90 Tage, enabled)

    ENV `RETENTION_DAYS` überschreibt `default_days` *nach* dem YAML-Laden
    — so kann Docker ohne Custom-YAML konfigurieren.
    """
    if path is not None:
        candidate = Path(path)
    elif env_path := os.environ.get("RETENTION_CONFIG"):
        candidate = Path(env_path)
    else:
        candidate = DEFAULT_CONFIG_PATH

    data: dict = {}
    if candidate.is_file():
        with open(candidate, encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}

    policy = RetentionPolicy(
        enabled=bool(data.get("enabled", True)),
        default_days=int(data.get("default_days", DEFAULT_DAYS)),
        policies={
            str(k): int(v.get("days", DEFAULT_DAYS)) if isinstance(v, dict) else int(v)
            for k, v in (data.get("policies") or {}).items()
        },
    )

    env_days = os.environ.get("RETENTION_DAYS")
    if env_days:
        try:
            return RetentionPolicy(
                enabled=policy.enabled,
                default_days=int(env_days),
                policies=policy.policies,
            )
        except ValueError:
            pass
    return policy


def apply_retention(
    df: pd.DataFrame,
    policy: RetentionPolicy | None = None,
    *,
    log_type: str | None = None,
    now: datetime | None = None,
) -> pd.DataFrame:
    """Trim ein DataFrame auf den Retention-Horizont.

    Args:
        df: Parsed-DataFrame mit Spalte `timestamp` (datetime64[ns], tz-naive).
        policy: Retention-Konfiguration. None = `load_policy()` aufrufen.
        log_type: Log-Typ-Schlüssel (z.B. "pihole") für policy-spezifische Regel.
        now: Referenz-Zeitpunkt für Tests. Default: datetime.now().

    Returns:
        Neues DataFrame ohne Zeilen älter als policy.days_for(log_type).
        Wenn `policy.enabled=False` oder `df` leer: Input unverändert.
        Grenzfall: timestamp == cutoff bleibt erhalten (inklusiv).
    """
    if df is None or df.empty:
        return df
    policy = policy if policy is not None else load_policy()
    if not policy.enabled:
        return df
    if "timestamp" not in df.columns:
        return df

    days = policy.days_for(log_type)
    if days <= 0:
        return df

    reference = now if now is not None else datetime.now()
    cutoff = reference - timedelta(days=days)
    mask = df["timestamp"] >= cutoff
    return df.loc[mask].reset_index(drop=True)


def summarize(
    df_before: pd.DataFrame,
    df_after: pd.DataFrame,
    policy: RetentionPolicy,
    log_type: str | None = None,
) -> dict:
    """Kennzahlen für die UI-Anzeige (Auditspur, DSGVO Art. 30)."""
    dropped = len(df_before) - len(df_after)
    return {
        "enabled": policy.enabled,
        "days": policy.days_for(log_type),
        "log_type": log_type,
        "rows_before": int(len(df_before)),
        "rows_after": int(len(df_after)),
        "rows_dropped": int(dropped),
    }
