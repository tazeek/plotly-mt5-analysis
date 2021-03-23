from datetime import datetime

import pandas as pd

import MetaTrader5 as mt5
 
# connect to MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

now_time = datetime.now()
start_day = datetime.now().replace(hour = 0, minute = 0, second = 0)

eurgbp_ticks = mt5.copy_ticks_range("EURGBP", start_day, now_time, mt5.COPY_TICKS_INFO)

# shut down connection to MetaTrader 5
mt5.shutdown()

ticks_frame = pd.DataFrame(eurgbp_ticks)

# convert time in seconds into the datetime format
ticks_frame['time']=pd.to_datetime(ticks_frame['time'], unit='s')
 