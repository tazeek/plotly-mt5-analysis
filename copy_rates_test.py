from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
 
def find_minutes_passed(current):
    start_day = datetime(current.year, current.month, current.day)
    time_delta = (current - start_day)
    
    return int(time_delta.total_seconds()/60)

 
# establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()


current = datetime.today()
bars_to_get = find_minutes_passed(current)

# Get all the bars since the start of the day
currency = "EURUSD"
rates = mt5.copy_rates_from(currency, mt5.TIMEFRAME_M1, current, bars_to_get)

# create DataFrame out of the obtained data
# convert time in seconds into the datetime format
rates_frame = pd.DataFrame(rates)
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')

# display data
print(currency)
print("\nDisplay dataframe with data")
print(rates_frame)  
 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()