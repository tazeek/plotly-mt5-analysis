from datetime import datetime, timedelta, date, time 
from tapy import Indicators

import MetaTrader5 as mt5
import pandas as pd

import pytz
import talib

class ForexAnalyzer:

    def __init__(self, forex_pair):

        self._mt5_timeframe_dict = {
            '1M': mt5.TIMEFRAME_M1,
            '30M': mt5.TIMEFRAME_M30,
            '1D': mt5.TIMEFRAME_D1,
        }
    
        self._forex_pair = forex_pair

        self._forex_multiplier = 0.001 if 'JPY' in forex_pair else 0.00001
        
        self._timezone = pytz.timezone('Europe/Moscow') # MT5 timezone

        self._rsi_today = None

        self._indicators_stats_df = {}

        if not mt5.initialize():
            print("initialize() failed, error code =",mt5.last_error())
            quit()

    def update_forex_pair(self, forex_pair):

        self._forex_pair = forex_pair
        self._forex_multiplier = 0.001 if 'JPY' in forex_pair else 0.00001

        return None

    def _calculate_pip(self, open_price, close_price):

        pips = round((close_price - open_price) / self._forex_multiplier)
        return int(pips)

    def _calculate_rsi(self, day_stats):

        self._rsi_df = pd.DataFrame({
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
        indicators.sma(period=15, column_name='sma')
        indicators.bears_power(period=15, column_name='bears_power')
        indicators.bulls_power(period=15, column_name='bulls_power')

        self._indicators_stats_df[timeframe] = indicators.df

        return None

    def _fetch_data_mt5(self, timeframe, bars_num):

        rates = mt5.copy_rates_from(
            self._forex_pair,
            self._mt5_timeframe_dict[timeframe],
            self.get_current_time(),
            bars_num
        )

        rates = pd.DataFrame(rates)
        rates['time'] = pd.to_datetime(rates['time'], unit='s')

        return rates

    def get_current_time(self):
        return datetime.now()  + timedelta(hours=3) # Local time is 3 hours behind

    def get_start_day(self):
        return datetime.now(self._timezone).replace(hour=0,minute=0)

    def get_rsi_today(self):
        return self._rsi_df

    def get_indicator_stats(self, timeframe):
        return self._indicators_stats_df[timeframe]

    def get_hourly_stats(self):

        # Last 24 hours, in 30-minute intervals
        rates_df = self._fetch_data_mt5('30M', 24*2)

        self._create_indicators(rates_df.copy(), '30M')

        # Numbers are too small, bigger multiplier
        pct_change_lambda = lambda a,b: ((b-a)/a) * 100
        rates_df['percentage_change'] = rates_df.apply(
            lambda x: pct_change_lambda(x['open'], x['close']), axis=1
        )

        return rates_df

    def get_daily_stats(self):

        # Last 24 hours, in 1-minute intervals
        rates_df = self._fetch_data_mt5('1M', 24*60)

        self._calculate_rsi(rates_df)
        self._create_indicators(rates_df.copy(), '1M')

        pip_lambda = lambda open_price, close_price: self._calculate_pip(open_price, close_price)
        rates_df['pip_difference'] = rates_df.apply(lambda x: pip_lambda(x['low'], x['high']), axis=1)

        return rates_df

    def get_d1_stats(self):

        # Last 24 hours, in 1-minute intervals
        rates_df = self._fetch_data_mt5('1D', 1)

        stats_dict = pd.DataFrame(rates_df).to_dict('records')[0]

        stats_dict['width_candlestick'] = self._calculate_pip(stats_dict['low'], stats_dict['high'])
        stats_dict['gap_high_open'] = self._calculate_pip(stats_dict['open'],stats_dict['high'])
        stats_dict['gap_open_low'] = self._calculate_pip(stats_dict['low'], stats_dict['open'])
        stats_dict['gap_close_open'] = self._calculate_pip(stats_dict['open'], stats_dict['close'])
        
        return stats_dict
    
    def get_month_stats(self):

        rates_df =  self._fetch_data_mt5('1D', 30)

        pip_lambda = lambda open_price, close_price: self._calculate_pip(open_price, close_price)
        rates_df['pip_difference'] = rates_df.apply(lambda x: pip_lambda(x['low'], x['high']), axis=1)

        return rates_df