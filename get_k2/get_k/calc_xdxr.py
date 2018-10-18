# -*- coding: utf-8 -*-
import traceback
from os.path import abspath, pardir, join
from sys import path

from datetime import datetime

from Mark import Mark
from app import markets, cpus
from app.actions import calc_xdxr_specified, get_stock_code_list
from app.query_str_analyzer import analyzer


path.append(abspath(join(abspath(join(abspath(__file__), pardir)), pardir)))

from multiprocessing import freeze_support, Pool

from app.models import Calendar, model_list


def gt(*args):
    _ = args[0]
    obj = model_list['XDXR_' + _['category']]
    obj.insert_batch(
        calc_xdxr_specified(stock_code_list=_['stock_code_list'], category_name=_['category'],
                            start_date=_['start_date'],
                            end_date=_['end_date']))
    # calc_xdxr_specified(stock_code_list=[600015], category_name=_['category'], start_date=_['start_date'],
    #                     end_date=_['end_date'])


if __name__ == '__main__':
    d=Calendar.today()
    if not Calendar.in_business(dt=d, day=True):
        print('not_ok')
        exit()
    print('0000')
    strategy = 'XDXR_day'  # day_XDXR   ���ܸĲ��ܸĲ��ܸ�Ӵ
    try:
        print('in')
        mm = ['sz', 'sh']
        s = list()
        sd = None
        ed = None
        for m in mm:
            sl = get_stock_code_list(markets[m])
            num = 10
            aa = (lambda a: map(lambda b: a[b:b + num], range(0, len(a), num)))(sl)
            for a in aa:
                s.append(dict(market=m, stock_code_list=a, start_date=sd, end_date=ed, category='day'))
        model_list['XDXR_day'].remove(analyzer('date >= {} and date <= {}'.format(sd, ed)))
        freeze_support()
        pool = Pool(cpus)
        pool.map(gt, s)
        pool.close()
        pool.join()
        Mark.update_mark_success(strategy)
        exit()
    except Exception as e:
        x = '合并30异常:' + str(e.message) + "追踪：" + str(traceback.format_exc())

        Mark.update_mark_fail(strategy=strategy, messages=x)
        exit(1)



