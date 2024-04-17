from dash import Dash, dcc, html, Input, Output
import plotly.express as px

from Dataset import Dataset

X_COL_OPTIONS = [
    {'label': 'Fuel', 'value': 'fuel'},
    {'label': 'Source', 'value': 'source'},
]

Y_COL_OPTIONS = [
    {'label': 'Estimated Area', 'value': 'estarea'},
    {'label': 'Fire Weather Index', 'value': 'fwi'},
    {'label': 'Rate of Spread', 'value': 'ros'},
    {'label': 'Head Fire Intensity', 'value': 'hfi'},
]

def box_plot(app: Dash, dataset: Dataset):
    @app.callback(
        Output('box-plot', 'figure'),
        Input('box-plot-group-col', 'value'),
        Input('box-plot-value-col', 'value'),
    )
    def update(x_col: str, y_col: str):
        fig = px.box(dataset.df, x=x_col, y=y_col)
        fig.update_layout(height=800)
        return fig

    
    return html.Div([
        html.H3('Box Plot'),
        html.Div([
            html.Div([
                html.H3("x-axis"),
                dcc.Dropdown(
                    id='box-plot-group-col',
                    options=X_COL_OPTIONS,
                    value=X_COL_OPTIONS[0]['value'],
                ),
            ], style={'flex': '1', 'margin-right': '12px'}),
            html.Div([
                html.H3("y-axis"),
                dcc.Dropdown(
                    id='box-plot-value-col',
                    options=Y_COL_OPTIONS,
                    value=Y_COL_OPTIONS[0]['value'],
                ),
            ], style={'flex': '1'}),
        ], style={'display': 'flex'}),
        dcc.Graph(id='box-plot')
    ])
