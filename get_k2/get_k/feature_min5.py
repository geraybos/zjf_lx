# -*- coding: utf-8 -*-
from collections import deque
from datetime import datetime
from multiprocessing import freeze_support, Pool

from app import cpus, markets
from app.actions import minute_feature_index, get_stock_code_list
from app.models import model_list, Calendar
from app.query_str_analyzer import analyzer


def calc_ma(raw_data_list, ma=5):
    lrdl = len(raw_data_list)
    # if lrdl < ma:
    #     return None
    ma_t = 'ma{}'.format(ma)
    ds = deque()
    to = raw_data_list[0]
    sub_ma = ma - 1 if lrdl > ma else lrdl
    for i in range(sub_ma):
        ri = raw_data_list[i]
        if to['date'] < ri['date']:
            to = ri
        ri[ma_t] = ri['close']
        ri['change_r'] = (ri['close'] - to['open']) / to['open']
        ri['sub_new'] = False  # 之后要把这行换掉
        ds.append(ri['close'])

    for i in range(sub_ma, lrdl):
        ri = raw_data_list[i]
        ds.append(ri['close'])
        ri[ma_t] = round(sum(ds) / ma, 4)
        ri['change_r'] = (ri['close'] - to['open']) / to['open']
        ri['sub_new'] = False  # 之后要把这行换掉
        ds.popleft()
    return raw_data_list


def gt(_):
    obj = model_list['kline_min5']
    result = list()
    sl = _['sl']
    for sc in sl:
        data = list(obj.asc(obj.query(stock_code=sc, date={'$gte': _['sd']}), ['date', 'time']))
        ld = len(data)
        if ld:
            # if ld >= 5:
            calc_ma(data, ma=5)
            # if ld >= 10:
            calc_ma(data, ma=10)
            # if ld >= 20:
            calc_ma(data, ma=20)
            # if ld >= 60:
            calc_ma(data, ma=60)
            # else:
            result.extend(data)
    print('{} done'.format(sl))

    fmobj = model_list['feature_min5']
    fmobj.insert_batch(result)


def ft(_):
    fmobj = model_list['feature_min5']
    data = list(fmobj.query(_[0]))
    model_list['feature_index_min5'].insert_batch(minute_feature_index(data, _[1]))
    print('{} done'.format(_))


if __name__ == '__main__':
    mm = ['sz', 'sh']
    sd = Calendar.to('datetime', 20180101)
    ed = Calendar.today()
    # sd = Calendar.today()
    s = datetime.now()
    p = list()
    for m in mm:
        sl = get_stock_code_list(markets[m])
        num = 30
        aa = (lambda a: map(lambda b: a[b:b + num], range(0, len(a), num)))(sl)
        for a in aa:
            p.append({'sd': sd, 'sl': a})
    func = gt
    for i in p:
        func(i)

    p = list()
    cs = list(Calendar().query(date={'$gte': sd, '$lte': ed}))
    # ts = model_list['feature_min5'].distinct('time')
    for cc in cs:
        for k, v in {'sz': 'stock_code < 600000', 'cyb': 'stock_code >= 300000 and stock_code < 600000',
                     'sh': 'stock_code >= 600000', 'zxb': 'stock_code >= 002000 and stock_code < 300000'}.items():
            # for t in ts:
            #     p.append([analyzer('date = {} and time = {} and {}'.format(Calendar.to('str', cc['date']), t, v)), k])
            p.append([analyzer('date = {} and time = 1500 and {}'.format(Calendar.to('str', cc['date']), v)), k])

    func = ft
    freeze_support()
    pool = Pool(cpus)
    pool.map(func, p)
    pool.close()
    pool.join()
    # exit()
    e = datetime.now()
    print(s, e)
