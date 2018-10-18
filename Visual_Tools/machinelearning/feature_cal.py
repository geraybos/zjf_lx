# t = time.clock()
import multiprocessing

from Calf.models import Calendar
from Calf.models.base_model import BaseModel

from Calf.data import KlineData
from Stock.Stock import Stock

from novel_features import n_KDJ, n_MA, n_MACD, n_RSI, n_DMI, n_BRAR, n_CR, n_VR, n_WR, n_CCI, n_BOLL, n_PSY
import datetime as dt
import pandas as pd
import numpy as np


def normal(employment):
    mean = employment.mean()  # 计算平均数
    deviation = employment.std()  # 计算标准差
    # 标准化数据的公式: (数据值 - 平均数) / 标准差
    standardized_employment = (employment - mean) / deviation
    return standardized_employment


if __name__ == '__main__':

    data = KlineData.read_data(code='880302', start_date=dt.datetime(2018, 9, 10), end_date=dt.datetime(2018, 9, 18),
                               kline='index_min5', timemerge=True)
    name = data.columns.values.tolist()
    if len(data):
        data = data.drop(['_id', 'classtype', 'market'], axis=1)
        data = n_KDJ(data, 9, 3)
        # t1 = time.clock()
        # print(t1-t)
        # t = time.clock()

        data = n_MA(data)
        # t1 = time.clock()
        # print(t1 - t1)
        # t = time.clock()

        data = n_MACD(data, 12, 26, 9)
        # t1 = time.clock()
        # print(t1 - t)
        # t = time.clock()
        data = n_RSI(data, 6, 12, 24)
        # t1 = time.clock()
        # print(t1 - t)
        # t = time.clock()
        data = n_DMI(data, 14, 6)
        # t1 = time.clock()
        # print(t1 - t)
        # t = time.clock()
        data = n_BRAR(data, 26)
        # t1 = time.clock()
        # print(t1 - t)
        # t = time.clock()
        data = n_CR(data, 26, 10, 20, 40)
        # t1 = time.clock()
        # print(t1 - t)
        # t = time.clock()
        data = n_VR(data, 26)
        # t1 = time.clock()
        # print(t1 - t)
        # t = time.clock()
        data = n_WR(data, 10, 6)
        # t1 = time.clock()
        # print(t1 - t)
        # t = time.clock()
        data = n_CCI(data, 14)
        # t1 = time.clock()
        # print(t1 - t)
        # t = time.clock()
        data = n_BOLL(data, 20)
        # t1 = time.clock()
        # print(t1 - t)
        # t = time.clock()
        data = n_PSY(data, 12)

        columns = data.columns.values.tolist()
        data = data.replace(to_replace=np.Infinity, value=np.NaN)
        for i in columns:
            if i not in name:
                v = data[i].iloc[0]
                if type(v).__name__ != 'bool_':
                    # print(i, v, type(v))
                    if data[i].min()==0:
                        # pass
                        # print(i, data[i].loc[0])
                        data.loc[data[i] != 0, i] = (data.loc[data[i] != 0, i] - data.loc[data[i] != 0, i].min()) / (
                        data.loc[data[i] != 0, i].max() - data.loc[data[i] != 0, i].min())
                        # print(i,data[i].loc[0])
                    else:
                        # print(i, v, type(v))
                        data[i] = (data[i] - data[i].min()) / (data[i].max() - data[i].min())


        data['up'] = data['up'] / (data['up'] + data['down'])
        data['down'] = data['down'] / (data['up'] + data['down'])
        name = ['open', 'close', 'high', 'low', 'amount', 'volume']

        for i in name:
            data[ i] = (data[i] - data[i].min()) / (data[i].max() - data[i].min())

        data = data[::-1]
        data = data.reset_index(drop=True)
        data['count'] = data.index.tolist()
        data.to_csv('C:\\Users\Administrator\Desktop\\memeda2.csv')
