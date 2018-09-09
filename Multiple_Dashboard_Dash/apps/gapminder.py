import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from app import app
from dataframes import gapminder_df # importing from dataframes.py

# Getting the layout
gapminder_layout = html.Div([
            dcc.Graph(id='graph-with-slider'),
            dcc.Slider(
                id='year-slider',
                min=gapminder_df['year'].min(),
                max=gapminder_df['year'].max(),
                value=gapminder_df['year'].min(),
                step=None,
                marks={str(year):str(year) for year in gapminder_df['year'].unique()}
            )
        ])

# Setting callback for this app
@app.callback(Output('graph-with-slider', 'figure'),
              [Input('year-slider','value')]
            )
def update_graph(selected_year):
    filtered_df = gapminder_df[gapminder_df['year']==selected_year]
    traces = []
    for i in filtered_df['continent'].unique():
        df_by_continent = filtered_df[filtered_df['continent']==i]
        traces.append(
            go.Scatter(
                x=df_by_continent['gdp_per_capita'],
                y=df_by_continent['life_expectancy'],
                text=df_by_continent['country'],
                opacity=0.7,
                mode='markers',
                marker={
                        'size':15,
                        'line':{
                                'width':0.5,
                                'color':'white'
                                }
                        },
                name=i
            )
        )

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'GDP Per Capita'},
            yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }
