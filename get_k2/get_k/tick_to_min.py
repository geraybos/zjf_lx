# -*- coding: utf-8 -*-
from datetime import datetime

import sys

from app import markets, cpus
from app.actions import generate_min_by_tick, get_stock_code_list
from multiprocessing import freeze_support, Pool

from app.models import model_list, Calendar
from app.query_str_analyzer import analyzer


def gt(_):
    for sc in _['stock_code_list']:
        generate_min_by_tick(sc, _['start_date'], _['end_date'])


if __name__ == '__main__':
    his = True if len(sys.argv) > 1 and sys.argv[1] == 'his' else False
    print('mod: {}'.format(his))
    if not Calendar.in_business(Calendar.today(), day=True):
        if his:
            pass
        else:
            exit()
    s = list()
    sd = 20170101 if his else None
    ed = None
    for m in ['sh', 'sz']:
        sl = get_stock_code_list(markets[m])
        dbsc = [a for a in list(
            model_list['kline_min1'].query(analyzer('date >= {} and date <= {}'.format(sd, ed))).distinct('stock_code'))
                if
                (m == 'sz' and int(a) < 600000) or (m == 'sh' and int(a) >= 600000)]
        sl = sorted(list(set(sl).difference(set(dbsc))))
        num = 10
        aa = (lambda a: map(lambda b: a[b:b + num], range(0, len(a), num)))(sl)
        for a in aa:
            s.append(dict(stock_code_list=a, start_date=sd, end_date=ed))
    print(s)

    dql = analyzer('date >= {} and date <= {}'.format(sd, ed))
    model_list['kline_min1'].remove(dql)
    print(datetime.now())
    cpus=30
    freeze_support()
    pool = Pool(cpus)
    pool.map(gt, s)
    pool.close()
    pool.join()
    # for i in s:
    #     gt(i)
    print(datetime.now())
