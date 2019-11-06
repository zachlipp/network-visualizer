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
from plotly.graph_objs import Scatter, Scatter3d

from app import app, get_visible_names_2d
from datasets import load_data
from viz import (
    display_network,
    display_table,
    graph_edges,
    graph_nodes,
    operators,
    split_filter_part,
    unpack_edges,
    unpack_nodes,
)

if __name__ == "__main__":
    nodes, edges, network = load_data(id_field="Name", graph_dimensions=3)

    nodes["color"] = nodes["Gender"].map({"male": "blue", "female": "red"})
    edge_trace = graph_edges(*unpack_edges(network))
    node_trace = graph_nodes(
        *unpack_nodes(network),
        node_colors=nodes["color"],
        node_text=nodes["Name"],
        ids=nodes["Name"]
    )

    app.layout = html.Div(
        [
            html.H1("Network Visualizer", className="header"),
            html.Div(
                [display_network(edge_trace, node_trace)],
                className="graph-container",
            ),
            html.Div(
                [
                    display_table(
                        df=nodes,
                        columns=["Name", "Historical Significance", "Gender"],
                    )
                ],
                className="pandas",
            ),
        ]
    )

    @app.callback(
        Output("description", "data"), [Input("description", "filter_query")]
    )
    def update_table(filter):
        filtering_expressions = filter.split(" && ")
        dff = nodes
        for filter_part in filtering_expressions:
            col_name, operator, filter_value = split_filter_part(filter_part)
            if operator in ("eq", "ne", "lt", "le", "gt", "ge"):
                # these operators match pandas series operator method names
                dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
            elif operator == "contains":
                dff = dff.loc[dff[col_name].str.contains(filter_value)]
            elif operator == "datestartswith":
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                dff = dff.loc[dff[col_name].str.startswith(filter_value)]
        return dff.to_dict("records")

    """
    @app.callback(
        Output("network", "selectedData"),
        [Input("description", "filter_query")],
    )
    def update_network(filter):
        filtering_expressions = filter.split(" && ")
        dff = nodes 
        for filter_part in filtering_expressions:
            col_name, operator, filter_value = split_filter_part(filter_part)
            if operator in ("eq", "ne", "lt", "le", "gt", "ge"):
                # these operators match pandas series operator method names
                dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
            elif operator == "contains":
                dff = dff.loc[dff[col_name].str.contains(filter_value)]
            elif operator == "datestartswith":
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                dff = dff.loc[dff[col_name].str.startswith(filter_value)]
        return dff["voterid_target"].tolist()
    """

    app.run_server(host="0.0.0.0", debug=True)
