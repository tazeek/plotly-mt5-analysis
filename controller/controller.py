import dash
from dash.dependencies import Input, Output, State

from currency_analysis import calculate_currency_strength
from economics_events_scraper import ForexFactoryScraper

from src.Graphs import Graphs
from src.ForexAnalyzer import ForexAnalyzer

import math

def register_callbacks(app):
    
    forex_analyzer = ForexAnalyzer.get_instance()
    graph_generator = Graphs()

    settlement_conversion = {
        'GBP': 1.40,
        'CHF': 1.10,
        'USD': 1.00,
        'JPY': 0.90,
        'CAD': 0.80,
    }

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

        digits = forex_analyzer.get_digits(changed_currency)

        forex_analyzer.update_symbol(changed_currency)
        graph_generator.update_symbol(changed_currency, digits)

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
            Output("candlesticks-1H-heiken","figure"),
            Output("adx-graph-1H","figure"),
            Output("rsi-4H-fig","figure"),
            Output("point-counts-1H", "figure"),
            Output("atr-graph-1H", "figure")
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

        digit_precision = forex_analyzer.get_digits()
        ask_value, bid_value = forex_analyzer.find_ask_bid()
        
        stats_1H = forex_analyzer.get_daily_stats('1H',600)
        stats_4H = forex_analyzer.get_daily_stats('4H',600)

        return [
            f"Ask value: {ask_value: .{digit_precision}f}",
            f"Bid value: {bid_value: .{digit_precision}f}",
            graph_generator.plot_candlesticks_fullday(stats_4H, '4H', forex_analyzer.get_trend_indicators('4H')),
            graph_generator.plot_heiken_ashi(forex_analyzer.get_heiken_ashi('1H'), forex_analyzer.get_trend_indicators('1H')),
            graph_generator.plot_adx_figure(forex_analyzer.get_lagging_indicator('1H', 'adx')),
            graph_generator.plot_rsi_figure(forex_analyzer.get_lagging_indicator('4H', 'rsi')),
            graph_generator.plot_pip_range_counts(stats_1H, forex_analyzer.get_multiplier()),
            graph_generator.plot_atr(forex_analyzer.get_trend_indicators('1H'), stats_1H, '1H'),
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

    @app.callback(
        [
            Output('currency-correlation-fig', 'figure'),
            Output('currency-correlation-fig','style')
        ],
        [
            Input('show-correlation-heatmap','n_clicks')
        ],
        [
            State('input_currencies_list','value')
        ],
        prevent_initial_call=True
    )
    def calculate_correlation_currencies(click, currencies):
        """Callback for finding the percentage, of a profit target

        Parameters:
            - click(int): dummy click whenever the button is clicked
            - profit_target(int): the profit target, broken down
        
        Returns:
            - list: the list of areas to update in layout
        
        """

        currencies_list = currencies.split(',')
        correlated_df = forex_analyzer.get_currency_correlations(currencies_list)

        return [
            graph_generator.plot_correlation_heatmap(correlated_df),
            {'display':'block'}
        ]

    @app.callback(
        [
            Output("download-volume-begin", "data")
        ],
        [
            Input("download-volume-data", "n_clicks")
        ],
        prevent_initial_call=True,
    )
    def get_symbol_volume_sorted(n_clicks):

        symbol_list_vol = forex_analyzer.get_symbol_volume()

        file_text = ""

        for index, symbol in enumerate(symbol_list_vol):
            file_text += f"{index+1}. {symbol}\n"
        
        return [
            dict(content=file_text, filename="volume_data.txt")
        ]

    @app.callback(
        [
            Output('points-fig','figure'),
            Output('points-fig','style')
        ],
        [
            Input('show-graph-points','n_clicks')
        ],
        [
            State('input_amount','value'),
            State('input_volume','value')
        ],
        prevent_initial_call=True
    )
    def calculate_point_profit(click, amount, leverage):

        amount = float(amount)
        leverage = float(leverage)

        points_req_dict = {}

        for currency, cur_rate in settlement_conversion.items():

            points_req_dict[currency] = math.ceil((amount / leverage)/cur_rate)

        return [
            graph_generator.plot_minimum_profit(points_req_dict),
            {'display':'block'}
        ]

    @app.callback(
        [
            Output("download-economic-begin", "data")
        ],
        [
            Input("download-today-economic", "n_clicks")
        ],
        prevent_initial_call=True,
    )
    def get_symbol_volume_sorted(n_clicks):

        economic_obj = ForexFactoryScraper('this')
        
        return [
            dict(content=economic_obj.get_today_events(), filename="today_economic_events.txt")
        ]