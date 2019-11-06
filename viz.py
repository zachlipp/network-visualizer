from typing import Dict, List, Tuple

import dash_core_components as dcc
import dash_table
import pandas as pd
import plotly.graph_objects as go
from networkx.classes.graph import Graph
from pandas.core.frame import DataFrame
from plotly.graph_objs import Scatter, Scatter3d


def unpack_edges(network: Graph) -> Tuple[List[float]]:
    """Manipulates the wonky network data into wonky lists
    
    Lists will be as follows:
    [point 1 x0, point 1 x1, np.nan, point 2 x0, point 2 x2, np.nan]

    The lists are one-dimensionsal; each dimension will have its
    own list
    """
    positions = []
    for edge in network.edges():
        # `edge` is a container with two values
        source = edge[0]
        target = edge[1]

        # "position" is an array with one element per network dimension
        source_coords = network.node[source]["position"]
        target_coords = network.node[target]["position"]
        padding = [None for _ in source_coords]

        positions.append(source_coords)
        positions.append(target_coords)
        positions.append(padding)

    # Transpose the list to get ndim lists of len(network.edges())
    transposed = pd.DataFrame(positions).T.values
    return transposed


def unpack_nodes(network: Graph) -> Tuple[List[float]]:
    positions = []
    for node in network.nodes():
        position = network.node[node]["position"]
        positions.append(position)

    # Transpose the list to get ndim lists of len(network.edges())
    transposed = pd.DataFrame(positions).T.values
    return transposed


def graph_edges(x: List, y: List, z: List, ids: List) -> Scatter3d:
    # TODO: Generalize
    edge_trace = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        line=dict(width=2, color="#888"),
        hoverinfo="skip",
        mode="lines",
        showlegend=False,
    )
    edge_trace.customdata = ids

    return edge_trace


def graph_nodes(
    x: List, y: List, z: List, node_colors: List, node_text: List, ids: List
) -> Scatter3d:
    # TODO: Generalize
    node_trace = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode="markers",
        hoverinfo="text",
        showlegend=True,
        marker=dict(color=node_colors, size=5, line_width=2),
        hoverlabel=dict(bgcolor=node_colors),
    )
    node_trace.customdata = ids
    node_trace.text = node_text
    return node_trace


def display_table(df: DataFrame, columns: List) -> dash_table.DataTable:
    # Dash requires a list of dictionaries with "id", "name" fields
    dash_columns = [{"id": column, "name": column} for column in columns]
    # Data needs to be list of dictionaries for the HTML table
    dash_data = df[columns].to_dict(orient="records")

    data_table = dash_table.DataTable(
        id="description",
        columns=dash_columns,
        data=dash_data,
        filter_action="custom",
        filter_query="",
    )
    return data_table


operators = [
    ["ge ", ">="],
    ["le ", "<="],
    ["lt ", "<"],
    ["gt ", ">"],
    ["ne ", "!="],
    ["eq ", "="],
    ["contains "],
    ["datestartswith "],
]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[
                    name_part.find("{") + 1 : name_part.rfind("}")
                ]

                value_part = value_part.strip()
                v0 = value_part[0]
                if v0 == value_part[-1] and v0 in ("'", '"', "`"):
                    value = value_part[1:-1].replace("\\" + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


def display_network(edge_trace: List, node_trace: List) -> dcc.Graph:
    return dcc.Graph(
        id="network",
        figure=go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                hovermode="closest",
                margin=dict(b=20, l=5, r=5, t=40),
                scene=dict(
                    xaxis=dict(
                        color="rgba(0,0,0,0)",
                        showbackground=False,
                        showgrid=False,
                        zeroline=False,
                        showticklabels=False,
                    ),
                    yaxis=dict(
                        color="rgba(0,0,0,0)",
                        showbackground=False,
                        showgrid=False,
                        zeroline=False,
                        showticklabels=False,
                    ),
                    zaxis=dict(
                        color="rgba(0,0,0,0)",
                        showbackground=False,
                        showgrid=False,
                        zeroline=False,
                        showticklabels=False,
                    ),
                ),
            ),
        ),
    )
