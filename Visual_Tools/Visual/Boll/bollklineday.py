import datetime as dt

import multiprocessing
import pandas as pd
import numpy as np
from Calf import KlineData, ModelData
from Calf.data import klinedata
from Calf.models import Calendar

from Calf.models.kline import KlineBase
from File.file import File
from Stock.Stock import Stock
from Visual.Boll.calculateboll import CalBoll
from Visual.Macd.calculatemacd import CalMacd
from Visual.Macd.getmacddata import MacdData
# from Visual.Visualization import visualization
from Visual.Visualization2 import visualization
from Visual.ma.calculatema import CalMa
from kline.klineInfo import KlineInfo

def jug_conditon(kline,profit):

    if ("min" in kline) and abs(profit)<0.11:
            return False


    if abs(profit)<40:
        return False
    return True

def fun(stocks):
    # print(os.getpid(), stocks)
    kline = 'kline_min30'
    market='A'
    pixel=64
    interval = KlineInfo.get_interval(kline)
    detal=KlineInfo.get_detal(kline)
    table_name='boll_'+market+'_'+kline

    for sc in stocks:
        end_time = dt.datetime(2018, 6, 25)
        start_time = dt.datetime(2016, 1, 1)
        data = KlineData.read_data(code=sc, start_date=Calendar.calc(start_time, -203)['date'], end_date=end_time,
                                   kline=kline, timemerge=True)
        if len(data) <= 200:
            continue
        data = CalBoll.cal_boll(data, interval)
        data = data.dropna()
        print(sc)
        while end_time > dt.datetime(2016, 1, 1):
            data0 = data.tail(pixel)
            data0 = data0.reset_index(drop=True)
            profit = data0['profit']
            date = data0['date']
            data0 = CalBoll.data_normalization(data0,pixel)
            data0['date'] = date
            data0['profit'] = profit
            profit = data0.profit.iloc[len(data0) - 1]
            if len(data0) < pixel:
                break
            if 'min' in kline:
                if abs(profit) > 0.11:
                    data = data[data.date < dt.datetime(date.year, date.month, date.day)]
                    continue
            else:
                if abs(profit) > 0.1 * interval:
                    data = data[data.date < dt.datetime(date.year, date.month, date.day)]
                    continue

            data0 = data0.reset_index(drop=True)

            date = data0.date.iloc[len(data0)-1]


            visualization.drow_boll_line(data=data0, profits=profit,
                                           date=date, code=sc,pixel=pixel,table_name=table_name)
            try:
                pass
            except Exception as e:
                print(e)
                pass
            data = data[0:len(data) - detal]
            end_time = date
    return 1


if __name__ == '__main__':
    data = Stock.get_stock_code_list()
    data = data[data.stock_code > '601216']
    stocks = data.stock_code.tolist()
    print(stocks)
    pool = multiprocessing.Pool(processes=4)
    m = 10
    li = [stocks[i:i + m] for i in range(0, len(stocks), m)]
    result = pool.map(fun, li)
    # fun(stocks)
