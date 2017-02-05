import time
import datetime


def human_time(date):
    return datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')


def unix_time(day, month, year, hour=0, minute=0, second=0):
    return time.mktime(datetime.datetime(year, month, day, hour, minute, second).timetuple())


def get_time(operation_date, date):
    hour = date.split(':')[0]
    minute = date.split(':')[1]
    current_date = datetime.datetime.fromtimestamp(operation_date)
    return unix_time(int(current_date.day), int(current_date.month), int(current_date.year), int(hour), int(minute))


def get_bounds(date):
    current_date = datetime.datetime.fromtimestamp(date)
    left = unix_time(current_date.day, current_date.month, current_date.year)
    right = left + 86400
    return (left, right)

