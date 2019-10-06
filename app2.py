import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/"
    "datasets/master/gapminderDataFiveYear.csv"
)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

countries = df["country"].unique()


app.layout = html.Div(
    [
        dcc.Graph(id="graph-with-slider"),
        dcc.Slider(
            id="year-slider",
            min=df["year"].min(),
            max=df["year"].max(),
            value=df["year"].min(),
            marks={str(year): str(year) for year in df["year"].unique()},
            step=None,
        ),
        dcc.Dropdown(
            id="country-dropdown",
            options=[{"label": x, "value": x} for x in countries],
            value="Afghanistan",
        ),
    ]
)


@app.callback(
    Output("graph-with-slider", "figure"),
    [Input("year-slider", "value"), Input("country-dropdown", "value")],
)
def update_figure(selected_year, selected_country):
    filtered_df = df[
        (df.year == selected_year) & (df.country == selected_country)
    ]
    traces = []
    for i in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df["continent"] == i]
        traces.append(
            go.Scatter(
                x=df_by_continent["gdpPercap"],
                y=df_by_continent["lifeExp"],
                text=df_by_continent["country"],
                mode="markers",
                opacity=0.7,
                marker={"size": 15, "line": {"width": 0.5, "color": "white"}},
                name=i,
            )
        )

    return {
        "data": traces,
        "layout": go.Layout(
            xaxis={"type": "log", "title": "GDP Per Capita"},
            yaxis={"title": "Life Expectancy", "range": [20, 90]},
            margin={"l": 40, "b": 40, "t": 10, "r": 10},
            legend={"x": 0, "y": 1},
            hovermode="closest",
        ),
    }


if __name__ == "__main__":
    app.run_server(debug=True)
