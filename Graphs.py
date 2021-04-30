import plotly.graph_objects as go
import numpy as np

class Graphs:

    def __init__(self, currency):
        self._currency = currency

    def plot_candlesticks_weekly(self, data):

        candlestick_week_fig = go.Figure(
            data=[
                go.Candlestick(
                    x=data['time'],
                    open=data['open'], 
                    high=data['high'],
                    low=data['low'], 
                    close=data['close']
                )
            ]
        )

        candlestick_week_fig.update_layout(
            title=f"{self._currency} - Series for last 30 working days",
            xaxis_title="Date",
            yaxis_title="Price (Close)",
            hovermode='x',
            yaxis_tickformat='k',
            xaxis_rangeslider_visible=False
        )

        return candlestick_week_fig