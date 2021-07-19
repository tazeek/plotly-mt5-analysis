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

        self._indicators_stats_df = {}

        if not mt5.initialize():
            print("initialize() failed, error code =",mt5.last_error())
            quit()

    def _get_multiplier(self, symbol=None):

        symbol_info = mt5.symbol_info(symbol or self._symbol)

        return 10 ** -symbol_info.digits

    def calculate_point_gap(self, open_price, close_price, symbol=None):

        points = round((close_price - open_price) / self._get_multiplier(symbol))
        return int(points)

    def _calculate_rsi(self, day_stats, timeframe):

        self._rsi_df[timeframe] = pd.DataFrame({
            'time': day_stats['time'],
            'value': talib.RSI(day_stats["close"], timeperiod=14)
        })

        return None
    
    def _create_indicators(self, day_stats, timeframe):

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

        last_tick_info = mt5.symbol_info_tick(self._symbol)

        return last_tick_info.ask, last_tick_info.bid


    def update_symbol(self, symbol):

        self._symbol = symbol

        return None

    def get_current_time(self, addition_hours=3):
        return datetime.now()  + timedelta(hours=addition_hours) # Local time is 3 hours behind

    def get_start_day(self):
        return datetime.now(self._timezone).replace(hour=0,minute=0,second=0).strftime("%Y-%m-%d %H:%M:%S")

    def get_rsi_today(self, timeframe):
        return self._rsi_df[timeframe]

    def get_indicator_stats(self, timeframe):
        return self._indicators_stats_df[timeframe]

    def get_daily_stats(self, timeframe='15M', bar_count=100):

        rates_df = self._fetch_data_mt5(timeframe, bar_count)

        self._calculate_rsi(rates_df, timeframe)
            
        self._create_indicators(rates_df.copy(), timeframe)

        return rates_df

    def get_currency_strength(self, symbol):
        rates_df = self._fetch_data_mt5('1W', 5, symbol)

        close_price_series = rates_df['close']

        oldest_close_price = close_price_series.iat[0]
        current_close_price = close_price_series.iat[-1]

        percentage_strength = ((current_close_price - oldest_close_price)/oldest_close_price) * 100

        return round(percentage_strength,3)