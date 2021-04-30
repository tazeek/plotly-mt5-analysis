from datetime import datetime, timedelta, date, time 
import MetaTrader5 as mt5
import pytz
import pandas as pd

class ForexAnalyzer:

    def __init__(self, forex_pair):
    
        self._forex_pair = forex_pair

        self._start_mt5()

    def __del__(self):
        mt5.shutdown()

    def _start_mt5(self):
        if not mt5.initialize():
            print("initialize() failed, error code =",mt5.last_error())
            quit()

    def get_current_time(self):
        return datetime.today()

    def get_start_day(self):
        return datetime.combine(date.today(), time()) 

    def get_hourly_stats(self):

        rates = mt5.copy_rates_from(
            self._forex_pair,
            mt5.TIMEFRAME_M30,
            self.get_current_time() + timedelta(hours=3),
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
            self.get_current_time() + timedelta(hours=3), # Local time is 3 hours behind
            24 * 60 # Last 24 hours, every minute
        )

        rates_frame = pd.DataFrame(rates)
        rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')

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

        stats_dict['width_candlestick'] = int((stats_dict['high'] - stats_dict['low']) * 10**5)
        stats_dict['gap_open_high'] = int((stats_dict['high'] - stats_dict['open']) * 10**5)
        stats_dict['gap_open_low'] = int((stats_dict['open'] - stats_dict['low']) * 10**5)
        stats_dict['gap_open_close'] = int((stats_dict['open'] - stats_dict['close']) * 10**5)
        
        return stats_dict
    
    def get_month_stats(self):

        d7_rates = mt5.copy_rates_from(
            self._forex_pair,
            mt5.TIMEFRAME_D1,
            self.get_current_time(),
            30
        )

        rates_frame = pd.DataFrame(d7_rates)
        rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')

        return rates_frame
