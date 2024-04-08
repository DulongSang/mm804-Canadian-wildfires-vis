from typing import Literal

from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px


HOTSPOTS_FILE_PATH = "./hotspots.csv"

def chart(app: Dash, df: pd.DataFrame):
    @app.callback(
        Output('heatmap', 'figure'),
        Input('heatmap-col', 'value'),
        Input('date-range-slider', 'value'))
    def update_bar_chart(col: str, date_range: list[int]):
        

        return px.density_mapbox(df, lat='lat', lon='lon', z=col, radius=5,
                            center={"lat": 50, "lon": -100}, zoom=3,
                            mapbox_style="open-street-map")

    return html.Div([
        html.H3('Heatmap'),
        dcc.Dropdown(
            id='heatmap-col',
            options=[
                {'label': 'Fire Weather Index', 'value': 'fwi'},
                {'label': 'Rate of Spread', 'value': 'ros'},
                {'label': 'Fire Intensity', 'value': 'hfi'},
                {'label': 'Estimated Area', 'value': 'estarea'}
            ],
            value='estarea'
        ),
        dcc.RangeSlider(
            id='date-range-slider',
            min=0,
            max=100,
            step=1,
            value=[0, 100],
            marks={
                0: '2024-01-01',
                100: '2024-02-29'
            }
        ),
        dcc.Graph(id='heatmap', style={'height': '70vh'})
    ])


df = pd.read_csv(HOTSPOTS_FILE_PATH)

app = Dash()
app.layout = html.Div([
    html.H1('Canadian Wildfire Visulization'),
    chart(app, df)
])
app.run_server(port=24804)
