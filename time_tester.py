from datetime import datetime

current = datetime.today()

start_day = datetime(current.year, current.month, current.day)

time_delta = (current - start_day)
minutes = int(time_delta.total_seconds()/60)

print(start_day)
print(current)
print(minutes)