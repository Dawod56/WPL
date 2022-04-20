from datetime import datetime, timedelta

year = datetime.now()
today = datetime.now()
year2 = year+timedelta(days=182)
year = year.strftime("%Y")
year2 = year2.strftime("%Y")
a = int(year)
b = int(year2)
start = datetime(day=1, month=7, year=a)
print('start', start)
end = datetime(day=30, month=6, year=b)
print(end)
