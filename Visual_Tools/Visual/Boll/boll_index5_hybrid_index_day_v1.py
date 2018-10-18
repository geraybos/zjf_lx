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
    def cal_boll(self, data, interval, detal,p1=20,p2=2,mid=26):
        data['mid'] = data['close'].rolling(mid).mean()  # 按照ma26的计算方式  这就是中轨线
        data['tmp2'] = data['close'].rolling(p1).std()
        data['top'] = data['mid'] + p2 * data['tmp2']  # 上轨线
        data['bottom'] = data['mid'] - p2 * data['tmp2']  # 下轨线数据
        data["close2"] = data.close.shift(-interval)
        data["close3"] = data.close.shift(detal)
        data['profit'] = data.close2 / data.close - 1
        data['profit_self'] = data.close / data.close3 - 1
        return data

    def cal_just_ma(self,data):
        data['ma5'] = data.close.rolling(5).mean()
        data['ma10'] = data.close.rolling(10).mean()
        data['ma20'] = data.close.rolling(20).mean()
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
        a = (a - amin) / (amax - amin) * (pixel - 3) + 2
        data = pd.DataFrame(a, columns=['close', 'open', 'high', 'low', 'ma5', 'ma10', 'ma20'])
        return data

        # 绘制美国线

    def draw_America_Line(self, data,data_day, pixel, no, count, table_name, code, profits,date):
        for i in data.columns.values:
            data[i] += 0.5
        for i in data_day.columns.values:
            data_day[i] += 0.5
        high = data.high.astype('int').tolist()
        low = data.low.astype('int').tolist()
        close = data.close.astype('int').tolist()
        open = data.open.astype('int').tolist()
        high2 = data_day.high.astype('int').tolist()
        low2 = data_day.low.astype('int').tolist()
        close2 = data_day.close.astype('int').tolist()
        open2 = data_day.open.astype('int').tolist()
        matrix = np.zeros((pixel, pixel), dtype=np.bool)
        num, mark = pixel//2, 0
        for i in range(no):
            # matrix[(num - ma5[i]), mark * count + 1: (mark + 1) * count - 1] = True
            # matrix[(num - ma10[i]), mark * count + 1: (mark + 1) * count - 1] = True
            # matrix[(num - ma20[i]), mark * count + 1: (mark + 1) * count - 1] = True
            position = ((mark * count + count // 3) + ((mark + 1) * count - count // 3)) // 2
            matrix[(num - open[i]), position - 2:position] = True  # 横开
            matrix[(num - close[i]), position:position + 3] = True  # 横开
            matrix[(num - high[i]):(num - low[i]) + 1, position] = True

            matrix[(2*num - open2[i]), position - 2:position] = True  # 横开
            matrix[(2*num - close2[i]),position:position + 3] = True  # 横开
            matrix[(2*num - high2[i]):(2*num - low2[i]) + 1, position] = True
            mark += 1

        # plt.matshow(matrix,cmap='hot')
        # plt.show()
        BaseModel(table_name).insert_batch(
            {'stock_code': code, 'profit': profits, 'date': date,
             'value': matrix.tolist()})

    def jug_data_length(self,data):
        return len(data)>200

    def exe(self,parm):
        kline=parm['kline']
        no=parm['no']
        pixel=parm['pixel']
        count=parm['count']
        table_name=parm['table_name']
        stocks=parm['stocks']
        obj = Line()
        for code in stocks:
            print(code)
            # 声明对象
            obj=Line() if obj==None else obj
            # 获取数据
            data = obj.get_data(stockno=code, start_date=dt.datetime(2016, 1, 1), end_date=dt.datetime(2018, 8, 31),
                                kline=kline)
            data_day = obj.get_data(stockno=code, start_date=dt.datetime(2016, 1, 1), end_date=dt.datetime(2018, 8, 31),
                                kline=str(kline).replace('min5','day'))
            if obj.jug_data_length(data) and obj.jug_data_length(data_day):
                # 获取计算收益的时间间隔
                detal, interval = obj.get_detal_by_kline('index_min5')
                # 计算ma
                data = obj.cal_ma(data, interval, detal)
                data_day = obj.cal_just_ma(data_day)
                # 清除计算ma产生的空数据
                data_day = data_day.dropna()
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
                    data_day = data_day[data_day.date < pre_date]
                    sub_data_day = data_day.tail(no)

                    if obj.jug_condition(date) and len(sub_data_day)==no:
                        sub_data = obj.normalization(sub_data, pixel//2)
                        sub_data_day = obj.normalization(sub_data_day, pixel//2)
                        # data, pixel, no, count, table_name, code, profits
                        obj.draw_America_Line(sub_data,sub_data_day, pixel, no, count, table_name, code, profit,date)
                        # break



if __name__ == '__main__':
    # 先决条件
    no = 12
    count = 5
    pixel = 64
    kline = 'index_min5'
    table_name='A_America_line_hybrid_v2_'+kline
    obj=Line()
    stocks=obj.get_stock_code()
    # stocks=['000001']
    a = time.clock()
    pool = multiprocessing.Pool(processes=3)
    m = 10
    parms = [{'stocks':stocks[i:i + m],'kline':kline,'pixel':pixel,'count':count,'table_name':table_name,'no':no} for i in range(0, len(stocks), m)]
    result = pool.map(obj.exe, parms)
    print(time.clock()- a)


