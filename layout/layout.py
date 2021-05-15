import dash_core_components as dcc
import dash_html_components as html

import random

def _fetch_forex_pairs():
    forex_pairs = []

    file_path = "\\".join([
        'C:','Users','Tazeek','Desktop','Projects',
        'plotly-mt5-analysis','files','forex_pairs.txt'
    ])

    with open(file_path) as f:
        for line in f.readlines():
            forex_pairs.append(line.strip())
    
    return forex_pairs

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

    forex_list = _fetch_forex_pairs()
    current_forex = random.choice(forex_list)

    dropdown_options = [{'label': currency, 'value': currency} for currency in forex_list]

    return html.Div(
        [
            dcc.Dropdown(
                id='currency-dropdown',
                options=dropdown_options,
                clearable=False,
                value=current_forex
            ),
            dcc.Store(id='current-currency',data=current_forex)
        ],
            style={"width": "10%"}
    )

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