# -*- coding: utf-8 -*-
from collections import deque


def calc_ma(raw_data_list, ma=5):
    lrdl = len(raw_data_list)
    if lrdl < ma:
        return None
    ma_t = 'ma{}'.format(ma)
    ds = deque()
    to = raw_data_list[0]
    for i in range(ma - 1):
        ri = raw_data_list[i]
        if to['date'] < ri['date']:
            to = ri
        ri[ma_t] = ri['close']
        ri['change_r'] = (ri['close'] - to['open']) / to['open']
        ri['sub_new'] = False  # 之后要把这行换掉
        ds.append(ri['close'])

    for i in range(ma, lrdl):
        ri = raw_data_list[i]
        ds.append(ri['close'])
        ri[ma_t] = round(sum(ds) / ma, 4)
        ds.popleft()
    return raw_data_list
