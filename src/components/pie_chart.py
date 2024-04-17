from dash import Dash, dcc, html, Input, Output
import plotly.express as px

from Dataset import Dataset

GROUP_COL_OPTIONS = [
    {'label': 'Fuel', 'value': 'fuel'},
    {'label': 'Source', 'value': 'source'},
]

VALUE_COL_OPTIONS = [
    {'label': 'Number of Hotspots', 'value': 'hotspots'},
    {'label': 'Estimated Area', 'value': 'estarea'},
    {'label': 'Fire Weather Index', 'value': 'fwi'},
    {'label': 'Rate of Spread', 'value': 'ros'},
    {'label': 'Head Fire Intensity', 'value': 'hfi'},
]

def pie_chart(app: Dash, dataset: Dataset):
    @app.callback(
        Output('pie-chart', 'figure'),
        Input('pie-chart-group-col', 'value'),
        Input('pie-chart-value-col', 'value'),
    )
    def update(group_col: str, value_col: str):
        if value_col == 'hotspots':
            df = dataset.df.groupby(group_col).size().reset_index(name='hotspots')
        else:
            df = dataset.df
        fig = px.pie(df, names=group_col, values=value_col)
        fig.update_layout(height=800, uniformtext_minsize=12, uniformtext_mode='hide')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig

    
    return html.Div([
        html.H3('Pie Chart'),
        html.Div([
            html.Div([
                html.H3("Group By"),
                dcc.Dropdown(
                    id='pie-chart-group-col',
                    options=GROUP_COL_OPTIONS,
                    value=GROUP_COL_OPTIONS[0]['value'],
                ),
            ], style={'flex': '1', 'margin-right': '12px'}),
            html.Div([
                html.H3("Value"),
                dcc.Dropdown(
                    id='pie-chart-value-col',
                    options=VALUE_COL_OPTIONS,
                    value=VALUE_COL_OPTIONS[0]['value'],
                ),
            ], style={'flex': '1'}),
        ], style={'display': 'flex'}),
        dcc.Graph(id='pie-chart')
    ])
