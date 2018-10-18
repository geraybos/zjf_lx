# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------
# # 算 feature_index_day
from multiprocessing import freeze_support, Pool

from app import cpus
from app.actions import day_feature_index
from app.models import Calendar, model_list
from app.query_str_analyzer import analyzer

def gti(*args):
    _ = args[0]
    day_feature_index(_[0], _[1])

# # daily
if __name__ == '__main__':
    if not Calendar.in_business(dt=Calendar.today(), day=True):
        exit()
    p = list()
    d = None

    c = list(Calendar().asc(Calendar().query(analyzer('date = {}'.format(d))), ['num']))
    for cc in c:
        for k, v in {'sz': 'stock_code < 600000', 'cyb': 'stock_code >= 300000 and stock_code < 600000',
                     'sh': 'stock_code >= 600000', 'zxb': 'stock_code >= 002000 and stock_code < 300000'}.items():
            p.append([analyzer('date = {} and {}'.format(Calendar.to('str', cc['date']), v)), k])
    print('done')
    model_list['feature_index_day'].remove(date=Calendar.today())
    cpus = 10
    freeze_support()
    pool = Pool(cpus)
    pool.map(gti, p)
    pool.close()
    pool.join()
    exit()
