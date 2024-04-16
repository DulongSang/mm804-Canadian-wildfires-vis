from datetime import datetime
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

from Dataset import Dataset

NORTH_AMERICA_MAPBOX_SETTINGS = {
    'center': {"lat": 50, "lon": -100},
    'zoom': 3,
}

HEATMAP_COLUMN_OPTIONS = [
    {'label': 'Fire Weather Index', 'value': 'fwi'},
    {'label': 'Rate of Spread', 'value': 'ros'},
    {'label': 'Head Fire Intensity', 'value': 'hfi'},
    {'label': 'Estimated Area', 'value': 'estarea'}
]

def heatmap(app: Dash, dataset: Dataset):
    @app.callback(
        Output('heatmap', 'figure'),
        Input('heatmap-value-col', 'value'),
        Input('heatmap-date-range-slider', 'value'),
        Input('heatmap-source-checklist', 'value'),
        Input('heatmap-fuel-checklist', 'value'))
    def update(col: str, date_range: list[int], sources: list[str], fuels: list[str]):
        [min_date, max_date] = date_range
        min_date = datetime.fromordinal(min_date)
        max_date = datetime.fromordinal(max_date)
        df = dataset.filter(min_date=min_date, max_date=max_date, sources=sources, fuels=fuels)
        return px.density_mapbox(df, lat='lat', lon='lon', z=col, radius=5,
                            **NORTH_AMERICA_MAPBOX_SETTINGS,
                            mapbox_style="open-street-map")

    min_date = dataset.min_date.toordinal()
    max_date = dataset.max_date.toordinal()

    return html.Div([
        html.H3('Heatmap'),
        html.Div([
            html.H3("Value"),
            dcc.Dropdown(
                id='heatmap-value-col',
                options=HEATMAP_COLUMN_OPTIONS,
                value='estarea',
            ),
        ]),
        html.Div([
            html.H3('Date Range'),
            dcc.RangeSlider(
                id='heatmap-date-range-slider',
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
        html.Div([
            html.H3('Sources'),
            dcc.Checklist(
                id='heatmap-source-checklist',
                options=[{'label': source,'value': source} for source in dataset.source_types],
                value=dataset.source_types,
                inline=True,
                labelStyle={'margin-right': '12px'},
            ),
        ]),
        html.Div([
            html.H3('Fuels'),
            dcc.Checklist(
                id='heatmap-fuel-checklist',
                options=[{'label': fuel, 'value': fuel} for fuel in dataset.fuel_types],
                value=dataset.fuel_types,
                inline=True,
                labelStyle={'margin-right': '12px'},
            ),
        ]),
        dcc.Graph(id='heatmap', style={'height': '80vh'})
    ])
