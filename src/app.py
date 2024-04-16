import argparse
from datetime import datetime
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

from Dataset import Dataset
from components.heatmap import heatmap
from components.scatter_mapbox import scatter_mapbox

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--hotspots-file-path', type=str, required=True)
    parser.add_argument('--port', type=int, default=24804)
    parser.add_argument('--debug', action='store_true')
    return parser.parse_args()


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
