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
            Output("ask-value","children"),
            Output("bid-value","chidlren")
        ],
        [
            Input("currency-dropdown", "value")
        ]
    )
    def update_new_forex(changed_currency):

        forex_analyzer.update_forex_pair(changed_currency)
        graph_generator.update_currency(changed_currency)

        ask_value, bid_value = forex_analyzer.find_ask_bid()

        return [
            changed_currency, 
            f"Ask value: {ask_value}",
            f"Bid value: {bid_value}"
        ]
    
    @app.callback(
        [
            Output("candlestick-today-stat","figure"),
            Output("tick-volatility-fig","figure"),
            Output("heatmap-price-changes-fig","figure"),
            Output("percentage-changes-fig","figure"),
            Output("candlestick-1H-fig","figure"),
            Output("candlestick-4H-fig","figure"),
            Output("candlestick-15M-fig","figure"),
            Output("rsi-1H-fig","figure"),
            Output("rsi-15M-fig","figure"),
            Output("bull-bear-1H-fig","figure"),
            Output("bull-bear-15M-fig", "figure")
        ],
        [
            Input("current-currency", "data"),
            Input("refresh-stats","n_clicks")
        ]
    )
    def update_all_graphs(value, clicks):
        
        start_time = forex_analyzer.get_start_day()
        quarterly_stats = forex_analyzer.get_quarterly_stats()
        stats_15M = forex_analyzer.get_daily_stats('15M',100)
        stats_1H = forex_analyzer.get_daily_stats('1H',100)
        stats_4H = forex_analyzer.get_daily_stats('4H',100)
        start_day = forex_analyzer.get_start_day()
        today_stats = forex_analyzer.get_d1_stats(quarterly_stats.to_dict('records')[-1])

        return [
            graph_generator.plot_candlestick_today(today_stats),
            graph_generator.plot_tick_volume_fullday(stats_1H, start_day),
            graph_generator.plot_heatmap_fullday(stats_1H, start_day),
            graph_generator.plot_percentage_change(stats_1H, start_day),
            graph_generator.plot_candlesticks_fullday(stats_1H, start_time, forex_analyzer.get_indicator_stats('1H'), '1H'),
            graph_generator.plot_candlesticks_fullday(stats_4H, start_time, forex_analyzer.get_indicator_stats('4H'), '4H'),
            graph_generator.plot_candlesticks_fullday(stats_15M, start_time, forex_analyzer.get_indicator_stats('15M'), '15M'),
            graph_generator.plot_rsi_figure(forex_analyzer.get_rsi_today('1H')),
            graph_generator.plot_rsi_figure(forex_analyzer.get_rsi_today('15M')),
            graph_generator.plot_bull_bears_graph(forex_analyzer.get_indicator_stats('1H')),
            graph_generator.plot_bull_bears_graph(forex_analyzer.get_indicator_stats('15M'))
        ]

    @app.callback(
        [
            Output('average-pip-text','children')
        ],
        [
            Input('start-calculation','n_clicks')
        ],
        [
            State('input_target','value'),
            State('input_leverage','value'),
            State('input_trade','value')
        ],
        prevent_initial_call=True
    )
    def perform_average_pip_calculation(click_count, target=0, leverage=0, min_trade=0):
        avg_pip = 0

        leverage = float(leverage)
        target = float(target)
        min_trade = float(min_trade)

        if leverage > 0 and min_trade > 0:

            avg_pip = math.ceil(target / (min_trade * leverage))

        return [
            f"Average pip per trade: {avg_pip}"
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
