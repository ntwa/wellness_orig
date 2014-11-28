import datetime

def timeDiff(time1,time2):
         timeA = datetime.datetime.strptime(time1, "%H:%M")
         timeB = datetime.datetime.strptime(time2, "%H:%M")
         newTime = timeA - timeB
         return newTime.seconds/3600


print timeDiff('09:00','23:00'), 'hour'