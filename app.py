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

########Python###############################################################################################
sns.set_style("whitegrid")
sf.set_data_dir('~/simfin_data/')
api_key="ZxGEGRnaTpxMF0pbGQ3JLThgqY2HBL17"

#######Income Statement########################################################################################
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

#######Key Ratios###################################################################################################################
df_negative = df_income
df_negative[['Cost of Revenue', 'Research & Development','Operating Expenses', 'Selling, General & Administrative', 'Income Tax (Expense) Benefit, Net', 'Depreciation & Amortization','Interest Expense, Net']] = df_negative[['Cost of Revenue', 'Research & Development','Operating Expenses', 'Selling, General & Administrative','Income Tax (Expense) Benefit, Net', 'Depreciation & Amortization', 'Interest Expense, Net']].apply(lambda x: x * -1)
df_signals = pd.DataFrame(index=df_negative.index)
df_signals['Fiscal Year']=df_negative['Fiscal Year']
df_signals['Gross Profit Margin %']=round((df_negative['Gross Profit'] / df_negative['Revenue']) *100,2)
df_signals['SGA Of Gross Profit']=round((df_negative['Selling, General & Administrative'] / df_negative['Gross Profit']) *100,2)
df_signals['R&D Of Gross Profit']=round((df_negative['Research & Development'] / df_negative['Gross Profit']) *100,2)
df_signals['Operating margin ratio']=round((df_negative['Operating Income (Loss)'] / df_negative['Revenue']) *100,2)
df_signals['Interest Coverage']=round((df_negative['Operating Income (Loss)'] / df_negative['Interest Expense, Net']) ,2)
df_signals['Taxes paid']=round((df_negative['Income Tax (Expense) Benefit, Net'] / df_negative['Pretax Income (Loss)']) *100,2)
df_signals['Net income margin']=round((df_negative['Net Income'] / df_negative['Revenue']) *100,2)
df2=df_signals.loc[ticker]

###########Balance Sheet########################################################################################################
df_balance = sf.load_balance(variant='annual', market='us', index=[TICKER])
df_balance = df_balance.drop(['Currency', 'SimFinId', 'Fiscal Period','Publish Date', 'Shares (Basic)','Report Date'], axis = 1)
df_balance=df_balance.fillna(0)
df_balance=df_balance.apply(lambda x: x / 1000000)
df3 = df_balance.loc[ticker]

########### Initiate the app
app = dash.Dash(__name__)
server = app.server
#app.title=tabtitle

########### Set up the layout
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
            ),

            html.Div(
                html.H1('Key Ratios %')
            ),
            dash_table.DataTable(
                id='table2',
                columns=[{"name": i, "id": i} for i in df2.columns],
                data=df2.to_dict('records'),
            )
        ]),
        dcc.Tab(label='Balance Sheet', id='tab2', value= 'Tab2', children=[

            html.Div(
                html.H1('Balance Sheet (m)')
            ),
            dash_table.DataTable(
                id='table3',
                columns=[{"name": i, "id": i} for i in df3.columns],
                data=df3.to_dict('records'),
            ),


        ]),
        dcc.Tab(label='Cash Flow Statement', id='tab3', value= 'Tab3', children=["yo"]),
        dcc.Tab(label='Intrinsic Value estimations', id='tab4', value= 'Tab4', children=["yo"]),

    ])
])


############Callbacks Net income#################################################################################################
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
    
#############Callbacks Key ratios#################################################################################################
@app.callback(
Output('table2', 'data'),
[Input("submit-button", "n_clicks")],
[State("stock-input", "value")])
def update_data(n_click, input_value):
    df2 = df_signals.loc[input_value]
    data = df2.to_dict("records")
    return data

@app.callback(
Output('table2', 'columns'),
[Input("submit-button", "n_clicks")],
[State("stock-input", "value")])
def update_columns(n_click, input_value):
        df2 = df_signals.loc[input_value]
        columns =[{"name": i, "id": i} for i in df2.columns]
        return columns

##############Callbacks Balance Sheet##########################################################################################
@app.callback(
Output('table3', 'data'),
[Input("submit-button", "n_clicks")],
[State("stock-input", "value")])
def update_data(n_click, input_value):
    df3 = df_balance.loc[input_value]
    data = df3.to_dict("records")
    return data

@app.callback(
Output('table3', 'columns'),
[Input("submit-button", "n_clicks")],
[State("stock-input", "value")])
def update_columns(n_click, input_value):
        df3 = df_balance.loc[input_value]
        columns =[{"name": i, "id": i} for i in df3.columns]
        return columns

##########Run############################################################################################################################
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False, dev_tools_props_check=False)
