from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd

class ForexAnalyzer:

    def __init__(self, forex_pair):

        self._forex_pair = forex_pair
        
        self._time_style = {
            'Minute_1' : mt5.TIMEFRAME_M1,
            'Hour_1': mt5.TIMEFRAME_H1,
            'Day 1': mt5.TIMEFRAME_D1
        }

    def get_current_time():
        return datetime.today()

    def _find_minutes_elapsed():

        current = self.get_current_time()
        start_day = datetime(current.year, current.month, current.day)

        time_delta = (current - start_day)
    
        return int(time_delta.total_seconds()/60)