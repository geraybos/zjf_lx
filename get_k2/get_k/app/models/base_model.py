# -*- coding: utf-8 -*-
import pymongo
from bson import ObjectId

from ..db import mongodb, ASCENDING, DESCENDING
from ..query_str_analyzer import analyzer
from ..utils import log


class BaseModel(object):
    '''
    _id 是 mongo 自带的，必须有这个字段
    其余 __fields__  的固定属性，未来会逐步添加
        classtype 是类名的小写
    '''
    __fields__ = [
        '_id',
        # (字段名, 类型)
        ('classtype', str),
    ]

    # @classmethod
    def __init__(self, tn=None):
        name = self.__class__.__name__
        self.tablename = tn.strip() if tn is not None and len(tn) else name.lower()
        self.mc = mongodb[self.tablename]
        # return cls

    # @classmethod
    def not_exists(self, *args, **kwargs):
        """
        检查一个元素是否在数据库中 用法如下
        Day.esists(stock_code=600000)
        """
        _ = kwargs if len(kwargs) else args[0]
        return self.query(_).count() == 0

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    # @classmethod
    def insert(self, *args, **kwargs):
        """
        插入一条数据
        例如 d = Day.insert({'stock_code': 600000, 'high': 1, ...})
        或者 d = Day.insert(stock_code=600000, high=1, ...)
        操作完成后返回 insert 成功的对象
        """
        _ = kwargs if len(kwargs) else args[0]
        _['classtype'] = self.tablename
        # 去掉 _id 这个特殊的字段
        if '_id' in _:
            _['_id'] = ObjectId()
            # del _['_id']

        # m = cls()
        # for f in fields:
        #     k, t, v = f
        #     if k in _:
        #         setattr(m, k, t(_[k]))
        #     else:
        #         # 设置默认值
        #         setattr(m, k, v)

        m = self.mc.insert_one(_)
        return m

    # # @classmethod
    def insert_batch(self, *args):
        """
        批量插入数据
        例如 ds = Day.insert_batch([{...}, {...}...])
        或者 ds = Day.insert_batch({...}, {...}...)
        """
        _ = list()
        if len(args) == 1:
            _ = args[0]
            if isinstance(_, list):
                pass
            else:
                _ = [_]

        elif len(args) > 1:
            _ = args

        result = []
        for i in _:
            if i is None:
                continue
            if '_id' in i:
                i['_id'] = ObjectId()
                # del i['_id']
            i['classtype'] = self.tablename.lower()
        try:
            if len(_):
                result = self.mc.insert_many(_)
        except pymongo.errors.BulkWriteError as e:
            if isinstance(_, list):
                r = _[0]
            else:
                r = _
            log('insert_batch', self.tablename, r, msg=e.details['writeErrors'])
        except Exception as e:
            log('insert_batch', self.tablename, msg=e.message)
        return result

    # @classmethod
    def all(self):
        return self.query()

    # @classmethod
    def query(self, *args, **kwargs):
        """
        数据查询
        ds = Day.query(stock_code=1)
        返回 list
        找不到则返回 []
        """
        _ = kwargs if len(kwargs) else args[0] if len(args) else None
        ds = self.mc.find(_)
        return ds

    # @classmethod
    def asc(self, q, fields):
        asc_list = list((x, ASCENDING) for x in fields)
        return q.sort(asc_list)

    # @classmethod
    def desc(self, q, fields):
        asc_list = list((x, DESCENDING) for x in fields)
        return q.sort(asc_list)

    # @classmethod
    def query_one(self, *args, **kwargs):
        """
        查找并返回第一个元素
        找不到就返回 None
        """
        _ = kwargs if len(kwargs) else args[0]
        l = self.mc.find_one(_)
        return l


    def update(self, cond, form):
        '''
        :param form: 更新数据，form 是一个表单
        :param hard: 默认为 False, 如果设置为 True, 可更新 __fields__ 尚未预定义好的属性
        '''
        # for k, v in form.items():
        #     if hard or hasattr(self, k):
        #         setattr(self, k, v)
        self.mc.find_one_and_update(cond, {'$set': form}, upsert=False)
        # self.mc.save()

    def save(self, form):
        '''
        保存数据
        '''
        result = self.mc.save(form)
        return result

    # @classmethod
    def upsert_batch(self, condition, *args):
        """
        批量更新
        condition: {field1: sign1, field2: sign2...}
        例如：{'date': '>', 'stock_code': '=' ...}
        args: [{data1}, {data2}...]
        例如：[{'stock_code': 1, 'open': 12.50...}, ...]
        """
        bulk = self.mc.initialize_ordered_bulk_op()
        for item in args[0]:
            qs = ''
            for c, s in condition:
                qs += '{} {} {}'.format(c, s, item[c])
            sql = analyzer(qs)
            bulk.find(sql).upsert().update({'$set': item})

    # @classmethod
    def distinct(self, field):
        return self.query().distinct(field)

    # @classmethod
    def remove_all(self):
        result = self.mc.delete_many({})
        return result

    # @classmethod
    def remove(self, *args, **kwargs):
        _ = kwargs if len(kwargs) else args[0]
        result = self.mc.delete_many(_)
        return result

    def blockfields(self):
        """
        供 json 函数使用
        排除不需要返回的字段
        子类需要排除字段时，覆盖这个方法即可
        """
        b = [
            '_id',
        ]
        return b

    def json(self):
        """
        导出 model 的 json 字典
        子类需要导出特殊格式的 json 时，覆盖这个方法即可
        """
        _dict = self.__dict__
        d = {k: v for k, v in _dict.items() if k not in self.blockfields()}
        return d

    def copyto(self, target, condition=None, source_data=None):
        if source_data is None:
            if condition is None:
                data = list(self.query())
            else:
                data = list(self.query(condition))
        else:
            data = source_data
        target.insert_batch(data)
        return True
