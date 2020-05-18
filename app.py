########Imports#######################################################################################################
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import seaborn as sns
from dash.dependencies import Output, Input, State
import pandas as pd
import simfin as sf
from simfin.names import *
import os
import dash_table

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div(
        html.H1('My Dashboard')
    ),

    html.Div([
        dcc.Input(id="stock-input", value=ticker, type="text"),
        html.Button(id="submit-button", n_clicks=0, children="Submit")
    ]),


    dcc.Tabs(id="tabs", value='Tab1', children=[
        dcc.Tab(label='Income Statement', id='tab1', value= 'Tab1', children=[]),
        dcc.Tab(label='Balance Sheet', id='tab2', value= 'Tab2', children=[]),
        dcc.Tab(label='Cash Flow Statement', id='tab3', value= 'Tab3', children=["yo"]),
        dcc.Tab(label='Intrinsic Value estimations', id='tab4', value= 'Tab4', children=["yo"]),

    ])
])
##########Run############################################################################################################################
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False, dev_tools_props_check=False)
