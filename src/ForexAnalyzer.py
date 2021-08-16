from datetime import datetime, timedelta, date, time 
from tapy import Indicators

import MetaTrader5 as mt5
import pandas as pd

import pytz
import talib

class ForexAnalyzer:

    __instance__ = None

    def __init__(self, symbol=None):

        if ForexAnalyzer.__instance__ is None:
           ForexAnalyzer.__instance__ = self
        else:
            raise Exception("You cannot create another ForexAnalyzer class")     

        self._mt5_timeframe_dict = {
            '15M': mt5.TIMEFRAME_M15,
            '1H': mt5.TIMEFRAME_H1,
            '1D': mt5.TIMEFRAME_D1,
            '4H': mt5.TIMEFRAME_H4,
            '1W': mt5.TIMEFRAME_W1
        }
        
        self._symbol = symbol
        
        self._timezone = pytz.timezone('Europe/Moscow') # MT5 timezone

        self._rsi_df = {}

        self._adx_df = {}

        self._lagging_indicators = {}

        self._indicators_stats_df = {}

        self._heiken_ashi_df = {}

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

    def _get_multiplier(self, symbol=None):
        """Get the multiplier, based on number of digits

        Parameters:
            - symbol(str): Get the underlying symbol
        
        Returns:
            - float: Return the divisor, based on number of decimal places
        
        """

        symbol_info = mt5.symbol_info(symbol or self._symbol)

        return 10 ** -symbol_info.digits

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

        adx = {
            'time': day_stats['time'],
            'value': talib.ADX(
                day_stats['high'],
                day_stats['low'],
                day_stats['close'],
                timeperiod=timeperiod
            )
        }

        pd.DataFrame({
            'time': day_stats['time'],
            'value': talib.RSI(day_stats["close"], timeperiod=timeperiod)
        })

        self._lagging_indicators[timeframe] = {
            'rsi': rsi_stats,
            'adx': adx
        }

        return None
    
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
        indicators.smma(period=50, column_name='sma_50', apply_to='Close')
        indicators.atr(period=50, column_name='atr')

        indicators.bollinger_bands(
            period=20, deviation=2, 
            column_name_top='upper_bound', 
            column_name_mid='sma_bollinger', 
            column_name_bottom='lower_bound'
        )

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

    def find_ask_bid(self):
        """Find the ask and bid price for the given symbol

        Parameters:
            None
        
        Returns:
            - str: the ask price of the symbol
            - str: the bid price of the symbol 
        
        """
        
        last_tick_info = mt5.symbol_info_tick(self._symbol)
        return last_tick_info.ask, last_tick_info.bid


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

    def calculate_point_gap(self, open_price, close_price, symbol=None):
        """Find the point gap between the opening price and closing price

        Parameters:
            - open_price(float_price): the opening price
            - close_price(float_price): the closing price
            - symbol(str): the underlying symbol
        
        Returns:
            - int: the point difference
        
        """

        points = round((close_price - open_price) / self._get_multiplier(symbol))
        return int(points) 
    
    def get_heiken_ashi(self, timeframe):
        return self._heiken_ashi_df[timeframe]

    def get_start_day(self):
        """Get the current time, based on the timezone

        Parameters:
            - additional_hours(int): the extra hours to be added in
        
        Returns:
            - datetime: datetime object that is ahead, based on the addition_hours
        
        """
        
        return datetime.now(self._timezone).replace(hour=0,minute=0,second=0).strftime("%Y-%m-%d %H:%M:%S")

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

    def get_currency_strength(self, symbol):
        """Get the strength of the symbol for currency strength analysis

        Parameters:
            - symbol(str): the given symbol
        
        Returns:
            - float: the strength of the given symbol
        
        """
        rates_df = self._fetch_data_mt5('1W', 5, symbol)

        close_price_series = rates_df['close']

        oldest_close_price = close_price_series.iat[0]
        current_close_price = close_price_series.iat[-1]

        percentage_strength = ((current_close_price - oldest_close_price)/oldest_close_price) * 100

        return round(percentage_strength,3)

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

    def get_symbol_list(self, filter=None):
        """Get all the symbols list from MT5
        """
        group_filter = filter or "!*BTC*, !*PLN*,!*GBX*,!*XBT*,!*ETH*,*USD*,*EUR*,*JPY*,*AUD*,*NZD*"
        symbols = mt5.symbols_get(group=group_filter)

        return [symbol.name for symbol in symbols]