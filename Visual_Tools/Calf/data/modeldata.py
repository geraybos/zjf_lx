# encoding: utf-8

"""
@version: 1.0
@author: LeungJain
@time: 2017/11/23 14:24
"""
import datetime

import pandas as pd
import numpy as np

from Calf.data import MODEL_TABLE, BaseModel
from Calf.base.query_str_analyzer import analyzer
from Calf.exception import MongoIOError, FileError, ExceptionInfo, WarningMessage, SuccessMessage


class ModelData(object):
    """
    有关公共模型所有的IO（数据库、文件）将通过这个类实现，在有关证券原始数据
    的读取过程中，纵向读取会按时间降序排列
    """
    location = None
    dbname = None
    
    def __init__(self, location=None, dbname=None):
        ModelData.location = location
        ModelData.dbname = dbname
        pass

    @classmethod
    def field(cls, table_name, field_name):
        """
        Query the value of a field in the database
        :param table_name: the database's table name
        :param field_name: the table's field name
        :return: all values in database
        """
        try:
            return BaseModel(table_name, cls.location,
                             cls.dbname).distinct(field_name)
        except Exception:
            raise MongoIOError('query the field raise a error')

    @classmethod
    def max(cls, table_name, field='_id', **kw):
        """
        找到满足kw条件的field列上的最大值
        :param table_name:
        :param field:
        :param kw:
        :return:
        """
        try:
            if not isinstance(field, str):
                raise TypeError('field must be an instance of str')
            cursor = BaseModel(table_name, cls.location,
                               cls.dbname).query(sql=kw, field={field: True})
            if cursor.count():
                d = pd.DataFrame(list(cursor))
                m = d.loc[:, [field]].max()[field]
            else:
                m = None
            cursor.close()
            return m
        except Exception as e:
            raise e

    @classmethod
    def min(cls, table_name, field='_id', **kw):
        """
        找到满足kw条件的field列上的最小值
        :param table_name:
        :param field:
        :param kw:
        :return:
        """
        try:
            if not isinstance(field, str):
                raise TypeError('field must be an instance of str')
            cursor = BaseModel(table_name, cls.location,
                               cls.dbname).query(sql=kw, field={field: True})
            if cursor.count():
                d = pd.DataFrame(list(cursor))
                m = d.loc[:, [field]].min()[field]
            else:
                m = None
            cursor.close()
            return m
        except Exception as e:
            raise e

    @classmethod
    def insert_data(cls, table_name, data):
        """
        一个简易的数据插入接口
        :param table_name:
        :param data:
        :return:
        """
        try:
            if len(data):
                d = data.to_dict(orient='records')
                BaseModel(table_name, cls.location,
                          cls.dbname).insert_batch(d)
        except Exception:
            raise MongoIOError('Failed with insert data by MongoDB')

    @classmethod
    def read_data(cls, table_name, field=None, **kw):
        """
        一个简易的数据读取接口
        :param table_name:
        :param field:
        :param kw:
        :return:
        """
        try:
            cursor = BaseModel(table_name, cls.location,
                               cls.dbname).query(kw, field)
            data = pd.DataFrame()
            if cursor.count():
                data = pd.DataFrame(list(cursor))
        except Exception as e:
            ExceptionInfo(e)
        finally:
            cursor.close()
            return data

    @classmethod
    def update_date(cls, table_name, condition, **kw):
        """
        按condition条件更新table_name表数据
        :param table_name:
        :param condition: 形如{‘date':datetime.datetime(2018,1,1)}的一个字典
        :param kw:形如close=0这样的参数组
        :return:
        """
        try:
            BaseModel(table_name, cls.location,
                      cls.dbname).update_batch(condition, kw)
        except Exception:
            raise MongoIOError('Failed with update by MongoDB')

    @classmethod
    def remove_data(cls, table_name, **kw):
        """
        删除数据
        :param table_name:
        :param kw:
        :return:
        """
        try:
            BaseModel(table_name, cls.location, cls.dbname).remove(kw)
        except Exception:
            raise MongoIOError('Failed with delete data by MongoDB')


    @classmethod
    def insert_trade_menu(cls, menus):
        """
        记录日交易所获得的收益
        :param menus:
        :return:
        """
        try:
            if len(menus):
                d = menus.to_dict(orient='records')
                MODEL_TABLE(cls.location, cls.dbname,
                            'trademenu').insert_batch(d)
        except Exception:
            raise MongoIOError('Failed with insert data by MongoDB')

    @classmethod
    def read_trade_menu(cls, model_from, start_date=None,
                        end_date=None, version=None, **kw):
        """
        读取模型收益数据，读取到的数据主要包括某种策略一个或一段时间所对应的收益
        :param model_from:
        :param start_date:
        :param end_date:
        :param version:
        :param kw:
        :return:
        """
        try:
            sql = {'model_from': model_from}
            if version is not None:
                sql['version'] = version
            if start_date is None and end_date is None:
                pass
            else:
                if start_date is not None and end_date is None:
                    date = analyzer("date >= {s}".format(s=start_date))
                elif end_date is not None and start_date is None:
                    date = analyzer("date <= {e}".format(e=end_date))
                else:
                    date = analyzer("date >= {s} and data <= {e}".format(s=start_date, e=end_date))
                sql = dict(sql, **date)
            sql = dict(sql, **kw)
            cursor = MODEL_TABLE(cls.location, cls.dbname, 'trademenu').query(sql)
            menus = list(cursor)
            if len(menus):
                menus = pd.DataFrame(menus)
                menus = menus.sort_values(['date'], ascending=True)
                menus = menus.reset_index(drop=True)
                menus.drop(['_id', 'classtype'], axis=1, inplace=True)
                return menus
            return pd.DataFrame()
        except Exception:
            raise MongoIOError('query trade menu from db raise a error')

    @classmethod
    def insert_finance_index(cls, fis):
        """
        保存模型回测过程中的一些财务指标
        :param fis:
        :return:
        """
        try:
            if len(fis):
                d = fis.to_dict(orient='records')
                MODEL_TABLE(cls.location, cls.dbname,
                            'financeindex').insert_batch(d)
        except Exception:
            raise MongoIOError('Failed with insert data by MongoDB')

    @classmethod
    def read_finance_index(cls, model_from, field=None, **kwargs):
        """
        读取模型回测的财务指标数据
        :return:
        """
        try:
            sql = {'model_from': model_from}
            sql = dict(sql, **kwargs)
            cursor = MODEL_TABLE(cls.location, cls.dbname,
                                 'financeindex').query(sql, field)
            if cursor.count():
                fis = pd.DataFrame(list(cursor))
                fis.drop(['_id', 'classtype'], axis=1, inplace=True)
                return fis
            return pd.DataFrame()
        except Exception:
            raise MongoIOError('query finance indicators from db raise a error')

    @classmethod
    def insert_risk_pst(cls, rps):
        """
        插入风险仓位数据
        :param rps: a DataFrame
        :return:
        """
        try:
            if len(rps):
                dit = []
                for i, row in rps.iterrows():
                    r = dict(row)
                    dit.append(r)
                # print(dit[0])
                MODEL_TABLE(cls.location, cls.dbname,
                            'risk_and_position').insert_batch(dit)
        except Exception:
            raise MongoIOError('Failed with insert data by MongoDB')

    @classmethod
    def read_risk_pst(cls, stock_code=None, date=None, **kw):
        """
        读取仓位数据
        :return:
        """
        try:
            sql = dict()
            if stock_code is not None:
                sql['stock_code'] = stock_code
            if date is not None:
                sql = dict(sql, **analyzer("date = {d}".format(d=date)))
            sql = dict(sql, **kw)
            cursor = MODEL_TABLE(cls.location, cls.dbname,
                                 'risk_and_position').query(sql)
            rps = list(cursor)
            if len(rps):
                rps = pd.DataFrame(rps)
                rps.drop(['_id', 'classtype'], axis=1, inplace=True)
                return rps
            return pd.DataFrame()
        except Exception:
            raise MongoIOError('query risk and position from db raise a error')

    @classmethod
    def insert_risk(cls, risks):
        """
        插入风险参数
        :param risks:
        :return:
        """
        try:
            if len(risks):
                dit = []
                for i, row in risks.iterrows():
                    r = dict(row)
                    dit.append(r)
                MODEL_TABLE(cls.location, cls.dbname,
                            'risk').insert_batch(dit)
        except Exception:
            raise MongoIOError('Failed with insert data by MongoDB')

    @classmethod
    def read_risk(cls, stock_code=None, date=None, **kw):
        """
        读取风险参数
        :param stock_code:
        :param date:
        :param kw:
        :return:
        """
        try:
            sql = dict()
            if stock_code is not None:
                sql['stock_code'] = stock_code
            if date is not None:
                sql = dict(sql, **analyzer("date = {d}".format(d=date)))
            sql = dict(sql, **kw)
            cursor = MODEL_TABLE(cls.location, cls.dbname, 'risk').query(sql)
            rks = list(cursor)
            if len(rks):
                rks = pd.DataFrame(rks)
                rks.drop(['_id', 'classtype'], axis=1, inplace=True)
                return rks
            return pd.DataFrame()
        except Exception:
            raise MongoIOError('query risk from db raise a error')

    @classmethod
    def insert_pst(cls, pst):
        """
        插入仓位
        :param pst:
        :return:
        """
        try:
            if len(pst):
                dit = []
                for i, row in pst.iterrows():
                    r = dict(row)
                    dit.append(r)
                MODEL_TABLE(cls.location, cls.dbname,
                            'position').insert_batch(dit)
        except Exception:
            raise MongoIOError('Failed with insert data by MongoDB')

    @classmethod
    def read_pst(cls, stock_code=None, date=None, **kw):
        """
        读取仓位
        :param stock_code:
        :param date:
        :param kw:
        :return:
        """
        try:
            sql = dict()
            if stock_code is not None:
                sql['stock_code'] = stock_code
            if date is not None:
                sql = dict(sql, **analyzer("date = {d}".format(d=date)))
            sql = dict(sql, **kw)
            cursor = MODEL_TABLE(cls.location, cls.dbname,
                                 'position').query(sql)
            pst = list(cursor)
            if len(pst):
                pst = pd.DataFrame(pst)
                pst.drop(['_id', 'classtype'], axis=1, inplace=True)
                return pst
            return pd.DataFrame()
        except Exception:
            raise MongoIOError('query position from db raise a error')

