from datetime import datetime

import pandas as pd

import MetaTrader5 as mt5
 
# connect to MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

intialize_today = datetime.now()
intialize_today.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
 
# request 1000 ticks from EURGBP
eurgbp_ticks = mt5.copy_ticks_from("EURGBP", intialize_today, 1000, mt5.COPY_TICKS_ALL) 

# shut down connection to MetaTrader 5
mt5.shutdown()
 
print('OUT HERE!')

#DATA
print('eurgbp_ticks(', len(eurgbp_ticks), ')')
for val in eurgbp_ticks[:10]: print(val)
 