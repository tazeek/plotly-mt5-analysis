from dash.dependencies import Input, Output

from Graphs import Graphs
from ForexAnalyzer import ForexAnalyzer

def register_callbacks(app):
    
    forex_analyzer = ForexAnalyzer()
    graph_generator = Graphs()

    @app.callback(
        [Output("current-currency","data")],
        [Input("currency-dropdown", "value")]
    )
    def update_forex_analyzer(value):
        forex_analyzer.update_forex_pair(value)
        graph_generator.update_currency(value)

        return [value]
    
    @app.callback(
        [
            Output("candlestick-30d-fig","figure"),
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
            graph_generator.plot_tick_volume_fullday(day_stats, start_day),
            graph_generator.plot_pip_difference_graph(day_stats),
            graph_generator.plot_heatmap_fullday(hourly_stats, start_day, high_price_time, low_price_time),
            graph_generator.plot_percentage_change(hourly_stats, start_day),
            graph_generator.plot_histogram_fullday(day_stats, today_stats),
            graph_generator.plot_candlesticks_fullday(day_stats, today_stats, start_day, forex_analyzer.get_indicator_stats('1M')),
            graph_generator.plot_rsi_figure(forex_analyzer.get_rsi_today(), start_day),
            graph_generator.plot_bull_bears_graph(forex_analyzer.get_indicator_stats('30M'), start_day)
        ]