from currency_analysis import load_forex_pairs

import dash_core_components as dcc
import dash_html_components as html

def _loading_figure_layout(fig_id, config=None, style=None):
    return dcc.Loading(
        type="default",
        children=html.Div([
            dcc.Graph(
                id=fig_id,
                config=config,
                style=style
            )
        ])
    )

def _generate_profit_percentage_graph():

    return html.Div([
        html.H1(
            children="Profit aim (percentage)"
        ),

        html.Div([
            dcc.Input(
                id=f"input_profit_target",
                type="text",
                placeholder="Enter profit target",
                style={"margin-right": "15px"}
            )
        ]),

        html.Button(
                'Display', 
                id='show-graph-profit',
                style={"margin-top": "15px", "margin-bottom": "15px"}
            )

    ])

def _generate_currency_correlation_input():

    return html.Div([
        html.H1(
            children="Currency correlation"
        ),

        html.Div([
            dcc.Input(
                id=f"input_currencies_list",
                type="text",
                placeholder="Symbols (seperated by ,)",
                style={"margin-right": "15px", "width": "30%"}
            )
        ]),

        html.Button(
            'Calculate', 
            id='show-correlation-heatmap',
            style={"margin-top": "15px", "margin-bottom": "15px"}
        )

    ]) 

def _generate_profit_pip_calculator():

    profit_loss_rm_dict = {
        'balance': 0.00,
        'percentage_target': 30,
        'percentage_loss': 20
    }

    leverage_trade_dict = {
        'leverage': 0.01,
        'trade_count': 1
    }

    return html.Div(
        [
            html.H1(
                children="Risk Management Calculator"
            ),

            html.Div([
                dcc.Input(
                    id=f"input_{field}",
                    type="text",
                    placeholder=f"{field}",
                    value=f"{value}",
                    style={"margin-right": "15px"}
                ) for field,value in profit_loss_rm_dict.items()
            ]),

            html.Div([
                dcc.Input(
                    id=f"input_{field}",
                    type="text",
                    placeholder=f"{field}",
                    value=f"{value}",
                    style={"margin-right": "15px"}
                ) for field,value in leverage_trade_dict.items()
            ],
                style={'margin-top': 10}
            ),

            html.Button(
                'Calculate', 
                id='start-profit-calculation', 
                style={'margin-top': 10}
            ),

            html.Div(
                id='profit-target',
                children='Target balance (0% increase): 0',
                style={'margin-top': 10}
            ),

            html.Div(
                id='loss-bound',
                children='Minimum balance (0% loss tolerance): 0',
                style={'margin-top': 10}
            )
        ]
    )

def _generate_dropdown(forex_list):

    current_forex = forex_list[0]

    dropdown_options = []

    for symbol in forex_list:
        
        dropdown_options.append({
            'label': f"{symbol}",
            'value': symbol
        })

    return html.Div([

        html.Div(
            [
                dcc.Dropdown(
                    id='currency-dropdown',
                    options=dropdown_options,
                    clearable=False,
                    value=current_forex
                ),
                dcc.Store(id='current-currency',data=current_forex),
                dcc.Store(id='candlesticks-width', data=forex_list)
            ],
                style={"width": "10%", "margin-top": 10}
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

def _generate_points_percentage_graph():
    return html.Div(
        [
            html.H1(
                children="Points aim (Certain profit)"
            ),

            html.Div([
                dcc.Input(
                    id=f"input_{field}",
                    type="text",
                    placeholder=f"Enter {field}",
                    style={"margin-right": "15px"}
                ) for field in ['amount', 'volume']
            ]),

            html.Button(
                'Display', 
                id='show-graph-points',
                style={"margin-top": "15px", "margin-bottom": "15px"}
            )
        ]
    )

def _generate_download_button():
    return html.Div(
        [
            html.Button(
                "Download volume data", 
                id="download-volume-data", 
                style={"margin-top": "15px", "margin-bottom": "15px"}
            ), 
            dcc.Download(id="download-volume-begin"),

            html.Button(
                "Download today economic events", 
                id="download-today-economic", 
                style={"margin-top": "15px", "margin-bottom": "15px", "margin-left": "15px"}
            ), 
            dcc.Download(id="download-economic-begin")
        ]
    )

def generate_layout():

    forex_list = load_forex_pairs()

    draw_config = {'modeBarButtonsToAdd': ['drawline','eraseshape', 'drawopenpath', 'drawrect']}
    hide_display = {'display':'none'}

    return html.Div([

        dcc.Tabs(id='analysis-tabs', value='risk-management-tab', children=[
            
            dcc.Tab(label='Risk Management', value='risk-management-tab', children=[
                _generate_profit_pip_calculator(),
                _loading_figure_layout('bar-average-pip-fig',None,hide_display),
                html.Hr(),
                _generate_profit_percentage_graph(),
                _loading_figure_layout('profit-percentage-fig',None,hide_display),
                html.Hr(),
                _generate_points_percentage_graph(),
                _loading_figure_layout('points-fig',None,hide_display)
            ]),

            dcc.Tab(label='Currency Analysis', value='currency-strength-tab', children=[
                _generate_download_button(),
                html.Hr(),
                _loading_figure_layout('bar-currency-strength-analysis',None,hide_display),
                html.Hr(),
                _generate_currency_correlation_input(),
                _loading_figure_layout('currency-correlation-fig',None,hide_display)
            ]),

            dcc.Tab(label='Price Analysis', value='price-analysis-tab', children=[

                _generate_dropdown(forex_list),

                dcc.Tabs(id='timeframe-tabs', value='high-timeframe', children=[

                    dcc.Tab(label='High Timeframe (4H)', value='high-timeframe', children=[
                        _loading_figure_layout('candlestick-4H-fig', draw_config),
                        _loading_figure_layout('rsi-4H-fig', draw_config),
                    ]),

                    dcc.Tab(label='Heiken Ashi (1H)',value='medium-timeframe-heiken', children=[
                        _loading_figure_layout('candlesticks-1H-heiken', draw_config),
                        _loading_figure_layout('adx-graph-1H'),
                        _loading_figure_layout('atr-graph-1H')
                    ]),

                    dcc.Tab(label='Point counts today (1H)',value='point-counts-today', children=[
                        _loading_figure_layout('point-counts-1H'),
                    ])
                ])
            ])
        ])
    ])