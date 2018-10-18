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

from Visual.ma.calculatema import CalMa
from kline.klineInfo import KlineInfo
def fun(stocks):
    # print(os.getpid(), stocks)
    kline = 'index_min5'
    pixel=54
    n=5
    count=2
    interval = KlineInfo.get_interval(kline=kline)
    detal=KlineInfo.get_detal(kline=kline)
    table_name='A_Volume_'+kline+'_version5'
    print(table_name)
    for sc in stocks:
        end_time = dt.datetime(2018, 8, 15)
        start_time = dt.datetime(2016, 1, 1)
        data = KlineData.read_data(code=sc, start_date=Calendar.calc(start_time, -203)['date'], end_date=end_time,
                                   kline=kline, timemerge=True)
        if len(data) <= 200 :
            continue
        data=CalMa.cal_profit(data,interval,detal)
        data=data.dropna()
        d = data.date.iloc[-1]
        data=data[data.date<=dt.datetime(d.year,d.month,d.day,9,55)]
        print(sc)
        while end_time > start_time:
            data0 = data.tail(pixel*4)
            amax=data0.volume.max()
            data0 = data0.tail(pixel)
            data0 = data0.reset_index(drop=True)
            profit = data0.profit.iloc[ - 1]
            profitself = data0.profit_self.iloc[- 1]
            date = data0['date']
            if len(data0) < pixel:
                break
            date2 = date.iloc[ - 6]
            date1 = date.iloc[ - 1]
            data0=CalMa.data_normalization_volume2(data0,pixel=pixel+n*count,amax=amax)
            if 'min' in kline:
                if 'A' in table_name:
                    if date1.hour != 9 and date1.minute!=55:
                        data = data[data.date <= dt.datetime(date2.year, date2.month, date2.day, 9, 55)]
                        break
                if abs(profit) > 0.11 or abs(profitself)>0.097:
                    data = data[data.date <= dt.datetime(date2.year, date2.month, date2.day, 9, 55)]
                    continue
            else:
                if abs(profit) > 0.1 * interval:
                    data = data[data.date <= dt.datetime(date2.year, date2.month, date2.day, 9, 55)]
                    continue
                if 'A' in table_name:
                    if abs(profitself) > 0.097:
                        data = data[data.date <= dt.datetime(date2.year, date2.month, date2.day, 9, 55)]
                        print(sc, str(profitself) + '_' + str(date))
                        continue
            try:
                visualization.draw_volume(data=data0, profits=profit,
                                          date=date1, code=sc,
                                          table_name=table_name, pixel=pixel, n=n,
                                          count=count)
                pass
            except Exception as e:
                print(e)
                pass
            data = data[data.date <= dt.datetime(date2.year, date2.month, date2.day,9,55)]
            end_time = date2

    return 1

if __name__ == '__main__':
    stocks = Stock.get_index_stock_code_list()

    pool = multiprocessing.Pool(processes=3)
    m = 10
    li = [stocks[i:i + m] for i in range(0, len(stocks), m)]
    print(li)
    result = pool.map(fun, li)
    # fun(['000001'])
