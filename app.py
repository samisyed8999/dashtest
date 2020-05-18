import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
server = app.server


app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div(
        html.H1('My Dashboard')
    ),

    html.Div([
        dcc.Input(id="stock-input", value="AAPL", type="text"),
        html.Button(id="submit-button", n_clicks=0, children="Submit")
    ]),


    dcc.Tabs(id="tabs", value='Tab1', children=[
        dcc.Tab(label='Income Statement', id='tab1', value= 'Tab1', children=["Hello"]),
        dcc.Tab(label='Balance Sheet', id='tab2', value= 'Tab2', children=["lol"]),
        dcc.Tab(label='Cash Flow Statement', id='tab3', value= 'Tab3', children=["yo"]),
        dcc.Tab(label='Intrinsic Value estimations', id='tab4', value= 'Tab4', children=["yo"]),
    ])
])


if __name__ == '__main__':
    app.run_server()
