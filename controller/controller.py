from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from daily_candlesticks_script import fetch_latest_candlesticks

from src.Graphs import Graphs
from src.ForexAnalyzer import ForexAnalyzer

import math

def register_callbacks(app):
    
    forex_analyzer = ForexAnalyzer()
    graph_generator = Graphs()

    @app.callback(
        [
            Output("current-currency","data"),
        ],
        [
            Input("currency-dropdown", "value")
        ]
    )
    def update_new_forex(changed_currency):

        forex_analyzer.update_forex_pair(changed_currency)
        graph_generator.update_currency(changed_currency)

        return [changed_currency]

    @app.callback(
        [
            Output("ask-value","children"),
            Output("bid-value","children"),
            Output("tick-volatility-fig","figure"),
            Output("atr-graph-4H","figure"),
            Output("percentage-changes-fig","figure"),
            Output("candlestick-1H-fig","figure"),
            Output("candlestick-4H-fig","figure"),
            Output("candlestick-15M-fig","figure"),
            Output("rsi-1H-fig","figure"),
            Output("rsi-15M-fig","figure")
        ],
        [
            Input("current-currency", "data"),
            Input("refresh-stats","n_clicks")
        ]
    )
    def update_all_graphs(value, clicks):

        ask_value, bid_value = forex_analyzer.find_ask_bid()
        
        start_time = forex_analyzer.get_start_day()
        stats_15M = forex_analyzer.get_daily_stats('15M',100)
        stats_1H = forex_analyzer.get_daily_stats('1H',100)
        stats_4H = forex_analyzer.get_daily_stats('4H',200)
        start_day = forex_analyzer.get_start_day()

        return [
            f"Ask value: {ask_value:.5f}",
            f"Bid value: {bid_value:.5f}",
            graph_generator.plot_tick_volume_fullday(stats_1H, start_day),
            graph_generator.plot_atr(forex_analyzer.get_indicator_stats('4H')),
            graph_generator.plot_percentage_change(stats_1H, start_day),
            graph_generator.plot_candlesticks_fullday(stats_1H, start_time, forex_analyzer.get_indicator_stats('1H'), '1H'),
            graph_generator.plot_candlesticks_fullday(stats_4H, start_time, forex_analyzer.get_indicator_stats('4H'), '4H'),
            graph_generator.plot_candlesticks_fullday(stats_15M, start_time, forex_analyzer.get_indicator_stats('15M'), '15M'),
            graph_generator.plot_rsi_figure(forex_analyzer.get_rsi_today('1H')),
            graph_generator.plot_rsi_figure(forex_analyzer.get_rsi_today('15M')),
        ]

    @app.callback(
        [
            Output('average-pip-text','children'),
            Output('profit-target', 'children'),
            Output('loss-bound', 'children')
        ],
        [
            Input('start-profit-calculation','n_clicks')
        ],
        [
            State('settlement-currency','value'),
            State('input_balance','value'),
            State('input_percentage_target','value'),
            State('input_percentage_loss','value'),
            State('input_leverage','value'),
            State('input_trade_count','value')
        ],
        prevent_initial_call=True
    )
    def perform_profit_calculation(click_count, rate, bal=0.0, pct_tar=0.3, pct_loss=0.2, lev=0, min_trade=0):
        bal = float(bal)

        avg_pip = 0
        amount_target = 0
        amount_loss = 0

        lev = float(lev)
        pct_tar = int(pct_tar)
        pct_loss = int(pct_loss)
        min_trade = float(min_trade)

        if bal > 0 and lev > 0 and min_trade > 0:

            amount_target = bal * (pct_tar / 100)
            amount_loss = bal * (pct_loss / 100)

            avg_pip = math.ceil(
                (amount_target / (min_trade * lev))/rate
            )

        return [
            f"Average pip per trade (Profit): {avg_pip}",
            f"Target balance ({pct_tar}% increase): {(bal + amount_target):.2f}",
            f"Minimum balance ({pct_loss}% loss tolerance): {(bal - amount_loss):.2f}"
        ]
    

    @app.callback(
        [
            Output("currency-dropdown","value"),
            Output("currency-dropdown","options"),
            Output("last-updated-candlesticks","children")
        ],
        [
            Input("update-candlesticks-stats", "n_clicks"),
            State("candlesticks-width","data")
        ],
        prevent_initial_call=True
    )
    def fetch_new_candlesticks_width(clicks, candlestick_data):

        if clicks is None:
            raise PreventUpdate

        updated_pairs = fetch_latest_candlesticks()

        last_updated_time = updated_pairs['last_updated']
        del updated_pairs['last_updated']

        widest_gap_symbol = next(iter(updated_pairs))
        dropdown_options = []

        for symbol, width in updated_pairs.items():
            
            dropdown_options.append({
                'label': f"{symbol} - {width}",
                'value': symbol
            })
        
        return [
            widest_gap_symbol,
            dropdown_options,
            f"Candlestick width last updated: {last_updated_time}"
        ]
