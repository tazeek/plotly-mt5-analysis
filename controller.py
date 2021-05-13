from dash.dependencies import Input, Output

from Graphs import Graphs
from ForexAnalyzer import ForexAnalyzer

def register_callbacks(app):
    
    @app.callback(
       [Output("candlestick-30d-fig","figure")],
       [Input("currency-dropdown", "value")]
    )
    def test_output(value):

        forex_analyzer = ForexAnalyzer(value)
        last_30days_stats = forex_analyzer.get_month_stats()

        graph_generator = Graphs(value)
        

        return [
            graph_generator.plot_candlesticks_weekly(last_30days_stats)
        ]