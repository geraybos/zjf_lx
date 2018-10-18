import multiprocessing
import datetime as dt
import os

from Calf import KlineData, BaseModel
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


def fun(data):
    stocks = data['stocks']
    kline = data['kline']
    pixel = 64
    interval = KlineInfo.get_interval(kline=kline)
    detal = KlineInfo.get_detal(kline=kline)
    table_name = 'MACD_A_' + kline
    day_interval = KlineInfo.get_day_interval(kline)
    print(table_name)
    for sc in stocks:
        # end_time = dt.datetime(2018, 8, 1)
        # start_time = dt.datetime(2018, 7, 16)
        end_time = Calendar.today()
        start_time =  Calendar.calc(end_time,-day_interval)['date']
        data = KlineData.read_data(code=sc, start_date=Calendar.calc(start_time, -203)['date'], end_date=end_time,
                                   kline=kline, timemerge=True)
        if len(data) <= 200:
            continue
        data = CalMacd.cal_macd(data=data, interval=interval, detal=detal)
        data = data.dropna()
        # data = data[0:len(data) - interval]
        print(sc)
        while end_time > start_time:
            # print(sc,dt.datetime.now())
            data0 = data.tail(pixel)
            data0 = data0.reset_index(drop=True)
            profit = data0['profit']
            profit_self = data0['profit_self']

            date = data0['date']
            data0 = CalMacd.data_normalization(data0, pixel=pixel)
            # print(sc, dt.datetime.now())
            data0['date'] = date
            data0['profit'] = profit
            data0['profit_self'] = profit_self
            # print(len(data0))
            if len(data0) < pixel:
                break
            data0 = data0.reset_index(drop=True)
            profit = data0.profit.iloc[pixel - 1]
            profitself = data0.profit_self.iloc[pixel - 1]
            date = data0.date.iloc[pixel - 1]
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
                        print(sc, str(profitself) + '_' + str(date))
                        continue

            try:
                visualization.draw_macd_line(data=data0, profits=profit,
                                             date=date, code=sc,
                                             table_name=table_name, pixel=pixel)
                pass
            except Exception as e:
                print(e)
                pass
            data = data[data.date < dt.datetime(date.year, date.month, date.day)]
            end_time = date

    return 1

import time
def macd_exe(kline='kline_min30'):
    a=time.clock()
    stocks = Stock.get_all_stock()
    pool = multiprocessing.Pool(processes=4)
    m = 10
    li = [{'stocks': stocks[i:i + m], 'kline': kline} for i in range(0, len(stocks), m)]
    result = pool.map(fun, li)
    BaseModel('kline_data_update_mark').insert_batch(
        {'status': 200, 'kline': 'macd_'+kline, 'other': 'speed ' + str(time.clock()-a), 'date': dt.datetime.now()})

    # fun(['000001'])
# if __name__ == '__main__':
#     macd_exe(kline='kline_day')
