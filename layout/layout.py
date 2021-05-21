import dash_core_components as dcc
import dash_html_components as html

import random

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

    field_list = ['profit_target','leverage','minimum_trade']

    return html.Div(
        [
            html.Button(
                'Refresh Page', 
                id='refresh-stats',
                style={"margin-bottom": "15px"}
            ),

            html.Div([
                dcc.Input(
                    id=f"input_{field}",
                    type="text",
                    placeholder=f"{field}",
                    style={"margin-right": "15px"}
                ) for field in field_list
            ]),

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

def _generate_dropdown():

    forex_list, last_updated_time = _fetch_forex_pairs()
    current_forex = forex_list[0]

    dropdown_options = []

    for forex in forex_list:
        
        symbol = forex['symbol']
        width = forex['width']
        
        dropdown_options.append({
            'label': f"{symbol} - {width}",
            'value': symbol
        })

    margin_style = {"margin-top": 10}

    return html.Div([

        html.Div(
            [
                dcc.Dropdown(
                    id='currency-dropdown',
                    options=dropdown_options,
                    clearable=False,
                    searchable=False,
                    value=current_forex['symbol']
                ),
                dcc.Store(id='current-currency',data=current_forex['symbol'])
            ],
                style={"width": "15%"}
        ),

        html.Div(
            id='spread-value',
            style=margin_style
        ),

        html.Div(
            children=f"Candlestick width last updated: {last_updated_time}",
            style=margin_style
        )
    ])

def generate_layout():

    draw_config = {'modeBarButtonsToAdd': ['drawline','eraseshape']}

    return html.Div([
        _generate_profit_pip_calculator(),
        html.Hr(),
        _generate_dropdown(),
        _loading_figure_layout('candlestick-30d-fig', draw_config),
        _loading_figure_layout('candlestick-fullday-fig'),
        html.Hr(),
        _loading_figure_layout('tick-volatility-fig'),
        _loading_figure_layout('pip-size-histogram-fig'),
        html.Hr(),
        _loading_figure_layout('heatmap-changes-fig'),
        _loading_figure_layout('percentage-changes-fig'),
        _loading_figure_layout('close-price-histogram-fig'),
        html.Hr(),
        _loading_figure_layout('candlestick-today-fig', draw_config),
        _loading_figure_layout('rsi-fig'),
        _loading_figure_layout('bull-bear-fig')
    ])