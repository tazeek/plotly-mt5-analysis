import plotly.graph_objects as go
import numpy as np
import pandas as pd

class Graphs:

    def __init__(self, currency=None):
        self._currency = currency
        self._missing_dates = {}

    def update_currency(self, currency):
        self._currency = currency

        return None

    def _filter_missing_dates(self, data, timeframe):

        if timeframe not in self._missing_dates:

            # build complete timeline from start date to end date
            dt_all = pd.date_range(start=data['time'].iat[0],end=data['time'].iat[-1])

            # retrieve the dates that ARE in the original datset
            original_dates = [d.strftime("%Y-%m-%d") for d in data['time']]

            # define dates with missing values
            break_dates = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in original_dates]

            self._missing_dates[timeframe] = break_dates

        return self._missing_dates[timeframe]

    def _filter_data(self, data, start_time):
        return data[data['time'] >= start_time]

    def _add_sma_graphs(self, fig, data, color, col_name):
        
        fig.add_trace(
            go.Scatter(
                x=data['time'], 
                y=data[col_name],
                line=dict(color=color, width=1),
                name=col_name.upper()
            )
        )

        return None

    def _candlestick_text(self, candlestick_info):

        return f"Open: {candlestick_info['open']:.5f}<br>" + \
                f"High: {candlestick_info['high']:.5f}<br>" + \
                f"Low: {candlestick_info['low']:.5f}<br>" + \
                f"Close: {candlestick_info['close']:.5f}<br>" + \
                f"Width: {candlestick_info['pip_difference']}"

    def _draw_hline(self, fig, y_val, line_dash, line_col, annotation=None):

        fig.add_hline(
            y=y_val,
            line_dash=line_dash,
            line_color=line_col,
            annotation_text=annotation or '',
            line_width=3
        )
        
        return None

    def plot_atr(self, data):
        
        atr_fig = go.Figure([
            go.Scatter(
                x=data['time'], 
                y=data['atr'],
                mode="lines"
            )
        ])

        current_atr = str(data['atr'].iat[-1]).split('.')
        current_atr = [num for num in current_atr[1] if num != '0']
        current_atr = ''.join(current_atr[:2])

        atr_fig.update_layout(
            title=f"{self._currency} - ATR (4H) (Current value: {current_atr})",
            template='simple_white',
            xaxis_title="Time",
            hovermode='x',
            xaxis_rangeslider_visible=False,
            showlegend=False,
            yaxis={'visible': False, 'showticklabels': False}
        )

        return atr_fig

    def plot_tick_volume_fullday(self, data, start_time):

        data = self._filter_data(data.copy(), start_time)

        tick_vol_fig = go.Figure([
            go.Scatter(
                x=data['time'], 
                y=data['tick_volume'],
                mode="lines+markers"
            )
        ])

        self._draw_hline(tick_vol_fig, data['tick_volume'].mean(), "solid", "black")

        tick_vol_fig.update_layout(
            title=f"{self._currency} - Tick Volume for today (1H)",
            template='simple_white',
            xaxis_title="Time",
            yaxis_title="Volume",
            hovermode='x',
            yaxis_tickformat='k'
        )

        return tick_vol_fig

    def plot_percentage_change(self, data, start_time):

        data = self._filter_data(data.copy(), start_time)

        percentage_change_fig = go.Figure([
            go.Scatter(
                x=data['time'], 
                y=data['price_percentage_change']
            )
        ])

        percentage_change_fig.update_layout(
            title=f"{self._currency} - Price Percentage Change for today (1H)",
            template='simple_white',
            xaxis_title="Time",
            yaxis_title="Percentage change",
            hovermode='x',
            yaxis_tickformat='.3f'
        )

        self._draw_hline(percentage_change_fig, 0, "solid", "black")

        percentage_change_fig.add_hrect(
            y0=0.03, 
            y1=-0.03,
            fillcolor="#D55A5A",
            annotation_text="Less activity zone",
            annotation_position="outside bottom left",
            layer="below", 
            opacity=0.25
        )

        return percentage_change_fig

    def plot_candlesticks_fullday(self, data_day, timeframe, indicators_df, support_resistance_levels=None):

        hover_list= data_day.apply(lambda data_row:self._candlestick_text(data_row), axis=1)

        candlesticks_minute_fig = go.Figure(
            data=[
                go.Candlestick(
                    x=data_day['time'],
                    open=data_day['open'], 
                    high=data_day['high'],
                    low=data_day['low'], 
                    close=data_day['close'],
                    text=hover_list,
                    hoverinfo='text',
                    showlegend=False
                )
            ]
        )

        self._add_sma_graphs(candlesticks_minute_fig, indicators_df, 'black', 'sma_50')

        if timeframe == '15M':
            self._add_sma_graphs(candlesticks_minute_fig, indicators_df, 'blue','sma_21')
            self._add_sma_graphs(candlesticks_minute_fig, indicators_df, 'red','sma_200')

        legend_config=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )

        candlesticks_minute_fig.update_layout(
            title=f"{self._currency} - Series ({timeframe})",
            xaxis_title="Time",
            yaxis_title="Price",
            hovermode='x',
            yaxis_tickformat='.5f',
            xaxis_rangeslider_visible=False,
            legend=legend_config
        )

        if support_resistance_levels:
            for level in levels:
                self._draw_hline(candlesticks_minute_fig, level, "solid", "purple")

        candlesticks_minute_fig.update_xaxes(
            rangebreaks=[
                dict(
                    values=self._filter_missing_dates(data_day, timeframe)
                )
            ]
        )
        
        return candlesticks_minute_fig

    def plot_rsi_figure(self, rsi_today, start_time):

        rsi_fig = go.Figure([
            go.Scatter(
                x=rsi_today['time'], 
                y=rsi_today['value'],
                mode="lines"
            )
        ])

        rsi_fig.update_layout(
            xaxis_title="Time",
            yaxis_title="RSI Value",
            title=f"RSI of {self._currency}",
            hovermode='x',
            yaxis_tickformat='.2f'
        )

        self._draw_hline(rsi_fig, 50, "solid", "black")

        rsi_fig.update_xaxes(
            rangebreaks=[
                dict(
                    values=self._filter_missing_dates(rsi_today, '1H')
                )
            ]
        )

        return rsi_fig

    def plot_pip_target(self, data):
        
        x_axis_val = list(data.keys())

        profit_targets = [target['profit'] for target in data.values()]
        loss_targets = [target['loss'] for target in data.values()]

        bar_fig = go.Figure(
            [
                go.Bar(
                    x=x_axis_val, 
                    y=profit_targets,
                    marker_color='green',
                    name='Profit',
                    opacity=0.5
                ),
                go.Bar(
                    x=x_axis_val,
                    y=loss_targets,
                    marker_color='indianred',
                    name='Loss',
                    opacity=0.5
                )
            ]
        )

        bar_fig.update_layout(
            template='simple_white',
            xaxis_title="Currency",
            yaxis_title="Points",
            title=f"Average points target",
            hovermode='x unified',
            height=700
        )

        return bar_fig

    def display_currency_strength(self, data):

        roc_values = list(data.values())
        marker_colors = ['green' if roc > 0 else 'red' for roc in roc_values]

        bar_fig = go.Figure(
            [
                go.Bar(
                    x=list(data.keys()), 
                    y=roc_values,
                    marker_color=marker_colors,
                    name='ROC',
                    opacity=0.35
                )
            ]
        )

        self._draw_hline(bar_fig, 0, "solid", "black")

        bar_fig.update_layout(
            template='simple_white',
            xaxis_title="Currency",
            yaxis_title="Strength",
            title=f"Currency Strength (with JPY as the apple)",
            hovermode='x unified',
            height=700
        )

        return bar_fig