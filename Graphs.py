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

    def plot_histogram_fullday(self, data, close):

        histogram_fig = go.Figure(
            data=[
                go.Histogram(
                    x=data['close'],
                    opacity=0.4,
                    bingroup='bar'
                )
            ]
        )

        histogram_fig.add_vline(
            x=close,
            line_dash="solid",
            line_color="black"
        )

        histogram_fig.update_layout(
            width=800,
            title=f"{self._currency} - Close price counts for the day",
            xaxis_title="Price range",
            yaxis_title="Counts",
            hovermode='x',
            yaxis_tickformat='k'
        )

        return histogram_fig

    def plot_tick_volume_fullday(self, data, start_time):

        tick_vol_fig = go.Figure([
            go.Scatter(
                x=data['time'], 
                y=data['tick_volume']
            )
        ])

        tick_vol_fig.update_layout(
            width=1000,
            title=f"{self._currency} - Tick Volume for today",
            xaxis_title="Time",
            yaxis_title="Volume",
            hovermode='x',
            yaxis_tickformat='k'
        )

        tick_vol_fig.add_vline(
            x=start_time,
            line_dash="solid",
            line_color="black"
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
                zmin=-25,
                zmax=25,
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

        heatmap_fig.add_vline(
            x=start_time,
            line_dash="solid",
            line_color="black"
        )

        heatmap_fig.add_vline(
            x=high_price_time,
            line_dash="dash",
            line_color="green"
        )

        heatmap_fig.add_vline(
            x=low_price_time,
            line_dash="dash",
            line_color="red"
        )


        heatmap_fig.update_yaxes(showticklabels=False)

        return heatmap_fig

    def plot_percentage_change(self, data):

        percentage_change_fig = go.Figure([
            go.Scatter(
                x=data['time'], 
                y=data['percentage_change']
            )
        ])

        percentage_change_fig.update_layout(
            width=1000,
            title=f"{self._currency} - Tick Volume for today",
            xaxis_title="Time",
            yaxis_title="Percentage change",
            hovermode='x',
            yaxis_tickformat='k'
        )

        percentage_change_fig.add_hline(
            y=0,
            line_dash="solid",
            line_color="black"
        )

        return percentage_change_fig

    def plot_candlesticks_fullday(self, data_day, overall_day, start_time):

        candlesticks_minute_fig = go.Figure(
            data=[
                go.Candlestick(
                    x=data_day['time'],
                    open=data_day['open'], 
                    high=data_day['high'],
                    low=data_day['low'], 
                    close=data_day['close']
                )
            ]
        )

        candlesticks_minute_fig.add_hline(
            y=overall_day['open'], 
            line_dash="dot",
            annotation_text=f"Open - {overall_day['open']}"
        )

        candlesticks_minute_fig.add_hline(
            y=overall_day['high'], 
            line_dash="dot",
            annotation_text=f"High - {overall_day['high']}",
            line_color='green'
        )

        candlesticks_minute_fig.add_hline(
            y=overall_day['close'] + 0.00070, 
            line_dash="dot",
            annotation_text=f"Stop-loss (Sell) - {overall_day['close'] + 0.00070}",
            line_color='purple'
        )

        candlesticks_minute_fig.add_hline(
            y=overall_day['close'] - 0.00070, 
            line_dash="dot",
            annotation_text=f"Stop-loss (Buy) - {overall_day['close'] - 0.00070}",
            line_color='purple'
        )

        candlesticks_minute_fig.add_hline(
            y=overall_day['low'], 
            line_dash="dot",
            annotation_text=f"Low - {overall_day['low']}",
            line_color='red'
        )

        candlesticks_minute_fig.add_vline(
            x=start_time,
            line_dash="solid",
            line_color="black"
        )

        candlesticks_minute_fig.update_layout(
            width=1000,
            title=f"{self._currency} - Series for today",
            xaxis_title="Time",
            yaxis_title="Price",
            hovermode='x',
            yaxis_tickformat='k'
        )

        return candlesticks_minute_fig