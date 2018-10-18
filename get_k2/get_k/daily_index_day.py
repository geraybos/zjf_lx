# -*- coding: utf-8 -*-
import traceback
from os.path import abspath, pardir, join
from sys import path

from datetime import datetime

from Mark import Mark
from app.models import Calendar, model_list
from get_data import get_index_data

path.append(abspath(join(abspath(join(abspath(__file__), pardir)), pardir)))

if __name__ == '__main__':
    if not Calendar.in_business(dt=Calendar.today(), day=True):
        exit()

    strategy = 'day'
    op = 'index_'
    try:
        get_index_data(strategy)
        # a = datetime.now()
        # dit = {'date': a, 'status': 200, 'kline': 'index_{}'.format(strategy), 'other': '正常'}
        # model_list['kline_data_update_mark'].insert(dit)
        Mark.update_mark_success(op + strategy)
        exit()
    except Exception as e:
        x = '合并30异常:' + str(e.message) + "追踪：" + str(traceback.format_exc())
        Mark.update_mark_fail(strategy=op + strategy, messages=x)
        exit(1)
