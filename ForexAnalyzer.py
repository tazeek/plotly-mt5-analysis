from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd

class ForexAnalyzer:

    def __init__(self, forex_pair):

        self.forex_pair = forex_pair