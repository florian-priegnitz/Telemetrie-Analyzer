"""Tests für Session-Korrelation (E2-6, Issue #23)."""

from __future__ import annotations

import re
from datetime import datetime, timedelta

import pandas as pd

from src.analytics.sessions import (
    SessionPair,
    build_session_graph,
    top_global_pairs,
    top_service_pairs_per_client,
)

_BASE = datetime(2026, 4, 22, 9, 0, 0)
_PSEUDO_PATTERN = re.compile(r"^client_[0-9a-f]{8}$")


def _df(rows: list[tuple[str, str, datetime]]) -> pd.DataFrame:
    """Erzeugt ein Minimal-DF mit client/domain/timestamp (Domain als Service-Quelle)."""
    return pd.DataFrame([
        {"client": c, "domain": s, "timestamp": t} for (c, s, t) in rows
    ])


# ---------------------------------------------------------------------------
# build_session_graph — Core-Logik
# ---------------------------------------------------------------------------

class TestBuildSessionGraph:

    def test_empty_df_returns_empty_graph(self):
        g = build_session_graph(pd.DataFrame())
        assert g.number_of_nodes() == 0
        assert g.number_of_edges() == 0

    def test_two_services_in_window_edge_exists(self):
        g = build_session_graph(_df([
            ("c1", "ChatGPT", _BASE),
            ("c1", "Cursor", _BASE + timedelta(minutes=5)),
        ]))
        assert g.number_of_edges() == 1
        assert g.has_edge("ChatGPT", "Cursor")
        assert g.edges["ChatGPT", "Cursor"]["weight"] == 1
        assert g.edges["ChatGPT", "Cursor"]["clients"] == 1

    def test_two_services_outside_window_no_edge(self):
        g = build_session_graph(_df([
            ("c1", "ChatGPT", _BASE),
            ("c1", "Cursor", _BASE + timedelta(minutes=31)),
        ]))
        assert g.number_of_edges() == 0

    def test_same_service_twice_no_self_loop(self):
        g = build_session_graph(_df([
            ("c1", "ChatGPT", _BASE),
            ("c1", "ChatGPT", _BASE + timedelta(minutes=2)),
        ]))
        assert g.number_of_edges() == 0
        # Single-Node-Graphen tragen keine Nodes, wenn kein Edge existiert
        assert g.number_of_nodes() == 0

    def test_edge_weight_counts_cooccurrences_across_windows(self):
        """Zwei unterschiedliche Fenster mit ChatGPT+Cursor → weight=2."""
        g = build_session_graph(_df([
            # Fenster 1
            ("c1", "ChatGPT", _BASE),
            ("c1", "Cursor", _BASE + timedelta(minutes=5)),
            # Fenster 2 (>30min Abstand zum ersten)
            ("c1", "ChatGPT", _BASE + timedelta(minutes=60)),
            ("c1", "Cursor", _BASE + timedelta(minutes=62)),
        ]))
        assert g.edges["ChatGPT", "Cursor"]["weight"] == 2
        assert g.edges["ChatGPT", "Cursor"]["clients"] == 1

    def test_clients_count_distinct_users(self):
        """Zwei verschiedene Clients mit demselben Paar → clients=2, weight=2."""
        g = build_session_graph(_df([
            ("c1", "ChatGPT", _BASE),
            ("c1", "Cursor", _BASE + timedelta(minutes=5)),
            ("c2", "ChatGPT", _BASE + timedelta(hours=3)),
            ("c2", "Cursor", _BASE + timedelta(hours=3, minutes=5)),
        ]))
        assert g.edges["ChatGPT", "Cursor"]["weight"] == 2
        assert g.edges["ChatGPT", "Cursor"]["clients"] == 2

    def test_window_minutes_configurable(self):
        """Mit 5-Min-Fenster sind 10-Min-auseinander liegende Events nicht mehr im Paar."""
        rows = [
            ("c1", "ChatGPT", _BASE),
            ("c1", "Cursor", _BASE + timedelta(minutes=10)),
        ]
        assert build_session_graph(_df(rows), window_minutes=30).number_of_edges() == 1
        assert build_session_graph(_df(rows), window_minutes=5).number_of_edges() == 0

    def test_three_services_in_window_all_pairs_edged(self):
        g = build_session_graph(_df([
            ("c1", "ChatGPT", _BASE),
            ("c1", "Cursor", _BASE + timedelta(minutes=2)),
            ("c1", "Claude", _BASE + timedelta(minutes=5)),
        ]))
        assert g.has_edge("ChatGPT", "Cursor")
        assert g.has_edge("ChatGPT", "Claude")
        assert g.has_edge("Claude", "Cursor")


# ---------------------------------------------------------------------------
# top_service_pairs_per_client — Pseudonymisierung + Ranking
# ---------------------------------------------------------------------------

class TestTopServicePairsPerClient:

    def test_keys_are_pseudonymized(self):
        result = top_service_pairs_per_client(
            _df([
                ("192.168.1.50", "ChatGPT", _BASE),
                ("192.168.1.50", "Cursor", _BASE + timedelta(minutes=5)),
            ]),
            salt="test-salt-abc",
        )
        assert result  # nicht leer
        for key in result:
            assert _PSEUDO_PATTERN.match(key), f"Key {key!r} leakt Plaintext"
            # Raw-IP darf nirgendwo auftauchen
            assert "192.168.1.50" not in key

    def test_top_n_caps_list(self):
        """Mehr als top_n Paare pro Client werden abgeschnitten."""
        # 4 Services im selben Fenster → C(4,2) = 6 Paare
        rows = [
            ("c1", s, _BASE + timedelta(minutes=i))
            for i, s in enumerate(["A", "B", "C", "D"])
        ]
        result = top_service_pairs_per_client(_df(rows), salt="s", top_n=3)
        assert len(next(iter(result.values()))) == 3

    def test_ranked_by_weight_descending(self):
        rows = [
            # Paar (A, B) kommt in 2 Fenstern vor → weight=2
            ("c1", "A", _BASE),
            ("c1", "B", _BASE + timedelta(minutes=2)),
            ("c1", "A", _BASE + timedelta(minutes=60)),
            ("c1", "B", _BASE + timedelta(minutes=62)),
            # Paar (A, C) nur in einem → weight=1
            ("c1", "C", _BASE + timedelta(minutes=3)),
        ]
        result = top_service_pairs_per_client(_df(rows), salt="s", top_n=5)
        pairs = next(iter(result.values()))
        assert pairs[0].weight >= pairs[-1].weight

    def test_empty_df_returns_empty_dict(self):
        assert top_service_pairs_per_client(pd.DataFrame(), salt="s") == {}


# ---------------------------------------------------------------------------
# top_global_pairs
# ---------------------------------------------------------------------------

class TestTopGlobalPairs:

    def test_returns_session_pair_dataclass(self):
        g = build_session_graph(_df([
            ("c1", "A", _BASE),
            ("c1", "B", _BASE + timedelta(minutes=3)),
        ]))
        pairs = top_global_pairs(g)
        assert len(pairs) == 1
        assert isinstance(pairs[0], SessionPair)
        assert pairs[0].service_a == "A"  # kanonisch sortiert
        assert pairs[0].service_b == "B"

    def test_top_n_limits_output(self):
        # 4 Services → 6 Paare; top_n=2 liefert 2
        rows = [
            ("c1", s, _BASE + timedelta(minutes=i))
            for i, s in enumerate(["A", "B", "C", "D"])
        ]
        g = build_session_graph(_df(rows))
        assert len(top_global_pairs(g, top_n=2)) == 2


# ---------------------------------------------------------------------------
# SessionPair serialisierung
# ---------------------------------------------------------------------------

class TestSessionPair:

    def test_as_dict_roundtrip(self):
        p = SessionPair(service_a="A", service_b="B", weight=3, clients_count=2)
        d = p.as_dict()
        assert d == {
            "service_a": "A", "service_b": "B", "weight": 3, "clients_count": 2,
        }


# ---------------------------------------------------------------------------
# Privacy-Invariante
# ---------------------------------------------------------------------------

def test_no_plaintext_client_in_graph_nodes():
    """Graph-Nodes und Edges dürfen keine Client-Identifier tragen."""
    raw_client = "203.0.113.42"
    g = build_session_graph(_df([
        (raw_client, "ChatGPT", _BASE),
        (raw_client, "Cursor", _BASE + timedelta(minutes=3)),
    ]))
    # Nodes = nur Service-Namen
    assert raw_client not in g.nodes()
    # Edge-Attribute dürfen den Raw-Key nicht enthalten
    for _a, _b, data in g.edges(data=True):
        assert raw_client not in str(data)
