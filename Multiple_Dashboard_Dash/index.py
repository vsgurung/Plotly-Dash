
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import gapminder, iris, mpg


# Function to return the salutation.
def greeting():
    import datetime
    current_time = datetime.datetime.now()
    if current_time.hour < 12:
        return 'Good Morning'
    elif 12 <= current_time.hour <18:
        return 'Good Afternoon'
    else:
        return 'Good Evening'
# Creating a layout for the landing pageself.
app.title = 'Welcome'
app.layout = html.Div([
                dcc.Location(id='url',refresh=False),
                html.Div([
                    html.H2(f'{greeting()}, Welcome to multi page demo'),
                    html.H3('Following dashboards are available. Click on the link to navigate to the page')],
                            className='row', style={'display':'inline-block'}),
                html.Div([
                    html.Div([dcc.Link('Gapminder', href='/apps/gapminder')],className='three columns'),
                    html.Div([dcc.Link('Iris', href='/apps/iris')],className='three columns'),
                    html.Div([dcc.Link('MPG', href='/apps/mpg')],className='three columns')
                    ], className='row'),
                html.Div(id='page-content')
            ],className='container', style={'width':'98%','margin-left':10, 'margin-right':10, 'max-width':50000})

## All the callbacks will be made here for navigating to various pages

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/gapminder':
         return gapminder.gapminder_layout
    elif pathname == '/apps/iris':
         return iris.iris_layout
    elif pathname == '/apps/mpg':
        return mpg.mpg_layout
    else:
        return ''

# This page will drive all the other pages
if __name__ == '__main__':
    app.run_server(debug=True)
