# -*- coding: utf-8 -*-

from os.path import abspath, pardir, join
from sys import path

from app import markets, cpus
from app.actions import k_history_a
from app.query_str_analyzer import analyzer

path.append(abspath(join(abspath(join(abspath(__file__), pardir)), pardir)))

from multiprocessing import freeze_support, Pool

from app.actions import get_stock_code_list
from app.models import Calendar, model_list


def gt(*args):
    _ = args[0]
    k_history_a(market_name=_['market'], category_name=_['category'], stock_code_list=_['stock_code_list'],
                start_date=_['start_date'], end_date=_['end_date'])
    print(_, 'done')


if __name__ == '__main__':
    print('in')
    t = Calendar.today()
    st=20160101
    et=None
    if Calendar().query(date=t):
        mm = [ 'sz', 'sh']
        # cc = ['day', 'min60', 'min30']
        cc = ['min5']
        s = list()
        for m in mm:
            sl = get_stock_code_list(markets[m])
            num = 10
            aa = (lambda a: map(lambda b: a[b:b + num], range(0, len(a), num)))(sl)
            for a in aa:
                for k in cc:
                    s.append(dict(market=m, category=k, stock_code_list=a, start_date=st, end_date=et))
        sql = analyzer('date <= {} and date >= {}'.format(et, st))
        print(sql)
        for c in cc:
            print('get kline_{}'.format(c))
            model_list['kline_'+c].remove(analyzer('date <= {} and date >= {}'.format(et, st)))

        pool = Pool(10)
        pool.map(gt, s)

