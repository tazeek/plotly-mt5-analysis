from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd

class ForexAnalyzer:

    def __init__(self, forex_pair):

        self._forex_pair = forex_pair

    def _find_minutes_elapsed():

        current = dateime.today()
        start_day = datetime(current.year, current.month, current.day)
        
        time_delta = (current - start_day)
    
        return int(time_delta.total_seconds()/60)