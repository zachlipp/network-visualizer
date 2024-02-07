from typing import Dict, List, Tuple

import dash
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output


app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True


def get_visible_names_2d(positions: Dict, visible: Dict) -> List:
    """Get the names visible in the 2d graph"""
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
