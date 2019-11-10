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
    edge_trace = graph_edges(*unpack_edges(network), nodes["Name"])
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
                    html.H3("Search"),
                    display_table(
                        df=nodes[["Name"]],
                        columns=["Name"],
                        html_id="search",
                        search=True,
                    ),
                ],
                className="table",
            ),
            html.Div(
                [
                    html.H3("Source"),
                    display_table(
                        df=nodes,
                        columns=["Name", "Historical Significance", "Gender"],
                        html_id="source",
                    ),
                ],
                className="table-wide",
            ),
            html.Div(
                [
                    html.H3("Target"),
                    display_table(
                        df=nodes,
                        columns=["Name", "Historical Significance", "Gender"],
                        html_id="target",
                    ),
                ],
                className="table-wide",
            ),
        ]
    )

    @app.callback(Output("search", "data"), [Input("search", "filter_query")])
    def update_names(filter, id_field="Name"):
        id_field = "Name"
        filtering_expressions = filter.split(" && ")
        dff = nodes[[id_field]].sort_values(id_field)
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

    @app.callback(Output("source", "data"), [Input("search", "active_cell")])
    def update_sources(
        selection,
        id_field="Name",
        target_field="Target",
        source_field="Source",
    ):
        columns = ["Name", "Historical Significance", "Gender"]
        sorted_names = nodes[id_field].sort_values().tolist()
        if selection:
            # Get occurrences of name in the source file
            row_index = selection["row"]
            person_id = sorted_names[row_index]

            # The people this person sourced
            source_names = edges[edges[source_field] == person_id][
                target_field
            ].tolist()
            sources = nodes[nodes[id_field].isin(source_names)]
            return sources[columns].to_dict("records")
        else:
            return nodes[columns].to_dict("records")

    @app.callback(Output("target", "data"), [Input("search", "active_cell")])
    def update_targets(
        selection,
        id_field="Name",
        target_field="Target",
        source_field="Source",
    ):
        columns = ["Name", "Historical Significance", "Gender"]
        sorted_names = nodes[id_field].sort_values().tolist()
        if selection:
            # Get occurrences of name in the source file
            row_index = selection["row"]
            person_id = sorted_names[row_index]

            # The people who sourced this person
            target_names = edges[edges[target_field] == person_id][
                source_field
            ].tolist()
            targets = nodes[nodes[id_field].isin(target_names)]
            return targets[columns].to_dict("records")
        else:
            return nodes[columns].to_dict("records")

    app.run_server(host="0.0.0.0", debug=True)
