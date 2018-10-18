import multiprocessing

from Calf.models.base_model import BaseModel

from Calf.data import KlineData, ModelData

from Stock.Stock import Stock
import datetime as dt
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt

from Visual.DMI.caculate import Caculate


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
        data = data.loc[:, ['PDI', 'MDI', 'ADX']]
        a = np.array(data)
        amin, amax = a.min(), a.max()  # 求最大最小值
        a = (a - amin) / (amax - amin) * (pixel - 3) + 2
        data = pd.DataFrame(a, columns=['PDI', 'MDI', 'ADX'])
        return data

        # 绘制美国线

    def draw_DMI(self, data, pixel, no, count, table_name, code, profits, date):
        if len(data)!=no:
            return
        for i in ['PDI', 'MDI', 'ADX']:
            data[i] += 0.5
        # data=data[::-1]
        PDI = data.PDI.astype('int').tolist()
        MDI = data.MDI.astype('int').tolist()
        ADX = data.ADX.astype('int').tolist()

        matrix = np.zeros((pixel, pixel), dtype=np.bool)
        num, mark = pixel , 0
        for i in range(no):
            # matrix[(num - ma5[i]), mark * count + 1: (mark + 1) * count - 1] = True
            # matrix[(num - ma10[i]), mark * count + 1: (mark + 1) * count - 1] = True
            # matrix[(num - ma20[i]), mark * count + 1: (mark + 1) * count - 1] = True
            # print(num- PDI[i])
            matrix[(num- PDI[i]), i] = True
            matrix[(num- MDI[i]), i] = True
            matrix[(num- ADX[i]), i] = True
        # print(date)
        # plt.matshow(matrix,cmap='hot')
        # plt.plot( range(len(data)),data['PDI'])
        # plt.plot( range(len(data)),data['MDI'])
        # plt.plot( range(len(data)),data['ADX'])
        # plt.show()
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
        obj = Line()
        for code in stocks:
            print(code)
            # 声明对象
            obj = Line() if obj == None else obj
            # 获取数据
            data = obj.get_data(stockno=code, start_date=dt.datetime(2016, 1, 1), end_date=dt.datetime(2018, 8, 31),
                                kline=kline)
            if obj.jug_data_length(data):
                # 获取计算收益的时间间隔
                detal, interval = obj.get_detal_by_kline('index_min5')
                # 计算ma
                data = Caculate.n_DMI(data=data, interval=interval, detal=detal)
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
                        try:
                            obj.draw_DMI(sub_data, pixel, no, count, table_name, code, profit, date)
                        except Exception as e:
                            print(e)
                    # break


if __name__ == '__main__':
    # 先决条件
    no = 64
    count = 1
    pixel = 64
    kline = 'index_min5'
    table_name = 'A_DMI_v1_' + kline
    obj = Line()
    stocks = obj.get_stock_code()
    # stocks=['399102']
    # BaseModel(table_name).remove({'stock_code':{'$in':stocks}})
    a = time.clock()
    pool = multiprocessing.Pool(processes=3)
    m = 10
    parms = [
        {'stocks': stocks[i:i + m], 'kline': kline, 'pixel': pixel, 'count': count, 'table_name': table_name, 'no': no}
        for i in range(0, len(stocks), m)]
    result = pool.map(obj.exe, parms)
    print(time.clock() - a)
