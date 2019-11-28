
import datetime


def getvalue(s):
    try:
        return float(s)
    except ValueError:
        return "false" # because 0 is also false but here in this case 0 is a valid value

def periodToHours(s):
    date1 = datetime.datetime.strptime(s.split(" - ")[0], "%Y-%m-%d %H:%M:%S") 
    date2 = datetime.datetime.strptime(s.split(" - ")[1], "%Y-%m-%d %H:%M:%S") 
    length = (date2 - date1)
    length = length.days*24 + length.seconds/3600
    return length

