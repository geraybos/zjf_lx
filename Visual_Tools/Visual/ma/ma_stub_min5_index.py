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
    pixel=64
    length=5
    count=12
    interval =48
    hour=9
    minute=50
    detal=KlineInfo.get_detal(kline=kline)
    # wave=0.02
    # amount_data=50000000
    table_name='A_MA_Stub_'+kline+'_version6'

    print(table_name)
    for sc in stocks:
        print(sc)
        end_time = dt.datetime(2018, 9, 10)
        start_time = dt.datetime(2016, 1, 1)
        data = KlineData.read_data(code=sc, start_date=Calendar.calc(start_time, -8)['date'], end_date=end_time,
                                   kline=kline, timemerge=True)



        if len(data) <= 200:
            continue
        # data = CalMacd.cal_macd(data=data, interval=interval, detal=detal)

        data=CalMa.cal_ma_stub(data=data,interval=interval,detal=detal)


        data = data.dropna()
        d = data.date.iloc[-1]




        data = data[data.date <= dt.datetime(d.year, d.month, d.day, hour, minute)]


        while end_time > start_time:
            # print(sc,dt.datetime.now())
            data0 = data.tail(length)
            data0 = data0.reset_index(drop=True)
            profit = data0['profit']
            profit_self = data0['profit_self']
            date = data0['date']
            # amin, amax = data0.low.min(), data0.high.max()


            if len(data0) < length:
                break

            date1 = date.iloc[length - 1]
            date2 = date.iloc[length - 10]


            # data0 = CalMacd.data_normalization(data0,pixel=pixel)
            data0=CalMa.data_normalization(data0,pixel=pixel)
            profit = profit.iloc[length - 1]
            profitself = profit_self.iloc[length - 1]



            profit_relative = 0
            if 'min' in kline:
                if 'A' in table_name:
                    if date1.hour != hour and date1.minute!=minute:
                        # data = data[data.date < dt.datetime(date2.year, date2.month, date2.day)]
                        break
                if abs(profit) > 0.11 or abs(profitself)>0.097:
                    data = data[data.date <= dt.datetime(date2.year, date2.month, date2.day, hour, minute)]
                    continue
            else:
                if abs(profit) > 0.1 * interval:
                    data = data[data.date <= dt.datetime(date2.year, date2.month, date2.day, hour, minute)]
                    continue
                if 'A' in table_name:
                    if abs(profitself) > 0.097:
                        data = data[data.date <= dt.datetime(date2.year, date2.month, date2.day, hour, minute)]
                        print(sc, str(profitself) + '_' + str(date1))
                        continue


            try:
                visualization.draw_ma_stub_line(data=data0, profits=profit,
                                                date=date1, code=sc,
                                                table_name=table_name, pixel=pixel, length=length,
                                                profit_relative=profit_relative,
                                                count=count)

                pass
            except Exception as e:
                print(e)
                pass
            data = data[data.date <= dt.datetime(date2.year, date2.month, date2.day,hour,minute)]
            end_time = date2
            # break

    return 1

import time
if __name__ == '__main__':
    a = time.clock()
    stocks = Stock.get_index_stock_code_list()
    pool = multiprocessing.Pool(processes=3)
    m = 10
    li = [stocks[i:i + m] for i in range(0, len(stocks), m)]
    result = pool.map(fun, li)
    print(time.clock() - a)
    # fun(['000001'])



