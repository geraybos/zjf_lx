import multiprocessing

from Calf.models.base_model import BaseModel

from Calf.data import KlineData, ModelData

from Stock.Stock import Stock
import datetime as dt
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt


class Line:
    # 确定哪些股票
    def get_stock_code(self):
        stocks = Stock.get_index_stock_code_list()
        return stocks

    # 确定需要哪些数据
    def get_data(self, stockno, start_date, end_date, kline):
        data = KlineData.read_data(code=stockno, start_date=start_date, end_date=end_date,
                                   kline=kline, timemerge=True)

        data = data[::-1]
        return data

    # 根据kline确定间隔长度，用于计算收益等
    def get_detal_by_kline(self, kline):
        data = {'index_min5': {'detal': 48, 'interval': 48}}
        return data[kline]['detal'], data[kline]['interval']

    # 计算ma
    def cal_ma(self, data, interval, detal):
        data['ma5'] = data.close.rolling(5).mean()
        data['ma10'] = data.close.rolling(10).mean()
        data['ma20'] = data.close.rolling(20).mean()
        data["close2"] = data.close.shift(-interval)
        data["close3"] = data.close.shift(detal)
        data['profit'] = data.close2 / data.close - 1
        data['profit_self'] = data.close / data.close3 - 1
        return data

    # 获取到最后一条数据
    def get_last_one(self, data):
        return data.tail(1)

    # 推进数据
    def hangdler_data(self, last_one, data):
        date = last_one.iloc[0].date
        date = dt.datetime(date.year, date.month, date.day, 9, 55)
        data = data[data.date <= date]
        return data

    # 判定条件
    def jug_condition(self, date):
        flag = False
        if date.hour == 9 and date.minute == 55:
            return True
        return flag

    # 归一化数据
    def normalization(self, data, pixel):
        data = data.loc[:, ['close', 'open', 'high', 'low', 'ma5', 'ma10', 'ma20']]
        a = np.array(data)
        amin, amax = a.min(), a.max()  # 求最大最小值
        a = (a - amin) / (amax - amin) * (pixel - 3)
        data = pd.DataFrame(a, columns=['close', 'open', 'high', 'low', 'ma5', 'ma10', 'ma20'])
        return data

        # 绘制美国线

    def draw(self, data, pixel, no, count, table_name, code, profits, date,h,w):
        if len(data)!=no:
            return
        for i in data.columns.values:
            data[i] += 0.5
        high = data.high.astype('int').tolist()
        low = data.low.astype('int').tolist()
        close = data.close.astype('int').tolist()
        open = data.open.astype('int').tolist()
        matrix = np.zeros((w, h), dtype=np.bool)
        num, mark = w-1 , 0

        for i in range(no):
            # matrix[(num - ma5[i]), mark * count + 1: (mark + 1) * count - 1] = True
            # matrix[(num - ma10[i]), mark * count + 1: (mark + 1) * count - 1] = True
            # matrix[(num - ma20[i]), mark * count + 1: (mark + 1) * count - 1] = True
            # position = ((mark * count + count // 3) + ((mark + 1) * count - count // 3)) // 2
            # matrix[(num - open[i]), position - 1] = True  # 横开
            # matrix[(num - close[i]), position + 1] = True  # 横开
            # matrix[(num - high[i]):(num - low[i]) + 1, position] = True

            if open[i] >= close[i]:
                matrix[(num - open[i]):(num - close[i]) + 1, mark * count + 1: (mark + 1) * count - 1] = True
                matrix[(num - high[i]):(num - low[i]) + 1,mark * count + count // 3 + 1: (mark + 1) * count - count // 3 - 1] = True
            else:
                matrix[(num - close[i]), mark * count + 1: (mark + 1) * count - 1] = True
                matrix[(num - open[i]), mark * count + 1: (mark + 1) * count - 1] = True
                matrix[(num - open[i]):(num - low[i]) + 1,mark * count + count // 3 + 1: (mark + 1) * count - count // 3 - 1] = True
                matrix[(num - high[i]):(num - close[i]) + 1,mark * count + count // 3 + 1: (mark + 1) * count - count // 3 - 1] = True

                matrix[(num - close[i]):(num - open[i]) +1, mark * count + count // 3  ] = True
                matrix[(num - close[i]):(num - open[i]) + 1, (mark + 1) * count - count // 3 - 1] = True
            mark += 1
        BaseModel(table_name).insert_batch(
            {'stock_code': code, 'profit': profits, 'date': date,
             'value': matrix.tolist()})

    def jug_data_length(self, data):
        return len(data) > 200

    def exe(self, parm):
        kline = parm['kline']
        no = parm['no']
        pixel = parm['pixel']
        count = parm['count']
        table_name = parm['table_name']
        stocks = parm['stocks']
        h = parm['h']
        w = parm['w']
        obj = Line()
        for code in stocks:
            print(code)
            # 声明对象
            obj = Line() if obj == None else obj
            # 获取数据
            data = obj.get_data(stockno=code, start_date=dt.datetime(2016, 1, 1), end_date=dt.datetime(2018, 9, 10),
                                kline=kline)
            if obj.jug_data_length(data):
                # 获取计算收益的时间间隔
                detal, interval = obj.get_detal_by_kline('index_min5')
                # 计算ma
                data = obj.cal_ma(data, interval, detal)
                # 清除计算ma产生的空数据
                data = data.dropna()
                # 获取到最后一天数据
                last_one = obj.get_last_one(data)
                # 得到最后一天日期，只保留9:55以前的数据
                data = obj.hangdler_data(last_one, data)
                # 迭代绘图
                while len(data) > interval:
                    sub_data = data.tail(no)
                    date = data.iloc[-1].date
                    profit = data.iloc[-1].profit
                    pre_date = data.iloc[-interval].date
                    data = data[data.date <= dt.datetime(pre_date.year, pre_date.month, pre_date.day, 9, 55)]
                    if obj.jug_condition(date):
                        sub_data = obj.normalization(sub_data, pixel)
                        # data, pixel, no, count, table_name, code, profits
                        obj.draw(sub_data, pixel, no, count, table_name, code, profit, date,h,w)


if __name__ == '__main__':
    # 先决条件
    h = 512
    w = 64
    count = 5
    no = h // count-1
    pixel = w
    kline = 'index_min5'
    table_name = 'A_MA_H512_W64_' + kline
    print(table_name)
    obj = Line()
    stocks = obj.get_stock_code()
    a = time.clock()
    # pool = multiprocessing.Pool(processes=2)
    m = 10
    parms = [{'stocks': stocks[i:i + m], 'kline': kline, 'h': h, 'w': w, 'pixel': pixel, 'count': count,
              'table_name': table_name, 'no': no} for i in range(0, len(stocks), m)]
    # result = pool.map(obj.exe, parms)
    for i in parms:
        obj.exe(i)
    print(time.clock() - a)
