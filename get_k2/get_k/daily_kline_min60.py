# -*- coding: utf-8 -*-
import traceback
from os.path import abspath, pardir, join
from sys import path

from Mark import Mark
from app import project_dir
from datetime import datetime

from  get_data import get_kline_data
from app.models import Calendar, model_list

path.append(abspath(join(abspath(join(abspath(__file__), pardir)), pardir)))

if __name__ == '__main__':
    # print('min60')
    strategy = 'min60'
    get_kline_data(strategy)
    try:

        Mark.update_mark_success('kline_' + strategy)

    except Exception as e:
        x = '60异常:' + str(e.message) + "追踪：" + str(traceback.format_exc())
        Mark.update_mark_fail(strategy='kline_' + strategy, messages=x)
    exit(0)

