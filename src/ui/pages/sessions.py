"""Sessions Page (E2-6, Issue #23) — Service-Co-Occurrence-Analyse.

Zeigt:
1. Globaler Netzwerk-Graph (Plotly) — Service-Knoten + gewichtete Edges.
2. Top-20-Paare-Tabelle (globales Ranking).
3. Per-Client-Drilldown mit Top-5-Paaren pro pseudonymisiertem User.

Privacy:
- Keine Client-Keys im Graph (nur Services).
- Bei ``privacy_redacted=True`` aus user_patterns wird der Drilldown
  unterdrückt, nur globaler Graph bleibt sichtbar.
"""

from __future__ import annotations

import math
from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.ui.components.help import glossary_block, page_intro, term_help


def render(report_data: dict[str, Any]) -> None:
    st.title("🔗 Sessions")
    sessions = report_data.get("sessions") or {}

    nodes = sessions.get("graph_nodes") or []
    edges = sessions.get("graph_edges") or []
    global_pairs = sessions.get("global_top_pairs") or []
    top_pairs = sessions.get("top_pairs") or {}
    window = sessions.get("window_minutes", 30)
    redacted = bool(
        (report_data.get("user_patterns") or {}).get("privacy_redacted")
    )

    page_intro(
        title="Sessions",
        what_you_see=(
            f"**Service-Co-Occurrence-Analyse** über ein {window}-Minuten-Fenster.\n\n"
            "Knoten = KI-Service (Größe ≈ Nutzungsfrequenz). Kanten = gemeinsame "
            "Nutzung im Fenster (Kantenbreite ≈ Häufigkeit). Kombinationen wie "
            "*ChatGPT + Cursor + Claude* indizieren typische Code-Kontext-Workflows — "
            "die Kombination ist risikorelevanter als die Einzelservices, weil Daten "
            "zwischen Tools fließen können (Kontextabfluss).\n\n"
            "Der Graph zeigt maximal 50 Knoten — bei mehr Services wird auf die "
            "haeufigsten gefiltert.\n\n"
            "Die Per-User-Drilldown-Tabelle ist nur sichtbar, wenn k-Anonymität low "
            "risk meldet."
        ),
        key_terms=(
            "co_occurrence_fenster",
            "session_graph",
            "edge_weight",
            "spring_layout_determinism",
            "burst",
            "k_anonymitaet",
        ),
    )

    if not edges:
        st.info(
            "Keine Service-Kombinationen im Zeitfenster erkannt. "
            "Entweder sind weniger als zwei unterschiedliche Services erkannt "
            "worden, oder sie lagen weiter als das Fenster auseinander."
        )
        return

    st.markdown("### Globaler Service-Graph")
    st.plotly_chart(
        _build_network_figure(nodes, edges),
        use_container_width=True,
    )

    st.markdown("### Top-20-Paare")
    st.dataframe(
        pd.DataFrame([
            {
                "Service A": p["service_a"],
                "Service B": p["service_b"],
                "Gewicht": p["weight"],
                "Unique Clients": p["clients_count"],
            }
            for p in global_pairs
        ]),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Gewicht": st.column_config.NumberColumn(
                "Gewicht",
                help=term_help("edge_weight"),
            ),
            "Unique Clients": st.column_config.NumberColumn(
                "Unique Clients",
                help=(
                    "Anzahl unterschiedlicher Pseudonyme, die beide Services im "
                    "Fenster genutzt haben — hoehere Werte = breitere Verbreitung."
                ),
            ),
        },
    )

    st.markdown("### Per-Client Drilldown")
    if redacted:
        st.warning(
            "🛡️ Drilldown redigiert (DSGVO Art. 25) — Dataset unterschreitet "
            "die halbe k-Anonymitäts-Schwelle. Nur der globale Graph wird angezeigt."
        )
        return
    if not top_pairs:
        st.info("Keine Per-Client-Paare erfasst.")
        return

    options = sorted(top_pairs.keys())
    chosen = st.selectbox("Client-Pseudonym", options=options)
    if not chosen:
        return
    st.dataframe(
        pd.DataFrame([
            {
                "Service A": p["service_a"],
                "Service B": p["service_b"],
                "Gewicht": p["weight"],
                "Unique Clients (global)": p["clients_count"],
            }
            for p in top_pairs[chosen]
        ]),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Gewicht": st.column_config.NumberColumn(
                "Gewicht",
                help=term_help("edge_weight"),
            ),
            "Unique Clients (global)": st.column_config.NumberColumn(
                "Unique Clients (global)",
                help=(
                    "Anzahl unterschiedlicher Pseudonyme global, die beide Services "
                    "im Fenster genutzt haben."
                ),
            ),
        },
    )

    glossary_block([
        "session_graph",
        "co_occurrence_fenster",
        "edge_weight",
        "co_occurrence_confidence",
        "k_anonymitaet",
    ])


def _build_network_figure(
    nodes: list[str],
    edges: list[dict[str, Any]],
) -> go.Figure:
    """Plotly-Netzwerk-Figure via deterministic Spring-Layout.

    Nutzt networkx.spring_layout mit seed=42 für Stabilität zwischen Reruns.
    Obere Grenze 50 Nodes/Edges — darüber wird das Layout visuell unlesbar.
    """
    import networkx as nx  # lazy import — reduziert Streamlit-Page-Kaltstart

    # Degree-basiertes Top-50-Cap: bei Graphen >50 Services greifen wir nur
    # die am stärksten verbundenen Services heraus.
    limited = _limit_to_top_nodes(nodes, edges, max_nodes=50)

    graph = nx.Graph()
    graph.add_nodes_from(limited["nodes"])
    for edge in limited["edges"]:
        graph.add_edge(edge["a"], edge["b"], weight=edge["weight"])

    pos = nx.spring_layout(graph, seed=42)

    edge_x: list[float] = []
    edge_y: list[float] = []
    for edge in limited["edges"]:
        x0, y0 = pos[edge["a"]]
        x1, y1 = pos[edge["b"]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    max_weight = max((e["weight"] for e in limited["edges"]), default=1)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1.5, color="#8b949e"),
        hoverinfo="none", mode="lines",
        opacity=0.6,
    )

    node_x = [pos[n][0] for n in graph.nodes()]
    node_y = [pos[n][1] for n in graph.nodes()]
    node_sizes = [
        10 + 3 * math.sqrt(max(graph.degree(n), 1)) for n in graph.nodes()
    ]
    node_hover = [
        f"{n}<br>Verbunden mit {graph.degree(n)} anderen Services" for n in graph.nodes()
    ]

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        text=list(graph.nodes()),
        textposition="top center",
        hoverinfo="text", hovertext=node_hover,
        marker=dict(
            color="#0969da",
            size=node_sizes,
            line=dict(width=1, color="#1f2328"),
        ),
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        showlegend=False,
        height=500,
        margin=dict(l=20, r=20, t=30, b=60),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        title=f"{len(graph.nodes())} Services · {len(limited['edges'])} Paare "
              f"(max Gewicht: {max_weight})",
    )
    fig.add_annotation(
        text="Knotengroesse = Nutzungsfrequenz · Kantenbreite = Co-Occurrence-Haeufigkeit",
        xref="paper", yref="paper",
        x=0.5, y=-0.08, xanchor="center", yanchor="top",
        showarrow=False,
        font=dict(family="Share Tech Mono, ui-monospace, monospace", size=10, color="#9B4A2F"),
    )
    return fig


def _limit_to_top_nodes(
    nodes: list[str],
    edges: list[dict[str, Any]],
    max_nodes: int,
) -> dict[str, list]:
    """Begrenzt den Graph auf die `max_nodes` Top-Services nach Degree.

    Reduziert visuelle Unleserlichkeit bei großen Endpoint-Inventaren
    (>50 erkannte Services im selben Dataset).
    """
    if len(nodes) <= max_nodes:
        return {"nodes": nodes, "edges": edges}

    degree: dict[str, int] = {}
    for edge in edges:
        degree[edge["a"]] = degree.get(edge["a"], 0) + 1
        degree[edge["b"]] = degree.get(edge["b"], 0) + 1
    top = sorted(degree.items(), key=lambda kv: kv[1], reverse=True)[:max_nodes]
    keep = {name for name, _ in top}
    return {
        "nodes": sorted(keep),
        "edges": [e for e in edges if e["a"] in keep and e["b"] in keep],
    }
