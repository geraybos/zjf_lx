import multiprocessing

from Calf.data import KlineData

from Calf.models.base_model import BaseModel

from Stock.Stock import Stock
import datetime as dt
import pandas as pd
import numpy as np


def n_DMI( data, interval=48, detal=48, N1=14, M1=6):
    data["close2"] = data.close.shift(-interval)
    data["close3"] = data.close.shift(detal)
    data['profit'] = data.close2 / data.close - 1
    data['profit_self'] = data.close / data.close3 - 1

    data['last_close'] = data.close.shift(1)
    data['last_high'] = data.high.shift(1)
    data['last_low'] = data.low.shift(1)

    data['MTR_D1'] = data['high'] - data['low']
    data['MTR_D2'] = abs(data['high'] - data.last_close)
    data['MTR_D3'] = abs(data.last_close - data['low'])
    data['MTR_1'] = data['MTR_D2']
    data.loc[data['MTR_D1'] > data['MTR_D2'], 'MTR_1'] = data['MTR_D1']
    # data['MTR_1'] = data.apply(lambda x: x['MTR_D1'] if x['MTR_D1'] > x['MTR_D2']  else x['MTR_D2'], axis=1)

    # 要删除的第一个属性
    data['MTR_2'] = data['MTR_D3']
    data.loc[data['MTR_1'] > data['MTR_D3'], 'MTR_2'] = data['MTR_1']
    # data['MTR_2'] = data.apply(lambda x: x['MTR_1'] if x['MTR_1'] > x['MTR_D3']  else x['MTR_D3'], axis=1)

    # roolling 必须依赖于 transform 才行，只能是先生成一列，然后在抛弃
    # roolling 操作要先进行反转才能。因为rolling操作会空前N行
    # data = data[::-1]

    data['MTR'] = data['MTR_2'].rolling(window=N1).sum()

    data['HD'] = data['high'] - data.last_high
    data['LD'] = data.last_low - data['low']

    # HD1 = np.where(HD <= 0, 0, HD)
    # data['DMP1'] = np.where(HD1 <= LD, 0, HD1)
    data['DMP1'] = 0
    data.loc[(data['HD'] > 0) & (data['HD'] > data['LD']), 'DMP1'] = data['HD']

    data['DMP'] = data['DMP1'].rolling(window=N1).sum()

    # LD1 = np.where(LD <= 0, 0, LD)
    # data['DMM1'] = np.where(LD1 <= HD, 0, LD1)
    data['DMM1'] = 0
    data.loc[(data['LD'] > 0) & (data['LD'] > data['HD']), 'DMM1'] = data['LD']

    data['DMM'] = data['DMM1'].rolling(window=N1).sum()

    data['PDI'] = data['DMP'] * 100 / data['MTR']
    data['MDI'] = data['DMM'] * 100 / data['MTR']

    # 要删除的第4个属性
    data['ADX1'] = abs(data['MDI'] - data['PDI']) / (data['MDI'] + data['PDI']) * 100

    data['ADX'] = data['ADX1'].rolling(window=M1).mean()
    data.dropna(inplace=True)
    return data


def get_result(sc, kline, start, end, table_name):
    data = KlineData.read_data(code=sc, start_date=start, end_date=end, kline=kline, timemerge=True)
    data = n_DMI(data)
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
                data = data[data.date < dt.datetime(date.year, date.month, date.day)]
                idata = idata.loc[:, ['PDI', 'MDI', 'ADX']]
                idata = np.array(idata)
                amin, amax = idata.min(), idata.max()  # 求最大最小值
                idata = (idata - amin) / (amax - amin)
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
    table_name = 'A_DMI_H64_W3_index_min5'
    start = dt.datetime(2015, 12, 20)
    end = dt.datetime(2018, 9, 10)
    param = {'kline': kline, 'start': start, 'end': end, 'table_name': table_name, 'stocks': ['000001']}
    pool = multiprocessing.Pool(processes=4)
    m = 10
    li = [{'kline': kline, 'start': start, 'end': end, 'table_name': table_name, 'stocks': stocks[i:i + m]} for i in
          range(0, len(stocks), m)]
    result = pool.map(deal_data, li)

