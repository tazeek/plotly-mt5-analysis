from datetime import datetime, timedelta, date, time 
from tapy import Indicators

import MetaTrader5 as mt5
import pandas as pd

import pytz
import talib

class ForexAnalyzer:

    def __init__(self, symbol=None):

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

        if not mt5.initialize():
            print("initialize() failed, error code =",mt5.last_error())
            quit()

    def _get_multiplier(self, symbol=None):
        """Get the multiplier, based on number of digits

        Parameters:
            - symbol(str): Get the underlying symbol
        
        Returns:
            - float: Return the divisor, based on number of decimal places
        
        """

        symbol_info = mt5.symbol_info(symbol or self._symbol)

        return 10 ** -symbol_info.digits

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
        indicators.smma(period=21, column_name='sma_21', apply_to='Close')
        indicators.smma(period=50, column_name='sma_50', apply_to='Close')
        indicators.smma(period=200, column_name='sma_200', apply_to='Close')
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
        # Local time is 3 hours behind
        return datetime.now()  + timedelta(hours=addition_hours) 

    def get_start_day(self):
        return datetime.now(self._timezone).replace(hour=0,minute=0,second=0).strftime("%Y-%m-%d %H:%M:%S")

    def get_lagging_indicator(self,timeframe, indicator):
        return self._lagging_indicators[timeframe][indicator]

    def get_trend_indicators(self, timeframe):
        return self._indicators_stats_df[timeframe]

    def get_daily_stats(self, timeframe='15M', bar_count=100):

        rates_df = self._fetch_data_mt5(timeframe, bar_count)

        self._calculate_lagging_indicators(rates_df, timeframe)
            
        self._create_trend_indicators(rates_df.copy(), timeframe)

        return rates_df

    def get_currency_strength(self, symbol):
        rates_df = self._fetch_data_mt5('1W', 5, symbol)

        close_price_series = rates_df['close']

        oldest_close_price = close_price_series.iat[0]
        current_close_price = close_price_series.iat[-1]

        percentage_strength = ((current_close_price - oldest_close_price)/oldest_close_price) * 100

        return round(percentage_strength,3)