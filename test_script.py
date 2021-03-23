from datetime import datetime

import pandas as pd

import MetaTrader5 as mt5
 
# connect to MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

now_time = datetime.now()
start_day = datetime.now().replace(hour = 0, minute = 0, second = 0)

eurgbp_ticks = mt5.copy_ticks_range("EURGBP", start_day, now_time)

# shut down connection to MetaTrader 5
mt5.shutdown()
 
print('OUT HERE!')

#DATA
print('eurgbp_ticks(', len(eurgbp_ticks), ')')
for val in eurgbp_ticks[-1]: print(val)
 