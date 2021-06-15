import dash_core_components as dcc
import dash_html_components as html

def _fetch_forex_pairs():
    forex_pairs = []
    last_updated_time = ""

    file_path = "\\".join([
        'C:','Users','Tazeek','Desktop','Projects',
        'plotly-mt5-analysis','files','candlesticks_width.txt'
    ])

    with open(file_path) as f:
        for line in f.readlines():

            forex_data = line.split(':')
            if len(forex_data[0]) < 7:
                forex_pairs.append({
                    'symbol': forex_data[0],
                    'width': forex_data[1].rstrip()
                })
            else:
                last_updated_time = ":".join(forex_data[1:]).rstrip()
    
    return forex_pairs, last_updated_time

def _loading_figure_layout(fig_id, config=None):
    return dcc.Loading(
        type="default",
        children=html.Div([
            dcc.Graph(
                id=fig_id,
                config=config
            )
        ])
    )

def _generate_profit_pip_calculator():

    dropdown_options = []

    for currency in ['CAD','JPY','USD','GBP']:

        dropdown_options.append({
            'label': currency,
            'value': currency
        })

    return html.Div(
        [
            html.Div([
                dcc.Input(
                    id=f"input_{field}",
                    type="text",
                    placeholder=f"{field}",
                    style={"margin-right": "15px"}
                ) for field in ['target','leverage','trade']
            ]),

            html.Div([
                dcc.Dropdown(
                    id='settlement-currency',
                    options=dropdown_options,
                    clearable=False,
                    value='USD'
                ),

                
            ], style={"width": "5%", 'margin-top': 10}
            
            ),

            html.Button(
                'Calculate pip count', 
                id='start-calculation', 
                style={'margin-top': 10}
            ),

            html.Div(
                id='average-pip-text',
                children='Average pip per trade: 0',
                style={'margin-top': 10}
            )
        ]
    )

def _generate_candlesticks_info(last_updated_time):

    return html.Div([

        html.Div(
            id="last-updated-candlesticks",
            children=f"Candlestick width last updated: {last_updated_time}",
            style={"margin-top": 10}
        ),

        html.Button(
            'Update candlesticks stats', 
            id='update-candlesticks-stats',
            style={"margin-top": "15px"}
        ),
    ])


def _generate_dropdown(forex_list):

    current_forex = forex_list[0]

    dropdown_options = []

    for forex in forex_list:
        
        symbol = forex['symbol']
        width = forex['width']
        
        dropdown_options.append({
            'label': f"{symbol} - {width}",
            'value': symbol
        })

    return html.Div([

        html.Div(
            [
                dcc.Dropdown(
                    id='currency-dropdown',
                    options=dropdown_options,
                    clearable=False,
                    value=current_forex['symbol']
                ),
                dcc.Store(id='current-currency',data=current_forex['symbol']),
                dcc.Store(id='candlesticks-width', data=forex_list)
            ],
                style={"width": "15%"}
        ),

        html.Div(children=[
            html.Div(
                id='ask-value',
                style={"margin-top": 10}
            ),

            html.Div(
                id='bid-value',
                style={"margin-top": 10}
            ),
        ]),

        html.Button(
            'Refresh Page', 
            id='refresh-stats',
            style={"margin-top": "15px", "margin-bottom": "15px"}
        ),
    ])

def generate_layout():

    forex_list, last_updated_time = _fetch_forex_pairs()

    draw_config = {'modeBarButtonsToAdd': ['drawline','eraseshape', 'drawopenpath', 'drawrect']}

    return html.Div([

        _generate_profit_pip_calculator(),
        html.Hr(),
        _generate_candlesticks_info(last_updated_time),
        html.Hr(),
        _generate_dropdown(forex_list),

        dcc.Tabs(id='timeframe-tabs', value='high-timeframe', children=[

            dcc.Tab(label='High Timeframe (4H)', value='high-timeframe', children=[
                _loading_figure_layout('candlestick-4H-fig', draw_config),
                _loading_figure_layout('candlestick-today-stat'),
            ]),

            dcc.Tab(label='Price Activtiy', value='price-activtiy', children=[
                _loading_figure_layout('tick-volatility-fig'),
                _loading_figure_layout('heatmap-price-changes-fig'),
                _loading_figure_layout('percentage-changes-fig')
            ]),

            dcc.Tab(label='Analysis Timeframe (1H)', value='low-timeframe', children=[
                _loading_figure_layout('candlestick-1H-fig', draw_config),
                _loading_figure_layout('rsi-1H-fig'),
                _loading_figure_layout('bull-bear-1H-fig'),
            ]),

            dcc.Tab(label='Entry Timeframe (15M)', value='medium-timeframe', children=[
                _loading_figure_layout('candlestick-15M-fig', draw_config),
                _loading_figure_layout('rsi-15M-fig'),
                _loading_figure_layout('bull-bear-15M-fig')
            ])

        ])
    ])