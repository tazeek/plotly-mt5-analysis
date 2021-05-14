import dash_core_components as dcc
import dash_html_components as html

def _loading_figure_layout(fig_id):
    return dcc.Loading(
        type="default",
        children=html.Div([
            dcc.Graph(
                id=fig_id
            )
        ])
    )

def _generate_dropdown():

    forex_list = ['GBPUSD','EURGBP','EURUSD','AUDUSD','AUDJPY','USDJPY']

    dropdown_options = [{'label': currency, 'value': currency} for currency in forex_list]

    return html.Div([
        dcc.Dropdown(
            id='currency-dropdown',
            options=dropdown_options,
            clearable=False,
            value='GBPUSD'
        ),
        dcc.Store(id='current-currency',data='GBPUSD')
        ],
        style={"width": "10%"}
    )

def generate_layout():

    return html.Div([
        _generate_dropdown(),
        _loading_figure_layout('candlestick-30d-fig'),
        html.Hr(),
        _loading_figure_layout('tick-volatility-fig'),
        _loading_figure_layout('pip-size-histogram-fig'),
        html.Hr(),
        _loading_figure_layout('heatmap-changes-fig'),
        _loading_figure_layout('percentage-changes-fig'),
        _loading_figure_layout('close-price-histogram-fig'),
        html.Hr(),
        _loading_figure_layout('candlestick-today-fig'),
        _loading_figure_layout('rsi-fig'),
        _loading_figure_layout('bull-bear-fig')
    ])