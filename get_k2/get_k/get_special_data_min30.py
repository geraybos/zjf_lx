# -*- coding: utf-8 -*-
import traceback
from datetime import datetime

from Mark import Mark
from app.models import Calendar, model_list
from get_special_data import get_kline_data, get_his, get_volumes, get_data

if __name__ == '__main__':


    strategy = 'min30'
    try:
        (get_data(strategy))
        Mark.update_mark_success('kline_' + strategy)


    except Exception as e:
        # a = datetime.now()
        # x = '异常:' + str(e.message) + "追踪：" + str(traceback.format_exc())
        x = '合并30异常:' + str(e.message) + "追踪：" + str(traceback.format_exc())
        Mark.update_mark_fail(strategy='kline_' + strategy, messages=x)
exit(0)



