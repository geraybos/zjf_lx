# -*- coding: utf-8 -*-
import traceback
from os.path import abspath, pardir, join
from sys import path
from datetime import datetime

from Mark import Mark
from get_data import get_kline_data
from app.models import Calendar, model_list
from app import project_dir

path.append(abspath(join(abspath(join(abspath(__file__), pardir)), pardir)))

if __name__ == '__main__':
    # print('min5')

    strategy = 'min5'

    try:
        get_kline_data(strategy)
        print('1')


        Mark.update_mark_success('kline_' + strategy)


    except Exception as e:
        # a = datetime.now()
        # x = '异常:' + str(e.message) + "追踪：" + str(traceback.format_exc())
        # file_log(strategy, 'time:' + str(datetime.now()) + '\n' + 'op:exception')
        x = '异常:' + str(e.message) + "追踪：" + str(traceback.format_exc())
        Mark.update_mark_fail(strategy='kline_' + strategy, messages=x)
    exit(0)

