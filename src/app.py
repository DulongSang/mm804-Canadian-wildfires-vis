import argparse
from dash import Dash, html

from Dataset import Dataset
from components.box_plot import box_plot
from components.heatmap import heatmap
from components.pie_chart import pie_chart
from components.scatter_mapbox import scatter_mapbox
from components.trend_line_chart import trend_line_chart

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--hotspots-file-path', type=str, required=True)
    parser.add_argument('--port', type=int, default=24804)
    parser.add_argument('--debug', action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    dataset = Dataset(args.hotspots_file_path)

    app = Dash()
    app.title = 'CWFIS Wildfire Visualization'
    app.layout = html.Div([
        html.H1('CWFIS Wildfire Visualization'),
        heatmap(app, dataset),
        scatter_mapbox(app, dataset),
        trend_line_chart(app, dataset),
        pie_chart(app, dataset),
        box_plot(app, dataset),
    ])
    app.run(port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
