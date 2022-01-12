from datetime import datetime

import plotly.graph_objects as go
import pandas as pd
import plotly.figure_factory as ff

import logging

class Graphs:

    def __init__(self):
        self._symbol = None
        self._digits_precision = None

    def update_symbol(self, symbol, digits):
        self._symbol = symbol
        self._digits_precision = digits

        return None

    def _find_earlier_hour_today(self, data_day):

        # Find the earliest point in the day
        current_date_time = datetime.strptime(str(data_day['time'].iat[-1]), "%Y-%m-%d %H:%M:%S")
        current_date_time = datetime.combine(current_date_time, datetime.min.time())

        return current_date_time

    def _filter_missing_dates(self, data, timeframe):

        # build complete timeline from start date to end date
        all_dates = pd.date_range(start=data['time'].iat[0],end=data['time'].iat[-1])

        # retrieve the dates that ARE in the original datset
        original_dates = [d.strftime("%Y-%m-%d") for d in data['time']]

        # define dates with missing values
        break_dates = [d for d in all_dates.strftime("%Y-%m-%d").tolist() if not d in original_dates]

        return break_dates

    def _draw_hline(self, fig, y_val, line_dash, line_col, annotation=None):

        fig.add_hline(
            y=y_val,
            line_dash=line_dash,
            line_color=line_col,
            annotation_text=annotation or '',
            line_width=1
        )
        
        return None

    def _fill_missing_dates(self, fig, data_day, timeframe):

        missing_dates = self._filter_missing_dates(data_day, timeframe)
        logging.info(missing_dates)

        fig.update_xaxes(
            rangebreaks=[
                dict(
                    values=missing_dates
                )
            ]
        )

        return None

    def plot_atr(self, data, data_day, timeframe):
        
        atr_fig = go.Figure([
            go.Scatter(
                x=data['time'], 
                y=data['atr'],
                mode="lines"
            )
        ])
        
        current_atr = data['atr'].iat[-1]

        atr_fig.update_layout(
            title=f"{self._symbol} - ATR (Current value: {current_atr: .{self._digits_precision}f})",
            template='simple_white',
            xaxis_title="Time",
            hovermode='x',
            xaxis_rangeslider_visible=False,
            showlegend=False,
            yaxis={'visible': False, 'showticklabels': False}
        )

        self._fill_missing_dates(atr_fig, data_day, timeframe)

        return atr_fig

    def plot_candlesticks_fullday(self, data_day, timeframe, indicators_df):

        candlesticks_minute_fig = go.Figure(
            data=[
                go.Candlestick(
                    x=data_day['time'],
                    open=data_day['open'], 
                    high=data_day['high'],
                    low=data_day['low'], 
                    close=data_day['close'],
                    hoverinfo='none',
                    showlegend=False
                )
            ]
        )

        legend_config=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )

        candlesticks_minute_fig.update_layout(
            title=f"{self._symbol} - Series ({timeframe})",
            xaxis_title="Time",
            yaxis_title="Price",
            hovermode='x',
            xaxis_rangeslider_visible=False,
            legend=legend_config
        )

        self._fill_missing_dates(candlesticks_minute_fig, data_day, timeframe)
        
        return candlesticks_minute_fig

    def plot_rsi_figure(self, rsi_today):

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
            yaxis_range=[0,100],
            yaxis_dtick=10,
            title=f"RSI of {self._symbol} - Period: 14",
            hovermode='x',
            yaxis_tickformat='.2f'
        )

        self._fill_missing_dates(rsi_fig, rsi_today, '15M')

        return rsi_fig

    def display_symbol_strength(self, data):

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
            xaxis_title="Symbol",
            yaxis_title="Strength",
            title=f"Symbol Strength (with JPY as the apple) - Recent 5 weeks",
            hovermode='x unified',
            height=700
        )

        return bar_fig

    def plot_heiken_ashi(self, data, indicator_df):

        candlesticks_fig = go.Figure(
            data=[
                go.Candlestick(
                    x=data['time'],
                    open=data['open'], 
                    high=data['high'],
                    low=data['low'], 
                    close=data['close'],
                    hoverinfo='none',
                    showlegend=False
                ),
                go.Scatter(
                    x=indicator_df['time'],
                    y=indicator_df['upper_bound'],
                    line=dict(color='black',width=2),
                    name="Upper bound"
                ),
                go.Scatter(
                    x=indicator_df['time'],
                    y=indicator_df['lower_bound'],
                    line=dict(color='black',width=2),
                    name="Lower bound"
                )
            ]
        )

        legend_config=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )

        candlesticks_fig.update_layout(
            title=f"{self._symbol} - Series (15M)",
            xaxis_title="Time",
            yaxis_title="Price",
            hovermode='x',
            yaxis_tickformat='.5f',
            xaxis_rangeslider_visible=False,
            legend=legend_config
        )

        self._fill_missing_dates(candlesticks_fig, data, '15M')
        
        return candlesticks_fig

    def plot_correlation_heatmap(self, correlation_df):
        currency_pairs = list(correlation_df.columns)
        values = correlation_df.values.tolist()

        ff_fig = ff.create_annotated_heatmap(
            x=currency_pairs, 
            y=currency_pairs, 
            z=values, 
            colorscale='Viridis',
            showscale = True
        )

        fig = go.FigureWidget(ff_fig)
        fig.layout.annotations = ff_fig.layout.annotations

        fig.update_layout(
            title=f"Currency correlation",
        )

        return fig

    def plot_pip_range_counts(self, data_day, multiplier):

        def _calculate_points(open_price, close_price):

            return round((close_price - open_price) / multiplier)

        # Find the earliest point in the day
        current_date_time = self._find_earlier_hour_today(data_day)

        data_day = data_day[data_day['time'] >= current_date_time]

        points_diff_lambda = lambda x: _calculate_points(x['open'], x['close'])

        colors_list = []
        points_list = []

        for index, row in data_day.iterrows():
            diff = points_diff_lambda(row)
            colors_list.append('green' if diff > 0 else 'red')
            points_list.append(int(abs(diff)))

        x_val = [x for x in range(0, len(points_list) + 1)]

        bar_fig = go.Figure(
            [
                go.Bar(
                    x=x_val, 
                    y=points_list,
                    marker_color=colors_list,
                    opacity=0.35,
                    hovertemplate='Hour: %{x}:00<br>Points: %{y}<extra></extra>'
                )
            ]
        )

        bar_fig.update_layout(
            template='simple_white',
            xaxis_title="Hour",
            yaxis_title="Points",
            title=f"Points count for the day",
            hovermode='x unified',
            height=700
        )

        for val in [100,200,300]:
            self._draw_hline(bar_fig, val, "solid","black")

        return bar_fig

    def plot_minimum_profit(self, data_dict):

        x_val = list(data_dict.keys())
        y_val = list(data_dict.values())

        fig = go.Figure(
            [
                go.Scatter(
                    x=x_val, 
                    y=y_val,
                    mode="lines"
                )
            ]
        )

        fig.update_layout(
            title=f"Points target",
            xaxis_title="Currency",
            yaxis_title=f"Points",
            hovermode='x'
        )

        return fig

    def plot_volume_graph(self, data):

        current_date_time = self._find_earlier_hour_today(data)
        data = data[data['time'] >= current_date_time]

        x_val = [x for x in range(0, len(data))]

        fig = go.Figure(
            [
                go.Scatter(
                    x=x_val, 
                    y=data['tick_volume']
                )
            ]
        )

        fig.update_layout(
            template='simple_white',
            title=f"Ticks Volume",
            xaxis_title="Hour",
            yaxis_title=f"Tick count",
            hovermode='x'
        )

        return fig