from datetime import datetime
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

from Dataset import Dataset

NORTH_AMERICA_MAPBOX_SETTINGS = {
    'center': {"lat": 50, "lon": -100},
    'zoom': 3,
}

COLUMN_OPTIONS = [
    {'label': 'Estimated Area', 'value': 'estarea'},
    {'label': 'Fire Weather Index', 'value': 'fwi'},
    {'label': 'Rate of Spread', 'value': 'ros'},
    {'label': 'Head Fire Intensity', 'value': 'hfi'},
]

SCATTER_COLOR_OPTIONS = [
    {'label': 'fuel', 'value': 'fuel'},
    {'label': 'source', 'value': 'source'},
]

def scatter_mapbox(app: Dash, dataset: Dataset):
    @app.callback(
        Output('scatter-mapbox', 'figure'),
        Input('scatter-mapbox-value-col', 'value'),
        Input('scatter-mapbox-color-col', 'value'),
        Input('scatter-mapbox-date-range-slider', 'value'),
    )
    def update(value_col: str, color_col: str, date_range: list[int]):
        [min_date, max_date] = date_range
        min_date = datetime.fromordinal(min_date)
        max_date = datetime.fromordinal(max_date)
        df = dataset.filter(min_date=min_date, max_date=max_date)
        return px.scatter_mapbox(df, lat="lat", lon="lon", size=value_col, size_max=20, color=color_col,
                        **NORTH_AMERICA_MAPBOX_SETTINGS,
                        mapbox_style="open-street-map")

    min_date = dataset.min_date.toordinal()
    max_date = dataset.max_date.toordinal()

    return html.Div([
        html.H3('Scatter Mapbox'),
        html.Div([
            html.Div([
                html.H3("Value"),
                dcc.Dropdown(
                    id='scatter-mapbox-value-col',
                    options=COLUMN_OPTIONS,
                    value=COLUMN_OPTIONS[0]['value'],
                ),
            ], style={'flex': '1', 'margin-right': '12px'}),
            html.Div([
                html.H3("Scatter Color"),
                dcc.Dropdown(
                    id='scatter-mapbox-color-col',
                    options=SCATTER_COLOR_OPTIONS,
                    value=SCATTER_COLOR_OPTIONS[0]['value'],
                ),
            ], style={'flex': '1'}),
        ], style={'display': 'flex'}),
        html.Div([
            html.H3('Date Range'),
            dcc.RangeSlider(
                id='scatter-mapbox-date-range-slider',
                min=min_date,
                max=max_date,
                step=1,
                value=[min_date, max_date],
                marks={
                    min_date: dataset.min_date.strftime('%Y-%m-%d'),
                    max_date: dataset.max_date.strftime('%Y-%m-%d'),
                },
                tooltip={
                    "always_visible": True,
                    "transform": "ordinalToDateStr" # function in assets/utils.js
                },
                allowCross=False,
            ),
        ]),
        dcc.Graph(id='scatter-mapbox', style={'height': '80vh'})
    ])
