from dash.dependencies import Input, Output, State

from src.Graphs import Graphs
from src.ForexAnalyzer import ForexAnalyzer

import math

def register_callbacks(app):
    
    forex_analyzer = ForexAnalyzer()
    graph_generator = Graphs()

    @app.callback(
        [
            Output("current-currency","data"), 
            Output("candlestick-width-text","children")
        ],
        [Input("currency-dropdown", "value")],
        [State("candlestick-width-dict","data")]
    )
    def update_forex_analyzer(changed_currency, candlestick_dict):

        forex_analyzer.update_forex_pair(changed_currency)
        graph_generator.update_currency(changed_currency)

        return [changed_currency, f"Candlestick width: {candlestick_dict[changed_currency]}"]
    
    @app.callback(
        [
            Output("candlestick-30d-fig","figure"),
            Output("candlestick-fullday-fig","figure"),
            Output("tick-volatility-fig","figure"),
            Output("pip-size-histogram-fig","figure"),
            Output("heatmap-changes-fig","figure"),
            Output("percentage-changes-fig","figure"),
            Output("close-price-histogram-fig","figure"),
            Output("candlestick-today-fig","figure"),
            Output("rsi-fig","figure"),
            Output("bull-bear-fig","figure")
        ],
        [Input("current-currency", "data")]
    )
    def display_tick_volatility(value):
        
        last_30days_stats = forex_analyzer.get_month_stats()
        day_stats = forex_analyzer.get_daily_stats()
        start_day = forex_analyzer.get_start_day()
        hourly_stats = forex_analyzer.get_hourly_stats()
        today_stats = forex_analyzer.get_d1_stats(last_30days_stats.to_dict('records')[-1])

        high_price_time = day_stats.loc[day_stats['high'] == today_stats['high']]['time'].iloc[-1]
        low_price_time = day_stats.loc[day_stats['low'] == today_stats['low']]['time'].iloc[-1]

        return [
            graph_generator.plot_candlesticks_weekly(last_30days_stats),
            graph_generator.plot_candlestick_today(today_stats),
            graph_generator.plot_tick_volume_fullday(day_stats, start_day),
            graph_generator.plot_pip_difference_graph(day_stats),
            graph_generator.plot_heatmap_fullday(hourly_stats, start_day),
            graph_generator.plot_percentage_change(hourly_stats, start_day),
            graph_generator.plot_histogram_fullday(day_stats, today_stats),
            graph_generator.plot_candlesticks_fullday(day_stats, today_stats, start_day, forex_analyzer.get_indicator_stats('1M')),
            graph_generator.plot_rsi_figure(forex_analyzer.get_rsi_today(), start_day),
            graph_generator.plot_bull_bears_graph(forex_analyzer.get_indicator_stats('30M'), start_day)
        ]

    @app.callback(
        [Output('average-pip-text','children')],
        [Input('start-calculation','n_clicks')],
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

        return [f"Average pip per trade: {avg_pip}"]