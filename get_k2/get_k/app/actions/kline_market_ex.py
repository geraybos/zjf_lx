# -*- coding: utf-8 -*-
from math import ceil

from . import data_client_ex
from .utils import row_str_to_list, split_start, sort_key
from .. import project_dir, categories, unit_conversion, markets
from ..models import Calendar, model_list


def get_kline_core(market, category_name, stock_code_list, num=None, start_date=None, end_date=None):
    category_id = categories[category_name]

    tradex_data = list()

    sd = Calendar.recent(_date=start_date, forward=False)
    ed = Calendar.recent(_date=end_date, forward=False)
    # 这里不能用 today，因为有可能是在非交易日跑的程序，那么 Calenday 表里是没有对应的序号的# 而且也不能设置参数 forawrd=False，因为在诸如周末等时间跑程序时，截止时间会取到下周的交易日
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
            if sub_num >= 700:
                end = 700
                sub_num -= 700
            else:
                end = sub_num + 1
            nflag = True
            count = 0
            result = None
            while nflag:
                err, count, result = data_client_ex.GetInstrumentBars(category_id, market['id'], s_c, start, end)
                nflag = 0 == len(result)
            start += 700
            trans_list.extend(
                row_str_to_list(
                    market=market,
                    category_name=category_name,
                    stock_code=s_c,
                    row_str=result,
                    start_date=sd['date'],
                    end_date=ed['date']
                ))
            if count < 700:
                break
        tl = len(trans_list)
        if num and num <= tl:
            e = num
        else:
            e = tl
        if e:
            tl = sorted(trans_list, key=sort_key(trans_list[0]), reverse=True)[s:s + e]
            tradex_data.extend(tl)
    return tradex_data


def get_history(market_name, category_name, stock_code_list, num=None, start_date=None, end_date=None):
    market = markets[market_name]
    if stock_code_list is None:
        pf = r'{}/{}'.format(project_dir, '{}.txt'.format(market_name))
        with open(pf) as f:
            stock_code_list = f.read().split('\n')
    if not category_name.startswith('kline_'):
        category_name = 'kline_' + category_name
    obj = model_list['{}_{}'.format(market_name, category_name)]
    for s_c in stock_code_list:
        fd = get_kline_core(market, category_name, [s_c], num, start_date, end_date)
        fd_l = len(fd)
        if fd_l:
            obj.insert_batch(fd)
            print(fd_l, s_c)
        else:
            print('0000000', s_c)


def get_specified(market_name, category_name, stock_code_list=None, num=None, start_date=None, end_date=None):
    market = markets[market_name]
    if stock_code_list is None:
        pf = r'{}/{}'.format(project_dir, '{}.txt'.format(market_name))
        with open(pf) as f:
            stock_code_list = f.read().split('\n')
    if not category_name.startswith('kline_'):
        category_name = 'kline_' + category_name
    return get_kline_core(market, category_name, stock_code_list, num, start_date, end_date)


def get_realtime(market_name, category_name):
    return get_specified(market_name, category_name, num=1)
