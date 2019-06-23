import datetime
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)
 
cur_date = datetime.datetime.now().date()
print(cur_date)
 
 
# d = datetime.date(2011, 7, 2)
next_monday = next_weekday(cur_date, 0) # 0 = Monday, 1=Tuesday, 2=Wednesday...
print(next_monday)