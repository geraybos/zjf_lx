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
from Visual.one_minute.caculate_one_data import CalOneData
from kline.klineInfo import KlineInfo
def fun(stocks):
    # print(os.getpid(), stocks)
    kline = 'kline_min1'
    pixel=256
    interval = KlineInfo.get_interval(kline=kline)
    detal=KlineInfo.get_detal(kline=kline)
    off=KlineInfo.get_off(kline=kline)
    table_name='AA_time_trends_'+kline
    print(table_name)
    for sc in stocks:
        end_time = dt.datetime(2018,6,25)
        start_time = dt.datetime(2015, 1, 1)
        data = KlineData.read_data(code=sc, start_date=Calendar.calc(start_time, -off)['date'], end_date=end_time,
                                   kline=kline,timemerge=True)
        if len(data)<off:
            break
        if len(data[data.time==1500]) < 3:
            continue
        data = data.sort_values(by=['date'], ascending=True)
        data['date2']=data.date.map(lambda x:dt.datetime(x.year,x.month,x.day))
        print(sc)
        while end_time > dt.datetime(2016, 1, 5):

            # print(sc,dt.datetime.now())

            data0 = data.tail(pixel+detal)

            if len(data0)<pixel+detal:
                break

            data0 = data0.reset_index(drop=True)
            dd = data.date.iloc[-1]
            data0 = CalOneData.data_normalization(data0,pixel=pixel,detal=detal)
            profit=data0.profit.iloc[-1]
            data0 = data0.reset_index(drop=True)
            profitself = data0.profit_self.iloc[-1]
            date = data0.date.iloc[-1]
            # print(sc,date)
            if 'min' in kline:

                if 'A' in table_name:
                    if date.hour != 15:
                        data = data[data.date < dt.datetime(date.year, date.month, date.day)]
                        break
                if abs(profit) > 0.11 or abs(profitself)>0.097:
                    data = data[data.date < dt.datetime(date.year, date.month, date.day)]
                    print(sc,str(profitself)+"__"+str(date))
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
                # data0=data0[data0.date>dt.datetime(date.year, date.month, date.day)]
                visualization.draw_time_trends(data=data0, profits=profit,
                                             date=date, code=sc,
                                             table_name=table_name,
                                             pixel=pixel,detal=detal)
                pass
            except Exception as e:
                print(e)
                pass
            data = data[data.date < dt.datetime(dd.year, dd.month, dd.day)]
            end_time = date
    return 1



if __name__ == '__main__':
    data = Stock.get_stock_code_list()
    # data=data[data.stock_code>'603289']
    stocks = data.stock_code.tolist()
    pool = multiprocessing.Pool(processes=4)
    m = 10
    li = [stocks[i:i + m] for i in range(0, len(stocks), m)]
    result = pool.map(fun, li)
    # fun(['000555'])
