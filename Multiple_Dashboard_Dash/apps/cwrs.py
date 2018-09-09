import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from datetime import datetime
import numpy as np
import pandas as pd

from app import app
from dataframes import cwrs_df

# Creating a new column in the dataframe.
# if coverage is not 100 than partial else complete
cwrs_df['Coverage_Level'] = np.where(
    cwrs_df['Coverage_Percentage'] != 100, 'Partial', 'Complete')

def get_year_month(pd_series):
    t = pd.to_datetime(str(pd_series))
    timestring = t.strftime('%Y%m')
    return int(timestring)


def sort_dates(cwrs_df):
    dt = []
    dates = cwrs_df['Svl_Date'].unique()
    for d in dates:
        t = pd.to_datetime(str(d))
        timestring = t.strftime('%Y%m')
        dt.append(int(timestring))
    dt = set(sorted(dt,reverse=True))
    month_dict={}
    for idx, v in enumerate(dt):
        month_dict[idx+1]=v
    return month_dict

#############################################
def get_coverage_level():
    coverage_level = list(cwrs_df['Coverage_Level'].unique())
    coverage_level.append('All')
    return coverage_level

##############################################################################
################ Creating the dash app #######################################
def onLoad_coverage_level_option():
    coverage_level_options = (
        [{'label':coveragelevel, 'value':coveragelevel} for coveragelevel in get_coverage_level()]
    )
    return coverage_level_options

def generate_table(dataframe, max_rows=10):
    return html.Table(
        [html.Tr([html.Th(col, style={'overflow':'hidden'}) for col in dataframe.columns])]+
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns]) for i in range(min(len(dataframe), max_rows))]
    )

#
def calculate_summary_table(cwrs_df):
    '''
    This function calculates summary regarding coverage level and return a html table
    '''
    results = cwrs_df.groupby(by=['Coverage_Level'])['Coverage_Level'].count()
    data = np.array([results['Complete'], results['Partial']])
    # creating a pandas dataframe
    summary = pd.DataFrame(
        data=[data],
        columns=['Completely Covered Zone', 'Partially Covered Zone'],
        index=[i for i in range(1)]
    )
    return summary

def generate_summary_table(cwrs_df):
    summary = calculate_summary_table(cwrs_df)
    # print(summary)
    table = html.Table(
        [html.Tr([html.Th(col) for col in summary.columns])]+
        [html.Tr([
            html.Td(summary.iloc[i][col]) for col in summary.columns
        ]) for i in range(1)]
    )
    return table

## Create a pie chart for the summary
def create_pie_chart(cwrs_df):
    tbl = calculate_summary_table(cwrs_df)
    # print(tbl.columns.values)
    figure = go.Figure(
                data= [go.Pie(  labels=tbl.columns.values,
                                values=tbl.values.tolist()[0],
                                hoverinfo='percent',
                                textinfo='value',
                                hole=0.6
                    )],
                layout= dict(title='Coverage Summary',
                            legend=dict(orientation='h',
                            y=1.15)
                        )
                )
    return figure

## Adding colour for each marker depending on condition
# colours = ['red' if val !=100 else 'green' for val in cwrs_df['Coverage_Percentage']]

def generate_graph(cwrs_df):
    figure = go.Figure(
                data=[
                    go.Scatter(x=cwrs_df['Svl_Date'],
                    y=cwrs_df['Coverage_Percentage'],
                    mode='markers',
                    text=cwrs_df['Name'],
                    marker=dict(
                        color=['red' if val !=100 else 'green' for val in cwrs_df['Coverage_Percentage']]
                    ))
                ],
                layout=go.Layout(
                    title='Surveillance and Percentage Coverage',
                    showlegend=False,
                    yaxis=dict(
                        range=[cwrs_df['Coverage_Percentage'].min()-10, cwrs_df['Coverage_Percentage'].max()+5]
                    )
                )
            )
    return figure

cwrs_layout = html.Div([
                html.Div([
                    # Header for the first row
                    html.Div(html.H2('Remote Sensing Surveillance Plan')),
                        # Second row with options and summary table
                        html.Div([
                            ###Dropdown menu
                            html.Div([
                                html.Label('Select Coverage Level'),
                                dcc.Dropdown(
                                    id='coverage_level',
                                    options=onLoad_coverage_level_option(),
                                    value='All'
                                )
                            ],className='two columns'),
                            # Summary table
                            html.Div([
                                html.Table(id='rs-summary-table',)
                            ], className='five columns')
                        ],className='row', style={'width':'98%', 'display':'inline-block'}),
                        # Third row with scatter plot and pie create_pie_chart
                        html.Div([
                            # Main graph
                            html.Div([
                                dcc.Graph(id='rs-graph')
                            ],className='seven columns'),
                            # # Pie chart
                            html.Div([
                                dcc.Graph(id='summary-pie-chart')
                            ],className='five columns')
                        ],className='row'),
                    html.Div(
                            html.Table(id='RS-complete-table',
                                       # style={'width':600,'margin-left':0,'margin-right':700},
                                       className='six columns'),
                                       style={'overflow':'auto', 'height':240})
                    ],className='row')
            ], style={'margin-left':10, 'margin-right':10, 'max_width':50000})

### Loading Complete table
@app.callback(
    Output(component_id='RS-complete-table', component_property='children'),
    [Input(component_id='coverage_level', component_property='value')]
)

def load_complete_table(coverage_level):
    if coverage_level == 'All' or coverage_level is None:
        return generate_table(cwrs_df, max_rows=20)
    else:
        return generate_table(cwrs_df[cwrs_df['Coverage_Level']==coverage_level], max_rows=20)

# Loading Summary table
@app.callback(
    Output(component_id='rs-summary-table', component_property='children'),
    [
        Input(component_id='coverage_level', component_property='value')
    ]
)

def update_rs_summary_table(coverage_level):
    if coverage_level:
        return generate_summary_table(cwrs_df)
#
## The graph not working with coverage level and slider
@app.callback(
    Output(component_id='rs-graph', component_property='figure'),
    [Input(component_id='coverage_level', component_property='value')]
)

def load_graph(selector):
    if selector =='All':
        figure = generate_graph(cwrs_df)
        return figure
    else:
        #cwrs_df['YearMonth'] = cwrs_df['Svl_Date'].apply(get_year_month)
        dff = cwrs_df[cwrs_df['Coverage_Level']==selector]
        figure_new = generate_graph(dff)
        return figure_new
#
@app.callback(
    Output(component_id='summary-pie-chart', component_property='figure'),
    [Input(component_id='coverage_level', component_property='value')]
)

def summary_pie_chart(coverage_level):
    if coverage_level:
        figure = create_pie_chart(cwrs_df)
        return figure
    else:
        return None
