# encoding: utf-8

"""
@version: 1.0
@author: LeungJain
@time: 2018/5/22 9:28
"""
import pandas as pd
from Calf.data import BaseModel
from Calf.exception import MongoIOError, ExceptionInfo

class TickData(object):
    """
    tick数据IO
    """
    location = None
    dbname = None

    def __init__(self, location=None, dbname=None):
        ModelData.location = location
        ModelData.dbname = dbname
        pass

    @classmethod
    def merge_time(cls, data):
        """
        merge the date and time to datetime
        :param data: must have columns of date and time
        :return:
        """
        try:
            # deltas = pd.DataFrame([cls.timedelta(x) for x in data['time']], columns=['timedelta'])
            # data['date'] = pd.eval("data['date'] + deltas['timedelta']")
            dts = pd.DataFrame()
            dts['date'] = data.date.astype('str')
            dts['time'] = data.time.astype('str')
            dts['time'] = '000' + dts.time
            dts['time'] = dts.time.map(lambda t: t[-4:])
            dts['date'] = dts.date + " " + dts.time
            data['date'] = pd.to_datetime(dts.date, format='%Y-%m-%d %H%M')
            return data
        except Exception:
            raise Exception

    @classmethod
    def read_data(cls, code, start_date, end_date, field=None, timemerge=False, **kw):
        """

        :param code:
        :param start_date:
        :param end_date:
        :param timemerge:
        :return:
        """
        try:
            sql = dict(stock_code=code, date={'$gte': start_date, '$lte': end_date})
            sql = dict(sql, **kw)
            cursor = BaseModel('kline_tick', cls.location, cls.dbname).query(sql, field)
            if cursor.count():
                data = pd.DataFrame(list(cursor))
                data = cls.merge_time(data) if timemerge else data
                cursor.close()
                return data
            else:
                cursor.close()
                return pd.DataFrame()
        except Exception as e:
            ExceptionInfo(e)
            return pd.DataFrame()
