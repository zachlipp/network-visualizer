from typing import List, Tuple

import networkx as nx
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from networkx.classes.graph import Graph
from plotly.graph_objs import Scatter


def unpack_edges(G: Graph) -> Tuple[List[float]]:
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.node[edge[0]]["pos"]
        x1, y1 = G.node[edge[1]]["pos"]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    return edge_x, edge_y


def unpack_nodes(G: Graph) -> Tuple[List[float]]:
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.node[node]["pos"]
        node_x.append(x)
        node_y.append(y)
    return node_x, node_y


def graph_edges(x: List, y: List) -> Scatter:
    edge_trace = go.Scatter(
        x=x,
        y=y,
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )
    return edge_trace


def graph_nodes(
    x: List, y: List, node_color: List, node_text: List
) -> Scatter:
    node_trace = go.Scatter(
        x=x,
        y=y,
        mode="markers",
        hoverinfo="text",
        marker=dict(
            showscale=True,
            colorscale="Viridis",
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title="Node Connections",
                xanchor="left",
                titleside="right",
            ),
            line_width=2,
        ),
    )

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text
    return node_trace


if __name__ == "__main__":
    nodes = pd.read_csv("quakers_nodelist.csv")
    edges = pd.read_csv("quakers_edgelist.csv")

    st.title("my app")

    G = nx.from_pandas_edgelist(edges, "Source", "Target")
    pos = nx.spring_layout(G)
    nx.set_node_attributes(G, name="pos", values=pos)

    node_adjacencies = []
    node_text = []
    for adjacencies in G.adjacency():
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append("# of connections: " + str(len(adjacencies[1])))

    edge_trace = graph_edges(*unpack_edges(G))
    node_trace = graph_nodes(
        *unpack_nodes(G), node_color=node_adjacencies, node_text=node_text
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title="<br>Network graph made with Python",
            titlefont_size=16,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )
    st.write(fig)
