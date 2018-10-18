import multiprocessing

from Calf.data import KlineData

from Calf.models.base_model import BaseModel

from Stock.Stock import Stock
import datetime as dt
import pandas as pd
import numpy as np


def cal_macd(data, interval=48, detal=48, short=12, long=26, mid=9):
    data = data.sort_values(by=['date'], ascending=True)
    data = data.reset_index(drop=True)
    data['sema'] = pd.Series(data['close']).ewm(span=short).mean()
    data['lema'] = pd.Series(data['close']).ewm(span=long).mean()
    data['dif'] = data['sema'] - data['lema']
    data['dea'] = pd.Series(data['dif']).ewm(span=mid).mean()
    data['macd'] = 2 * (data['dif'] - data['dea'])
    data["close2"] = data.close.shift(-interval)
    data["close3"] = data.close.shift(detal)
    data['profit'] = data.close2 / data.close - 1
    data['profit_self'] = data.close / data.close3 - 1
    return data


def get_result(sc, kline, start, end, table_name):
    data = KlineData.read_data(code=sc, start_date=start, end_date=end, kline=kline, timemerge=True)
    data = cal_macd(data)
    data = data.dropna()
    while len(data) >= 64:
        last_one = data.iloc[-1]
        if last_one.time != 1500:
            break
        elif abs(last_one.profit_self) >= 0.097:
            continue
        else:
            date = last_one.date
            data = data[data.date <= dt.datetime(date.year, date.month, date.day, 9, 55)]
            if len(data)>=64:
                profit = data.iloc[-1].profit
                date = data.iloc[-1].date
                idata = data.tail(64)
                idata = idata.loc[:, ['macd', 'dif', 'dea']]

                data = data[data.date < dt.datetime(date.year, date.month, date.day)]
                idata = np.array(idata)
                amin, amax = idata.min(), idata.max()  # 求最大最小值
                max = -amax if abs(amax) > abs(amin) else amin
                idata = idata * (64 / 2 - 1) / max
                idata = idata + 64 / 2
                BaseModel(table_name).insert_batch(
                    {'stock_code': sc, 'profit': profit, 'date': date,
                     'value': idata.tolist()})


def deal_data(data):
    kline = data['kline']
    stock = data['stocks']
    start = data['start']
    end = data['end']
    table_name = data['table_name']
    for sc in stock:
        print(sc)
        get_result(sc, kline, start, end, table_name)


if __name__ == '__main__':
    stocks = Stock.get_index_stock_code_list()
    kline = 'index_min5'
    table_name = 'A_MACD_H64_W3_index_min5'
    start = dt.datetime(2015, 12, 20)
    end = dt.datetime(2018, 9, 10)
    param = {'kline': kline, 'start': start, 'end': end, 'table_name': table_name, 'stocks': ['000001']}

    pool = multiprocessing.Pool(processes=4)
    m = 10
    li = [{'kline': kline, 'start': start, 'end': end, 'table_name': table_name, 'stocks': stocks[i:i + m]} for i in
          range(0, len(stocks), m)]
    result = pool.map(deal_data, li)

