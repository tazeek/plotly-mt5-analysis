from datetime import datetime, timedelta, date, time 
from tapy import Indicators

import MetaTrader5 as mt5
import pandas as pd

import pytz
import talib

class ForexAnalyzer:

    def __init__(self, forex_pair):
    
        self._forex_pair = forex_pair

        self._forex_multiplier = 0.001 if 'JPY' in forex_pair else 0.00001

        self._timezone = pytz.timezone('Europe/Moscow') # MT5 timezone

        self._rsi_today = None

        self._indicators_stats_df = None

        self._start_mt5()

    def __del__(self):
        mt5.shutdown()

    def _calculate_pip(self, open_price, close_price):

        pips = round((close_price - open_price) / self._forex_multiplier)
        return abs(int(pips))

    def _calculate_rsi(self, day_stats):

        self._rsi_df = pd.DataFrame({
            'time': day_stats['time'],
            'value': talib.RSI(day_stats["close"], timeperiod=14)
        })

        return None
    
    def _create_indicators(self, day_stats):

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

        self._indicators_stats_df = indicators.df

        return None

    def _start_mt5(self):
        if not mt5.initialize():
            print("initialize() failed, error code =",mt5.last_error())
            quit()

    def get_current_time(self):
        return datetime.now()  + timedelta(hours=3) # Local time is 3 hours behind

    def get_start_day(self):
        return datetime.now(self._timezone).replace(hour=0,minute=0)

    def get_rsi_today(self):
        return self._rsi_df

    def get_hourly_stats(self):

        rates = mt5.copy_rates_from(
            self._forex_pair,
            mt5.TIMEFRAME_M30,
            self.get_current_time(),
            24 * 2 # Last 24 hours, in 30-minute intervals
        )

        rates_frame = pd.DataFrame(rates)
        rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')

        pct_change_lambda = lambda a,b: ((b-a)/a) * 10000 # Numbers are too small, bigger multiplier
        rates_frame['percentage_change'] = rates_frame.apply(
            lambda x: pct_change_lambda(x['open'], x['close']), axis=1
        )

        return rates_frame

    def get_daily_stats(self):

        rates = mt5.copy_rates_from(
            self._forex_pair, 
            mt5.TIMEFRAME_M1, 
            self.get_current_time(),
            24 * 60 # Last 24 hours, every minute
        )

        rates_frame = pd.DataFrame(rates)
        rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')

        self._calculate_rsi(rates_frame)

        pip_lambda = lambda open_price, close_price: self._calculate_pip(open_price, close_price)
        rates_frame['pip_difference'] = rates_frame.apply(lambda x: pip_lambda(x['open'], x['close']), axis=1)

        return rates_frame

    def get_d1_stats(self):

        d1_rates = mt5.copy_rates_from(
            self._forex_pair,
            mt5.TIMEFRAME_D1,
            self.get_current_time(),
            1
        )

        stats_dict = pd.DataFrame(d1_rates).to_dict('records')[0]

        del stats_dict['time']
        del stats_dict['tick_volume']
        del stats_dict['spread']
        del stats_dict['real_volume']

        stats_dict['width_candlestick'] = self._calculate_pip(stats_dict['low'], stats_dict['high'])
        stats_dict['gap_high_open'] = self._calculate_pip(stats_dict['open'],stats_dict['high'])
        stats_dict['gap_open_low'] = self._calculate_pip(stats_dict['low'], stats_dict['open'])
        stats_dict['gap_close_open'] = self._calculate_pip(stats_dict['open'], stats_dict['close'])
        
        return stats_dict
    
    def get_month_stats(self):

        d30_rates = mt5.copy_rates_from(
            self._forex_pair,
            mt5.TIMEFRAME_D1,
            self.get_current_time(),
            30
        )

        rates_frame = pd.DataFrame(d30_rates)
        rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')

        return rates_frame
