"""Tests für Retention Management (#38, DSGVO Art. 5 (1e))."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import pytest

from src.privacy.retention import (
    DEFAULT_DAYS,
    RetentionPolicy,
    apply_retention,
    load_policy,
    summarize,
)


NOW = datetime(2026, 4, 21, 12, 0, 0)


def _make_df(days_old: list[int]) -> pd.DataFrame:
    """Baut ein DataFrame mit `timestamp`-Spalte, je Eintrag `days_old` Tage alt."""
    rows = [{
        "timestamp": NOW - timedelta(days=d),
        "client": f"client_{i}",
        "domain": "example.com",
    } for i, d in enumerate(days_old)]
    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


# ---------------------------------------------------------------------------
# apply_retention — Core-Boundary-Tests
# ---------------------------------------------------------------------------
class TestApplyRetention:

    def test_keeps_all_within_window(self):
        df = _make_df([0, 1, 30, 89])
        policy = RetentionPolicy(default_days=90)
        out = apply_retention(df, policy, now=NOW)
        assert len(out) == 4

    def test_drops_rows_older_than_window(self):
        df = _make_df([0, 95, 120])
        policy = RetentionPolicy(default_days=90)
        out = apply_retention(df, policy, now=NOW)
        assert len(out) == 1
        assert out.iloc[0]["client"] == "client_0"

    def test_boundary_exactly_on_cutoff_is_kept(self):
        """Rows at exactly `now - days` must be kept (inclusive)."""
        df = _make_df([90])
        policy = RetentionPolicy(default_days=90)
        out = apply_retention(df, policy, now=NOW)
        assert len(out) == 1

    def test_boundary_one_day_over_is_dropped(self):
        df = _make_df([91])
        policy = RetentionPolicy(default_days=90)
        out = apply_retention(df, policy, now=NOW)
        assert len(out) == 0

    def test_disabled_policy_returns_unchanged(self):
        df = _make_df([0, 120, 500])
        policy = RetentionPolicy(enabled=False, default_days=90)
        out = apply_retention(df, policy, now=NOW)
        assert len(out) == 3

    def test_empty_df_passthrough(self):
        df = pd.DataFrame({"timestamp": pd.to_datetime([])})
        policy = RetentionPolicy(default_days=90)
        out = apply_retention(df, policy, now=NOW)
        assert out.empty

    def test_missing_timestamp_column_returns_unchanged(self):
        df = pd.DataFrame({"client": ["a", "b"]})
        policy = RetentionPolicy(default_days=90)
        out = apply_retention(df, policy, now=NOW)
        assert len(out) == 2

    def test_zero_or_negative_days_disables_trim(self):
        df = _make_df([0, 365])
        policy = RetentionPolicy(default_days=0)
        out = apply_retention(df, policy, now=NOW)
        assert len(out) == 2


# ---------------------------------------------------------------------------
# Per-Log-Type-Policy
# ---------------------------------------------------------------------------
class TestPolicyPerLogType:

    def test_policy_override_applies(self):
        df = _make_df([0, 40, 100])
        policy = RetentionPolicy(
            default_days=90,
            policies={"aws_vpc_flow": 30},
        )
        out = apply_retention(df, policy, log_type="aws_vpc_flow", now=NOW)
        assert len(out) == 1  # nur der heutige

    def test_unknown_log_type_falls_back_to_default(self):
        df = _make_df([0, 40, 100])
        policy = RetentionPolicy(
            default_days=90,
            policies={"aws_vpc_flow": 30},
        )
        out = apply_retention(df, policy, log_type="pihole", now=NOW)
        assert len(out) == 2

    def test_none_log_type_falls_back_to_default(self):
        df = _make_df([0, 100])
        policy = RetentionPolicy(default_days=90, policies={"aws_vpc_flow": 30})
        out = apply_retention(df, policy, log_type=None, now=NOW)
        assert len(out) == 1


# ---------------------------------------------------------------------------
# load_policy — YAML-Loader
# ---------------------------------------------------------------------------
class TestLoadPolicy:

    def test_loads_default_yaml(self):
        """config/retention.yaml im Repo muss parsebar sein."""
        policy = load_policy()
        assert policy.enabled is True
        assert policy.default_days >= 1
        assert "pihole" in policy.policies

    def test_loads_custom_yaml(self, tmp_path: Path):
        yaml_file = tmp_path / "retention.yaml"
        yaml_file.write_text(
            "enabled: false\n"
            "default_days: 7\n"
            "policies:\n"
            "  custom_type:\n"
            "    days: 14\n",
            encoding="utf-8",
        )
        policy = load_policy(yaml_file)
        assert policy.enabled is False
        assert policy.default_days == 7
        assert policy.policies == {"custom_type": 14}

    def test_missing_file_returns_defaults(self, tmp_path: Path):
        policy = load_policy(tmp_path / "does-not-exist.yaml")
        assert policy.enabled is True
        assert policy.default_days == DEFAULT_DAYS

    def test_env_override_default_days(self, tmp_path: Path, monkeypatch):
        yaml_file = tmp_path / "retention.yaml"
        yaml_file.write_text("default_days: 90\n", encoding="utf-8")
        monkeypatch.setenv("RETENTION_DAYS", "42")
        policy = load_policy(yaml_file)
        assert policy.default_days == 42


# ---------------------------------------------------------------------------
# summarize — Audit-Report für UI
# ---------------------------------------------------------------------------
class TestSummarize:

    def test_summary_fields(self):
        df_in = _make_df([0, 100])
        policy = RetentionPolicy(default_days=90)
        df_out = apply_retention(df_in, policy, now=NOW)
        s = summarize(df_in, df_out, policy, log_type="pihole")
        assert s["enabled"] is True
        assert s["days"] == 90
        assert s["rows_before"] == 2
        assert s["rows_after"] == 1
        assert s["rows_dropped"] == 1
        assert s["log_type"] == "pihole"


# ---------------------------------------------------------------------------
# Privacy-Invariante: Retention verändert nur Zeilenzahl, nicht Inhalte
# ---------------------------------------------------------------------------
def test_retention_does_not_modify_pseudonyms():
    """Smoketest: Pseudonymisierte client-Werte bleiben unverändert."""
    df = _make_df([1, 2, 3])
    df["client"] = ["ip_a1b2c3d4", "ip_deadbeef", "ip_12345678"]
    policy = RetentionPolicy(default_days=90)
    out = apply_retention(df, policy, now=NOW)
    assert list(out["client"]) == ["ip_a1b2c3d4", "ip_deadbeef", "ip_12345678"]
