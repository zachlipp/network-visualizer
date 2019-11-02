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

from datasets import helper_text, load_data
from viz import graph_edges, graph_nodes, unpack_edges, unpack_nodes


def get_visible_names(positions: Dict, visible: Dict) -> List:
    # Index based on nodes, names in this case
    coords = pd.DataFrame(positions).T

    x_min = visible.get("xaxis.range[0]")
    x_max = visible.get("xaxis.range[1]")
    y_min = visible.get("yaxis.range[0]")
    y_max = visible.get("yaxis.range[1]")

    if all([x_min, y_min]):
        new_coords = coords[
            coords[0].between(x_min, x_max) & coords[1].between(y_min, y_max)
        ]
    elif x_min:
        new_coords = coords[coords[0].between(x_min, x_max)]
    elif y_min:
        new_coords = coords[coords[1].between(y_min, y_max)]
    return new_coords.index.tolist()



if __name__ == "__main__":
    external_stylesheets = [
        "http://berniesandersofficial.com/wp-includes/css/dist/block-library/style.min.css?ver=5.2.3",
        "http://berniesandersofficial.com/wp-content/plugins/cpo-companion/assets/css/fontawesome.css?ver=5.2.3",
        "http://berniesandersofficial.com/wp-content/plugins/kiwi-social-share/assets/vendors/icomoon/style.css?ver=2.0.15",
        "http://berniesandersofficial.com/wp-content/themes/allegiant/core/css/base.css?ver=5.2.3",
        "http://berniesandersofficial.com/wp-content/themes/allegiant/style.css?ver=5.2.3",
    ]
    nodes, edges, network = load_data(id_field="Name", graph_dimensions=2)
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    node_adjacencies = []
    for adjacencies in network.adjacency():
        node_adjacencies.append(len(adjacencies[1]))

    node_text = [
        f"Name: {x} <br># Connections: {y}"
        for x, y in zip(nodes.Name, node_adjacencies)
    ]

    node_colors = nodes["Gender"].map({"male": "blue", "female": "red"})
    edge_trace = graph_edges(*unpack_edges(network))
    node_trace = graph_nodes(
        *unpack_nodes(network),
        node_colors=node_colors,
        node_text=nodes.Name,
        ids=nodes.Name,
    )

    app.layout = html.Div(
        [
            html.H1("Network Visualizer", className="header"),
            html.Div(
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
                    )
                ],
                className="graph-container",
            ),
            html.Div([html.P(helper_text)], className="text"),
            html.Div(
                [
                    dash_table.DataTable(
                        id="description",
                        columns=[
                            {"id": c, "name": c}
                            for c in [
                                "Name",
                                "Historical Significance",
                                "Gender",
                            ]
                        ],
                        data=nodes[
                            ["Name", "Historical Significance", "Gender"]
                        ].to_dict(orient="records"),
                    )
                ],
                className="pandas",
            ),
        ]
    )

    @app.callback(
        Output("description", "data"), [Input("network", "relayoutData")]
    )
    def update_table(relayoutData):
        print(relayoutData)
        display = ["Name", "Historical Significance", "Gender"]
        if relayoutData:
            if "autosize" in relayoutData or "xaxis.autorange" in relayoutData:
                return nodes[display].to_dict(orient="records")
            else:
                visible = get_visible_names(
                    nx.get_node_attributes(network, "position"), relayoutData
                )
                return nodes[nodes["Name"].isin(visible)][display].to_dict(
                    orient="records"
                )
        else:
            return nodes[display].to_dict(orient="records")

    app.run_server(host="0.0.0.0", debug=True)
