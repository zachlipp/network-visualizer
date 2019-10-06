from typing import Dict, List, Tuple

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import networkx as nx
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
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
        showlegend=False,
    )
    return edge_trace


def graph_nodes(
    x: List, y: List, node_colors: List, node_text: List, ids: List
) -> Scatter:
    node_trace = go.Scatter(
        x=x,
        y=y,
        mode="markers",
        hoverinfo="text",
        showlegend=False,
        marker=dict(color=node_colors, size=10, line_width=2),
    )

    node_trace.customdata = ids
    node_trace.text = node_text
    return node_trace


def get_visible_names(positions: Dict, visible: Dict) -> List:
    # Index based on nodes, names in this case
    coord = pd.DataFrame(positions).T

    x_min, x_max, y_min, y_max = visible.values()

    new_coord = coord[
        coord[0].between(x_min, x_max) & coord[1].between(y_min, y_max)
    ]
    return new_coord.index.tolist()


if __name__ == "__main__":
    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    nodes = pd.read_csv("quakers_nodelist.csv")
    edges = pd.read_csv("quakers_edgelist.csv")

    G = nx.from_pandas_edgelist(edges, "Source", "Target")
    pos = nx.spring_layout(G)
    nx.set_node_attributes(G, name="pos", values=pos)

    node_adjacencies = []
    for adjacencies in G.adjacency():
        node_adjacencies.append(len(adjacencies[1]))

    node_text = [
        f"Name: {x} <br># Connections: {y}"
        for x, y in zip(nodes.Name, node_adjacencies)
    ]

    node_colors = nodes["Gender"].map({"male": "blue", "female": "red"})
    edge_trace = graph_edges(*unpack_edges(G))
    node_trace = graph_nodes(
        *unpack_nodes(G),
        node_colors=node_colors,
        node_text=node_text,
        ids=nodes.Name,
    )

    app.layout = html.Div(
        [
            dcc.Graph(
                id="network",
                figure=go.Figure(
                    data=[edge_trace, node_trace],
                    layout=go.Layout(
                        hovermode="closest",
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(
                            showgrid=False,
                            zeroline=False,
                            showticklabels=False,
                        ),
                        yaxis=dict(
                            showgrid=False,
                            zeroline=False,
                            showticklabels=False,
                        ),
                    ),
                ),
            ),
            dash_table.DataTable(
                id="description",
                columns=[{"id": c, "name": c} for c in nodes.columns],
                data=nodes.to_dict(orient="records"),
            ),
        ]
    )

    @app.callback(
        Output("description", "data"),
        [Input("network", "clickData"), Input("network", "relayoutData")],
    )
    def update_table(clickData, relayoutData):
        print(clickData)
        print("------")
        print(relayoutData)
        if clickData:
            points = clickData["points"]
            user_names = [p["customdata"] for p in points]
            return nodes[nodes["Name"].isin(user_names)].to_dict(
                orient="records"
            )
        else:
            return nodes.to_dict(orient="records")

    app.run_server(debug=True)
