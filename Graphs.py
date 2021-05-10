from tapy import Indicators

import plotly.graph_objects as go
import numpy as np

class Graphs:

    def __init__(self, currency):
        self._currency = currency

    def _draw_hline(self, fig, y_val, line_dash, line_col, annotation=None):

        fig.add_hline(
            y=y_val,
            line_dash=line_dash,
            line_color=line_col,
            annotation_text=annotation or ''
        )
        
        return None

    def _draw_vline(self, fig, x_val, line_dash, line_col):
        
        fig.add_vline(
            x=x_val,
            line_dash=line_dash,
            line_color=line_col
        )
        
        return None

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
            yaxis_tickformat='.3f',
            xaxis_rangeslider_visible=False,
            showlegend=False
        )

        return candlestick_week_fig

    def plot_histogram_fullday(self, data, day_stats):

        histogram_fig = go.Figure(
            data=[
                go.Histogram(
                    x=data['close'],
                    opacity=0.4,
                    bingroup='bar'
                )
            ]
        )

        self._draw_vline(histogram_fig, day_stats['close'], "solid", "black")
        self._draw_vline(histogram_fig, day_stats['open'], "dash", "green")

        histogram_fig.update_layout(
            width=800,
            title=f"{self._currency} - Close price counts for the day (Current closing price: {day_stats['close']})",
            xaxis_title="Price range",
            yaxis_title="Counts",
            hovermode='x',
            yaxis_tickformat='k',
            bargap=0.20
        )

        return histogram_fig

    def plot_tick_volume_fullday(self, data, start_time):

        tick_vol_fig = go.Figure([
            go.Scatter(
                x=data['time'], 
                y=data['tick_volume'],
                opacity=0.5
            )
        ])

        self._draw_vline(tick_vol_fig, start_time, "solid", "black")

        self._draw_hline(tick_vol_fig, 30, "dash", "red", "Average Volatility")
        self._draw_hline(tick_vol_fig, 60, "dash", "green", "High Volatility")

        tick_vol_fig.update_layout(
            width=1000,
            title=f"{self._currency} - Tick Volume for today",
            xaxis_title="Time",
            yaxis_title="Volume",
            hovermode='x',
            yaxis_tickformat='k'
        )

        return tick_vol_fig

    def plot_heatmap_fullday(self, data, start_time, high_price_time, low_price_time):

        info_text = 'Time: %{x}<br><br>' + \
            'Open price: %{customdata[0]:.5f}<br>' + \
            'Close price: %{customdata[1]:.5f}<br>' + \
            '% Change: %{z:.3f}<br><br>' + \
            'High price: %{customdata[2]:.5f}<br>' + \
            'Low price: %{customdata[3]:.5f}<br><extra></extra>'
            
        customdata_list = np.dstack(
            (data['open'], data['close'], data['high'], data['low'])
        )

        heatmap_fig = go.Figure(
            data=go.Heatmap(
                customdata=customdata_list,
                z=[data['percentage_change']],
                y=None,
                x=data['time'],
                zmin=-0.25,
                zmax=0.25,
                colorscale='rdylgn',
                hovertemplate= info_text
            )
        )

        heatmap_fig.update_layout(
            width=1000,
            title=f"{self._currency} - Heatmap for price changes today",
            xaxis_title="Time",
            hovermode='x',
        )

        self._draw_vline(heatmap_fig, start_time, "solid", "black")
        self._draw_vline(heatmap_fig, high_price_time, "dash", "green")
        self._draw_vline(heatmap_fig, low_price_time, "dash", "red")

        heatmap_fig.update_yaxes(showticklabels=False)

        return heatmap_fig

    def plot_percentage_change(self, data, start_time):

        percentage_change_fig = go.Figure([
            go.Scatter(
                x=data['time'], 
                y=data['percentage_change'],
                mode='lines+markers',
                opacity=0.5
            )
        ])

        percentage_change_fig.update_yaxes(range=[-1,1])

        percentage_change_fig.update_layout(
            width=1000,
            title=f"{self._currency} - Percentage Change for today",
            xaxis_title="Time",
            yaxis_title="Percentage change",
            hovermode='x',
            yaxis_tickformat='.3f'
        )

        self._draw_hline(percentage_change_fig, 0.03, "dash", "red")
        self._draw_hline(percentage_change_fig, -0.03, "dash", "red")
        self._draw_hline(percentage_change_fig, 0.10, "dash", "green")
        self._draw_hline(percentage_change_fig, -0.10, "dash", "green")
        self._draw_hline(percentage_change_fig, 0, "solid", "black")

        self._draw_vline(percentage_change_fig, start_time, "solid", "black")

        return percentage_change_fig

    def plot_candlesticks_fullday(self, data_day, overall_day, start_time, indicators_df):

        candlesticks_minute_fig = go.Figure(
            data=[
                go.Candlestick(
                    x=data_day['time'],
                    open=data_day['open'], 
                    high=data_day['high'],
                    low=data_day['low'], 
                    close=data_day['close']
                ),
                go.Scatter(
                    x=indicators_df['time'], 
                    y=indicators_df['sma'],
                    line=dict(color='black')
                )
            ]
        )

        self._draw_hline(
            candlesticks_minute_fig,
            overall_day['high'],
            "dot",
            'green',
            f"High - {overall_day['high']}"
        )

        self._draw_hline(
            candlesticks_minute_fig,
            overall_day['low'],
            "dot",
            'red',
            f"Low - {overall_day['low']}"
        )

        self._draw_vline(candlesticks_minute_fig, start_time, "solid", "black")

        candlesticks_minute_fig.update_layout(
            width=1000,
            title=f"{self._currency} - Series for today",
            xaxis_title="Time",
            yaxis_title="Price",
            hovermode='x',
            yaxis_tickformat='.5f',
            xaxis_rangeslider_visible=False,
            showlegend=False
        )

        return candlesticks_minute_fig

    def plot_rsi_figure(self, rsi_today):

        fig = go.Figure([
            go.Scatter(
                x=rsi_today['time'], 
                y=rsi_today['value']
            )
        ])

        self._draw_hline(fig, 20, "dash", "green", "Ideal - Buy")
        self._draw_hline(fig, 80, "dash", "green", "Ideal - Sell")
        self._draw_hline(fig, 30, "solid", "black", "Oversold")
        self._draw_hline(fig, 70, "solid", "black", "Overbought")

        fig.update_layout(
            width=1000,
            xaxis_title="Time",
            yaxis_title="RSI Value",
            hovermode='x',
            yaxis_tickformat='.2f'
        )

        return fig

    def plot_bull_bears_graph(self, indicators_df):

        bull_bear_power_fig = go.Figure(
            data=[
                go.Bar(
                    x=indicators_df['time'],
                    y=indicators_df['bears_power'],
                    name='Bear Power',
                    marker_color='red'
                ),
                go.Bar(
                    x=indicators_df['time'],
                    y=indicators_df['bulls_power'],
                    name='Bull Power',
                    marker_color='blue'
                )
            ]
        )

        bull_bear_power_fig.update_yaxes(range=[-0.0008, 0.0008])

        bull_bear_power_fig.update_layout(template='simple_white')

        return bull_bear_power_fig

    def plot_pip_difference_graph(self, day_stats):
        
        return go.Figure(
            data=[
                go.Bar(
                    x=day_stats['time'],
                    y=day_stats['pip_difference'],
                    marker_color='blue'
                )
            ]
        )