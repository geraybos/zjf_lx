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


def fun(stocks):
    # print(os.getpid(), stocks)
    kline = 'usa_kline_day'

    pixel=64
    # path = "f://zjf/image/USA_boll_kline_day_test"
    interval = KlineInfo.get_interval(kline)
    detal=KlineInfo.get_detal(kline)
    tabel_name="boll_"+kline
    # path = "f://zjf/image/ma_kline_min30_test"

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
            if len(data0) < pixel:
                break
            data0 = data0.reset_index(drop=True)
            profit = data0.profit.iloc[len(data0)-1]
            date = data0.date.iloc[len(data0)-1]
            if 'min' in kline:
                if abs(profit) > 0.11:
                    data = data[data.date < dt.datetime(date.year, date.month, date.day)]
                    continue
            else:
                if abs(profit) > 0.1 * interval:
                    data = data[data.date < dt.datetime(date.year, date.month, date.day)]
                    continue
            try:
                visualization.drow_boll_line(data=data0, profits=profit,
                                           date=date, code=sc,
                                           pixel=pixel,table_name=tabel_name)
            except Exception as e:
                print(e)
                pass
            data = data[0:len(data) - detal]
            end_time = date
    return 1


if __name__ == '__main__':
    stocks = Stock.get_markets_stock('usa')
    # data = data[data.stock_code > '600333']

    print(stocks)
    pool = multiprocessing.Pool(processes=1)
    m = 10
    li = [stocks[i:i + m] for i in range(0, len(stocks), m)]
    result = pool.map(fun, li)
    # fun(stocks)
