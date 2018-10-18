# -*- coding: utf-8 -*-

from os.path import abspath, pardir, join
from sys import path

from datetime import datetime

from app import markets, project_dir
from app.actions import k_specified_ex, k_history_ex
from app.query_str_analyzer import analyzer

path.append(abspath(join(abspath(join(abspath(__file__), pardir)), pardir)))

from multiprocessing import freeze_support, Pool


from app.models import Calendar, model_list


def gt_ex(*args):
    _ = args[0]
    obj = model_list['{}_kline_{}'.format(_['market'], _['category'])]
    obj.insert_batch(k_specified_ex(market_name=_['market'], category_name=_['category'], stock_code_list=_['stock_code_list'],
                  start_date=_['start_date'], end_date=_['end_date']))
    # k_specified_a(market_name=_['market'], category_name=_['category'], stock_code_list=_['stock_code_list'],
    #                             start_date=_['start_date'], end_date=_['end_date'])
    # k_history_a(market_name=_['market'], category_name=_['category'], stock_code_list=_['stock_code_list'],
    #               start_date=_['start_date'], end_date=_['end_date'])
    # obj.insert_batch(k_realtime_a(market_name=_['market'], category_name=_['category'], stock_code_list=_['stock_code_list']))
    print(_['stock_code_list'])


if __name__ == '__main__':
    print('in')
    t = Calendar.today()
    if Calendar().query(date=t):
        mm = ['usa']
        cc = ['day', 'min60', 'min30', 'min15', 'min5']
        # cc = ['min5']
        # cc = ['day']
        s = list()
        # sd = Calendar.today()
        sd = analyzer('date = {}'.format(20170101))['date']
        ed = Calendar.today()
        for m in mm:
            pf = r'{}/{}'.format(project_dir, '{}.txt'.format(m))
            with open(pf) as f:
                sl = f.read().split('\n')
            num = 30
            aa = (lambda a: map(lambda b: a[b:b + num], range(0, len(a), num)))(sl)
            for a in aa:
                for k in cc:
                    s.append(dict(market=m, category=k, stock_code_list=a, start_date=sd, end_date=ed))
        dql = analyzer('date >= {} and date <= {}'.format(Calendar.to(str, Calendar.calc(sd, -1)['date']), Calendar.to(str, Calendar.calc(ed, -1)['date'])))

        for m in mm:
            for c in cc:
                model_list['{}_kline_{}'.format(m, c)].remove(dql)
        # exit()
        print(s)
        st = datetime.now()
        freeze_support()
        pool = Pool(7)
        pool.map(gt_ex, s)
        pool.close()
        pool.join()
        # for i in s:
        #     gt_ex(i)
        print('{} {}'.format(st, datetime.now()))



