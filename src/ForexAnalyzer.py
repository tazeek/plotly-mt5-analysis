from datetime import datetime, timedelta, date, time 
from tapy import Indicators

import MetaTrader5 as mt5
import pandas as pd

import pytz
import talib

class ForexAnalyzer:

    __instance__ = None

    def __init__(self):

        if ForexAnalyzer.__instance__ is None:
           ForexAnalyzer.__instance__ = self
        else:
            raise Exception("You cannot create another ForexAnalyzer class")     

        self._mt5_timeframe_dict = {
            '1H': mt5.TIMEFRAME_H1,
            '4H': mt5.TIMEFRAME_H4,
            '1W': mt5.TIMEFRAME_W1
        }
        
        self._symbol = None
        
        self._timezone = pytz.timezone('Europe/Moscow') # MT5 timezone

        self._lagging_indicators = {}

        self._indicators_stats_df = {}

        self._heiken_ashi_df = {}

        self._currency_strength_list = []

        self._full_currency_list = []

        if not mt5.initialize():
            print("initialize() failed, error code =",mt5.last_error())
            quit()

    @staticmethod
    def get_instance():
        """Static method to fetch the current instance
        """

        if not ForexAnalyzer.__instance__:
            ForexAnalyzer()
        
        return ForexAnalyzer.__instance__

    def _create_heiken_ashi(self, rates_df, timeframe):
        """Create data for heiken ashi plots, based on the given timeframe

        Parameters:
            - data: a copy of the forex data fetched
            - timeframe: the given timeframe
        
        Return:
            - None
        
        """

        data = rates_df.copy()
        
        for i in range(data.shape[0]):
            if i > 0:
                data.loc[data.index[i],'open'] = (rates_df['open'][i-1] + rates_df['close'][i-1])/2
            
            data.loc[data.index[i],'close'] = (rates_df['open'][i] + rates_df['close'][i] + rates_df['low'][i] +  rates_df['high'][i])/4
        
        data = data.iloc[1:,:]
        
        self._heiken_ashi_df[timeframe] = data

        return None

    def _calculate_lagging_indicators(self, day_stats, timeframe):
        """Create the lagging indicators and store in object attribute (self._lagging_indicators)

        Parameters:
            - day_stats(dataframe): dataframe containting the stats of the given symbol
            - timeframe(str): the given timeframe to create the stats on
        
        Returns:
            - None
        
        """

        timeperiod = 14

        rsi_stats = {
            'time': day_stats['time'],
            'value': talib.RSI(day_stats["close"], timeperiod=14)
        }

        self._lagging_indicators[timeframe] = {
            'rsi': rsi_stats
        }

        return None

    def _get_symbol_info_tick(self, symbol):
        return mt5.symbol_info_tick(symbol)

    def _get_margin_calculation(self, lot, action, symbol, ask):
        return mt5.order_calc_margin(action,symbol,lot,ask)
    
    def _create_trend_indicators(self, day_stats, timeframe):
        """Create the trend indicators and store in object attribute (self._indicator_stats_df)

        Parameters:
            - day_stats(dataframe): dataframe containting the stats of the given symbol
            - timeframe(str): the given timeframe to create the stats on
        
        Returns:
            - None
        
        """

        day_stats.rename(
            columns={
                "close": "Close", 
                "high": "High",
                "low": "Low",
                "open": "Open"
            },
            inplace=True
        )

        indicators = Indicators(day_stats)
        indicators.atr(period=50, column_name='atr')

        self._indicators_stats_df[timeframe] = indicators.df

        return None

    def _fetch_data_mt5(self, timeframe, bar_count, symbol=None):
        """Fetch the data from MT5 servers, based on the given symbol

        Parameters:
            - timeframe(str): the given timeframe to fetch the stats
            - bar_count(int): the number of candlesticks to fetch
            - symbol(str): the underlying symbol
        
        Returns:
            - dataframe: the statistical data from MT5 for the given symbol 
        
        """

        rates = mt5.copy_rates_from(
            symbol or self._symbol,
            self._mt5_timeframe_dict[timeframe],
            self.get_current_time(),
            bar_count
        )

        rates = pd.DataFrame(rates)
        rates['time'] = pd.to_datetime(rates['time'], unit='s')

        return rates

    def get_digits(self, symbol=None):
        symbol_info = mt5.symbol_info(symbol or self._symbol)

        return symbol_info.digits
    
    def get_multiplier(self, symbol=None):
        """Get the multiplier, based on number of digits

        Parameters:
            - symbol(str): Get the underlying symbol
        
        Returns:
            - float: Return the divisor, based on number of decimal places
        
        """

        return 10 ** -self.get_digits(symbol)


    def update_symbol(self, symbol):
        """Update the symbol, whenever there is a new symbol passed

        Parameters:
            - symbol(str): the new symbol to be updated
        
        Returns:
            - None
        
        """

        self._symbol = symbol
        return None

    def get_current_time(self, addition_hours=3):
        """Get the current time, based on the timezone

        Parameters:
            - additional_hours(int): the extra hours to be added in
        
        Returns:
            - datetime: datetime object that is ahead, based on the addition_hours
        
        """

        # Local time is 3 hours behind
        return datetime.now()  + timedelta(hours=addition_hours)
    
    def get_heiken_ashi(self, timeframe):
        return self._heiken_ashi_df[timeframe]

    def get_lagging_indicator(self,timeframe, indicator):
        """Get the respective lagging indicator, based on the timeframe

        Parameters:
            - indicator(str): the indicator to fetch
            - timeframe(str): the timeframe to fetch in
        
        Returns:
            - dataframe: dataframe containing the indicator stats
        
        """

        return self._lagging_indicators[timeframe][indicator]

    def get_trend_indicators(self, timeframe):
        """Get the trend indicators, based on the timeframe

        Parameters:
            - timeframe(str): the timeframe to fetch in
        
        Returns:
            - dataframe: dataframe containing the indicator stats
        
        """

        return self._indicators_stats_df[timeframe]

    def get_daily_stats(self, timeframe='15M', bar_count=100):
        """Get the data of the symbol, based on the timeframe and candlesticks
        This is followed by creating the lagging and trend indicators

        Parameters:
            - timeframe(str): the timeframe to fetch in
            - bar_count(int): how many candlesticks to fetch
        
        Returns:
            - dataframe: dataframe containing the symbol stats
        
        """

        rates_df = self._fetch_data_mt5(timeframe, bar_count)

        self._calculate_lagging_indicators(rates_df, timeframe)
        self._create_trend_indicators(rates_df.copy(), timeframe)
        self._create_heiken_ashi(rates_df, timeframe)

        return rates_df

    def get_currency_strength(self):
        """Get the strength of the symbol for currency strength analysis

        Parameters:
            - symbol(str): the given symbol
        
        Returns:
            - float: the strength of the given symbol
        
        """
        currency_strength = {
            'JPY': 0.00
        }

        for symbol in self._currency_strength_list:

            rates_df = self._fetch_data_mt5('1W', 5, symbol)

            close_price_series = rates_df['close']

            oldest_close_price = close_price_series.iat[0]
            current_close_price = close_price_series.iat[-1]

            percentage_strength = ((current_close_price - oldest_close_price)/oldest_close_price) * 100
            currency_strength[symbol[:3]] = round(percentage_strength,3)

        # Sort out dictionary in descending order
        currency_strength = dict(
            sorted(currency_strength.items(), key=lambda item: item[1], reverse=True)
        )

        return currency_strength

    def get_currency_correlations(self, symbols_list):
        """Get the correlations between different currency pairs

        Parameters:
            - symbols_list(list): the list of symbols

        Returns:
            - dataframe: the dataframe containing the correlated data
        """

        currency_correlation_df = pd.DataFrame()

        for currency_pair in symbols_list:
            # 1. Fetch the last 30 days data, in 4-hour intervals
            # 1 day = 24 hours (6 4-hour intervals); 30 days = (6 * 30 = 180)
            data = self._fetch_data_mt5('4H', 180, currency_pair)

            # 2. Fetch only the closing price of the given pair
            currency_correlation_df[currency_pair] = data['close']

        return currency_correlation_df.corr().round(3)

    def get_symbol_list(self):
        """Get all the symbols list from MT5
        """

        if self._full_currency_list:
            return self._full_currency_list

        symbols = mt5.symbols_get()

        for symbol in symbols:

            symbol = symbol.name

            if 'JPY' in symbol:
                self._currency_strength_list.append(symbol)
            
            self._full_currency_list.append(symbol)
    
        return self._full_currency_list

    def get_symbol_volume(self):
        """Get the volume data, based on the weekly timeframe
        """

        symbol_info_list = []

        for symbol in self._full_currency_list:
            data = self._fetch_data_mt5('1W', 1, symbol)
            symbol_info_list.append({
                'symbol': symbol,
                'volume': data['tick_volume'].iat[0]
            })
        
        symbol_info_list = sorted(symbol_info_list, key=lambda k: k['volume'], reverse=True)

        symbols_only = []

        for symbol_info in symbol_info_list:
            if symbol_info['symbol'] not in symbols_only:
                symbols_only.append(symbol_info['symbol'])
        
        return symbols_only

    def calculate_margin(self, action_type, lot_size, symbol):

        # Find the MT5 action for Buy/Sell
        mt5_action = None
        price = None

        symbol_data = self._get_symbol_info_tick(symbol)

        if action_type == 'buy':
            mt5_action = mt5.ORDER_TYPE_BUY
            price = symbol_data.ask
        else:
            mt5_action = mt5.ORDER_TYPE_SELL
            price = symbol_data.bid

        price = float(price)
        lot_size = float(lot_size)

        return self._get_margin_calculation(float(lot_size), mt5_action, symbol, price)
