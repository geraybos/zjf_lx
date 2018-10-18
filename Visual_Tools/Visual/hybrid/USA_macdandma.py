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

from Visual.hybrid.calculate import calculate
from Visual.ma.calculatema import CalMa
from kline.klineInfo import KlineInfo


def fun(stocks):
    # print(os.getpid(), stocks)
    kline = 'usa_kline_day'
    pixel=64
    length=pixel*2
    interval = KlineInfo.get_interval(kline=kline)
    off=KlineInfo.get_off(kline=kline)
    table_name='MACD_and_MA_'+kline
    print(table_name)
    for sc in stocks:
        print(os.getpid(),sc)
        end_time = dt.datetime(2018, 6, 20)
        start_time = dt.datetime(2015, 1, 1)
        data = KlineData.read_data(code=sc, start_date=Calendar.calc(start_time, -off)['date'], end_date=end_time,
                                   kline=kline,timemerge=True)
        if len(data) <= (off-20):
            continue
        data = calculate.calculate_data(data, interval)
        # data = data.sort_values(by=['date'], ascending=True)
        data= data.dropna()
        # data = data[0:len(data) - interval]

        while end_time > dt.datetime(2016, 1, 5):
            # print(sc,dt.datetime.now())
            data0 = data.tail(length)
            data0 = data0.reset_index(drop=True)
            profit = data0['profit']
            date = data0['date']
            data0 = calculate.data_normalization(data=data0,pixel=pixel,length=length)
            # print(sc, dt.datetime.now())
            data0['date'] = date
            data0['profit'] = profit
            if len(data0) < length:
                break
            data0 = data0.reset_index(drop=True)
            profit = data0.profit.iloc[length-1]
            date = data0.date.iloc[length-1]
            if 'min' in kline:
                if 'A' in table_name:
                    if date.hour != 15:
                        data = data[data.date < dt.datetime(date.year, date.month, date.day)]
                        break
                if abs(profit) > 0.11:
                    data = data[data.date < dt.datetime(date.year, date.month, date.day)]
                    continue
            else:
                if abs(profit) > 0.1 * interval:
                    data = data[data.date < dt.datetime(date.year, date.month, date.day)]
                    continue


            # print(sc, dt.datetime.now())
            try:
                visualization.draw_macd_and_ma(data=data0, profits=profit,
                                             date=date, code=sc,
                                             table_name=table_name, pixel=pixel,length=length)
                pass
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
    # fun(['00700'])

    # fun(['000001'])
