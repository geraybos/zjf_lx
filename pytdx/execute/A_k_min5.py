import multiprocessing

from pytdx.hq import TdxHq_API
import datetime as dt
import tushare as ts
import pandas as pd

from db.db_connection import DBConnection

api = TdxHq_API()
api = TdxHq_API(multithread=True)
api = TdxHq_API(heartbeat=True)
con = api.connect('119.147.212.81', 7709)
def get_all_day_data(code, num, market):
    if con:
        data = []
        no = num // 800
        for i in range(no + 1):
            count = 800 if num >= 800 else num
            num -= count
            data += api.get_security_bars(0, market, code, (no - i) * 800, count)

        data = api.to_df(data)
        if len(data):
            data['time'] = data.hour * 100 + data.minute

            data['date'] = data.datetime.map(lambda x: x[0:10])
            data['datetime'] = pd.to_datetime(data.datetime)
            data['date'] = pd.to_datetime(data.date)
            data['stock_code'] = code
            data = data.drop(['year', 'month', 'day', 'hour', 'minute', 'datetime'], axis=1)
            # print(data.head())
            # obj.insert_many(data.to_dict(orient='records'))
    else:
        print('out of date')


def get_all_stock():
    df = ts.get_stock_basics()
    df['stock'] = df.index
    df = df.sort_values(by=['stock'], ascending=True)
    return df['stock'].tolist()


def exe(parms):
    print(parms['code'])
    get_all_day_data(parms['code'], parms['num'], parms['market'])


if __name__ == '__main__':
    start = dt.datetime(2016, 1, 1)
    end = dt.datetime(2018, 10, 16)
    obj = DBConnection()
    dbcon = obj.connect2()
    date_list = list(dbcon['calendar'].find({'date': {'$gte': start, '$lte': end}}, {'_id': 0, 'classtype': 0}))
    num = (date_list[0]['num'] - date_list[len(date_list) - 1]['num'] + 1) * 48
    print('start:', date_list[0]['date'], 'end:', date_list[len(date_list) - 1]['date'], 'num:', num)

    stocks = get_all_stock()
    parms = [{'code': stocks[i], 'num': num, 'market': 1 if str(stocks[i]).startswith('60') else 0} for i in
             range(0, len(stocks))]
    pool = multiprocessing.Pool(processes=2)
    result = pool.map(exe, parms)

    #=============================================================================遍历
    # for i in stocks:
    #
    #     print(i)
    #     market=1 if str(i).startswith('60') else 0
    #     get_all_day_data(code=i, num=num, obj=dbcon['kline_min5'],market=market,con=con)
    # =============================================================================遍历



    obj.connection.close()
    api.disconnect()
