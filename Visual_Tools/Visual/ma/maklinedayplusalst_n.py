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
from Visual.Macd.calculatemacd import CalMacd
from Visual.Macd.getmacddata import MacdData
# from Visual.Visualization import visualization
from Visual.Visualization2 import visualization
from Visual.ma.calculatema import CalMa
from kline.klineInfo import KlineInfo


def fun(stocks):
    # print(os.getpid(), stocks)
    kline = 'kline_day'
    table_name='A_new_plus_last8_MA_'+kline
    print(table_name)
    interval = KlineInfo.get_interval(kline)
    detal=KlineInfo.get_detal(kline)
    pixel=64
    n=8
    for sc in stocks:
        end_time = dt.datetime(2018, 6, 25)
        start_time = dt.datetime(2016, 1, 1)
        data = KlineData.read_data(code=sc, start_date=Calendar.calc(start_time, -203)['date'], end_date=end_time,
                                   kline=kline, timemerge=True)
        if len(data) <= 200:
            continue
        data = CalMa.cal_ma(data, interval,detal)
        data = data.dropna()
        print(sc)


        while end_time > dt.datetime(2016, 1, 1):
            data0 = data.tail(pixel)
            data0 = data0.reset_index(drop=True)
            profit = data0['profit']
            profitself = data0['profit_self']
            date = data0['date']
            data0 = CalMa.data_normalization2(data0,pixel)
            data0['date'] = date
            data0['profit'] = profit
            data0['profitself'] = profitself
            if len(data0) < pixel:
                break
            data0 = data0.reset_index(drop=True)
            profit = data0.profit.iloc[len(data0)-1]
            profitself = data0.profitself.iloc[len(data0)-1]
            date = data0.date.iloc[len(data0)-1]

            if 'min' in kline:
                if 'A' in table_name:
                    if date.hour != 15:
                        data = data[data.date < dt.datetime(date.year, date.month, date.day)]
                        break
                if abs(profit) > 0.11 or abs(profitself) > 0.097:
                    data = data[data.date < dt.datetime(date.year, date.month, date.day)]
                    continue
            else:
                if abs(profit) > 0.1 * interval:
                    data = data[data.date < dt.datetime(date.year, date.month, date.day)]
                    continue
                if 'A' in table_name:
                    if abs(profitself) > 0.097:
                        data = data[data.date < dt.datetime(date.year, date.month, date.day)]
                        print(sc,str(profitself)+'_'+str(date))
                        continue
            try:
                visualization.draw_ma_line2(data=data0, profits=profit,
                                           date=date, code=sc,
                                           table_name=table_name,pixel=pixel,n=n)
            except Exception as e:
                print(e)
                pass
            data = data[data.date < dt.datetime(date.year, date.month, date.day)]
            end_time = date
    return 1


if __name__ == '__main__':
    data = Stock.get_stock_code_list()
    # data = data[data.stock_code > '600333']
    stocks = data.stock_code.tolist()
    a=(dt.datetime.now())
    pool = multiprocessing.Pool(processes=1)
    m = 10
    li = [stocks[i:i + m] for i in range(0, len(stocks), m)]
    result = pool.map(fun, li)
    print(a)
    print(dt.datetime.now())
    # fun(['000001'])
