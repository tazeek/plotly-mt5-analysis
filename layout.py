import dash_core_components as dcc
import dash_html_components as html

def _generate_dropdown():

    forex_list = ['GBPUSD','EURGBP','EURUSD','AUDUSD','AUDJPY','USDJPY']

    dropdown_options = [{'label': currency, 'value': currency} for currency in forex_list]

    return html.Div([
        dcc.Dropdown(
            id='currency-dropdown',
            options=dropdown_options,
            value='GBPUSD'
        ),
        dcc.Store(id='current-currency',data='GBPUSD')
        ],
        style={"width": "10%"}
    )

def _generate_candlestick_monthly():

    return dcc.Loading(
        type="default",
        children=html.Div([
            dcc.Graph(
                id="candlestick-30d-fig"
            )
        ])
    )

def _generate_tick_volatility():

    return dcc.Loading(
        type="default",
        children=html.Div([
            dcc.Graph(
                id='tick-volatility-fig'
            )
        ])
    )

def _generate_pip_size_histogram():
    return dcc.Loading(
        type="default",
        children=html.Div([
            dcc.Graph(
                id='pip-size-histogram-fig'
            )
        ])
    )

def generate_layout():

    return html.Div([
        _generate_dropdown(),
        _generate_candlestick_monthly(),
        _generate_tick_volatility(),
        _generate_pip_size_histogram()
    ])