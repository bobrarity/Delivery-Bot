import datetime


def order_number(num):
    last_cleared_time = datetime.datetime.now()
    current_time = datetime.datetime.now()
    if (current_time - last_cleared_time).total_seconds() >= 24 * 60 * 60:
        num = 1
        last_cleared_time = current_time
        return num
