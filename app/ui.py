import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import requests

app = dash.Dash()
logger = app.server.logger


# get available series
url = os.environ['API_URL']
response = requests.get(f'{url}/series')
series = {i: j for i, j in enumerate(response.json())}

def serve_layout():
    return html.Div([
        html.Div([

            html.Div([
                dcc.Dropdown(
                    id='timeseries-dropdown',
                    options=[{
                        'label': value['id'] + ':' + value['series'],
                        'value': key} for key, value in series.items()],
                    value=0,
                    placeholder='Select a timeseries...'
                ),
                html.Div(id='output-container')
            ],
            style={'width': '49%', 'display': 'inline-block'})
        ], style={
            'borderBottom': 'thin lightgrey solid',
            'backgroundColor': 'rgb(250, 250, 250)',
            'padding': '10px 5px'
        }),

        html.Div([
            dcc.Graph(
                id='timeseries',
                hoverData={'points': [{'customdata': 'Japan'}]}
            )
        ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),
    ])

app.layout = serve_layout


@app.callback(
    dash.dependencies.Output('timeseries', 'figure'),
    [dash.dependencies.Input('timeseries-dropdown', 'value')])
def update_graph(value):
    if value is None:
        return {}

    response = requests.get(f'{url}/{series[value]["id"]}/{series[value]["series"]}')
    if not response.ok:
        raise ValueError(response.status_code)

    df = pd.DataFrame.from_dict(response.json())

    return {
        'data': [go.Scatter(
            x=df['t'],
            y=df['v'],
            mode='lines+markers'
        )],
        'layout': {
            # 'height': 225,
            'margin': {'l': 30, 'b': 30, 'r': 30, 't': 30},
            'yaxis': {'type': 'linear'},
            'xaxis': {'showgrid': True}
        }
    }

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8000)