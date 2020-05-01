#Perform basic imports
import dash
import dash_auth #pip install dash-auth / required for Passcode Authorization
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output, State  
import pandas_datareader.data as pdr
from datetime import datetime       
import os
import pandas as pd 
import yfinance as yf  #pip install yfinance / required to access live stock data

yf.pdr_override()

USERNAME_PASSWORD_PAIRS = [
    ['JamesBond', '007'],['username', 'password']
]
#os.environ["IEX_API_KEY"] = "pk_b9fad1b9686e425092b7ba6a52471ea1"

#Application launch
app = dash.Dash() 
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
server = app.server

nsdq = pd.read_csv('data/NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace = True)
options = []

for tic in nsdq.index:
    #{'label':'user sees', 'value' : 'script sees' }
    options.append({'label':'{} {}'.format(tic,nsdq.loc[tic]['Name']), 'value':tic})


#Create a Div to contain the basic headers( H1 and H3 ), an input box and the graph
app.layout = html.Div(style={'backgroundColor':'#23272c'},children=[
    html.H1('Stock Ticker Dashboard'),
    html.Div([
        html.H3('Select a stock symbol', style = {'paddingRight':'30px','color':'#687c0b'}),
        dcc.Dropdown(
                id='my_stock_picker', #Input box ID
                options = options,
                value=['TSLA'],
                multi= True
                )
    ], style={'display':'inline-block', 'verticalAlign':'top', 'width:':'30%','color':'#0E85AF'}),
    html.Div([
        html.H3( 'Select a Start and End Date:'),
        dcc.DatePickerRange(
            id='my_date_picker',
            min_date_allowed = datetime(2015,1,1),
            max_date_allowed = datetime.today(),
            start_date = datetime(2018,1,1),
            end_date = datetime.today()
                                    
            )
    ], style={'display':'inline-block'}),
    
    html.Div([
            html.Button(id='submit-button',
                        n_clicks=0,
                        children='Submit',
                        style={'fontSize':24, 'marginLeft':'30px'}
            ),
    ],style={'display':'inline-block'}),

    dcc.Graph(
        id='my_graph',        #Graph ID
        figure={
            'data':[
                {'x':[1,2], 'y':[3,1]}
            ]
        }
    )
])

#Add a callback function
@app.callback(
    Output('my_graph', 'figure'),
    [Input('submit-button','n_clicks')],
    [State('my_stock_picker','value'),
    State('my_date_picker', 'start_date'),
    State('my_date_picker', 'end_date')])

def update_graph(n_clicks,stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    traces = []
    for tic in stock_ticker:
        df = pdr.get_data_yahoo(tic,start,end) 
        traces.append({'x': df.index, 'y': df['Close'], 'name':tic})
    fig = {
        'data': traces,
        'layout':{'title':', '.join(stock_ticker)+' Closing Prices'} 
    }
    return fig

#Server clause
if __name__ == '__main__':
    app.run_server()
