from typing import Dict, List, Tuple

import dash
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output

external_stylesheets = [
    "http://berniesandersofficial.com/wp-includes/css/dist/block-library/style.min.css?ver=5.2.3",
    "http://berniesandersofficial.com/wp-content/plugins/cpo-companion/assets/css/fontawesome.css?ver=5.2.3",
    "http://berniesandersofficial.com/wp-content/plugins/kiwi-social-share/assets/vendors/icomoon/style.css?ver=2.0.15",
    "http://berniesandersofficial.com/wp-content/themes/allegiant/core/css/base.css?ver=5.2.3",
    "http://berniesandersofficial.com/wp-content/themes/allegiant/style.css?ver=5.2.3",
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


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
