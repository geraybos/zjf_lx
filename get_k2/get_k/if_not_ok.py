# -*- coding: utf-8 -*-
import datetime as dt

from app.models import model_list

strategy="kline_min5"
# strategy="index_min5"

dit = {'date': dt.datetime(2018,6,22,9,56), 'status': 200, 'kline': strategy, 'other': '正常'}
model_list['kline_data_update_mark'].insert(dit)