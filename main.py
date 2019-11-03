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
from datasets import helper_text, load_data
from viz import (
    display_network,
    display_table,
    graph_edges,
    graph_nodes,
    unpack_edges,
    unpack_nodes,
    split_filter_part,
    operators
)

if __name__ == "__main__":
    nodes, edges, network = load_data(id_field="voterid", graph_dimensions=3)
    tall = edges.merge(nodes, left_on="source", right_on="voterid", how="left")
    tall = tall.merge(nodes, left_on="target", right_on="voterid",
        suffixes=("_source", "_target"),
        how="left")
    # M = Male / F = Female
    nodes["color"] = nodes["gender"].map({"M": "blue", "F": "red"})
    edge_trace = graph_edges(*unpack_edges(network), ids=nodes["voterid"])

    text = (
        "First Name: " +
        nodes["first_name"] +
        "<br>" +
        "Last Name: " +
        nodes["last_name"] +
        "<br>" +
        "Precinct: " +
        nodes["precinct"]
    )

    # text = ()'' nodes["first_name"] + '<br>' + nodes["last_name"] + '<br>' + nodes["last_name"]

    node_trace = graph_nodes(
        *unpack_nodes(network),
        node_colors=nodes["color"],
        # node_text=nodes["voterid"],
        node_text=text,
        ids=nodes["voterid"]
    )

    app.layout = html.Div(
        [
            html.H1("Network Visualizer", className="header"),
            html.Div(
                [display_network(edge_trace, node_trace)],
                className="graph-container",
            ),
            html.Div([html.P(helper_text)], className="text"),
            html.Div(
                [
                    display_table(
                        df=tall,
                        columns=[
                            "first_name_target",
                            "last_name_target",
                            "gender_target",
                            "precinct_target",
                                "first_name_source",
                                "last_name_source",
                                "gender_source",
                                "precinct_source",],
                    )
                ],
                className="pandas",
            ),
        ]
    )
    @app.callback(Output('description', "data"), [Input('description', "filter_query")])
    def update_table(filter):
        filtering_expressions = filter.split(' && ')
        dff = tall
        for filter_part in filtering_expressions:
            col_name, operator, filter_value = split_filter_part(filter_part)
            if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                # these operators match pandas series operator method names
                dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
            elif operator == 'contains':
                dff = dff.loc[dff[col_name].str.contains(filter_value)]
            elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                dff = dff.loc[dff[col_name].str.startswith(filter_value)]
        return dff.to_dict('records')

    @app.callback(Output('network', "selectedData"), [Input('description', "filter_query")])
    def update_network(filter):
        filtering_expressions = filter.split(' && ')
        dff = tall
        for filter_part in filtering_expressions:
            col_name, operator, filter_value = split_filter_part(filter_part)
            if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                # these operators match pandas series operator method names
                dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
            elif operator == 'contains':
                dff = dff.loc[dff[col_name].str.contains(filter_value)]
            elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                dff = dff.loc[dff[col_name].str.startswith(filter_value)]
        return dff["voterid_target"].tolist()



    """
    @app.callback(
        Output("description", "data"), [Input("network", "relayoutData")]
    )
    def update_table(relayoutData):
        display = ["Name", "Historical Significance", "Gender"]
        if relayoutData:
            if "autosize" in relayoutData or "xaxis.autorange" in relayoutData:
                return nodes[display].to_dict(orient="records")
            else:
                visible = get_visible_names_2d(
                    nx.get_node_attributes(network, "position"), relayoutData
                )
                return nodes[nodes["Name"].isin(visible)][display].to_dict(
                    orient="records"
                )
        else:
            return nodes[display].to_dict(orient="records")
    """
    app.run_server(host="0.0.0.0", debug=True)
