import dash
import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import simfin as sf
from simfin.names import *
import dash_table
from dash.dependencies import Output, Input, State

from test1 import python
from test2 import callbacks

python()
callbacks()

app = dash.Dash(__name__)
server = app.server
app.title = 'Financial Statements'
app.layout = html.Div([
    html.Div([
        html.H2('Fundemental Analysis'),
        html.Img(src="/assets/stock-icon.png")
    ], className="banner"),

    html.Div([
        dcc.Input(id="stock-input", value=ticker, type="text"),
        html.Button(id="submit-button", n_clicks=0, children="Submit", className="ticker2")
    ], className="ticker1"),

    html.Div([
        html.A(html.Button(id="logout-button", n_clicks=0, children="Log Out", className="logout2"),
            href = 'https://testsami999.herokuapp.com/logout/')
    ], className="logout1"),


    dcc.Tabs(id="tabs", value='Tab1', className='custom-tabs-container', children=[
        dcc.Tab(label='Income Statement', id='tab1', value= 'Tab1', selected_className='custom-tab--selected', children=[

            html.Div(
                html.H3('Income statement (m)')
            ),
            dash_table.DataTable(
                style_cell={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                    },
                id='table',
                columns=[{"name": i, "id": i} for i in df1.columns],
                data=df1.to_dict('records'),
            ),

            html.Div(
                html.H3('Key Ratios %')
            ),
            dash_table.DataTable(
                id='table2',
                columns=[{"name": i, "id": i} for i in df2.columns],
                data=df2.to_dict('records'),
            )

        ]),
        dcc.Tab(label='Balance Sheet', id='tab2', value= 'Tab2', selected_className='custom-tab--selected' ,children=[

            html.Div(
                html.H3('Balance Sheet (m)')
            ),
            dash_table.DataTable(
                id='table3',
                columns=[{"name": i, "id": i} for i in df3.columns],
                data=df3.to_dict('records'),
            ),
        ]),
        dcc.Tab(label='Cash Flow Statement', id='tab3', value= 'Tab3',selected_className='custom-tab--selected',  children=["yo"]),
        dcc.Tab(label='Intrinsic Value estimations', id='tab4', value= 'Tab4', selected_className='custom-tab--selected',  children=["yo"]),

    ])
])



if __name__ == '__main__':
    app.run_server()


