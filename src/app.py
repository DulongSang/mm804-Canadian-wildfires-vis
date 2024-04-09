from datetime import datetime

from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px


HOTSPOTS_FILE_PATH = "./hotspots.csv"

def chart(app: Dash, df: pd.DataFrame):
    @app.callback(
        Output('heatmap', 'figure'),
        Input('heatmap-col', 'value'),
        Input('date-range-slider', 'value'),
        Input('source-checklist', 'value'),
        Input('fuel-checklist', 'value'))
    def update_bar_chart(col: str, date_range: list[int], sources: list[str], fuels: list[str]):
        [min_date, max_date] = date_range
        df_filtered = df[(df['rep_date'] >= datetime.fromordinal(min_date)) & (df['rep_date'] <= datetime.fromordinal(max_date))]
        df_filtered = df_filtered[df_filtered['source'].isin(sources)]
        df_filtered = df_filtered[df_filtered['fuel'].isin(fuels)]

        return px.density_mapbox(df_filtered, lat='lat', lon='lon', z=col, radius=5,
                            center={"lat": 50, "lon": -100}, zoom=3,
                            mapbox_style="open-street-map")

    min_date = datetime(2024, 1, 1).toordinal()
    max_date = datetime(2024, 3, 1).toordinal()

    sources = ['NASAwusa', 'NASA7', 'NASA6', 'NASA3', 'NASA2', 'NASAwcan', 'NASA_usa', 'NASA_can']
    fuels = ['D1', 'C6', 'C5', 'M1_50', 'farm', 'O1a', 'low_veg', 'C3', 'C4', 'C7', 'non_fuel', 'water', 'M1_35', 'M1_75', 'M1_65', 'C1', 'C2', 'M1_25', 'D2', 'O1b', 'S2', 'urban', 'M2_65', 'M2_50']

    return html.Div([
        html.H3('Heatmap'),
        dcc.Dropdown(
            id='heatmap-col',
            options=[
                {'label': 'Fire Weather Index', 'value': 'fwi'},
                {'label': 'Rate of Spread', 'value': 'ros'},
                {'label': 'Head Fire Intensity', 'value': 'hfi'},
                {'label': 'Estimated Area', 'value': 'estarea'}
            ],
            value='estarea'
        ),
        html.H3('Date Range'),
        dcc.RangeSlider(
            id='date-range-slider',
            min=min_date,
            max=max_date,
            step=1,
            value=[min_date, max_date],
            marks={
                min_date: '2024-01-01',
                max_date: '2024-03-01'
            }
        ),
        html.H3('Sources'),
        dcc.Checklist(
            id='source-checklist',
            options=[{'label': source, 'value': source} for source in sources],
            value=sources,
            inline=True
        ),
        html.H3('Fuels'),
        dcc.Checklist(
            id='fuel-checklist',
            options=[{'label': fuel, 'value': fuel} for fuel in fuels],
            value=fuels,
            inline=True
        ),
        dcc.Graph(id='heatmap', style={'height': '100vh'})
    ])


df = pd.read_csv(HOTSPOTS_FILE_PATH)
df['rep_date'] = pd.to_datetime(df['rep_date'])

app = Dash()
app.title = 'Wildfire Visulization'
app.layout = html.Div([
    html.H1('Wildfire Visulization'),
    chart(app, df)
])
app.run(port=24804, debug=True)
