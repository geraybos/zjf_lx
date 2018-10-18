# -*- coding: utf-8 -*-

from multiprocessing import freeze_support, Pool

from app import markets, cpus
from app.actions import get_stock_code_list
from app.actions import get_xdxr
from app.models import model_list
from app.query_str_analyzer import analyzer


def gt(_):
    get_xdxr(market_name=_['market'], stock_code_list=_['stock_code_list'], start_date=_['start_date'],
             end_date=_['end_date'])


if __name__ == '__main__':
    mm = ['sh', 'sz']
    s = list()
    sd = 20180416
    ed = None
    for m in mm:
        sl = get_stock_code_list(markets[m])
        num = 10
        aa = (lambda a: map(lambda b: a[b:b + num], range(0, len(a), num)))(sl)
        for a in aa:
            s.append(dict(market=m, stock_code_list=a, start_date=sd, end_date=ed, category='day'))

    model_list['XDXR'].remove(analyzer('date >= {} and date <= {}'.format(sd, ed)))
    freeze_support()
    pool = Pool(cpus)
    pool.map(gt, s)
    pool.close()
    pool.join()
