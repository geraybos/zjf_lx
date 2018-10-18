# -*- coding: utf-8 -*-
#  ----------------------------------------------------------------------------------------
# 多线程算 feature_day
from math import ceil
from multiprocessing import freeze_support, Pool

from app import markets, cpus
from app.actions import capital_to_db, get_stock_code_list
from app.models import model_list, Calendar
from app.query_str_analyzer import analyzer


def ft(*args):
    # capital 数据，每日
    _ = args[0]
    capital_to_db(_['market_name'], _['stock_code_list'], _['start_date'], _['end_date'])


if __name__ == '__main__':
    if not Calendar.in_business(dt=Calendar.today(), day=True):
        exit()
    s = list()
    market_name = ["sz", 'sh']

    # stock_codes = {'sh': model_list['kline_day'].query(market=markets['sh']['id']).distinct('stock_code'),
    #                'sz': model_list['kline_day'].query(market=markets['sz']['id']).distinct('stock_code')}

    # sd = Calendar.today()
    sd = 20180206
    ed = None
    # 不传的话就是计算今天（15点后）/昨天（15点前）
    # sd = 20171215
    # ed = 20171218
    # tobj = model_list['tushare']

    mm = ['sz', 'sh']
    for m in mm:
        stock_codes = get_stock_code_list(markets[m])
        sl = len(stock_codes)
        t = int(ceil(sl * 1.0 / cpus))
        for i in range(cpus):
            s.append(dict(stock_code_list=stock_codes[i * t: (i + 1) * t], market_name=m,
                          start_date=sd,
                          end_date=ed,
                          his=False))
    print('done')

    freeze_support()
    pool = Pool(cpus)
    model_list['capital'].remove(analyzer('date >= {} and date <= {}'.format(sd, ed)))
    pool.map(ft, s)
    pool.close()
    pool.join()
    exit()
