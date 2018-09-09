import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from dataframes import iris_df


iris_layout = html.Div([
            html.H2('IRIS Flower Data Visualisation'),
            html.Div([
                html.Div([dcc.Dropdown(
                    id='sepal',
                    options=[{'label': i.upper(), 'value': i.upper()} for i in iris_df.columns[1:5] if i.startswith('sepal')]
                )],className='five columns'),
                html.Div([dcc.Dropdown(
                    id='petal',
                    options=[{'label': i.upper(), 'value': i.upper()} for i in iris_df.columns[1:5] if i.startswith('petal')],
                    value='sepal_length'
                )],className='five columns')
            ],className='row')
        ])
