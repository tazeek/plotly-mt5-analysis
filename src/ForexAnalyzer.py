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
            '1H': mt5.TIMEFRAME_H1,
            '1D': mt5.TIMEFRAME_D1,
            '4H': mt5.TIMEFRAME_H4,
            '1W': mt5.TIMEFRAME_W1
        }
        
        self._forex_pair = forex_pair
        
        self._timezone = pytz.timezone('Europe/Moscow') # MT5 timezone

        self._rsi_df = {}

        self._indicators_stats_df = {}

        if not mt5.initialize():
            print("initialize() failed, error code =",mt5.last_error())
            quit()

    def _get_multiplier(self):

        symbol_info = mt5.symbol_info(self._forex_pair)

        return 10 ** -symbol_info.digits

    def _calculate_pip(self, open_price, close_price):

        pips = round((close_price - open_price) / self._get_multiplier())
        return int(pips)

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

    def _fetch_data_mt5(self, timeframe, bars_num, pair=None):

        rates = mt5.copy_rates_from(
            pair or self._forex_pair,
            self._mt5_timeframe_dict[timeframe],
            self.get_current_time(),
            bars_num
        )

        rates = pd.DataFrame(rates)
        rates['time'] = pd.to_datetime(rates['time'], unit='s')

        return rates

    def _find_support_areas(self,df,i):

        current_previous = df['Low'][i] < df['Low'][i-1]
        current_next = df['Low'][i] < df['Low'][i+1]
        previous_two = df['Low'][i+1] < df['Low'][i+2]
        next_two = df['Low'][i-1] < df['Low'][i-2]

        support = current_previous and current_next and previous_two and next_two

        return support

    def _find_resistance_areas(self, df,i):

        current_previous = df['High'][i] > df['High'][i-1]
        current_next = df['High'][i] > df['High'][i+1]
        previous_two = df['High'][i+1] > df['High'][i+2]
        next_two = df['High'][i-1] > df['High'][i-2]

        resistance = current_previous and current_next and previous_two and next_two

        return resistance

    def find_ask_bid(self):

        last_tick_info = mt5.symbol_info_tick(self._forex_pair)

        return last_tick_info.ask, last_tick_info.bid


    def update_forex_pair(self, forex_pair):

        self._forex_pair = forex_pair

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
        stats_dict['gap_high_close'] = self._calculate_pip(stats_dict['close'],stats_dict['high'])
        stats_dict['gap_close_low'] = self._calculate_pip(stats_dict['low'], stats_dict['close'])
        stats_dict['gap_close_open'] = self._calculate_pip(stats_dict['open'], stats_dict['close'])
        
        return stats_dict

    def get_currency_strength(self, currency_pair):
        rates_df = self._fetch_data_mt5('1W', 5, currency_pair)

        close_price_series = rates_df['close']

        oldest_close_price = close_price_series.iat[0]
        current_close_price = close_price_series.iat[-1]

        rop_val = ((current_close_price - oldest_close_price)/oldest_close_price) * 100

        return round(rop_val,3)

    def find_support_resistance(self, df):
        levels = []
        
        for i in range(2,df.shape[0]-2):
            if self._find_support_areas(df, i):
                levels.append(df['Low'].iat[i])
            elif self._find_resistance_areas(df, i):
                levels.append(df['High'].iat[i])
        
        print(levels)