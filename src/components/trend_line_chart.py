from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

from Dataset import Dataset

GROUP_COL_OPTIONS = [
    {'label': 'All', 'value': 'all'},
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

AGGREGATE_TYPE_OPTIONS = [
    {'label': 'Sum', 'value': 'sum'},
    {'label': 'Mean', 'value': 'mean'},
    {'label': 'Median', 'value': 'median'},
]

# daily_count = dataset.df.groupby(dataset.df['rep_date'].dt.date).size()
# fig.add_trace(
#     go.Scatter(x=list(daily_count.index), y=list(daily_count.values))
# )

def trend_line_chart(app: Dash, dataset: Dataset):
    @app.callback(
        Output('trend-line-chart', 'figure'),
        Input('trend-line-group-col', 'value'),
        Input('trend-line-value-col', 'value'),
        Input('trend-line-aggregate-type', 'value'),
    )
    def update_line_chart(group_col: str, value_col: str, aggregate_type: str):
        if group_col == 'all':
            grouped = [('all', dataset.df)]
        else:
            grouped = dataset.df.groupby(group_col)
        
        fig = go.Figure()
        for group, df in grouped:
            daily_group = df.groupby(df['rep_date'].dt.date)
            if value_col == 'hotspots':
                daily_value = daily_group.size()
            else:
                if aggregate_type == 'sum':
                    daily_value = daily_group[value_col].sum()
                elif aggregate_type == 'mean':
                    daily_value = daily_group[value_col].mean()
                elif aggregate_type == 'median':
                    daily_value = daily_group[value_col].median()
                else:
                    raise ValueError(f'Invalid aggregate type: {aggregate_type}')

            daily_value = daily_value.fillna(0)
            fig.add_trace(go.Scatter(x=list(daily_value.index), y=list(daily_value.values), name=group))

        # range slider, ref: https://plotly.com/python/range-slider/
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
        return fig


    @app.callback(
        Output('trend-line-aggregate-type', 'disabled'),
        Input('trend-line-value-col', 'value'),
    )
    def update_aggregate_type_options(value_col: str):
        # disable aggregate type dropdown if value_col is 'hotspots'
        return value_col == 'hotspots'


    return html.Div([
        html.H3('Trend Line Chart'),
        html.Div([
            html.Div([
                html.H3("Group By"),
                dcc.Dropdown(
                    id='trend-line-group-col',
                    options=GROUP_COL_OPTIONS,
                    value=GROUP_COL_OPTIONS[0]['value'],
                ),
            ], style={'flex': '1', 'margin-right': '12px'}),
            html.Div([
                html.H3("Value"),
                dcc.Dropdown(
                    id='trend-line-value-col',
                    options=VALUE_COL_OPTIONS,
                    value=VALUE_COL_OPTIONS[0]['value'],
                ),
            ], style={'flex': '1', 'margin-right': '12px'}),
            html.Div([
                html.H3("Aggregate Type"),
                dcc.Dropdown(
                    id='trend-line-aggregate-type',
                    options=AGGREGATE_TYPE_OPTIONS,
                    value=AGGREGATE_TYPE_OPTIONS[0]['value'],
                ),
            ], style={'flex': '1'}),
        ], style={'display': 'flex'}),
        dcc.Graph(id='trend-line-chart')
    ])
