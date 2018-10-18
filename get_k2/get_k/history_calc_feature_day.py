# -*- coding: utf-8 -*-
from math import ceil
from multiprocessing import freeze_support, Pool

from app import markets, cpus
from app.actions import day_feature, get_stock_code_list
from app.models import model_list
from app.query_str_analyzer import analyzer


def gt(*args):
    _ = args[0]
    sd = _['start_date']
    ed = _['end_date']
    his = _['his']
    for s_c in _['stock_code_list']:
        day_feature(s_c, sd, ed, his)


if __name__ == '__main__':
    s = list()
    market_name = ["sz", 'sh']
    sd = None
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
                          his=True))
    print('done')
    model_list['feature_day'].remove(analyzer('date >= {} and date <= {}'.format(sd, ed)))
    freeze_support()
    pool = Pool(cpus)
    pool.map(gt, s)
    pool.close()
    pool.join()
    print('ok')
    # for i in s:
    #     gt(i)
