import dash
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

df_cashflow = sf.load_cashflow(variant='annual', market='us', index=[TICKER, FISCAL YEAR])
df_freecashflow = pd.DataFrame()
#df_freecashflow['Year'] = df_cashflow['Fiscal Year'].copy()
df_freecashflow['FCF'] = df_cashflow[NET_CASH_OPS] + df_cashflow[CAPEX]
df_freecashflow['FCF']= df_freecashflow['FCF'].apply(lambda x: x / 1000000)
transposed_table = df_freecashflow.loc['AAPL']
transposed_table = transposed_table.transpose()
# for some reason transpose just does not work, take out transpose and there are two columns year
# and cash flow but for some reason when transposed the output is the same for each column. 

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([

    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Cash Flow Statement', value='tab-1'),

    ]),

    html.Div(id='tabs-content'),
])


@app.callback(Output('tabs-content', 'children'),
                   [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Div(
                html.H3('Cashflow Statement (m)')
            ),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in transposed_table.columns],
                data=transposed_table.to_dict('records'),
            )
        ])
if __name__ == '__main__':
    app.run_server()


