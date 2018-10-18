# -*- coding: utf-8 -*-
from datetime import datetime

from app.models import model_list


class Mark:
    @classmethod
    def update_mark_success(cls,strategy):
        a = datetime.now()
        dit = {'date': a, 'status': 200, 'kline': strategy, 'other': '正常'}
        model_list['kline_data_update_mark'].insert(dit)

    @classmethod
    def update_mark_fail(cls, strategy,messages):
        a = datetime.now()
        dit = {'date': a, 'status': 500, 'kline': strategy, 'other':messages}
        model_list['kline_data_update_mark'].insert(dit)