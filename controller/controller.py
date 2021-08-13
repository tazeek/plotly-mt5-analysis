import dash
from dash.dependencies import Input, Output, State

from currency_analysis import calculate_currency_strength

from src.Graphs import Graphs
from src.ForexAnalyzer import ForexAnalyzer

import math

def register_callbacks(app):
    
    forex_analyzer = ForexAnalyzer()
    graph_generator = Graphs()

    @app.callback(
        [
            Output("current-currency","data"),
        ],
        [
            Input("currency-dropdown", "value")
        ]
    )
    def update_new_forex(changed_currency):
        """Callback for updating the symbol attribute

        Parameters:
           - changed_currency(str): the underlying symbol
        
        Returns:
            - list: the list of areas to update in layout
        
        """

        forex_analyzer.update_symbol(changed_currency)
        graph_generator.update_symbol(changed_currency)

        return [changed_currency]

    @app.callback(
        [
            Output("bar-currency-strength-analysis","figure"),
            Output('bar-currency-strength-analysis','style'),
        ],
        [
            Input('analysis-tabs', 'value')
        ],
        prevent_initial_call=True
    )
    def update_new_forex(tab_value):
        """Callback for displaying the currency strength analysis

        Parameters:
           - tab_value(str): the tab currently displayed at
        
        Returns:
            - list: the list of areas to update in layout
        
        """

        # Only update for currency strength tab
        if tab_value != 'currency-strength-tab':
            return [
                dash.no_update,
                {'display':'none'}
            ]

        currency_stregnth_dict = calculate_currency_strength()

        return [
            graph_generator.display_symbol_strength(currency_stregnth_dict),
            {'display':'block'}
        ]

    @app.callback(
        [
            Output("ask-value","children"),
            Output("bid-value","children"),
            Output("candlestick-4H-fig","figure"),
            Output("candlestick-15M-fig","figure"),
            Output("candlesticks-15M-heiken","figure"),
            Output("atr-graph-4H","figure"),
            Output("adx-graph-15M","figure"),
            Output("rsi-15M-fig","figure")
        ],
        [
            Input("current-currency", "data"),
            Input("refresh-stats","n_clicks")
        ]
    )
    def update_all_graphs(value, clicks):
        """Callback for updating the respective graphs, of a given symbol

        Parameters:
            - value(str): the new symbol to update at
            - clicks(int): dummy click whenever the refresh button is clicked
        
        Returns:
            - list: the list of areas to update in layout
        
        """

        ask_value, bid_value = forex_analyzer.find_ask_bid()
        
        stats_15M = forex_analyzer.get_daily_stats('15M',600)
        stats_4H = forex_analyzer.get_daily_stats('4H',600)

        return [
            f"Ask value: {ask_value:.5f}",
            f"Bid value: {bid_value:.5f}",
            graph_generator.plot_candlesticks_fullday(stats_4H, '4H', forex_analyzer.get_trend_indicators('4H')),
            graph_generator.plot_candlesticks_fullday(stats_15M, '15M', forex_analyzer.get_trend_indicators('15M')),
            graph_generator.plot_heiken_ashi(forex_analyzer.get_heiken_ashi('15M'), forex_analyzer.get_trend_indicators('15M')),
            graph_generator.plot_atr(forex_analyzer.get_trend_indicators('4H')),
            graph_generator.plot_adx_figure(forex_analyzer.get_lagging_indicator('15M', 'adx')),
            graph_generator.plot_rsi_figure(forex_analyzer.get_lagging_indicator('15M', 'rsi')),
        ]

    @app.callback(
        [
            Output('profit-target', 'children'),
            Output('loss-bound', 'children'),
            Output('bar-average-pip-fig','figure'),
            Output('bar-average-pip-fig','style')
        ],
        [
            Input('start-profit-calculation','n_clicks')
        ],
        [
            State('input_balance','value'),
            State('input_percentage_target','value'),
            State('input_percentage_loss','value'),
            State('input_leverage','value'),
            State('input_trade_count','value')
        ],
        prevent_initial_call=True
    )
    def perform_profit_calculation(click_count, bal, pct_tar, pct_loss, lev, min_trade):
        """Callback for performing risk management, on different currencies

        Parameters:
            - click(int): dummy click whenever the button is clicked
            - bal(float): the balance in the account
            - pct_tar(float): how much percentage of profit
            - pct_loss(float): how much percentage of loss
            - lev(float): the leverage input
            - min_trade(int): the number of trades to use
        
        Returns:
            - list: the list of areas to update in layout
        
        """
        
        bal = float(bal)

        amount_target = 0
        amount_loss = 0

        lev = float(lev)
        pct_tar = int(pct_tar)
        pct_loss = int(pct_loss)
        min_trade = float(min_trade)
        avg_pip_list = {}

        settlement_conversion = {
            'GBP': 1.40,
            'CHF': 1.10,
            'USD': 1.00,
            'JPY': 0.90,
            'CAD': 0.80,
        }

        if bal > 0 and lev > 0 and min_trade > 0:

            amount_target = bal * (pct_tar / 100)
            amount_loss = bal * (pct_loss / 100)
            divisor = min_trade * lev

            for currency, cur_rate in settlement_conversion.items():
                avg_pip_profit = math.ceil((amount_target / divisor)/cur_rate)
                avg_pip_loss = math.ceil((amount_loss / divisor)/cur_rate)

                avg_pip_list[currency] = {
                    'profit': avg_pip_profit,
                    'loss': avg_pip_loss
                }

        return [
            f"Target balance ({pct_tar}% increase): {(bal + amount_target):.2f} (+{amount_target:.2f})",
            f"Minimum balance ({pct_loss}% loss tolerance): {(bal - amount_loss):.2f} (-{amount_loss:.2f})",
            graph_generator.plot_pip_target(avg_pip_list),
            {'display':'block'}
        ]

    @app.callback(
        [
            Output('points-percentage-fig','figure'),
            Output('points-percentage-fig','style')
        ],
        [
            Input('show-graph-points','n_clicks')
        ],
        [
            State('input_upper','value'),
            State('input_lower','value'),
            State('input_currency','value')
        ],
        prevent_initial_call=True
    )
    def calculate_point_percentage(click, upper_num, lower_num, underlying):
        """Callback for finding the percentage, of points in a range

        Parameters:
            - click(int): dummy click whenever the button is clicked
            - upper_num(float): the upper bound
            - lower_num(float): the lower bound
            - underlying(str): the symbol to compare against
        
        Returns:
            - list: the list of areas to update in layout
        
        """

        # Find the number of points
        points_diff = forex_analyzer.calculate_point_gap(float(lower_num), float(upper_num), underlying)
        
        percentage_target = {0: 0}

        for i in range(1, 11):
            perc = i * 10
            percentage_target[perc] = int(points_diff * (perc/100))

        return [
            graph_generator.plot_profit_target(percentage_target, 'Points'),
            {'display':'block'}
        ]

    @app.callback(
        [
            Output('profit-percentage-fig','figure'),
            Output('profit-percentage-fig','style')
        ],
        [
            Input('show-graph-profit','n_clicks')
        ],
        [
            State('input_profit_target','value')
        ],
        prevent_initial_call=True
    )
    def calculate_point_percentage(click, profit_target):
        """Callback for finding the percentage, of a profit target

        Parameters:
            - click(int): dummy click whenever the button is clicked
            - profit_target(int): the profit target, broken down
        
        Returns:
            - list: the list of areas to update in layout
        
        """
 
        percentage_target = {0: 0}
        profit_target = float(profit_target)

        for i in range(1, 11):
            perc = i * 10
            percentage_target[perc] = round((profit_target * (perc/100)),2)

        return [
            graph_generator.plot_profit_target(percentage_target, 'Profit'),
            {'display':'block'}
        ]