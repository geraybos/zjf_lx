import multiprocessing
import time
from Calf.data import KlineData
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
from Stock.Stock import Stock


def get(code, table='kline_tick'):
    print(code)
    start_date = dt.datetime(2018, 6, 12)
    end_date = dt.datetime(2018, 6, 12)
    data = KlineData.read_data(code=code, start_date=start_date,
                               end_date=end_date, kline=table,
                               timemerge=True)

    if len(data) <= 0:
        return {}
    data = data.sort_values(by=['_id'])
    data['pre_price'] = data.price.shift(-1)
    data['change'] = data.pre_price - data.price
    data['amount'] = data.price * data.volume
    data0=data[data.price==data.price.max()]
    max_price_amount=data0.amount.sum()

    data1 = data[data.price == data.price.min()]
    min_price_amount = data1.amount.sum()

    up = (data[data.change > 0])
    down = data[data.change < 0]
    ping = data[data.change == 0]
    up_volume = up['amount'].sum()
    down_volume = down['amount'].sum()
    ping_volume = ping['amount'].sum()
    up_max_amount = up['amount'].max()
    down_max_amount = down['amount'].max()
    return dict(code=code, date=start_date, up_amount=up_volume, down_amount=down_volume,
                ping_amount=ping_volume, up_max_amount=up_max_amount,
                down_max_amount=down_max_amount,max_price_amount=max_price_amount,min_price_amount=min_price_amount)

def fun(stocks):
    li = list()
    for sc in stocks:
        li.append(get(code=sc))
    return li


if __name__ == '__main__':
    a = time.clock()
    datas = Stock.get_stock_code_list()
    stocks = datas['stock_code'].tolist()
    stocks = stocks
    m = 20
    li = [stocks[i:i + m] for i in range(0, len(stocks), m)]
    pool = multiprocessing.Pool(processes=4)
    result = pool.map(fun, li)
    r = list()
    for res in result: r.extend(res)
    data = pd.DataFrame(data=r)
    data = data.dropna()
    data.to_csv('tick.csv')
    print('speed', time.clock() - a)
