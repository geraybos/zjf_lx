# -*- coding: utf-8 -*-
from datetime import datetime
import pandas as pd
from app.models import model_list, Calendar
from app.query_str_analyzer import analyzer


class Check_Data:
    @classmethod
    def number_of_branches(cls, strategy):
        if strategy[-3:] == 'day':
            return 1

        elif strategy[-2:] == '30':
            return 8
        elif strategy[-2:] == '15':
            return 16
        elif strategy[-1] == '5':
            return 48
        else:
            return 4

    @classmethod
    def check_kline(cls, strategy='kline_min5'):
        dt = Calendar.today()
        # pre_date = Calendar.calc(dt, -10)

        dt = Calendar.calc(dt, -1)['date']
        # sql = analyzer('date = {}'.format(str(dt.year * 10000 + dt.month * 100 + dt.day)))
        # model_list['check_data'].remove(sql)
        # print(pre_date)
        sql = analyzer("date >= {} and date <= {}".format(str(20180111), str(dt.year * 10000 + dt.month * 100 + dt.day)))
        print("____________________" + strategy)
        print(sql)
        print('稍等几秒')
        cursor = model_list[strategy].query(sql)
        print(cursor)
        all_count = cursor.count()
        print(all_count)
        day_count = cls.number_of_branches(strategy)
        print(day_count)
        dic = {'date': dt, 'strategy': strategy, 'all_count': all_count, 'day_count': day_count,
               'result': all_count % day_count == 0}
        print('insert')
        model_list['check_data'].insert(dic)
        if all_count % day_count == 0:
            return strategy + ' is true'
            print("____________________")
        else:
            return strategy + "有问题"

    @classmethod
    def self_check(cls, date=Calendar.today()):
        date = Calendar.calc(date=date, offset=-1)['date']
        sql = analyzer('date = {}'.format(date.year * 10000 + date.month * 100 + date.day))
        print(sql)

        result = list(model_list['check_data'].query(sql))
        data = pd.DataFrame(result)
        all_count = list(data['all_count'])
        for i in range(0,len(all_count)-1):
            if i != 4:
                if all_count[i]%all_count[i+1] != 0:
                    print(all_count[i],all_count[i+1])
                    return False

        print(data)
        return True

dt = Calendar.today()
# pre_date = Calendar.calc(dt, -10)
dt = Calendar.calc(dt, -1)['date']
sql = analyzer('date = {}'.format(str(dt.year * 10000 + dt.month * 100 + dt.day)))
model_list['check_data'].remove(sql)
print(Check_Data.check_kline('kline_min5'))
print(Check_Data.check_kline('kline_min15'))
print(Check_Data.check_kline('kline_min30'))
print(Check_Data.check_kline('kline_min60'))
print(Check_Data.check_kline('kline_day'))
print(Check_Data.check_kline('index_min5'))
print(Check_Data.check_kline('index_min15'))
print(Check_Data.check_kline('index_min30'))
print(Check_Data.check_kline('index_min60'))
print(Check_Data.check_kline('index_day'))
#
# a = Check_Data.self_check()
# print(a)