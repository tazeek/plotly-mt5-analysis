from datetime import datetime

import plotly.graph_objects as go
import pandas as pd
import plotly.figure_factory as ff

class Graphs:

    def __init__(self, symbol=None):
        self._symbol = symbol
        self._missing_dates = {}

    def update_symbol(self, symbol):
        self._symbol = symbol

        return None

    def _filter_missing_dates(self, data, timeframe):

        if timeframe not in self._missing_dates:

            # build complete timeline from start date to end date
            all_dates = pd.date_range(start=data['time'].iat[0],end=data['time'].iat[-1])

            # retrieve the dates that ARE in the original datset
            original_dates = [d.strftime("%Y-%m-%d") for d in data['time']]

            # define dates with missing values
            break_dates = [d for d in all_dates.strftime("%Y-%m-%d").tolist() if not d in original_dates]

            self._missing_dates[timeframe] = break_dates

        return self._missing_dates[timeframe]

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

        fig.update_xaxes(
            rangebreaks=[
                dict(
                    values=missing_dates
                )
            ]
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
            title=f"{self._symbol} - ATR (4H) (Current value: {current_atr})",
            template='simple_white',
            xaxis_title="Time",
            hovermode='x',
            xaxis_rangeslider_visible=False,
            showlegend=False,
            yaxis={'visible': False, 'showticklabels': False}
        )

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
            title=f"{self._symbol} - Series ({timeframe})",
            xaxis_title="Time",
            yaxis_title="Price",
            hovermode='x',
            yaxis_tickformat='.5f',
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
            title=f"RSI of {self._symbol}",
            hovermode='x',
            yaxis_tickformat='.2f'
        )

        self._draw_hline(rsi_fig, 50, "solid", "black")
        self._fill_missing_dates(rsi_fig, rsi_today, '15M')

        return rsi_fig

    def plot_adx_figure(self, adx_df):

        adx_fig = go.Figure([
            go.Scatter(
                x=adx_df['time'], 
                y=adx_df['value'],
                mode="lines"
            )
        ])

        adx_fig.update_layout(
            xaxis_title="Time",
            yaxis_title="ADX value",
            title=f"ADX of {self._symbol}",
            hovermode='x',
            yaxis_tickformat='.2f'
        )

        self._fill_missing_dates(adx_fig, adx_df, '15M')

        for num in [25,50,75,100]:
            self._draw_hline(adx_fig, num, 'dash', 'black')

        return adx_fig

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
            xaxis_title="Payout Currency",
            yaxis_title="Points",
            title=f"Average points target",
            hovermode='x unified',
            height=700
        )

        return bar_fig

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

    def plot_profit_target(self, data_dict, definer):

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
            title=f"{definer} percentage target",
            xaxis_title="Percentage",
            yaxis_title=f"{definer}",
            hovermode='x',
            xaxis=dict(
                tickmode='linear',
                tick0 = 0,
                dtick = 10
            )
        )

        return fig

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

            points = round((close_price - open_price) / multiplier)
            return int(abs(points))

        # Find the earliest point in the day
        current_date_time = datetime.strptime(str(data_day['time'].iat[-1]), "%Y-%m-%d %H:%M:%S")
        current_date_time = datetime.combine(current_date_time, datetime.min.time())

        data_day = data_day[data_day['time'] >= current_date_time]

        points_diff = data_day.apply(
            lambda x: _calculate_points(x['open'], x['close']), axis=1
        )

        points_diff = list(points_diff)
        x_val = [x for x in range(0, len(points_diff) + 1)]

        bar_fig = go.Figure(
            [
                go.Bar(
                    x=x_val, 
                    y=points_diff,
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