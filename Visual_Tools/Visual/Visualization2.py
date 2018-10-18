# encoding=utf-8

# from matplotlib.finance import candlestick2_ohlc
# from pylab import *  # 支持中文
import pandas as pd

from Calf import BaseModel

import numpy as np
import matplotlib.pyplot as plt

class visualization:
    @classmethod
    def draw_volume(cls, data, profits, date, code, pixel, table_name, n, count):
        if len(data) != pixel:
            return

        data['volume'] += 0.5

        volume = data['volume'].astype('int').tolist()

        # pixel=
        matrix = np.zeros((pixel + n * count, pixel + n * count), dtype=np.bool)

        # val = int((pixel + n * count) / 2 - 1)
        num = pixel + n * count
        num2=num//2
        mark = 0
        for i in range(pixel + n):
            if i < len(volume):
                if (num-volume[i])<num2:
                    matrix[(num-volume[i]):num2+1, i] = True
                else:
                    matrix[num2:(num - volume[i])+1, i] = True



            else:
                if (num - volume[i-n]) < num2:
                    matrix[ (num-volume[i-n]):num2+1, (pixel) + mark * count:(pixel) + (mark + 1) * count] = True
                else:
                    matrix[num2:(num - volume[i - n])+1, (pixel) + mark * count:(pixel) + (mark + 1) * count] = True



                mark += 1
        obj = BaseModel(table_name)
        # obj.remove(dict(date=date,stock_code=code))
        obj.insert_batch(
            {'stock_code': code, 'profit': profits, 'date': date,
             'value': matrix.tolist()})

    @classmethod
    def drow_boll_line(cls, data, profits, date, code, pixel, table_name):
        # 'mid', 'top', 'bottom'
        if len(data) != pixel:
            return
        data['mid'] += 0.5
        data['top'] += 0.5
        data['bottom'] += 0.5
        data['low'] += 0.5
        data['high'] += 0.5

        mid = data['mid'].astype('int').tolist()
        top = data['top'].astype('int').tolist()
        bottom = data['bottom'].astype('int').tolist()
        low = data['low'].astype('int').tolist()
        high = data['high'].astype('int').tolist()
        matrix = np.zeros((pixel, pixel), dtype=np.bool)
        num = pixel - 1
        for i in range(len(mid)):
            matrix[(num - mid[i]), i] = True
            matrix[(num - top[i]), i] = True
            matrix[(num - bottom[i]), i] = True
            matrix[(num - high[i]):(num - low[i]), i] = True

        BaseModel(table_name).insert_batch(
            {'stock_code': code, 'profit': profits, 'date': date, 'value': matrix.tolist()})

    @classmethod
    def draw_ma_line(cls, data, profits, date, pixel, code, table_name):

        if len(data) != pixel:
            return

        data['ma5'] += 0.5
        data['ma10'] += 0.5
        data['ma20'] += 0.5
        data['ma60'] += 0.5
        data['ma120'] += 0.5
        data['high'] += 0.5
        data['low'] += 0.5
        ma5 = data['ma5'].astype('int').tolist()
        ma20 = data['ma20'].astype('int').tolist()
        ma10 = data['ma10'].astype('int').tolist()
        ma60 = data['ma60'].astype('int').tolist()
        ma120 = data['ma120'].astype('int').tolist()

        high = data.high.astype('int').tolist()
        low = data.low.astype('int').tolist()

        matrix = np.zeros((pixel, pixel), dtype=np.bool)
        num = pixel - 1
        for i in range(len(ma5)):
            matrix[(num - ma5[i]), i] = True
            matrix[(num - ma10[i]), i] = True
            matrix[(num - ma20[i]), i] = True
            matrix[(num - ma60[i]), i] = True
            matrix[(num - ma120[i]), i] = True
            matrix[(num - high[i]):(num - low[i]), i] = True

        # BaseModel(table_name).insert_batch(
        #     {'stock_code': code, 'profit': profits, 'date': date, 'value': matrix.tolist()})
        BaseModel(table_name).remove(date=date, stock_code=code)
        BaseModel(table_name).insert_batch(
            {'stock_code': code, 'profit': profits, 'date': date, 'value': matrix.tolist()})

    @classmethod
    def draw_ma_line3(cls, data, profits, date, code, pixel, table_name, n, count,profit_relative):
        # 'dif', 'dea', 'macd'




        if len(data) != pixel:
            return

        data['ma5'] += 0.5
        data['ma10'] += 0.5
        data['ma20'] += 0.5
        data['ma60'] += 0.5
        data['ma120'] += 0.5
        data['ma200'] += 0.5
        data['high'] += 0.5
        data['low'] += 0.5
        ma5 = data['ma5'].astype('int').tolist()
        ma20 = data['ma20'].astype('int').tolist()
        ma10 = data['ma10'].astype('int').tolist()
        ma60 = data['ma60'].astype('int').tolist()
        ma200 = data['ma120'].astype('int').tolist()
        ma120 = data['ma200'].astype('int').tolist()

        high = data.high.astype('int').tolist()
        low = data.low.astype('int').tolist()

        # pixel=
        matrix = np.zeros((pixel + n * count, pixel + n * count), dtype=np.bool)

        # val = int((pixel + n * count) / 2 - 1)
        num = pixel + n * count
        mark = 0
        for i in range(pixel + n):
            if i < len(ma5):
                matrix[(num - ma5[i]), i] = True
                matrix[(num - ma10[i]), i] = True
                matrix[(num - ma20[i]), i] = True
                matrix[(num - ma60[i]), i] = True
                # print((num - ma120[i]))
                matrix[(num - ma120[i]), i] = True
                matrix[(num - ma200[i]), i] = True
                matrix[(num - high[i]):(num - low[i]), i] = True

            else:

                matrix[(num - ma5[i - n]), (pixel) + mark * count:(pixel) + (mark + 1) * count] = True
                matrix[(num - ma10[i - n]), (pixel) + mark * count:(pixel) + (mark + 1) * count] = True
                matrix[(num - ma20[i - n]), (pixel) + mark * count:(pixel) + (mark + 1) * count] = True
                matrix[(num - ma60[i - n]), (pixel) + mark * count:(pixel) + (mark + 1) * count] = True
                matrix[(num - ma120[i - n]), (pixel) + mark * count:(pixel) + (mark + 1) * count] = True
                matrix[(num - ma200[i - n]), (pixel) + mark * count:(pixel) + (mark + 1) * count] = True
                matrix[(num - high[i - n]):num - low[i - n], (pixel) + mark * count:(pixel) + (mark + 1) * count] = True

                mark += 1
        # plt.matshow(matrix, cmap='hot')
        # plt.show()
        obj=BaseModel(table_name)
        obj.remove(dict(date=date,stock_code=code))
        obj.insert_batch(
            {'stock_code': code, 'profit': profits, 'profit_relative': profit_relative, 'date': date,
             'value': matrix.tolist()})

    @classmethod
    def draw_ma_stub_line(cls, data, profits,date, code, table_name, pixel, length, profit_relative,count):
        if len(data) != length:
            return

        data['ma5'] += 0.5
        data['ma10'] += 0.5
        data['ma20'] += 0.5
        data['ma60'] += 0.5
        data['ma120'] += 0.5
        # data['ma200'] += 0.5
        data['high'] += 0.5
        data['low'] += 0.5
        ma5 = data['ma5'].astype('int').tolist()
        ma20 = data['ma20'].astype('int').tolist()
        ma10 = data['ma10'].astype('int').tolist()
        ma60 = data['ma60'].astype('int').tolist()
        ma120 = data['ma120'].astype('int').tolist()
        # ma200 = data['ma200'].astype('int').tolist()

        high = data.high.astype('int').tolist()
        low = data.low.astype('int').tolist()
        close = data.close.astype('int').tolist()
        open= data.open.astype('int').tolist()

        # pixel=
        matrix = np.zeros((pixel, pixel), dtype=np.bool)

        # val = int((pixel + n * count) / 2 - 1)
        num = pixel
        mark = 0
        for i in range(length):
                matrix[(num - ma5[i ]),  mark * count: (mark + 1) * count] = True
                matrix[(num - ma10[i ]),  mark * count:(mark + 1) * count] = True
                matrix[(num - ma20[i ]),  mark * count: (mark + 1) * count] = True
                matrix[(num - ma60[i ]),  mark * count: (mark + 1) * count] = True
                matrix[(num - ma120[i ]),  mark * count: (mark + 1) * count] = True
                # matrix[(num - ma200[i ]),  mark * count: (mark + 1) * count] = True


                # matrix[(num - high[i ]):(num - low[i])+1,  mark * count+count//3+1: (mark + 1) * count-count//3-1] = True

                if open[i]>=close[i]:
                    matrix[(num - open[i]):(num - close[i])+1, mark * count+1: (mark + 1) * count-1] = True
                    matrix[(num - high[i]):(num - low[i]) + 1,mark * count + count // 3 + 1: (mark + 1) * count - count // 3 - 1] = True
                else:
                    matrix[(num - close[i]),  mark * count+1: (mark + 1) * count-1] = True
                    matrix[(num - open[i]),  mark * count+1: (mark + 1) * count-1] = True
                    matrix[(num - open[i]):(num - low[i]) + 1,mark * count + count // 3 + 1: (mark + 1) * count - count // 3 - 1] = True
                    matrix[(num - high[i]):(num - close[i]) + 1,mark * count + count // 3 + 1: (mark + 1) * count - count // 3 - 1] = True

                    matrix[(num - close[i]):(num - open[i])+1, mark * count+1] = True
                    matrix[(num - close[i]):(num - open[i])+1, (mark + 1) * count-1] = True
                mark += 1

        # plt.matshow(matrix, cmap='hot')
        # plt.show()
        BaseModel(table_name).insert_batch(
            {'stock_code': code, 'profit': profits, 'profit_relative': profit_relative, 'date': date,
             'value': matrix.tolist()})

    @classmethod
    def draw_ma_stub_line2(cls, data, profits, date, code, table_name, pixel, length, profit_relative, count):
        if len(data) != length:
            return
        data['high'] += 0.5
        data['low'] += 0.5
        data['open'] += 0.5
        data['close'] += 0.5
        high = data.high.astype('int').tolist()
        low = data.low.astype('int').tolist()
        close = data.close.astype('int').tolist()
        open = data.open.astype('int').tolist()
        matrix = np.zeros((pixel, pixel), dtype=np.bool)
        # val = int((pixel + n * count) / 2 - 1)
        num = pixel
        mark = 0
        for i in range(length):
            # matrix[(num - high[i ]):(num - low[i])+1,  mark * count+count//3+1: (mark + 1) * count-count//3-1] = True
            if open[i] >= close[i]:
                matrix[(num - open[i]):(num - close[i])+1 , mark * count : (mark + 1) * count ] = True
                matrix[(num - high[i]):(num - low[i])+ 1,mark * count + count // 3 : (mark + 1) * count - count // 3 ] = True
            else:
                matrix[(num - close[i]), mark * count : (mark + 1) * count ] = True#横收
                matrix[(num - open[i]), mark * count : (mark + 1) * count ] = True#横开
                matrix[(num - open[i]):(num - low[i]) + 1,mark * count + count // 3 : (mark + 1) * count - count // 3 ] = True
                matrix[(num - high[i]):(num - close[i]) + 1,mark * count + count // 3 : (mark + 1) * count - count // 3 ] = True
                matrix[(num - close[i]):(num - open[i]) + 1, mark * count ] = True
                matrix[(num - close[i]):(num - open[i]) + 1, (mark + 1) * count - 1] = True
            mark += 1
        BaseModel(table_name).insert_batch(
            {'stock_code': code, 'profit': profits, 'profit_relative': profit_relative, 'date': date,'value': matrix.tolist()})

    @classmethod
    def draw_ma_stub_line3(cls, data,data_day, profits, date, code, table_name, pixel, length, profit_relative, count):
        if len(data) != length and len(data_day) != length:
            return
        data['high'] += 0.5
        data['low'] += 0.5
        data['open'] += 0.5
        data['close'] += 0.5
        data['ma5'] += 0.5
        data['ma10'] += 0.5
        data['ma20'] += 0.5
        high = data.high.astype('int').tolist()
        low = data.low.astype('int').tolist()
        close = data.close.astype('int').tolist()
        open = data.open.astype('int').tolist()
        ma5=data.ma5.astype('int').tolist()
        ma10=data.ma10.astype('int').tolist()
        ma20=data.ma20.astype('int').tolist()

        data_day['high'] += 0.5
        data_day['low'] += 0.5
        data_day['open'] += 0.5
        data_day['close'] += 0.5
        data_day['ma5'] += 0.5
        data_day['ma10'] += 0.5
        data_day['ma20'] += 0.5
        high2 = data_day.high.astype('int').tolist()
        low2 = data_day.low.astype('int').tolist()
        close2 = data_day.close.astype('int').tolist()
        open2 = data_day.open.astype('int').tolist()
        ma52 = data_day.ma5.astype('int').tolist()
        ma102 = data_day.ma10.astype('int').tolist()
        ma202 = data_day.ma20.astype('int').tolist()

        matrix = np.zeros((pixel, pixel), dtype=np.bool)
        num2 = pixel//2-1
        num=pixel-1
        mark = 0
        for i in range(length):
            matrix[(num2 - ma5[i]), mark * count + 1: (mark + 1) * count - 1] = True
            matrix[(num2 - ma10[i]), mark * count + 1: (mark + 1) * count - 1] = True
            matrix[(num2 - ma20[i]), mark * count + 1: (mark + 1) * count - 1] = True

            matrix[(num - ma52[i]), mark * count + 1: (mark + 1) * count - 1] = True
            matrix[(num - ma102[i]), mark * count + 1: (mark + 1) * count - 1] = True
            matrix[(num - ma202[i]), mark * count + 1: (mark + 1) * count - 1] = True

            if open[i] >= close[i]:
                matrix[(num2 - open[i]):(num2 - close[i]) + 1, mark * count + 1: (mark + 1) * count - 1] = True
                matrix[(num2 - high[i]):(num2 - low[i]) + 1,mark * count + count // 3 + 1: (mark + 1) * count - count // 3 - 1] = True

            else:
                matrix[(num2 - close[i]), mark * count + 1: (mark + 1) * count - 1] = True  # 横收
                matrix[(num2- open[i]), mark * count + 1: (mark + 1) * count - 1] = True  # 横开
                matrix[(num2 - open[i]):(num2 - low[i]) + 1,mark * count + count // 3 + 1: (mark + 1) * count - count // 3 - 1] = True
                matrix[(num2 - high[i]):(num2 - close[i]) + 1,mark * count + count // 3 + 1: (mark + 1) * count - count // 3 - 1] = True
                matrix[(num2 - close[i]):(num2 - open[i]) + 1, mark * count + 1] = True
                matrix[(num2 - close[i]):(num2 - open[i]) + 1, (mark + 1) * count - 2] = True
            if open2[i]>=close2[i]:
                matrix[(num - open2[i]):(num - close2[i]) + 1, mark * count + 1: (mark + 1) * count - 1] = True
                matrix[(num - high2[i]):(num - low2[i]) + 1,
                mark * count + count // 3 + 1: (mark + 1) * count - count // 3 - 1] = True
            else:
                matrix[(num - close2[i]), mark * count + 1: (mark + 1) * count - 1] = True  # 横收
                matrix[(num - open2[i]), mark * count + 1: (mark + 1) * count - 1] = True  # 横开
                matrix[(num - open2[i]):(num - low2[i]) + 1,mark * count + count // 3 + 1: (mark + 1) * count - count // 3 - 1] = True
                matrix[(num - high2[i]):(num - close2[i]) + 1,mark * count + count // 3 + 1: (mark + 1) * count - count // 3 - 1] = True
                matrix[(num - close2[i]):(num - open2[i]) + 1, mark * count + 1] = True
                matrix[(num - close2[i]):(num - open2[i]) + 1, (mark + 1) * count - 2] = True
            mark += 1

        BaseModel(table_name).insert_batch(
            {'stock_code': code, 'profit': profits, 'profit_relative': profit_relative, 'date': date,
             'value': matrix.tolist()})


    @classmethod
    def draw_ma_line_one_four(cls, data, profits, date, pixel, code, table_name):

        if len(data) != pixel:
            return
        temp = []

        for i, r in data.iterrows():
            temp.append(r)
            temp.append(r)
            temp.append(r)
            temp.append(r)
        pixel *= 4
        temp = pd.concat(temp)
        data = temp

        data['ma5'] += 0.5
        data['ma10'] += 0.5
        data['ma20'] += 0.5
        data['ma60'] += 0.5
        data['ma120'] += 0.5
        data['high'] += 0.5
        data['low'] += 0.5
        ma5 = data['ma5'].astype('int').tolist()
        ma20 = data['ma20'].astype('int').tolist()
        ma10 = data['ma10'].astype('int').tolist()
        ma60 = data['ma60'].astype('int').tolist()
        ma120 = data['ma120'].astype('int').tolist()

        high = data.high.astype('int').tolist()
        low = data.low.astype('int').tolist()

        data['ma5_index'] += 0.5
        data['ma10_index'] += 0.5
        data['ma20_index'] += 0.5
        data['ma60_index'] += 0.5
        data['ma120_index'] += 0.5
        data['high_index'] += 0.5
        data['low_index'] += 0.5
        ma5_index = data['ma5_index'].astype('int').tolist()
        ma20_index = data['ma20_index'].astype('int').tolist()
        ma10_index = data['ma10_index'].astype('int').tolist()
        ma60_index = data['ma60_index'].astype('int').tolist()
        ma120_index = data['ma120_index'].astype('int').tolist()

        high_index = data.high_index.astype('int').tolist()
        low_index = data.low_index.astype('int').tolist()

        matrix = np.zeros((pixel, pixel), dtype=np.bool)
        num = int(pixel / 2 - 1)
        num2 = int(pixel / 2)
        for i in range(len(ma5)):
            matrix[(num - ma5_index[i]), i] = True
            matrix[(num - ma10_index[i]), i] = True
            matrix[(num - ma20_index[i]), i] = True
            matrix[(num - ma60_index[i]), i] = True
            matrix[(num - ma120_index[i]), i] = True
            matrix[(num - high_index[i]):(num - low_index[i]), i] = True

            matrix[(num - ma5[i] + num2), i] = True
            matrix[(num - ma10[i] + num2), i] = True
            matrix[(num - ma20[i] + num2), i] = True
            matrix[(num - ma60[i] + num2), i] = True
            matrix[(num - ma120[i] + num2), i] = True
            matrix[(num - high[i]) + num2:(num - low[i]) + num2, i] = True

        BaseModel(table_name).insert_batch(
            {'stock_code': code, 'profit': profits, 'date': date, 'value': matrix.tolist()})

    @classmethod
    def draw_ma_line2(cls, data, profits, date, pixel, code, table_name, n):

        if len(data) != pixel:
            return

        data['ma5'] += 0.5
        data['ma10'] += 0.5
        data['ma20'] += 0.5
        data['ma60'] += 0.5
        data['ma120'] += 0.5
        data['high'] += 0.5
        data['low'] += 0.5
        ma5 = data['ma5'].astype('int').tolist()
        ma20 = data['ma20'].astype('int').tolist()
        ma10 = data['ma10'].astype('int').tolist()
        ma60 = data['ma60'].astype('int').tolist()
        ma120 = data['ma120'].astype('int').tolist()

        high = data.high.astype('int').tolist()
        low = data.low.astype('int').tolist()

        matrix = np.zeros((pixel, pixel), dtype=np.bool)
        num = int(pixel / 2 - 1)
        mark = 0
        num2 = int(pixel / 2)
        for i in range(len(ma5)):
            matrix[(num - ma5[i]), i] = True
            matrix[(num - ma10[i]), i] = True
            matrix[(num - ma20[i]), i] = True
            matrix[(num - ma60[i]), i] = True
            matrix[(num - ma120[i]), i] = True
            matrix[(num - high[i]):(num - low[i]), i] = True
            if (i >= len(ma5) - n):
                matrix[(num - ma5[i]) + num2, mark * n:(mark + 1) * n] = True
                matrix[(num - ma10[i]) + num2, mark * n:(mark + 1) * n] = True
                matrix[(num - ma20[i]) + num2, mark * n:(mark + 1) * n] = True
                matrix[(num - ma60[i]) + num2, mark * n:(mark + 1) * n] = True
                matrix[(num - ma120[i]) + num2, mark * n:(mark + 1) * n] = True
                matrix[(num - high[i] + num2):(num - low[i]) + num2, mark * n:(mark + 1) * n] = True
                mark += 1
        BaseModel(table_name).insert_batch(
            {'stock_code': code, 'profit': profits, 'date': date, 'value': matrix.tolist()})

    @classmethod
    def draw_macd_line(cls, data, profits, date, code, pixel, table_name):
        # 'dif', 'dea', 'macd'

        if len(data) != pixel:
            return
        data['dif'] += 0.5
        data['dea'] += 0.5
        data['macd'] += 0.5

        dif = data['dif'].astype('int').tolist()
        dea = data['dea'].astype('int').tolist()
        macd = data['macd'].astype('int').tolist()
        matrix = np.zeros((pixel, pixel), dtype=np.bool)

        val = int(pixel / 2 - 1)
        for i in range(len(dif)):
            matrix[(dif[i]), i] = True
            matrix[(dea[i]), i] = True
            if (macd[i]) > val:
                matrix[val:(macd[i]), i] = True
            else:
                matrix[(macd[i]):val, i] = True

        BaseModel(table_name).insert_batch(
            {'stock_code': code, 'profit': profits, 'date': date, 'value': matrix.tolist()})

    @classmethod
    def draw_time_trends(cls, data, profits, date, code, pixel, table_name, detal):
        # 'dif', 'dea', 'macd'

        # print("x")
        data = data.tail(detal)
        data['volume'] = pixel / 2 - data['volume'] + 0.5 + pixel / 2 - 1
        data['up'] += 0.5

        volume = data['volume'].astype('int').tolist()
        close = data['up'].astype('int').tolist()
        matrix = np.zeros((pixel, pixel), dtype=np.bool)

        val = int(pixel - 1)
        for i in range(len(close)):
            # matrix[volume[i], i] = True
            if close[i] > pixel / 4:
                matrix[int(pixel / 4):close[i], i] = True
            else:
                matrix[close[i]:int(pixel / 4), i] = True
            matrix[volume[i]:val, i] = True
        # BaseModel(table_name).insert_batch(
        #     {'stock_code': code, 'profit': profits, 'date': date, 'value': matrix.tolist()})
        BaseModel(table_name).remove(date=date, stock_code=code)
        BaseModel(table_name).insert_batch(
            {'stock_code': code, 'profit': profits, 'date': date, 'value': matrix.tolist()})

    @classmethod
    def draw_macd_line2(cls, data, profits, profit_relative, date, code, pixel, table_name, n):
        # 'dif', 'dea', 'macd'

        if len(data) != pixel:
            return
        data['dif'] += 0.5
        data['dea'] += 0.5
        data['macd'] += 0.5

        dif = data['dif'].astype('int').tolist()
        dea = data['dea'].astype('int').tolist()
        macd = data['macd'].astype('int').tolist()
        # pixel=
        matrix = np.zeros((pixel, pixel), dtype=np.bool)

        val = int(pixel / 2 / 2 - 1)
        val2 = int(pixel * 3 / 4 - 1)
        num = int(pixel / 2)
        mark = 0
        detal = int(pixel / n)
        for i in range(len(dif)):
            matrix[(dif[i]), i] = True
            matrix[(dea[i]), i] = True
            if (macd[i]) > val:
                matrix[val:(macd[i]), i] = True
            else:
                matrix[(macd[i]):val, i] = True

            if (i >= len(dif) - n):
                # matrix[(dif[i])+num, mark*n:(mark+1)*n] = True
                # matrix[(dea[i])+num, mark*n:(mark+1)*n] = True
                if (macd[i] + num) > val2:
                    matrix[val2:(macd[i] + num), mark * detal:(mark + 1) * detal] = True
                else:
                    matrix[(macd[i] + num):val2, mark * detal:(mark + 1) * detal] = True
                mark += 1

        BaseModel(table_name).insert_batch(
            {'stock_code': code, 'profit': profits, 'profit_relative': profit_relative, 'date': date,
             'value': matrix.tolist()})

    @classmethod
    def draw_macd_and_ma(cls, data, profits, date, code, pixel, length, table_name, profit_relative=None):
        # 'dif', 'dea', 'macd'

        if len(data) != length:
            return
        print(code)
        data['dif'] += 0.5
        data['dea'] += 0.5
        data['macd'] += 0.5

        dif = data['dif'].astype('int').tolist()
        dea = data['dea'].astype('int').tolist()
        macd = data['macd'].astype('int').tolist()
        data['ma5'] += 0.5
        data['ma10'] += 0.5
        data['ma20'] += 0.5
        data['ma60'] += 0.5
        data['ma120'] += 0.5
        data['high'] += 0.5
        data['low'] += 0.5
        ma5 = data['ma5'].astype('int').tolist()
        ma20 = data['ma20'].astype('int').tolist()
        ma10 = data['ma10'].astype('int').tolist()
        ma60 = data['ma60'].astype('int').tolist()
        ma120 = data['ma120'].astype('int').tolist()

        high = data.high.astype('int').tolist()
        low = data.low.astype('int').tolist()

        matrix = np.zeros((length, length), dtype=np.bool)

        val = int(length / 4 * 3)
        num = int(length / 4 - 1)

        for i in range(len(dif)):
            matrix[(dif[i]), i] = True
            matrix[(dea[i]), i] = True
            if (macd[i]) > val:
                matrix[val:(macd[i]), i] = True
            else:
                matrix[(macd[i]):val, i] = True

            matrix[(num - ma5[i]), i] = True
            matrix[(num - ma10[i]), i] = True
            matrix[(num - ma20[i]), i] = True
            matrix[(num - ma60[i]), i] = True
            matrix[(num - ma120[i]), i] = True
            matrix[num - high[i]:num - low[i], i] = True
        # print('-----')
        BaseModel(table_name).insert_batch(
            {'stock_code': code, 'profit': profits, 'profit_relative': profit_relative, 'date': date,
             'value': matrix.tolist()})

    @classmethod
    def draw_macd_line4(cls, data, profits, profit_relative, date, code, pixel, table_name, n, count):
        # 'dif', 'dea', 'macd'

        if len(data) != pixel:
            return
        data['dif'] += 0.5
        data['dea'] += 0.5
        data['macd'] += 0.5

        dif = data['dif'].astype('int').tolist()
        dea = data['dea'].astype('int').tolist()
        macd = data['macd'].astype('int').tolist()
        matrix = np.zeros((pixel + n * count, pixel + n * count), dtype=np.bool)
        val = int(pixel / 2 +2)
        mark = 0
        for i in range(pixel + n):
            if i < len(dif):
                matrix[(dif[i]), i] = True
                matrix[(dea[i]), i] = True
                if (macd[i]) > val:
                    matrix[val:(macd[i]) + 1, i] = True
                else:
                    matrix[(macd[i]):val + 1, i] = True
            else:
                matrix[(dif[i - n]), (pixel) + mark * count:(pixel) + (mark + 1) * count] = True
                matrix[(dea[i - n]), (pixel) + mark * count:(pixel) + (mark + 1) * count] = True
                if (macd[i - n]) > val:
                    matrix[val:(macd[i - n]) + 1, (pixel) + mark * count:(pixel) + (mark + 1) * count] = True
                else:
                    matrix[(macd[i - n]):val + 1, (pixel) + mark * count:(pixel) + (mark + 1) * count] = True
                mark += 1
        # plt.matshow(matrix,cmap='hot')
        # plt.show()
        BaseModel(table_name).insert_batch(
            {'stock_code': code, 'profit': profits, 'profit_relative': profit_relative, 'date': date,
             'value': matrix.tolist()})

    @classmethod
    def draw_macd_line5(cls, data, profits, profit_relative, date, code, length, table_name, n, count, pixel):
        if len(data) != length:
            return
        data['dif'] += 0.5
        data['dea'] += 0.5
        data['macd'] += 0.5

        dif = data['dif'].astype('int').tolist()
        dea = data['dea'].astype('int').tolist()
        macd = data['macd'].astype('int').tolist()
        data['ma5'] += 0.5
        data['ma10'] += 0.5
        data['ma20'] += 0.5
        data['ma60'] += 0.5
        data['ma120'] += 0.5
        data['high'] += 0.5
        data['low'] += 0.5
        ma5 = data['ma5'].astype('int').tolist()
        ma20 = data['ma20'].astype('int').tolist()
        ma10 = data['ma10'].astype('int').tolist()
        ma60 = data['ma60'].astype('int').tolist()
        ma120 = data['ma120'].astype('int').tolist()

        high = data.high.astype('int').tolist()
        low = data.low.astype('int').tolist()

        matrix = np.zeros((pixel, pixel), dtype=np.bool)

        val = int(pixel / 4 * 3)
        num = int(pixel / 2 - 1)
        mark = 0

        for i in range(length + n):
            if i < len(dif):
                matrix[(dif[i]), i] = True
                matrix[(dea[i]), i] = True
                if (macd[i]) > val:
                    matrix[val:(macd[i]) + 1, i] = True
                else:
                    matrix[(macd[i]):val + 1, i] = True

                matrix[(num - ma5[i]), i] = True
                matrix[(num - ma10[i]), i] = True
                matrix[(num - ma20[i]), i] = True
                matrix[(num - ma60[i]), i] = True
                matrix[(num - ma120[i]), i] = True
                matrix[num - high[i]:num - low[i] + 1, i] = True
            else:
                matrix[(num - ma5[i - n]), (length) + mark * count:(length) + (mark + 1) * count] = True
                matrix[(num - ma10[i - n]), (length) + mark * count:(length) + (mark + 1) * count] = True
                matrix[(num - ma20[i - n]), (length) + mark * count:(length) + (mark + 1) * count] = True
                matrix[(num - ma60[i - n]), (length) + mark * count:(length) + (mark + 1) * count] = True
                matrix[(num - ma120[i - n]), (length) + mark * count:(length) + (mark + 1) * count] = True
                matrix[num - high[i - n]:num - low[i - n] + 1,
                (length) + mark * count:(length) + (mark + 1) * count] = True

                matrix[(dif[i - n]), (length) + mark * count:(length) + (mark + 1) * count] = True
                matrix[(dea[i - n]), (length) + mark * count:(length) + (mark + 1) * n] = True
                if (macd[i - n]) > val:
                    matrix[val:(macd[i - n]) + 1, (length) + mark * count:(length) + (mark + 1) * count] = True
                else:
                    matrix[(macd[i - n]):val + 1, (length) + mark * count:(length) + (mark + 1) * count] = True
                mark += 1

        # print('-----')
        BaseModel(table_name).insert_batch(
            {'stock_code': code, 'profit': profits, 'profit_relative': profit_relative, 'date': date,
             'value': matrix.tolist()})
