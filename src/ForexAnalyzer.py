from datetime import datetime, timedelta, date, time 
from tapy import Indicators

import MetaTrader5 as mt5
import pandas as pd

import pytz
import talib

class ForexAnalyzer:

    def __init__(self, forex_pair=None):

        self._mt5_timeframe_dict = {
            '15M': mt5.TIMEFRAME_M15,
            '30M': mt5.TIMEFRAME_M30,
            '1D': mt5.TIMEFRAME_D1,
        }
        
        self._forex_pair = forex_pair
        
        self._timezone = pytz.timezone('Europe/Moscow') # MT5 timezone

        self._rsi_today = None

        self._indicators_stats_df = {}

        if not mt5.initialize():
            print("initialize() failed, error code =",mt5.last_error())
            quit()

    def _get_multiplier(self):

        multiplier = 0.00001

        if 'JPY' in self._forex_pair:
            multiplier = 0.001
        elif 'XAU' in self._forex_pair:
            multiplier = 0.01

        return multiplier

    def _calculate_pip(self, open_price, close_price):

        pips = round((close_price - open_price) / self._get_multiplier())
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
        indicators.bollinger_bands(period=15)
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

    def find_spread(self):

        last_tick_info = mt5.symbol_info_tick(self._forex_pair)
        spread_num = self._calculate_pip(last_tick_info.bid, last_tick_info.ask)

        return spread_num


    def update_forex_pair(self, forex_pair):

        self._forex_pair = forex_pair

        return None

    def get_current_time(self, addition_hours=3):
        return datetime.now()  + timedelta(hours=addition_hours) # Local time is 3 hours behind

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
        pct_change_lambda = lambda open,close: ((close-open)/open) * 100

        rates_df['price_percentage_change'] = rates_df.apply(
            lambda x: pct_change_lambda(x['open'], x['close']), axis=1
        )

        starting_diff = 0
        diff_prev_list = []
        for pct in rates_df['price_percentage_change']:
            starting_diff += pct
            diff_prev_list.append(starting_diff)

        rates_df['percentage_diff'] = diff_prev_list

        return rates_df

    def get_daily_stats(self):

        # Last 24 hours, in 15-minute intervals
        rates_df = self._fetch_data_mt5('15M', 4*24)

        self._calculate_rsi(rates_df)
        self._create_indicators(rates_df.copy(), '15M')

        pip_lambda = lambda open_price, close_price: self._calculate_pip(open_price, close_price)
        
        rates_df['pip_difference'] = rates_df.apply(
            lambda x: pip_lambda(x['low'], x['high']), 
            axis=1
        )

        rates_df['width_candlestick'] = rates_df.apply(
            lambda x: self._calculate_pip(x['low'], x['high']),
            axis=1
        )

        return rates_df

    def get_d1_stats(self, stats_dict=None):

        # Last 24 hours, in 1-minute intervals
        if stats_dict is None:
            rates_df = self._fetch_data_mt5('1D', 1)

            stats_dict = rates_df.to_dict('records')[0]

        stats_dict['width_candlestick'] = self._calculate_pip(stats_dict['low'], stats_dict['high'])
        stats_dict['gap_high_open'] = self._calculate_pip(stats_dict['open'],stats_dict['high'])
        stats_dict['gap_open_low'] = self._calculate_pip(stats_dict['low'], stats_dict['open'])
        stats_dict['gap_close_open'] = self._calculate_pip(stats_dict['open'], stats_dict['close'])
        
        return stats_dict
    
    def get_month_stats(self):

        rates_df =  self._fetch_data_mt5('1D', 100)

        pip_lambda = lambda open_price, close_price: self._calculate_pip(open_price, close_price)
        rates_df['pip_difference'] = rates_df.apply(lambda x: pip_lambda(x['low'], x['high']), axis=1)

        self._create_indicators(rates_df.copy(), '1D')

        return rates_df