# -*- coding: utf-8 -*-
from datetime import datetime, time
import pandas as pd
import time
from app.models import model_list, Calendar
from app.query_str_analyzer import analyzer


def get_min5_time():

    min5_list = []
    start = 9 * 60 + 35
    end = 11 * 60 + 35
    for i in range(start, end, 5):
        min5_list.append(i)
        a=i/60
        b=i-a*60
        print (a,b)
    print(min5_list)
    start = 13 * 60 +5
    end = 15 * 60 +5
    for i in range(start, end, 5):
        min5_list.append(i)
        a = i / 60
        b = i - a * 60
        print (a, b)
    print(min5_list)
    return min5_list

def get_min15_time():

    min15_list = []
    start = 9 * 60 + 46
    end = 11 * 60 + 46
    for i in range(start, end, 15):
        min15_list.append(i)
        a=i/60
        b=i-a*60
        print (a,b)
    start = 13 * 60 + 16
    end = 15 * 60 + 16
    for i in range(start, end, 15):
        min15_list.append(i)
        a = i / 60
        b = i - a * 60
        print (a, b)
    return min15_list

def get_min30_time():

    min30_list = []
    start = 10 * 60 + 3
    end = 12 * 60 + 3
    for i in range(start, end, 30):
        min30_list.append(i)
        a=i/60
        b=i-a*60
        print (a,b)
    start = 13 * 60 +33
    end = 15 * 60 + 13
    for i in range(start, end, 30):
        min30_list.append(i)
        a = i / 60
        b = i - a * 60
        print (a, b)
    return min30_list

def get_min60_time():

    min60_list = []
    start = 10 * 60 + 40
    end = 12 * 60 + 40
    for i in range(start, end, 60):
        min60_list.append(i)
        a=i/60
        b=i-a*60
        print (a,b)
    start = 14 * 60 + 10
    end = 16 * 60 + 10
    for i in range(start, end, 60):
        min60_list.append(i)
        a = i / 60
        b = i - a * 60
        print (a, b)
    return min60_list

def get_day_time():

    day_list = []
    start=14*60+35
    end=15*60+5
    for i in range(start, end, 5):
        day_list.append(i)
        a = i / 60
        b = i - a * 60
        print (a, b)
    print (day_list)
    return day_list

def in_business(dt, strategy, hard=True):
    strategy = change_status(strategy)
    hour_open = 9
    minute_open = 35
    hour_af = 13
    minute_af = 15
    if (strategy['style'] == 'min5'):
        hour_open = 9
        minute_open = 36
        hour_af = 13
        minute_af = 16
    if (strategy['style'] == 'min15'):
        hour_open = 9
        minute_open = 46
        hour_af = 13
        minute_af = 46
    if (strategy['style'] == 'min30'):
        hour_open = 10
        minute_open = 1
        hour_af = 14
        minute_af = 1
    if (strategy['style'] == 'min60'):
        hour_open = 10
        minute_open = 31
        hour_af = 14
        minute_af = 31
    ms = datetime(year=dt.year, month=dt.month, day=dt.day, hour=hour_open, minute=minute_open)
    me = datetime(year=dt.year, month=dt.month, day=dt.day, hour=hour_open + 2, minute=minute_open)
    afs = datetime(year=dt.year, month=dt.month, day=dt.day, hour=hour_af, minute=minute_af)
    afe = datetime(year=dt.year, month=dt.month, day=dt.day, hour=hour_af + 2, minute=minute_open)
    if hard:
        if (ms <= dt <= me) or (afs <= dt <= afe):
            return True
    else:
        if ms <= dt <= afe:
            return True
    return False

def data_is_update(strategy, data_type):
    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    cql = analyzer(
        "date = {s}".format(s=today))
    strategy=data_type+"_"+strategy
    cursor=model_list[strategy].query(cql)
    stock_data = list(cursor)
    if len(stock_data) > 0:
        data = pd.DataFrame(stock_data)
        a=(data.time.max())
        print (a)
        bf=a/100
        af=a-bf*100
        now_hour=datetime.now().hour
        now_minute=datetime.now().minute
        database_data_time=bf*60+af
        now_time=now_hour*60+now_minute
        if ((now_time - database_data_time) < change_status(strategy)['time']):
            return {'time': a, 'isupdate': True}
        return {'time': a, 'isupdate': False}

def change_status(strategy):
    """
    following this strategy  return 'style' and 'time'
    :param strategy:
    :return: dict  include style and time
    """
    status = {'style': '', 'time': 0}
    if strategy[-2:] == 'n5':
        status['style'] = 'min5'
        status['time'] = 5
    if strategy[-2:] == '15':
        status['style'] = 'min15'
        status['time'] = 15
    if strategy[-2:] == '30':
        status['style'] = 'min30'
        status['time'] = 30
    if strategy[-2:] == '60':
        status['style'] = 'min60'
        status['time'] = 60
    if strategy[-2:] == 'ay':
        status['style'] = 'day'
        status['time'] = 1440
    return status

def is_business(strategy):
    """
    judge wether now time is in bussiness
    :param strategy:
    :return: mark (bool)  true means in business ,and false means not
    """
    mark = False
    d=datetime.now()
    h=d.hour
    m=d.minute
    t=h*60+m
    list=[]
    if (strategy == 'min5'):
        list = get_min5_time()
    if (strategy == 'min15'):
        list = get_min15_time()
    if (strategy == 'min30'):
        list = get_min30_time()
    if (strategy == 'min60'):
        list = get_min60_time()
    if (strategy == 'day'):
        list = get_day_time()
    le=len(list)
    if (t>=list[1] and t <= list[le/2-1]) or (t>=list[le/2] and t<=list[-1]):
        print(str(h*100+m)+'it is time to done')
        mark=True
    print(str(h*100+m)+'is not time to do ')
    return mark







