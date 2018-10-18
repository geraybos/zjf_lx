import datetime as dt

import multiprocessing
import pandas as pd
import numpy as np
from Calf import KlineData, ModelData, BaseModel, ModelAction, ModelRun
from Calf.data import klinedata
from Calf.models.calendar1 import Calendar

from Calf.models.kline import KlineBase
from File.file import File
from Stock.Stock import Stock
from Visual.Macd.calculatemacd import CalMacd
from Visual.Macd.getmacddata import MacdData
# from Visual.Visualization import visualization
from Visual.Visualization2 import visualization
from Visual.ma.calculatema import CalMa
from kline.klineInfo import KlineInfo


def fun(data):
    stocks=data['stocks']
    kline=data['kline']
    # print(os.getpid(), stocks)
    table_name='MA_A_'+kline
    interval = KlineInfo.get_interval(kline)
    detal=KlineInfo.get_detal(kline)
    off=KlineInfo.get_off(kline=kline)
    day_interval=KlineInfo.get_day_interval(kline)
    pixel=64
    for sc in stocks:
        end_time = Calendar.today()
        start_time = Calendar.calc(end_time,-day_interval)['date']
        # end_time = dt.datetime(2018,8,1)
        # start_time=dt.datetime(2018,6,20)

        data = KlineData.read_data(code=sc, start_date=Calendar.calc(start_time, -off)['date'], end_date=end_time,
                                   kline=kline, timemerge=True)
        if len(data) <= 200:
            continue
        data = CalMa.cal_ma(data, interval,detal)
        data = data.dropna()
        print(sc)
        while end_time > start_time:
            data0 = data.tail(pixel)
            data0 = data0.reset_index(drop=True)
            profit = data0['profit']
            profitself = data0['profit_self']
            date = data0['date']
            data0 = CalMa.data_normalization(data0,pixel)
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
                        continue


            try:
                visualization.draw_ma_line(data=data0, profits=profit,
                                           date=date, code=sc,
                                           table_name=table_name,pixel=pixel)
            except Exception as e:
                print(e)
                pass
            data = data[data.date < dt.datetime(date.year, date.month, date.day)]
            end_time = date

    return 1

import time
def start_exe(kline='kline_min30'):
    a=time.clock()
    data = Stock.get_all_stock()
    stocks = data

    pool = multiprocessing.Pool(processes=4)
    m = 10
    li = [{'stocks':stocks[i:i + m],'kline':kline} for i in range(0, len(stocks), m)]
    result = pool.map(fun, li)
    spend=time.clock()-a
    BaseModel('kline_data_update_mark').insert_batch({'status':200,'kline':'ma_'+kline,'other':'speed '+str(spend),'date':dt.datetime.now()})

# if __name__ == '__main__':
#  start_exe(kline='kline_day')