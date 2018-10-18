import multiprocessing
import datetime as dt
import os

from Calf import KlineData
from Calf.data import klinedata
from Calf.models import Calendar

from Calf.models.kline import KlineBase
from File.file import File
from Stock.Stock import Stock
from Visual.Macd.calculatemacd import CalMacd
from Visual.Macd.getmacddata import MacdData
from Visual.Visualization2 import visualization
import pandas as pd
import datetime as dt
from kline.klineInfo import KlineInfo


def fun(stocks):
    # print(os.getpid(), stocks)
    kline = 'usa_kline_day'
    pixel=64
    table_name="MACD_"+kline
    interval = KlineInfo.get_interval(kline=kline)
    detal= KlineInfo.get_detal(kline=kline)
    # path = "//DESKTOP-4JKCMO0/zjf1/USA_macd_kline_day"
    # path = "f:/zjf/image/macd
    # _kline_day_test"
    # File.check_file(path=path)
    for sc in stocks:
        end_time = dt.datetime(2018, 6, 20)
        start_time = dt.datetime(2015, 1, 1)
        data = KlineData.read_data(code=sc, start_date=Calendar.calc(start_time, -203)['date'], end_date=end_time,
                                   kline=kline,timemerge=True)
        if len(data) <= 200:
            continue
        data = CalMacd.cal_macd(data, interval)
        data = data.sort_values(by=['date'], ascending=True)
        data= data.dropna()
        # data = data[0:len(data) - interval]
        print(sc)
        while end_time > dt.datetime(2016, 1, 5):
            # print(sc,dt.datetime.now())
            data0 = data.tail(pixel)
            data0 = data0.reset_index(drop=True)
            profit = data0['profit']
            date = data0['date']
            data0 = CalMacd.data_normalization(data0,pixel=pixel)
            # print(sc, dt.datetime.now())
            data0['date'] = date
            data0['profit'] = profit
            if len(data0) < pixel:
                break
            data0 = data0.reset_index(drop=True)
            profit = data0.profit.iloc[pixel-1]
            date = data0.date.iloc[pixel-1]
            if 'min' in kline:
                if abs(profit) > 0.11:
                    data = data[data.date < dt.datetime(date.year, date.month, date.day)]
                    continue
            else:
                if abs(profit) > 0.1 * interval:
                    data = data[data.date < dt.datetime(date.year, date.month, date.day)]
                    continue
            # print(sc, dt.datetime.now())
            try:
                visualization.draw_macd_line(data=data0, profits=profit,
                                             date=date, code=sc,
                                             table_name=table_name, pixel=pixel)
                # pass
            except Exception as e:
                print(e)
                pass
            data = data[data.date < dt.datetime(date.year, date.month, date.day)]
            end_time = date
    return 1


if __name__ == '__main__':
    stocks = Stock.get_markets_stock('usa')
    pool = multiprocessing.Pool(processes=1)
    m=10
    li=[stocks[i:i+m] for i in range(0,len(stocks),m)]
    result = pool.map(fun, li)
    # fun(['002774'])
