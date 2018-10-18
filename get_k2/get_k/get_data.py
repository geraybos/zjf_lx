# -*- coding: utf-8 -*-
import multiprocessing
import subprocess
import time
from datetime import datetime
from multiprocessing import freeze_support, Pool

import gc

import os

from Mark import Mark
from app import markets, cpus, index_dict
from app import project_dir
from app.actions import get_stock_code_list
from app.actions import i_specified_a
from app.actions import k_specified_a
from app.models import model_list, Calendar
from utils import change_status, get_min5_time, get_min60_time, get_min30_time, get_min15_time, get_day_time


def gt_kline(*args):
    # print('gt')
    _ = args[0]
    obj = model_list['kline_' + _['category']]
    t = Calendar.today()
    data = None

    # print(os.getpid())
    try:
        data = k_specified_a(market_name=_['market'], category_name=_['category'],
                             stock_code_list=_['stock_code_list'],
                             start_date=_['start_date'], end_date=_['end_date'])
    except Exception as e:
        print(e)
    # if _['category'] == 'min5':
    #     if datetime.now() <= n and datetime.now() >= n2:
    #         obj2 = model_list['tmp_kline_min5']
    #         obj2.insert_batch(data)
    #         print('ojb2 ok')
            # Mark.update_mark_success('tmp_kline_min5')

    # for sc in _['stock_code_list']:
    #     obj.remove(date=t, stock_code=sc)
    obj.insert_batch(data)

    # gc.collect()
    # print('____')
    print(os.getpid(),_['stock_code_list'])


    return 0


def gt_index(*args):
    _ = args[0]
    obj = model_list['index_' + _['category']]

    a = obj.insert_batch(
        i_specified_a(market_name=_['market'], category_name=_['category'], stock_code_list=_['stock_code_list'],
                      start_date=_['start_date'], end_date=_['end_date']))
    print(a)

    return 0
    # print(a)

# def file_log(strategy,content):
#     f= open('F:\get_k2\get_k\kline_'+strategy+'_log.txt', 'a')
#     f.write(content+'\n')
#     f.close()
#     return
def get_kline_data(strategy):
    # print('kline_in')
    # file_log(strategy,'time:'+str(datetime.now())+'\n'+'op:start')
    # t = Calendar.today()
    print('step into')
    t = Calendar.today()
    # 111=555
    if Calendar().query(date=t):
        mm = ['sh', 'sz']
        # cc = ['day', 'min60', 'min30', 'min15', 'min5']
        cc = [strategy]
        strategy = 'kline_' + strategy
        s = list()
        # ss = datetime.now()
        # print(ss)
        for m in mm:
            sl = get_stock_code_list(markets[m])
            num = 10
            aa = (lambda a: map(lambda b: a[b:b + num], range(0, len(a), num)))(sl)
            print(aa)
            for a in aa:
                for k in cc:
                    s.append(dict(market=m, category=k, stock_code_list=a, start_date=None, end_date=None))
        # e = datetime.now()
        # print(e)
        # file_log(strategy, 'time:' + str(datetime.now()) + '\n' + 'op:get stock_code')
        print('step getstocks')
        model_list[strategy].remove(date=t)
        print('remove over')
        # file_log(strategy, 'time:' + str(datetime.now()) + '\n' + 'op:remove today')
        # f = datetime.now()
        # print(f)

        pool = Pool(10)
        pool.map(gt_kline, s)
        # for i in s:
        #     gt_kline(i)



        # pool.close()
        # pool.join()

        # print('s=',s)
        # p = multiprocessing.Process(target=gt_kline, args=s)
        # p.start()
        # p.join(timeout=300)
        # for i in s:
        #     gt_kline(i)
        # model_list[strategy].remove(volume=0)
        # file_log(strategy, 'time:' + str(datetime.now()) + '\n' + 'op:complate')
        print('kline_done')
        return 0


# 修改备注：  多了一个for循环，注释掉

def get_index_data(strategy):
    print('index_in')
    t = Calendar.today()
    if Calendar().query(date=t):
        mm = ['sh', 'sz']
        cc = [strategy]
        strategy = 'index_' + strategy
        s = list()

        for m in mm:
            sl = index_dict[m]
            num = 10
            aa = (lambda a: map(lambda b: a[b:b + num], range(0, len(a), num)))(sl)
            for a in aa:
                for k in cc:
                    s.append(dict(market=m, category=k, stock_code_list=a, start_date=None, end_date=None))
        print('item')
        model_list[strategy].remove(date=t)
        print(s)

        pool = Pool(7)
        pool.map(gt_index, s)



        # p=multiprocessing.Process(target=gt_index,args=s)
        # p.start()
        # p.join(timeout=60)
        print('index_done')


def get_data_allocate(strategy, data_type):
    dd = Calendar.today()
    a = Calendar.in_business(dd, day=True)
    if (a == False):
        print('非工作日！')
        exit(0)
    t1 = time.clock()
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    command = "python {}\daily_{}_{}.py".format(project_dir, data_type, strategy)
    list = []
    if (strategy == 'min5'):
        list = get_min5_time()
    if (strategy == 'min15'):
        list = get_min15_time()
    if (strategy == 'min30'):
        list = get_min30_time()
    if (strategy == 'min60'):
        list = get_min60_time()
    if (strategy == 'day'):
        list = get_day_time()
    print (strategy)

    while True:
        # if in_business(datetime.now(), strategy, True):
        x = datetime.now().hour * 60 + datetime.now().minute
        # print ( datetime.now().hour,datetime.now().minute)
        # print(x)
        # if(x>list[-1]):

        if (x > list[-1]):
            print(list[-1])
            print('收盘！')
            exit(0);
        if (x == 11 * 60 + 45):
            print('上午结束')
            exit(0);
        if (x in list):

            print ('finded')
            t1 = time.clock()

            subprocess.call(command, shell=True)
            t3 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print (t3)
            dit = {'date': t3, 'status': 1, 'kline': strategy, 'other': ''}
            model_list['kline_data_update_mark'].insert(dit)
            t2 = time.clock()
            a = (change_status(strategy)['time']) - ((t2 - t1) / 60)
            print(a)
            if (a > 0):
                time.sleep(a * 60)
                print('睡眠结束')
        else:
            print('finding:')
            time.sleep(10)


def get_kline_data_allocate(strategy):
    try:
        get_data_allocate(strategy, 'kline')

    except Exception:
        print ('异常')
        exit(0)


def get_index_data_allocate(strategy):
    get_data_allocate(strategy, 'index')
