import datetime

def parseDate(train_date):
    """
    :param train_date: '2019-02-27'
    :return:
    """
    # Wed Feb 27 2019 00:00:00 GMT+0800 (中国标准时间)
    week_name = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    month_name = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    y, m, d = map(int,train_date.split("-"))
    weekday = datetime.datetime(y, m, d).weekday()
    return "{0} {1} {2} {3} 00:00:00 GMT+0800 (中国标准时间)".format(week_name[weekday], month_name[m - 1], d, y)

if __name__ == '__main__':
    print(parseDate("2019-02-27"))