# -*- coding: utf-8 -*-
from os.path import abspath, pardir, join
from sys import path

from datetime import datetime

from app.models import Calendar, model_list
from get_data import get_index_data


path.append(abspath(join(abspath(join(abspath(__file__), pardir)), pardir)))

if __name__ == '__main__':

    if not Calendar.in_business(dt=Calendar.today(), day=True):
        exit()
    strategy='min5'  
    get_index_data(strategy)
    # a = datetime(2018,1,16,9,55)
    a = datetime.now()
    dit = {'date': a, 'status': 200, 'kline': 'index_{}'.format(strategy), 'other': '正常'}
    model_list['kline_data_update_mark'].insert(dit)
    exit()
