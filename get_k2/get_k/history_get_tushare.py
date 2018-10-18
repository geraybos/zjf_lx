# -*- coding: utf-8 -*-
from multiprocessing import freeze_support, Pool

from app import cpus
from app.actions import tushare_to_db


def gt(*args):
    _ = args[0]
    tushare_to_db(start_date=_['start_date'], end_date=_['end_date'])
    print(_)


if __name__ == '__main__':
    s = list()
    for i in range(2000, 2017):
        s.append(dict(start_date='{}0101'.format(i), end_date='{}1231'.format(i)))
    freeze_support()
    pool = Pool(cpus)
    pool.map(gt, s)
    pool.close()
    pool.join()