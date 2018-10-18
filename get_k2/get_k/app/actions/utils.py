# -*- coding: utf-8 -*-
from datetime import datetime

import requests

from app.models.base_model import BaseModel
from app.query_str_analyzer import analyzer
from . import data_client
from ..models import Calendar, model_list
from ..utils import list_combine, log

import pandas as pd
def get_stock_code_list(market):


    t=Calendar.today()
    obj=BaseModel('daily_stocks')
    # obj.insert({'a':'a'})
    sql={'date':t,'market':market['id']}
    curror=obj.query(sql)
    if curror.count()==0:
        stock_list = []
        flag = True
        while flag:
            err, stock_counts = data_client.GetSecurityCount(market['id'])
            loop_time = stock_counts // 1000
            for loop in range(loop_time + 1):
                err, stock_count, result = data_client.GetSecurityList(market['id'], loop * 1000)
                r_list = result.split('\n')
                for r in r_list:
                    xcode = r.split('\t')[0]
                    rrrrr = market['filter'](xcode)
                    if rrrrr:
                        stock_list.append(xcode)
            flag = len(stock_list) == 0
        obj.insert({'date':t,'market':market['id'],'stock_list':stock_list})
        print(stock_list)
        return stock_list
    else:
        data=pd.DataFrame(list(curror))
        return data.stock_list.tolist()[0]


def split_start(category_name):  # category 为日线实时数据的情况下可以不截掉第一条数据
    now = datetime.now()
    if category_name.endswith('day') or (not Calendar.in_business(now) or now.hour >= 15):
        s = 0
    else:
        s = 1
    return s


def sort_key(row):
    if 'time' in row:
        k = lambda x: (x['date'], x['time'])
    else:
        k = lambda x: (x['date'])
    return k


def row_str_to_list(market, category_name, stock_code, row_str, start_date, end_date):
    obj = model_list[category_name]
    if category_name.startswith('index'):
        field = ['date', 'open', 'close', 'high', 'low', 'volume', 'amount', 'up', 'down', 'market', 'stock_code']
    else:
        if market['name'] in ['usa', 'hk']:
            field = ['date', 'open', 'high', 'low', 'close', 'chicang', 'volume', 'amount', 'market', 'stock_code']
        else:
            field = ['date', 'open', 'close', 'high', 'low', 'volume', 'amount', 'market', 'stock_code']
    rows = set(row_str.split('\n'))
    r_list = list()

    for row in rows:
        tmp_r = row.split('\t')
        tmp_r.append(market['id'])
        tmp_r.append(stock_code)
        raw_r = list_combine(field, tmp_r)
        try:
            r = obj.trans_data(raw_r)
        except Exception as e:
            if not (e.message.startswith('need more than') or
                        e.message.startswith('invalid literal ') or
                        e.message.startswith("'NoneType' object has no attribute 'groups'")
                    ):
                log('error', obj.tablename, d_raw=raw_r, err_msg=e.message)
            continue
        if r['volume'] > 0 and (start_date <= r['date'] <= end_date and r['open'] != 0.0) or \
                (market['name'] in ['usa'] and start_date <= Calendar.calc(r['date'], 1)['date'] <= end_date):
            r_list.append(r)
    return r_list


def xdxr_str_to_list(xdxr_str, start_date, end_date):
    obj = model_list['XDXR']
    field = ['market', 'stock_code', 'date', 'save', 'cache', 'stock_p', 'stock_v', 'percent']
    xdxrs = set(xdxr_str.split('\n'))
    r_list = list()
    for xdxr in xdxrs:
        tmp_xdxr = xdxr.split('\t')
        raw_xdxr = list_combine(field, tmp_xdxr)
        try:
            r = obj.trans_data(raw_xdxr)
        except Exception as e:
            if (not (e.message.startswith('need more than') or e.message.startswith('invalid literal '))) and xdxr.decode('gbk') != u'\u5e02\u573a\t\u8bc1\u5238\u4ee3\u7801\t\u65e5\u671f\t\u4fdd\u7559\t\u9001\u73b0\u91d1\t\u914d\u80a1\u4ef7\t\u9001\u80a1\u6570\t\u914d\u80a1\u6bd4\u4f8b':
                print('Error: XDXR', obj.tablename, xdxr, e.message)
            continue
        if r['date'] <= end_date and r['date'] >= start_date:
            r_list.append(r)
    return r_list


def crawl(url, params):
    return requests.get(url, params=params)


def date_range(start_date=None, end_date=None):

    if start_date:
        ssql = 'date >= {}'.format(Calendar.to(str, start_date))
    else:
        ssql = 'date >= 20120130'
    if end_date:
        esql = 'date <= {}'.format(Calendar.to(str, end_date))
    else:
        esql = 'date <= {}'.format(Calendar.to(str, Calendar.recent()))

    sql = ' and '.join([ssql, esql])
    cond = analyzer(sql)
    calendar = list(Calendar().query(cond))
    return calendar


def date_preprocess(start_date=None, end_date=None):
    # start_date==None & end_date==None----> today
    # start_date==None & end_date!=None----> from end_date-1 to end_date
    # start_date!=None & end_date==None----> from start_date to today
    # start_date!=None & end_date!=None----> from start_date to end_date
    ed = Calendar.recent(end_date, forward=False)['date']
    if start_date is None:
        if end_date is None:
            today = Calendar.recent(Calendar.today())['date']
            return today, today
        else:
            sd = Calendar.calc(ed, -1)['date']
            return sd, ed
    else:
        sd = Calendar.recent(start_date, forward=False)['date']
        return sd, ed
