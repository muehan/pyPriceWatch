import datetime

now = datetime.datetime.now()
dateStr = '' + str(now.year) + '-' + str(now.month).zfill(2) + '-' + str(now.day).zfill(2)

print(dateStr)