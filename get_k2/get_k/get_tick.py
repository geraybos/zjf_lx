# -*- coding: utf-8 -*-

# from app.actions import k_history_a
#
# c = 'kline_day'
# k_history_a('sz', c, ['000001'], start_date=19900101)
# print('ok')

# from app.actions import get_xdxr, calc_xdxr_specified
# # get_xdxr('sz', ['000001'], start_date=19900101)
# calc_xdxr_specified('min30', ['600000'])

# default date: 20120130
# from app.actions import f_zybk_ttm_a
# f_zybk_ttm_a(start_date=20120130)
#
# from app.actions import f_zz_ttm_a
# f_zz_ttm_a(p_type='zz', start_date=20120130)

# from app.actions import f_zjh_ttm_a
# f_zjh_ttm_a(p_type='zjh', start_date=20120130)

# from app.actions import get_trade_cal
#
# get_trade_cal(True)

from multiprocessing import freeze_support, Pool

from app import markets, cpus
from app.actions import k_tick_a, get_stock_code_list
from app.models import model_list, Calendar
from app.query_str_analyzer import analyzer
import sys


def gt(_):
    n = len(_['stock_code_list'])
    obj = model_list['kline_tick']
    for i in range(n):
        s_c=_['stock_code_list'][i]
        print(s_c)
        obj.insert_batch(k_tick_a(_['market'], s_c, _['start_date'], _['end_date'], his=_['his']))
    # k_tick_a('sh', '600000', 20150101)


if __name__ == '__main__':
    his = True if len(sys.argv) > 1 and sys.argv[1] == 'his' else False
    print('mod: {}'.format(his))
    if not  Calendar.in_business(dt=Calendar.today(), day=True):
        if his:
            pass
        else:
            exit()
    # sd = 20170101 if his else None
    sd = 20180608
    ed = None
    s = list()
    done = True
    dbsc = []
    flag = False
    while done:
        try:
            for m in ['sh', 'sz']:
                sl = get_stock_code_list(markets[m])
                dbsc = [a for a in list(model_list['kline_tick'].query(analyzer('date >= {} and date <= {}'.format(sd, ed))).distinct('stock_code')) if (m=='sz' and int(a) < 600000) or (m=='sh' and int(a) >= 600000)]
                sl = list(set(sl).difference(set(dbsc)))
                num = 3
                aa = (lambda a: map(lambda b: a[b:b + num], range(0, len(a), num)))(sl)
                print('aa ok')
                for a in aa:
                    s.append(dict(market=m, stock_code_list=a, start_date=sd, end_date=ed, his=his))
            print('s is ok, {}'.format(s))
            cpus=30
            freeze_support()
            pool = Pool(cpus)
            pool.map(gt, s)
            pool.close()
            pool.join()
            # for i in s:
            #     gt(i)
        except Exception as e:
            print(e.message.decode('gbk'))
            flag = True
            continue
        else:
            done = False


# from app.actions import calendar
#
# calendar.get_trade_cal(all=True)