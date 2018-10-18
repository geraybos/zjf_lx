# -*- coding: utf-8 -*-
from math import ceil
from multiprocessing import freeze_support, Pool

from app import markets, cpus
from app.actions import capital_to_db, get_stock_code_list
from app.models import model_list
from app.query_str_analyzer import analyzer


def ft(*args):
    # capital 数据，每日
    _ = args[0]
    capital_to_db(_['market_name'], _['stock_code_list'], _['start_date'], _['end_date'])


if __name__ == '__main__':
    s = list()
    market_name = ["sz", 'sh']
    sd = None
    ed = None
    # 不传的话就是计算今天（15点后）/昨天（15点前）
    sd = 20180416
    ed = None

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
    freeze_support()
    pool = Pool(cpus)
    model_list['capital'].remove(analyzer('date >= {} and date <= {}'.format(sd, ed)))
    pool.map(ft, s)
    pool.close()
    pool.join()
