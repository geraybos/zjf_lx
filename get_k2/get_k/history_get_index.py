# -*- coding: utf-8 -*-

from os.path import abspath, pardir, join
from sys import path

from app import markets, cpus, index_dict
from app.actions import i_history_a
from app.query_str_analyzer import analyzer

path.append(abspath(join(abspath(join(abspath(__file__), pardir)), pardir)))

from multiprocessing import freeze_support, Pool

from app.actions import get_stock_code_list
from app.models import Calendar, model_list


def gt(*args):
    _ = args[0]
    i_history_a(market_name=_['market'], category_name=_['category'],
              start_date=_['start_date'], end_date=_['end_date'], stock_code_list=_['stock_code_list'])
    print(args, 'ok')
if __name__ == '__main__':
    print('in')
    t = Calendar.today()
    st = 20180604
    et = None
    if Calendar().query(date=t):
        mm = ['sh', 'sz']
        cc = ['day', 'min60', 'min30', 'min15', 'min5']
        cc = ['min5']
        s = list()
        for m in mm:
            sl = index_dict[m]
            num = 10
            aa = (lambda a: map(lambda b: a[b:b + num], range(0, len(a), num)))(sl)
            for k in cc:
                for a in aa:
                    s.append(dict(market=m,
                              category=k,
                              stock_code_list=a,
                              start_date=st,
                              end_date=et))
        sql = analyzer('date <= {} and date >= {}'.format(et, st))
        for c in cc:
            model_list['index_{}'.format(c)].remove(sql)
        freeze_support()
        pool = Pool(cpus)
        pool.map(gt, s)
        pool.close()
        pool.join()
        # for ss in s:
        #     gt(ss)
