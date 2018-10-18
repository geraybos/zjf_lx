# -*- coding: utf-8 -*-
import traceback
from os.path import abspath, pardir, join
from sys import path

from datetime import datetime

from Mark import Mark
from app.models import model_list
from get_data import get_kline_data


path.append(abspath(join(abspath(join(abspath(__file__), pardir)), pardir)))

if __name__ == '__main__':
    strategy = 'min5'
    try:
        get_kline_data(strategy)
        Mark.update_mark_success('kline_' + strategy)

    except Exception as e:
        # a = datetime.now()
        # x = '异常:' + str(e.message) + "追踪：" + str(traceback.format_exc())
        # dit = {'date': a, 'status': 500, 'kline': strategy, 'other': x}
        # model_list['kline_data_update_mark'].insert(dit)
        x = '合并30异常:' + str(e.message) + "追踪：" + str(traceback.format_exc())
        Mark.update_mark_fail(strategy='kline_' + strategy, messages=x)
    exit()