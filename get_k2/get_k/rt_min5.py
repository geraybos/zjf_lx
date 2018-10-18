# -*- coding: utf-8 -*-
import traceback
from os.path import abspath, pardir, join
from sys import path

from datetime import datetime

from app import markets
from app.models import model_list, Calendar
from app.actions import k_realtime_a, get_stock_code_list

import multiprocessing


from utils import is_business

path.append(abspath(join(abspath(join(abspath(__file__), pardir)), pardir)))

def gt_kline(*args):
    """
    get kline data from remote server
    :param args:
    :return:
    """
    print('gt')
    _ = args[0]
    obj = model_list['kline_' + _['category']]
    result=k_realtime_a(market_name=_['market'], category_name=_['category'], stock_code_list=_['stock_code_list'])

    obj.insert_batch(result)


    print(_['stock_code_list'])
def get_kline_data(strategy):
    """
    this function acts on kline
    first get all stock code
    then call the function named get_kline by multiprocessing
    :param strategy:
    :return:
    """
    dd = Calendar.today()
    if not Calendar.in_business(dt=Calendar.today(), day=True):
        exit()
    print('kline_in')
    # t = Calendar.today()
    st=None
    et=None
    t=Calendar.today()
    if Calendar().query(date=t):
        mm = ['sh', 'sz']
        #cc = ['day', 'min60', 'min30', 'min15', 'min5']
        cc = [strategy]
        strategy = 'kline_' + strategy
        s = list()
        for m in mm:
            sl = get_stock_code_list(markets[m])
            num = 50
            aa = (lambda a: map(lambda b: a[b:b + num], range(0, len(a), num)))(sl)
            for a in aa:
                for k in cc:
                    s.append(dict(market=m, category=k, stock_code_list=a, start_date=st, end_date=et))
        # if st == None and et == None:
        # model_list[strategy].remove(date=t)
        # else:
        # sql = analyzer('date >= {} and date <= {}'.format(st, et))
        # model_list[strategy].remove(sql)

        pool=multiprocessing.Pool(processes=10)
        for i in s:
            pool.apply_async(gt_kline,(i,))
        pool.close()
        pool.join()
        # for i in s:
        #     gt_kline(i)
        # model_list[strategy].remove(volume=0)
        print('-----------------'+str())
        print('kline_done')
 #修改备注：  多了一个for循环，注释掉


path.append(abspath(join(abspath(join(abspath(__file__), pardir)), pardir)))

if __name__ == '__main__':
    # if is_ok_now_decimal_time()==False:
    #     exit(0)
    strategy = 'min5'



    try:
        get_kline_data(strategy)
        dit = {'date': datetime.now(), 'status': 200, 'kline': strategy, 'other': '正常'}
        model_list['kline_data_update_mark'].insert(dit)

    except Exception as e:
        a = datetime.now()
        x = '异常:' + str(e.message) + "追踪：" + str(traceback.format_exc())
        dit = {'date': a, 'status': 500, 'kline': strategy, 'other': x}
        model_list['kline_data_update_mark'].insert(dit)
    exit(0)