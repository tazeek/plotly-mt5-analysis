from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
import pytz
 
# import the 'pandas' module for displaying data obtained in the tabular form
# import pytz module for working with time zone
 
# establish connection to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()
 
# set time zone to UTC
timezone = pytz.timezone("Etc/UTC")
today = datetime.today()

# create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
utc_from = datetime(today.year, today.month, today.day, tzinfo=timezone)

# get 10 EURUSD H4 bars starting from 01.10.2020 in UTC time zone
currency = "EURUSD"
rates = mt5.copy_rates_from(currency, mt5.TIMEFRAME_D1, utc_from, 12)
 
# shut down connection to the MetaTrader 5 terminal
mt5.shutdown()
 
# create DataFrame out of the obtained data
rates_frame = pd.DataFrame(rates)
# convert time in seconds into the datetime format
rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')
                           
# display data
print(currency)
print("\nDisplay dataframe with data")
print(rates_frame)  