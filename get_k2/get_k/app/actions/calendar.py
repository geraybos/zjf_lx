# -*- coding: utf-8 -*-

import tushare as ts

from ..models import Calendar


def get_trade_cal(all=False):
    """
    该方法用于获取所有中国交易日
    :param all:all 为 False 则只获取当年的
    :return:
    """
    c = ts.trade_cal()
    lc = len(c)
    if all:
        cal_list = Calendar.trans_data(c, lc)
    else:
        cal_list = Calendar.trans_data(c[-365:], lc)
    Calendar().insert_batch(cal_list)
