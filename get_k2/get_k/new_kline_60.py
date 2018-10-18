# -*- coding: utf-8 -*-
import traceback
from os.path import abspath, pardir, join
from sys import path

from datetime import datetime

from Mark import Mark
from app.models import model_list, Calendar
from app.query_str_analyzer import analyzer
import pandas as pd

from get_data import get_kline_data


path.append(abspath(join(abspath(join(abspath(__file__), pardir)), pardir)))


def min60_time_list():
    list=[1500,1430,1400,1330,1300,1100,1030,1000]
    return list

def get_data():
    dt = datetime.now()

    # if dt.hour > 15:
    # dt = datetime(2018, 6, 12, 14, 10)
    now_time = dt.hour * 100 + dt.minute
    if (now_time >=1030 and now_time<1100)or (now_time>=1130 and now_time<1300) or (now_time>=1400 and now_time<1430) :
        start_time=0
        if dt.hour >=11 and dt.hour<13:
            now_time=1300
        for i in range(0,len(min60_time_list())):
             if now_time>=min60_time_list()[i]:
                 now_time=min60_time_list()[i]
                 start_time=min60_time_list()[i+1]
                 print(now_time)
                 print(start_time)
                 break

        sql = analyzer('date = {} and time <= {} and time >= {}'.format(dt.year * 10000 + dt.month * 100 + dt.day, now_time,
                                                                       start_time))
        print(sql)
        data = model_list['kline_min30'].query(sql)
        data = pd.DataFrame(list(data))
        data.sort_values(by=['time'])
        kline_data = data[data.time == now_time]
        kline_data_his = data[data.time == start_time]
        grouped = data.groupby(['stock_code']).agg({'amount': 'sum','volume':'sum','high':'max','low':'min'})
        grouped['stock_code'] = grouped.index
        data = pd.merge(kline_data, grouped, on='stock_code')
        data['time'] = now_time
        data['amount'] = data.amount_y
        data['volume'] = data.volume_y
        data['high'] = data.high_y
        data['low'] = data.low_y
        # data.open=kline_data_his.open
        data.drop(['_id', 'classtype', 'amount_x', 'amount_y','volume_x','volume_y','high_y','high_x','low_x','low_y'], axis=1, inplace=True)

        dicts = []
        for i,r in data.iterrows():
            dicts.append(dict(r))
        x=model_list['kline_min60'].insert_batch(dicts)
        print(dicts[0:10])
        return data
    else:
        exit()
if __name__ == '__main__':



    strategy = 'min60'

    try:

        print('start')
        get_data()
        Mark.update_mark_success('kline_'+strategy)
        # a=datetime.now()
        # dit = {'date': a, 'status': 200, 'kline': strategy, 'other': '正常'}
        # model_list['kline_data_update_mark'].insert(dit)


    except Exception as e:
        # a = datetime.now()
        x = '合并30异常:' + str(e.message) + "追踪：" + str(traceback.format_exc())
        Mark.update_mark_fail(strategy='kline_'+strategy,messages=x)
        # dit = {'date': a, 'status': 500, 'kline': strategy, 'other': x}
        # model_list['kline_data_update_mark'].insert(dit)


        try:
            get_kline_data(strategy)
            # a = datetime.now()
            # dit = {'date': a, 'status': 200, 'kline': strategy, 'other': '正常'}
            # model_list['kline_data_update_mark'].insert(dit)
            Mark.update_mark_success('kline_' + strategy)
        except Exception as e:
            a = datetime.now()
            # x = '异常:' + str(e.message) + "追踪：" + str(traceback.format_exc())
            # dit = {'date': a, 'status': 500, 'kline': strategy, 'other': x}
            # model_list['kline_data_update_mark'].insert(dit)
            x = '合并30异常:' + str(e.message) + "追踪：" + str(traceback.format_exc())
            Mark.update_mark_fail(strategy='kline_' + strategy, messages=x)
            exit(1)
        exit(1)
    exit(0)
