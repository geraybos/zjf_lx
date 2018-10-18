# -*- coding: utf-8 -*-
import subprocess
import time
from multiprocessing import freeze_support, Pool



from app import markets
from app import project_dir
from app.actions import get_stock_code_list
from app.actions import i_specified_a
from app.actions import k_specified_a
from app.models import model_list, Calendar
from app.query_str_analyzer import analyzer

from utils import in_business, change_status, data_is_update, get_min5_time, get_min60_time, get_min30_time, \
    get_min15_time, get_day_time
import  pandas as pd
import datetime



import datetime

from app.models import model_list
from app.query_str_analyzer import analyzer
import pandas as pd

def get_volumes(strategy):
        obj = model_list['kline_' + 'min5']
        t = 0
        if (strategy[-2:] == '30'):
            t = 1425
            c = 6
        if (strategy[-2:] == '60'):
            t = 1355
            c = 12
        print (strategy)
        dt = datetime.datetime.now()
        str1 = str(dt.year * 10000 + dt.month * 100 + dt.day)  # data testing  please update
        print(str1)
        sql = analyzer("time >= {} and time < {} and date = {}".format(t, 1455, int(str1)))
        print(sql)
        a = obj.query(sql)
        a = list(a)
        df = pd.DataFrame(a)
        print (list)

        if (len(df) == 0):
            print ('df is None')

        df = df.sort_values(['stock_code', 'time'], ascending=True)
        df.reset_index(inplace=True)
        grouped = df['amount'].groupby(df['stock_code'])
        data = grouped.sum()

        # for i,r in data.iterrows():
        #   dic[r.stock_code]=r.volume
        return (dict(data))

def gt_kline(*args):
    # print('gt')
    _ = args[0]

    a=k_specified_a(market_name=_['market'], category_name=_['category'], stock_code_list=_['stock_code_list'],
                  start_date=_['start_date'], end_date=_['end_date'])
    # print(a)
    return pd.DataFrame(a)
    # obj.insert_batch()
def get_sql(strategy):
    if strategy[-2:] == '30':
        sql = {'time': 1430}

    if strategy[-2:] == '60':
        sql = {'time':1400}
    return sql;
def get_his(stratrgy):
    sql=get_sql(stratrgy)

    obj = model_list['kline_' + stratrgy]
    print (stratrgy)
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print (sql)
    dt = datetime.datetime.now()
    str1 = str(dt.year*10000+dt.month*100+dt.day)
    sql=dict(sql,**analyzer("date = {}".format(str1)))
    a=obj.query(sql)
    a=list(a)
    df=pd.DataFrame(a)
    df.reset_index(inplace=True)
    return df




def get_kline_data(strategy):
    print('kline_in')
    t = Calendar.today()
    if Calendar().query(date=t):
        mm = ['sh', 'sz']
        cc = [strategy]
        strategy = 'kline_' + strategy
        s = list()
        for m in mm:
            sl = get_stock_code_list(markets[m])
            num = 50
            aa = (lambda a: map(lambda b: a[b:b + num], range(0, len(a), num)))(sl)
            for a in aa:
                for k in cc:
                    s.append(dict(market=m, category=k, stock_code_list=a, start_date=None, end_date=None))

        # model_list[strategy].remove(date=t)
        # model_list['kline_min15'].remove(date=t)
        # model_list['kline_min5'].remove(date=t)
        # model_list['kline_min30'].remove(date=t)
        # model_list['kline_min60'].remove(date=t)
        # model_list['kline_day'].remove(date=t)
        print("((((((((((((")
        print(len(s))
        freeze_support()
        pool = Pool(5)
        r=pool.map(gt_kline, s)
        df = pd.concat(r,join='outer',ignore_index=False)
        df.reset_index(inplace=True)
        # print(df.head(10))
        pool.close()
        pool.join()
        return df

# def get_volumes(strategy):
#     obj = model_list['kline_' + 'min5']
#     t=0
#     if (strategy[-2:] == '30'):
#         t= 1430
#         c=6
#     if (strategy[-2:] == '60'):
#         t=1400
#         c=12
#     print (strategy)
#     dt = datetime.datetime.now()
#     str1 = str(dt.year*10000+dt.month*100+dt.day)   # data testing  please update
#     print(str1)
#     sql=analyzer("time > {} and time <= {} and date = {}".format(t,1500,int(str1)))
#     a=obj.query(sql)
#     a=list(a)
#     df=pd.DataFrame(a)
#     print (list)
#
#     if(len(df)==0):
#         print ('df is None')
#
#     df = df.sort_values(['stock_code','time'],ascending=True)
#     df.reset_index(inplace=True)
#     print('stock_code')
#     print((df['stock_code']))
#     print(len(df))
#     pp={}
#     sum = 0
#     his=df['stock_code'].iloc[0]
#     i=0
#     for i in range(0,len(df)):
#        if(df['stock_code'].iloc[i]=='600057'):
#             print('youyouyouyou')
#        a=df['stock_code'].iloc[ i]
#        if(a==his):
#            sum = sum + df['amount'].iloc[i]
#        else:
#            pp[df['stock_code'].iloc[i-1]] = sum;
#            his=a
#            sum=0+df['amount'].iloc[i]
#
#     pp[df['stock_code'].iloc[i]] = sum;
#
#
#
#     print('a len:')
#
#     print(pp['000001'])
#     print (len(pp))
#     return pp


# print(get_volumes('min5'))
import datetime as dt


def get_data(kline):
    t = 1425 if kline == 'min30' else 1355
    today = dt.datetime.strftime(dt.date.today(), '%Y%m%d')
    tt = {'$gte': t, '$lte': 1450}
    sql = analyzer("date = {} and time <= {} and time >= {}".format(today,1450,t))
    print(sql)
    a = model_list['kline_min5'].query(sql)
    a = list(a)
    data = pd.DataFrame(a)
    # data = md.get_stock_data(kline='min5', start_date=today, end_date=today, axis=0, timemerge=False, time=t)
    kline_data = data[data.time == 1450]
    spl_data = data.amount.groupby(data.stock_code).sum()

    spl_data = spl_data.to_frame()
    spl_data['stock_code'] = spl_data.index
    data = pd.merge(kline_data, spl_data, on='stock_code')
    data['amount'] = data.amount_x + data.amount_y
    data['time'] = 1500
    data.drop(['_id', 'classtype', 'amount_x', 'amount_y'], axis=1, inplace=True)
    dicts = []
    for i,r in data.iterrows():
        dicts.append(dict(r))

    x=model_list['kline_'+kline].insert_batch(dicts)
    print(x)
    return data
# print(get_data('min30').head())







