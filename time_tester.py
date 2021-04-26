from datetime import datetime

today = datetime.today()

utc_from = datetime(today.year, today.month, today.day)

print(utc_from)
print(today)