import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import simfin as sf
from simfin.names import *
import dash_table
from dash.dependencies import Output, Input, State

sf.set_data_dir('~/simfin_data/')
api_key="ZxGEGRnaTpxMF0pbGQ3JLThgqY2HBL17"

df_income = sf.load(dataset='income', variant='annual', market='us',index=[TICKER])
df_income = df_income.drop(['Currency', 'SimFinId', 'Fiscal Period','Publish Date', 'Shares (Basic)',
                            'Abnormal Gains (Losses)','Abnormal Gains (Losses)','Net Extraordinary Gains (Losses)',
                            'Income (Loss) from Continuing Operations',
                            'Net Income (Common)','Pretax Income (Loss), Adj.','Report Date'], axis = 1)
df_income=df_income.fillna(0)

df_income[['Shares (Diluted)','Revenue','Cost of Revenue','Gross Profit','Operating Expenses',
           'Selling, General & Administrative','Research & Development','Operating Income (Loss)',
           'Non-Operating Income (Loss)','Pretax Income (Loss)','Income Tax (Expense) Benefit, Net','Net Income','Interest Expense, Net', 'Depreciation & Amortization']]= df_income[['Shares (Diluted)','Revenue','Cost of Revenue','Gross Profit','Operating Expenses',
             'Selling, General & Administrative','Research & Development','Operating Income (Loss)',
             'Non-Operating Income (Loss)','Pretax Income (Loss)','Income Tax (Expense) Benefit, Net',
             'Net Income','Interest Expense, Net', 'Depreciation & Amortization']].apply(lambda x: x / 1000000)

ticker="AAPL"
df1=df_income.loc[ticker]



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
        dcc.Tab(label='Income Statement', id='tab1', value= 'Tab1', children=[

            html.Div(
                html.H1('Income statement (m)')
            ),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df1.columns],
                data=df1.to_dict('records'),
            )

        ]),
        dcc.Tab(label='Balance Sheet', id='tab2', value= 'Tab2', children=["Heelo"]),
        dcc.Tab(label='Cash Flow Statement', id='tab3', value= 'Tab3', children=["yo"]),
        dcc.Tab(label='Intrinsic Value estimations', id='tab4', value= 'Tab4', children=["yo"]),

    ])
])



@app.callback(
Output('table', 'data'),
[Input("submit-button", "n_clicks")],
[State("stock-input", "value")])
def update_data(n_click, input_value):
    df1 = df_income.loc[input_value]
    data = df1.to_dict("records")
    return data

@app.callback(
Output('table', 'columns'),
[Input("submit-button", "n_clicks")],
[State("stock-input", "value")])
def update_columns(n_click, input_value):
        df1 = df_income.loc[input_value]
        columns =[{"name": i, "id": i} for i in df1.columns]
        return columns

if __name__ == '__main__':
    app.run_server()
