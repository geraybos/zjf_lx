# -*- coding: utf-8 -*-
from . import data_client
from .utils import xdxr_str_to_list, date_preprocess
from .. import markets
from ..models import model_list, Calendar, XDXROffset
from ..query_str_analyzer import analyzer
from ..utils import log


def get_xdxr(market_name, stock_code_list, start_date=None, end_date=None):
    obj = model_list['XDXR']

    ed = Calendar.recent(_date=end_date, forward=False)
    sd = Calendar.recent(_date=start_date, forward=False)

    market = markets[market_name]

    for s_c in stock_code_list:
        err, result = data_client.GetXDXRInfo(market['id'], s_c)
        trans_list = xdxr_str_to_list(xdxr_str=result, start_date=sd['date'], end_date=ed['date'])
        fd = sorted(trans_list, key=lambda x: (x['date']), reverse=True)
        obj.insert_batch(fd)
        log('XDXR', '{} lines of stock:{} inserted'.format(len(fd), s_c))


def calc_xdxr_core(stock_data_list, xdxr_raw_list, category_name):
    xo = XDXROffset('XDXR_offset')

    stock_code = stock_data_list[0]['stock_code']
    xobj = model_list['XDXR_' + category_name]

    # 获取上一次计算中最后一条记录，以便在之后遇到当天进行 xdxr 时计算其 offset
    # 这里不能直接获取 [0] 位置的值，因为在计算历史数据时，可能这支股票并没有历史数据，那么直接获取会报错
    se = list(xobj.desc(xobj.query(stock_code=stock_code), ['date', 'time']))

    trans_list = list()
    i = 0
    sdl = len(stock_data_list)
    offset = 1
    # xdxr_raw_list 最后增加一个超大的截止时间，防止下面的for循环到最后一个时直接跳出导致待计算的数据未计算完成
    xdxr_raw_list.append({'date': Calendar.to('datetime', 20991231)})
    xl = len(xdxr_raw_list)
    xn = xdxr_raw_list[0]
    for xi in range(1, xl):
        x = xn # 本次循环所用的 xdxr 系数
        xn = xdxr_raw_list[xi] # 下次循环要用到的 xdxr 系数
        new_loop = True
        # for si in range(i, sdl):
        #     s = stock_data_list[si]
        #     if xn['date'] <= s['date']:
        #         tmp_o = list(xo.query(stock_code=stock_code, date=s['date']))
        #         if len(tmp_o):
        #             offset = tmp_o[0]['offset']
        #         else:
        #             if len(se):
        #                 # 这里的 len(se) 必须每次算，不能提前算好，因为提前算好的话是不会变的
        #                 # 但 se 是可能由空变为有效数据的
        #                 if isinstance(se, list):
        #                     se = se[0]
        #                 if category_name == 'day':
        #                     # 粒度小于 day 的情况
        #                     offset = round(se['close'] / s['open'], 4)
        #                     xo.insert(stock_code=stock_code,
        #                               date=s['date'],
        #                               market=s['market'],
        #                               offset=offset)
        #                 else:
        #                     raise Exception('please calculate day first to get the xdxr_offset.')
        #             else:
        #                 # 在第一次计算时，没有之前的计算记录，se 是取不到的
        #                 # 一般来说不存在这种情况，但以防万一
        #                 pass
        #         # 一旦遇到进行 xdxr 的日期，就将 se 更新
        #         new_loop = True
        #     elif new_loop and x['date'] < s['date']:
        #         # 在算历史数据即 sdl == 0 的情况下
        #         # 遇到这种情况不能直接break
        #         # 应该把不参与 xdxr 的存入 trans_list
        #         i = si
        #         break
        #
        #     s['open'] = round(offset * s['open'], 4)
        #     s['close'] = round(offset * s['close'], 4)
        #     s['low'] = round(offset * s['low'], 4)
        #     s['high'] = round(offset * s['high'], 4)
        #     trans_list.append(s)
        #     se = s
        for si in range(i, sdl):
            s = stock_data_list[si]
            if s['date'] < x['date']:
                # 直接用现有的 offset 参与计算
                pass
            elif new_loop and s['date'] >= x['date'] and s['date'] < xn['date']:
                # 计算下一轮会用到的 offset
                tmp_o = list(xo.query(stock_code=stock_code, date=x['date']))
                if len(tmp_o):
                    offset = tmp_o[0]['offset']
                else:
                    if len(se):
                        # 这里的 len(se) 必须每次算，不能提前算好，因为提前算好的话是不会变的
                        # 但 se 是可能由空变为有效数据的
                        if isinstance(se, list):
                            se = se[0]
                        if category_name == 'day':
                            # 粒度小于 day 的情况
                            offset = round(se['close'] / s['open'], 4)
                            xo.remove(stock_code=stock_code,
                                      date=x['date'])
                            xo.insert(stock_code=stock_code,
                                      date=x['date'],
                                      market=s['market'],
                                      offset=offset)
                        else:
                            raise Exception('please calculate day first to get the xdxr_offset.')
                    else:
                        # 在第一次计算时，没有之前的计算记录，se 是取不到的
                        # 一般来说不存在这种情况，但以防万一
                        pass
                new_loop = False
            elif s['date'] >= xn['date']:
                i = si
                break

            s['open'] = round(offset * s['open'], 4)
            s['close'] = round(offset * s['close'], 4)
            s['low'] = round(offset * s['low'], 4)
            s['high'] = round(offset * s['high'], 4)
            trans_list.append(s)
            se = s
    return trans_list


def calc_xdxr_offset():
    pass


def calc_xdxr_specified(category_name, stock_code_list, start_date=None, end_date=None):
    kobj = model_list['kline_' + category_name]
    xobj = model_list['XDXR']
    # cobj = model_list['XDXR_' + category_name]
    history_flag = False
    calc_res_list = list()
    for s_c in stock_code_list:
        sd, ed = date_preprocess(start_date, end_date)
        # if start_date is None:
        #     # 起始日期为 None，表示要计算的是历史数据
        #     history_flag = True
        #     start_date = 20000101
        # if end_date is None:
        #     # 结束日期为 None，直接计算到最近的一个交易日
        #     end_date = Calendar.recent()
        sd = Calendar.to(str, sd)
        ed = Calendar.to(str, ed)
        sql = 'date >= {} and date <= {}'.format(sd, ed)
        cond = analyzer(sql)
        stock_data_list = list(kobj.asc(kobj.query(stock_code=s_c, **cond), ['date', 'time']))
        if len(stock_data_list):
            xdxr_all = xobj.query(stock_code=s_c, save=1)
            if xdxr_all.count():
                xdxr_raw_list = list(xobj.asc(xobj.query(stock_code=s_c, save=1, **cond), ['date']))

                # 因为 xdxr 的后复权是用前一次的 xdxr 数据进行计算
                # 所以要在上面筛选的基础上再往前补充一个并且要放在首位
                # 但在计算历史数据时，对于很多老股票，其 k 线数据无法追溯到 xdxr 数据那么久远
                # 在这种情况下不能往前追溯 xdxr 数据，所以使用 history_flag 来区分
                if not history_flag:
                    ncond = analyzer('date <= {}'.format(sd))
                    pre = xobj.desc(xobj.query(stock_code=s_c, save=1, **ncond), ['date'])
                    if pre.count():
                        xdxr_raw_list.insert(0, pre[0])

                result = calc_xdxr_core(stock_data_list, xdxr_raw_list, category_name)
            else:
                result = stock_data_list
            calc_res_list.extend(result)
            print(s_c, 'raw', len(stock_data_list), 'trans', len(result))
        else:
            print(s_c, 'empty')
    print('total', stock_code_list, len(calc_res_list))
    return calc_res_list
