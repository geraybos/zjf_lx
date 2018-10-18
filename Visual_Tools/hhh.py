import multiprocessing

from Calf.models.base_model import BaseModel
import datetime as dt

from Stock.Stock import Stock


def fun(data):
    for i in data:
        BaseModel('kline_min5').remove(date=i['date'])
        print(i['date'], 'over')


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=3)
    datelist = list(
        BaseModel('calendar').query(sql={'date': {'$gte': dt.datetime(2016, 1, 1), '$lte': dt.datetime(2018, 9, 18)}}))
    print(datelist)
    m = 10
    parms = [datelist[i:i + m] for i in range(0, len(datelist), m)]
    result = pool.map(fun, parms)
