"""Session-Korrelation (E2-6, Issue #23).

Erkennt Service-Co-Occurrence innerhalb konfigurierbarer Zeitfenster pro
Client. Grundthese: wer in einem 30-Min-Fenster ChatGPT + Cursor + Claude
nutzt, macht vermutlich Code-Entwicklung mit Kontextabfluss — die
*Kombination* ist risikorelevanter als die Einzelservices.

Output-Contract:
- ``build_session_graph`` → ``networkx.Graph`` mit Services als Knoten und
  gewichteten Kanten (weight = globale Co-Occurrence-Häufigkeit,
  clients = distinct User, die das Paar zeigen).
- ``top_service_pairs_per_client`` → Dict pseudonymisierte_client → Top-N.

Privacy-Invariante: **keine Client-Keys im Graph-Output**. Nodes und
Edges tragen ausschließlich Service-Namen. Per-Client-Pairs werden über
``pseudonymize_client()`` re-keyed bevor sie das Modul verlassen.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import networkx as nx
import pandas as pd

from src.reports.privacy import pseudonymize_client

_DEFAULT_WINDOW_MIN = 30
_DEFAULT_TOP_N = 5


@dataclass(frozen=True)
class SessionPair:
    """Ein Service-Paar mit Co-Occurrence-Statistik."""
    service_a: str
    service_b: str
    weight: int         # Anzahl Co-Occurrence-Fenster (global)
    clients_count: int  # Anzahl distinct User, die das Paar zeigen

    def as_dict(self) -> dict[str, object]:
        return {
            "service_a": self.service_a,
            "service_b": self.service_b,
            "weight": self.weight,
            "clients_count": self.clients_count,
        }


@dataclass
class _EdgeAccumulator:
    """Akkumuliert Fenster-Co-Occurrences für ein Service-Paar."""
    weight: int = 0
    clients: set[str] = field(default_factory=set)


def _service_column(df: pd.DataFrame) -> pd.Series:
    """Wählt die Service-Spalte: ``ai_match.service`` wenn vorhanden, sonst ``domain``."""
    if "ai_match" in df.columns:
        return df["ai_match"].apply(
            lambda ep: ep.service if ep is not None else None
        )
    if "domain" in df.columns:
        return df["domain"]
    return pd.Series([None] * len(df), index=df.index)


def _iter_client_pairs(
    df: pd.DataFrame,
    window: pd.Timedelta,
):
    """Yieldet ``(client, pair)`` für jedes Service-Paar im jeweiligen Fenster.

    Nutzt das Two-Pointer-Sliding-Window-Pattern analog zu
    ``src/analytics/bursts.py`` — O(N·E) statt O(N²) über alle Events.
    Innerhalb eines Fensters werden alle Paarkombinationen der enthaltenen
    Services (dedupliziert, kanonisch sortiert, keine Self-Loops) gemeldet.
    """
    if df.empty:
        return
    required = {"timestamp", "client"}
    missing = required - set(df.columns)
    if missing:
        return

    services = _service_column(df)
    work = df.assign(_service=services)
    work = work[work["_service"].notna()].copy()
    if work.empty:
        return

    for client, group in work.groupby("client"):
        sorted_group = group.sort_values("timestamp").reset_index(drop=True)
        timestamps = pd.to_datetime(sorted_group["timestamp"])
        services_arr = sorted_group["_service"].astype(str).tolist()
        n = len(services_arr)

        left = 0
        for right in range(n):
            while left < right and timestamps.iloc[right] - timestamps.iloc[left] > window:
                left += 1
            # Distinkte Services im aktuellen Fenster [left..right] bestimmen
            window_services = sorted(set(services_arr[left : right + 1]))
            if len(window_services) < 2:
                continue
            # NOTE: Für weight-Semantik zählen wir pro „neu eingetretener"
            # Service am right-Pointer genau einmal mit jedem bereits aktiven
            # Service — nur wenn services_arr[right] zum ersten Mal im Fenster
            # auftaucht. Sonst würden wir kontinuierlich für jede weitere
            # Request dasselbe Paar wieder zählen (O(N²) Inflation).
            new_service = services_arr[right]
            if new_service in set(services_arr[left:right]):
                continue
            for partner in set(services_arr[left:right]):
                if partner == new_service:
                    continue
                pair = tuple(sorted([new_service, partner]))
                yield str(client), pair


def build_session_graph(
    df: pd.DataFrame,
    window_minutes: int = _DEFAULT_WINDOW_MIN,
) -> nx.Graph:
    """Baut einen ungerichteten Service-Co-Occurrence-Graphen.

    Args:
        df: DataFrame mit mindestens ``timestamp`` und ``client``, dazu
            entweder ``ai_match`` (bevorzugt, von ``DetectionEngine`` gesetzt)
            oder ``domain``.
        window_minutes: Zeitfenster-Breite in Minuten (Default 30).

    Returns:
        ``networkx.Graph`` ohne Client-Informationen. Nodes = Service-Namen;
        Edges haben ``weight`` (int, globale Co-Occurrence) und
        ``clients`` (int, distinct User). Leerer Graph wenn kein Fenster
        mindestens zwei unterschiedliche Services enthält.
    """
    graph = nx.Graph()
    if df.empty:
        return graph

    window = pd.Timedelta(minutes=window_minutes)
    accumulator: dict[tuple[str, str], _EdgeAccumulator] = {}

    for client, pair in _iter_client_pairs(df, window):
        slot = accumulator.setdefault(pair, _EdgeAccumulator())
        slot.weight += 1
        slot.clients.add(client)

    for (svc_a, svc_b), acc in accumulator.items():
        graph.add_node(svc_a)
        graph.add_node(svc_b)
        graph.add_edge(svc_a, svc_b, weight=acc.weight, clients=len(acc.clients))

    return graph


def top_service_pairs_per_client(
    df: pd.DataFrame,
    salt: str,
    window_minutes: int = _DEFAULT_WINDOW_MIN,
    top_n: int = _DEFAULT_TOP_N,
) -> dict[str, list[SessionPair]]:
    """Top-N-Service-Paare pro pseudonymisiertem Client.

    Args:
        df: Wie ``build_session_graph``.
        salt: Pseudonymisierungs-Salt (z. B. ``st.session_state.report_salt``).
        window_minutes: Fensterbreite.
        top_n: Wie viele Paare pro Client (Default 5).

    Returns:
        Dict ``{pseudonym: [SessionPair, …]}`` sortiert nach Gewicht
        absteigend. Keys folgen dem Muster ``client_<hex>`` (siehe
        ``pseudonymize_client``).
    """
    if df.empty:
        return {}
    window = pd.Timedelta(minutes=window_minutes)

    per_client_counts: dict[str, dict[tuple[str, str], int]] = {}
    for client, pair in _iter_client_pairs(df, window):
        per_client_counts.setdefault(client, {})
        per_client_counts[client][pair] = per_client_counts[client].get(pair, 0) + 1

    # Global Clients-Count pro Pair (für SessionPair.clients_count)
    global_clients_per_pair: dict[tuple[str, str], set[str]] = {}
    for client, pairs in per_client_counts.items():
        for pair in pairs:
            global_clients_per_pair.setdefault(pair, set()).add(client)

    result: dict[str, list[SessionPair]] = {}
    for client, pairs in per_client_counts.items():
        pseudo = pseudonymize_client(str(client), salt)
        ranked = sorted(pairs.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
        result[pseudo] = [
            SessionPair(
                service_a=pair[0],
                service_b=pair[1],
                weight=weight,
                clients_count=len(global_clients_per_pair[pair]),
            )
            for pair, weight in ranked
        ]
    return result


def top_global_pairs(graph: nx.Graph, top_n: int = 20) -> list[SessionPair]:
    """Top-N-Paare des globalen Graphen, sortiert nach weight absteigend."""
    pairs: list[SessionPair] = []
    for svc_a, svc_b, data in graph.edges(data=True):
        a, b = sorted([svc_a, svc_b])
        pairs.append(SessionPair(
            service_a=a,
            service_b=b,
            weight=int(data.get("weight", 0)),
            clients_count=int(data.get("clients", 0)),
        ))
    pairs.sort(key=lambda p: p.weight, reverse=True)
    return pairs[:top_n]
