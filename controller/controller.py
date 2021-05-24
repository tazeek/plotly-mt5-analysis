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
            Output("spread-value","children")
        ],
        [
            Input("currency-dropdown", "value")
        ]
    )
    def update_new_forex(changed_currency):

        forex_analyzer.update_forex_pair(changed_currency)
        graph_generator.update_currency(changed_currency)

        spread_num = forex_analyzer.find_spread()

        return [
            changed_currency, 
            f"Spread value: {spread_num}"
        ]
    
    @app.callback(
        [
            Output("candlestick-30d-fig","figure"),
            Output("candlestick-fullday-fig","figure"),
            Output("tick-volatility-fig","figure"),
            Output("agg-percentage-fig","figure"),
            Output("pip-size-histogram-fig","figure"),
            Output("heatmap-changes-fig","figure"),
            Output("percentage-changes-fig","figure"),
            Output("close-price-histogram-fig","figure"),
            Output("candlestick-today-fig","figure"),
            Output("rsi-fig","figure"),
            Output("bull-bear-fig","figure")
        ],
        [
            Input("current-currency", "data"),
            Input("refresh-stats","n_clicks")
        ]
    )
    def update_all_graphs(value, clicks):
        
        last_30days_stats = forex_analyzer.get_month_stats()
        day_stats = forex_analyzer.get_daily_stats()
        start_day = forex_analyzer.get_start_day()
        hourly_stats = forex_analyzer.get_hourly_stats()
        today_stats = forex_analyzer.get_d1_stats(last_30days_stats.to_dict('records')[-1])

        return [
            graph_generator.plot_candlesticks_weekly(last_30days_stats, forex_analyzer.get_indicator_stats('1D')),
            graph_generator.plot_candlestick_today(today_stats),
            graph_generator.plot_tick_volume_fullday(day_stats, start_day),
            graph_generator.plot_percentage_difference(hourly_stats, start_day),
            graph_generator.plot_pip_difference_graph(day_stats),
            graph_generator.plot_heatmap_fullday(hourly_stats, start_day),
            graph_generator.plot_percentage_change(hourly_stats, start_day),
            graph_generator.plot_histogram_fullday(day_stats, today_stats),
            graph_generator.plot_candlesticks_fullday(day_stats, today_stats, start_day, forex_analyzer.get_indicator_stats('1M')),
            graph_generator.plot_rsi_figure(forex_analyzer.get_rsi_today(), start_day),
            graph_generator.plot_bull_bears_graph(forex_analyzer.get_indicator_stats('30M'), start_day)
        ]

    @app.callback(
        [
            Output('average-pip-text','children')
        ],
        [
            Input('start-calculation','n_clicks')
        ],
        [
            State('input_profit_target','value'),
            State('input_leverage','value'),
            State('input_minimum_trade','value')
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

        symbol_list = [forex['symbol'] for forex in candlestick_data]
        updated_pairs = fetch_latest_candlesticks(symbol_list)

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
