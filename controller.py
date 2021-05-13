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
        [Output("candlestick-30d-fig","figure")],
        [Input("current-currency", "data")]
    )
    def display_30day_info(value):
        
        last_30days_stats = forex_analyzer.get_month_stats()

        return [
            graph_generator.plot_candlesticks_weekly(last_30days_stats)
        ]
    
    @app.callback(
        [Output("tick-volatility-fig","figure")],
        [Input("current-currency", "data")]
    )
    def display_tick_volatility(value):
        
        day_stats = forex_analyzer.get_daily_stats()
        start_day = forex_analyzer.get_start_day()

        return [
            graph_generator..plot_tick_volume_fullday(day_stats, start_day)
        ]
    
    @app.callback(
        [Output("pip-size-histogram-fig","figure")],
        [Input("current-currency", "data")]
    )
    def display_tick_volatility(value):
        
        day_stats = forex_analyzer.get_daily_stats()

        return [
            graph_generator.plot_pip_difference_graph(day_stats)
        ]