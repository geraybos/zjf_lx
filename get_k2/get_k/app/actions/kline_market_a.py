# -*- coding: utf-8 -*-
from math import ceil
from .. import TradeX
from app.models import Tick
from app.query_str_analyzer import analyzer
from . import data_client
from .utils import split_start, row_str_to_list, sort_key, get_stock_code_list, date_preprocess
from .. import categories, markets, unit_conversion
from ..models import model_list, Calendar
market_a_server= [
      "113.105.73.88",
      "121.14.110.194",
      "119.147.171.206",
      "61.152.249.56",
      "114.80.80.222",
      "218.108.50.178",
      "61.49.50.190",
      "61.135.142.88",
      "221.194.181.176",
      "117.184.140.156"
   ]

def get_kline_core(market, category_name, stock_code_list, num=None, start_date=None, end_date=None):
    category_id = categories[category_name]

    kline_data_list = list()

    sd = Calendar.recent(_date=start_date, forward=False)
    ed = Calendar.recent(_date=end_date, forward=False)
    # 这里不能用 today，因为有可能是在非交易日跑的程序，那么 Calenday 表里是没有对应的序号的# 而且也不能设置参数 forawrd=False，因为在诸如周末等时间跑程序时，截止时间会取到下周的交易日
    td = Calendar.recent()
    if ed['date'] > td['date']:
        ed = td

    if num is None:
        # 对于不同单位的数据，需要换算数量，以 1day 为单位基准
        unit = category_name.split('_', 1)[-1]
        num = int(ceil((ed['num'] - sd['num'] + 1) * unit_conversion[unit]))  # 这里必须 +1 否则起始的那天会被切掉
    s = split_start(category_name)
    for s_c in stock_code_list:
        start = 0
        trans_list = list()
        sub_num = num

        while True:
            if sub_num >= 800:
                # 取指定数目，但数量大于等于 800 的，一次只能取 800 条数据
                end = 800
                sub_num -= 800
            else:
                # 取指定数目，且数量小于 800 的，直接取指定条数 + 1，因为最新一条往往无用，会被切掉
                end = sub_num + 1
            nflag = True
            result = None
            kline_count = 0
            # i=0
            print(s_c)
            err, kline_count, result =data_client.GetSecurityBars(category_id, market['id'], s_c, start, end)
            # if len(result) > 0 :
            #         break
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

            if kline_count < 800:
                break

        # s 会返回 0 或者 1 表示：
        # 一支股票的所有数据都放入 trans_list，然后去掉第一行，因为很可能是在交易进行中，所以第一条数据无意义
        tl = len(trans_list)
        if num and num <= tl:
            e = num
        else:
            e = tl

        if e:
            tl = sorted(trans_list, key=sort_key(trans_list[0]), reverse=True)[s:s + e]
            kline_data_list.extend(tl)
    return kline_data_list


def get_history(market_name, category_name, stock_code_list, num=None, start_date=None, end_date=None):
    market = markets[market_name]
    if not category_name.startswith('kline_'):
        category_name = 'kline_' + category_name
    obj = model_list[category_name]
    fd = get_kline_core(market, category_name, stock_code_list, num, start_date, end_date)
    fd_l = len(fd)
    if fd_l:
        obj.insert_batch(fd)
        print(category_name, fd_l, stock_code_list)
    else:
        print('0000000')
    return


def get_specified(market_name, category_name, stock_code_list=None, num=None, start_date=None, end_date=None):
    market = markets[market_name]
    if not category_name.startswith('kline_'):
        category_name = 'kline_' + category_name
    if stock_code_list is None:
        stock_code_list = get_stock_code_list(market)
    return get_kline_core(market, category_name, stock_code_list, num, start_date, end_date)


def get_realtime(market_name, category_name, stock_code_list=None):
    return get_specified(market_name, category_name, stock_code_list, num=1)


def get_history_tick(market_name, stock_code, start_date=None, end_date=None, his=False):
    sd, ed = date_preprocess(start_date, end_date)
    days = list(Calendar().query(
        analyzer(
            'date >= {} and date <= {}'.format(Calendar.to(str, Calendar.recent(sd)),
                                               Calendar.to(str, Calendar.recent(ed))))))
    tick_data_list = list()
    market = markets[market_name]
    for day in days:
        d = day['date']
        loop = True
        start = 0
        while loop:
            if his:
                err, count, result = TradeX.TdxHq_Connect('61.152.249.56',7709).GetHistoryTransactionData(market['id'], stock_code, start, 2000,
                                                                           Calendar.to(int, d))
            else:
                err, count, result = TradeX.TdxHq_Connect('61.152.249.56',7709).GetTransactionData(market['id'], stock_code, start, 2000)
            # print(result.decode('gbk'))
            row = result.split('\n')
            tick_data_list.extend(Tick.trans_data(stock_code, market_name, d, row))
            start += 2000
            loop = count == 2000

    # obj.insert_batch(tick_data_list)
    print('{} done: {}'.format(stock_code, len(tick_data_list)))
    return tick_data_list


def generate_min_by_tick(stock_code, start_date, end_date):
    sd, ed = date_preprocess(start_date, end_date)
    days = list(Calendar().query(date={'$gte': sd, '$lte': ed}))
    tobj = model_list['kline_tick']
    min_data = list()
    for day in days:
        a = tobj.to_min(stock_code, day['date'])
        la = len(a)
        if la == 0:
            continue
        ma_t = 1
        a[0]['ma'] = a[0]['close']
        for i in range(1, la):
            ma_tt = ma_t + 1
            a[i]['ma'] = round((a[i - 1]['ma'] * ma_t + a[i]['close']) / ma_tt, 4)
            ma_t = ma_tt
        min_data.extend(a)
    mobj = model_list['kline_min1']
    mobj.insert_batch(min_data)
    print('{} done'.format(stock_code))
