from tkinter import *
import time
import datetime 
# START_TIME=time.time()
# datetime.datetime.today().weekday()
# THIS_TIME=datetime.datetime.now()
# from datetime import date
# import calendar
# my_date = date.today()
# calendar.day_name[my_date.weekday()] 
# #datetime.today().strftime('%A')#'Wednesday'

# import datetime
# dt = '21/03/2012'
# day, month, year = (int(x) for x in dt.split('/'))    
# ans = datetime.date(year, month, day)
# print (ans.strftime("%A"))

import datetime

intDay = datetime.date(year=2000, month=12, day=1).weekday()
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
print(days[intDay])


# => datetime.datetime(2009, 12, 15, 13, 50, 35, 833175)

# # check if weekday is 1..5
# >>> d.isoweekday() in range(1, 6)
# True

# # check if hour is 10..15
# >>> d.hour in range(10, 15)
# True

# # check if minute is 30
# >>> d.minute==30
# False

# import calendar
# >>> d=dict(enumerate(calendar.day_name))
# >>> d

# >>> d=dict(zip(calendar.day_name,range(7)))
# >>> d
# {'Monday': 0, 'Tuesday': 1, 'Friday': 4, 'Wednesday': 2, 'Thursday': 3, 'Sunday': 6, 'Saturday': 5}

# import datetime
# # make a list of seven arbitrary dates in a row
# dates=[datetime.date.fromtimestamp(0) + datetime.timedelta(days=d) for d in range(7)]
# # make a dictionary showing the names and numbers of the days of the week
# print ({d.strftime('%A'): d.weekday() for d in dates})

import calendar
def week_day(time:datetime.datetime=datetime.datetime.today()):
    week_index=calendar.weekday(time.year,time.month,time.day)
    weekdays=[]
    for day in range(1,7-week_index):
        weekdays.append(time+datetime.timedelta(day))

    for day in range(0,week_index+1):
        weekdays.append(time-datetime.timedelta(day))
    weekdays=list(set(weekdays))
    weekdays.sort(key=datetime.datetime.weekday)
    return weekdays

the_time=datetime.datetime(2021,2,3)
print(days[the_time.isocalendar()[2]-1],[(day.strftime("%a"),(day.day,day.month),the_time.isocalendar()[1]) for day in week_day(the_time)])