# -*- coding: utf-8 -*-
from math import ceil

from . import data_client
from .utils import row_str_to_list, split_start, sort_key
from .. import index_dict, categories, unit_conversion, markets
from ..models import model_list, Calendar

postfix = {
    'index_day': '',
    'index_week': '_week',
    'index_month': '_month',
    'index_min5': '_m5',
    'index_min15': '_m15',
    'index_min30': '_m30',
    'index_min60': '_m60',
}


def get_index_core(market, category_name, stock_code_list, num=None, start_date=None, end_date=None):
    category_id = categories[category_name]

    index_data_list = list()

    sd = Calendar.recent(_date=start_date, forward=False)
    ed = Calendar.recent(_date=end_date, forward=False)
    # 这里不能用 today，因为有可能是在非交易日跑的程序，那么 Calenday 表里是没有对应的序号的
    # 而且也不能设置参数 forawrd=False，因为在诸如周末等时间跑程序时，截止时间会取到下周的交易日
    td = Calendar.recent()
    if ed['date'] > td['date']:
        ed = td

    if num is None:
        # 对于不同单位的数据，需要换算数量，以 1day 为单位基准
        unit = category_name.split('_', 1)[-1]
        num = int(ceil((ed['num'] - sd['num'] + 1) * unit_conversion[unit]))

    s = split_start(category_name)

    for s_c in stock_code_list:
        start = 0
        trans_list = list()
        sub_num = num

        while True:
            if sub_num >= 800:
                end = 800
                sub_num -= 800
            else:
                end = sub_num + 1
            sc = '{}{}'.format(s_c, postfix[category_name])
            nflag = True
            index_count = 0
            result = None
            i=0
            while i<50:
                print(i)
                err, index_count, result = data_client.GetIndexBars(category_id, market['id'], sc, start, end)
                i = i + 1
                if len(result)>0:
                    break

            start += 800
            trans_list.extend(
                row_str_to_list(
                    market=market,
                    category_name=category_name,
                    stock_code=s_c,
                    row_str=result,
                    start_date=sd['date'],
                    end_date=ed['date']
                ))
            if index_count < 800:
                break
        tl = len(trans_list)
        if num and num <= tl:
            e = num
        else:
            e = tl
        if e:
            tl = sorted(trans_list, key=sort_key(trans_list[0]), reverse=True)[s:s + e]
            index_data_list.extend(tl)
    return index_data_list


def get_history(market_name, category_name, stock_code_list, num=None, start_date=None, end_date=None):
    market = markets[market_name]
    if not category_name.startswith('index_'):
        category_name = 'index_' + category_name
    obj = model_list[category_name]
    fd = get_index_core(market, category_name, stock_code_list, num, start_date, end_date)
    fd_l = len(fd)
    if fd_l:
        obj.insert_batch(fd)
        print(fd_l)
    else:
        print('0000000')


def get_specified(market_name, category_name, stock_code_list, num=None, start_date=None, end_date=None):
    market = markets[market_name]
    if not category_name.startswith('index_'):
        category_name = 'index_' + category_name
    return get_index_core(market, category_name, stock_code_list, num, start_date, end_date)


def get_realtime(market_name, category_name, stock_code_list):
    return get_specified(market_name, category_name, stock_code_list, num=1)
