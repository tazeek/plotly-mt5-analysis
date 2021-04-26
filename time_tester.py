from datetime import datetime
import pytz

timezone = pytz.timezone("Etc/UTC")
today = datetime.today()

utc_from = datetime(today.year, today.month, today.day, tzinfo=timezone)

print(utc_from)