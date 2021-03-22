from datetime import datetime

import pandas as pd

import MetaTrader5 as mt5
 
# connect to MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()
 
# request connection status and parameters
print(mt5.terminal_info())
# get data on MetaTrader 5 version
print(mt5.version())
 
# request 1000 ticks from EURAUD
eurgbp_ticks = mt5.copy_ticks_from("EURGBP", datetime(2020,1,28,13), 1000, mt5.COPY_TICKS_ALL) 

# shut down connection to MetaTrader 5
mt5.shutdown()
 
#DATA
print('eurgbp_ticks(', len(eurgbp_ticks), ')')
for val in eurgbp_ticks[:10]: print(val)
 