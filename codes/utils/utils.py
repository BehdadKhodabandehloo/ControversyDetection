import datetime
import time


def datetime_to_timestamp(t):
    timestamp = datetime.datetime.strptime(t.replace(' +0000', ''), '%a %b %d %H:%M:%S %Y')
    return time.mktime(timestamp.timetuple())