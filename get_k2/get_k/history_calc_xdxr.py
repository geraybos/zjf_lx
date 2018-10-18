# -*- coding: utf-8 -*-
from multiprocessing import freeze_support, Pool

from app import markets, cpus
from app.actions import calc_xdxr_specified, get_stock_code_list
from app.models import model_list, Calendar
from app.query_str_analyzer import analyzer


def gt(*args):
    _ = args[0]
    obj = model_list['XDXR_'+_['category_name']]
    obj.insert_batch(calc_xdxr_specified(**_))

if __name__ == '__main__':
    # 参数含义见上例
    market_name = ['sz', 'sh']
    category_name = 'day'
    start_date = 20180706
    end_date = None
    s = list()
    num = 10
    for m in market_name:
        stock_code_list = get_stock_code_list(market=markets[m])
        aa = (lambda a: map(lambda b: a[b:b + num], range(0, len(a), num)))(stock_code_list)
        for s_c_l in aa:
            s.append(dict(category_name=category_name,
                          start_date=start_date,
                          end_date=end_date,
                          stock_code_list=s_c_l))
    model_list['XDXR_day'].remove(analyzer('date >= {} and date <= {}'.format(start_date, end_date)))
    cpus = 30
    freeze_support()
    pool = Pool(cpus)
    pool.map(gt, s)
    pool.close()
    pool.join()
