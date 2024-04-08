import argparse
from datetime import datetime
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

from Dataset import Dataset


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--hotspots-file-path', type=str, required=True)
    parser.add_argument('--port', type=int, default=24804)
    parser.add_argument('--debug', action='store_true')
    return parser.parse_args()


def heatmap(app: Dash, dataset: Dataset):
    @app.callback(
        Output('heatmap', 'figure'),
        Input('heatmap-col', 'value'),
        Input('date-range-slider', 'value'),
        Input('source-checklist', 'value'),
        Input('fuel-checklist', 'value'))
    def update_bar_chart(col: str, date_range: list[int], sources: list[str], fuels: list[str]):
        [min_date, max_date] = date_range
        min_date = datetime.fromordinal(min_date)
        max_date = datetime.fromordinal(max_date)
        df = dataset.filter(min_date=min_date, max_date=max_date, sources=sources, fuels=fuels)
        return px.density_mapbox(df, lat='lat', lon='lon', z=col, radius=5,
                            center={"lat": 50, "lon": -100}, zoom=3,
                            mapbox_style="open-street-map")

    min_date = dataset.min_date.toordinal()
    max_date = dataset.max_date.toordinal()

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
                min_date: dataset.min_date.strftime('%Y-%m-%d'),
                max_date: dataset.max_date.strftime('%Y-%m-%d'),
            }
        ),
        html.H3('Sources'),
        dcc.Checklist(
            id='source-checklist',
            options=[{'label': source, 'value': source} for source in dataset.source_types],
            value=dataset.source_types,
            inline=True
        ),
        html.H3('Fuels'),
        dcc.Checklist(
            id='fuel-checklist',
            options=[{'label': fuel, 'value': fuel} for fuel in dataset.fuel_types],
            value=dataset.fuel_types,
            inline=True
        ),
        dcc.Graph(id='heatmap', style={'height': '80vh'})
    ])


def scatter_mapbox(app: Dash, dataset: Dataset):
    fig = px.scatter_mapbox(dataset.df, lat="lat", lon="lon", size='estarea', size_max=15,
                        color='fuel',
                        center={"lat": 50, "lon": -100}, zoom=3,
                        mapbox_style="open-street-map")
    return html.Div([
        html.H3('Scatter Mapbox'),
        dcc.Graph(id='scatter-mapbox', figure=fig, style={'height': '80vh'})
    ])

def line_chart(app: Dash, dataset: Dataset):
    fig = go.Figure()
    daily_count = dataset.df.groupby(dataset.df['rep_date'].dt.date).size().sort_index()
    fig.add_trace(
        go.Scatter(x=list(daily_count.index), y=list(daily_count.values)))
    
    fig.update_layout(
        height=800,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    return html.Div([
        html.H3('Line Chart'),
        dcc.Graph(id='line-chart', figure=fig)
    ])


def pie_chart(app: Dash, dataset: Dataset):
    fig = px.pie(dataset.df, names='source', title='Sources of Wildfires')
    fig.update_layout(height=800)
    return html.Div([
        html.H3('Pie Chart'),
        dcc.Graph(id='pie-chart', figure=fig)
    ])


def box_plot(app: Dash, dataset: Dataset):
    fig = px.box(dataset.df, x='fuel', y='estarea', title='Estimated Area by Source')
    fig.update_layout(height=800)
    return html.Div([
        html.H3('Box Plot'),
        dcc.Graph(id='box-plot', figure=fig)
    ])


def main():
    args = parse_args()
    dataset = Dataset(args.hotspots_file_path)

    app = Dash()
    app.title = 'Wildfire Visualization'
    app.layout = html.Div([
        html.H1('Wildfire Visualization'),
        heatmap(app, dataset),
        scatter_mapbox(app, dataset),
        line_chart(app, dataset),
        pie_chart(app, dataset),
        box_plot(app, dataset),
    ])
    app.run(port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
