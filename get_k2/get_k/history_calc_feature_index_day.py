# -*- coding: utf-8 -*-
from multiprocessing import freeze_support, Pool

from app import cpus
from app.actions import day_feature_index
from app.models import Calendar, model_list
from app.query_str_analyzer import analyzer


def gti(*args):
    _ = args[0]
    day_feature_index(_[0], _[1])


if __name__ == '__main__':
    sd = 20180625
    ed = None
    dates = list(Calendar().query(analyzer('date >= {} and date <= {}'.format(sd, ed))))
    p = list()
    for d in dates:
        for k, v in {'sz': 'stock_code < 600000', 'cyb': 'stock_code >= 300000 and stock_code < 600000',
                     'sh': 'stock_code >= 600000', 'zxb': 'stock_code >= 002000 and stock_code < 300000'}.items():
            p.append([analyzer('date = {} and {}'.format(Calendar.to('str', d['date']), v)), k])
    sql=analyzer('date >= {} and date <= {}'.format(sd,ed))
    iobj = model_list['feature_index_day'].remove(sql)
    print('done')
    freeze_support()
    pool = Pool(cpus)
    pool.map(gti, p)
    pool.close()
    pool.join()
