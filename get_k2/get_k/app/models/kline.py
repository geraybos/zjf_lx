# -*- coding: utf-8 -*-
import re
from datetime import datetime

import pandas as pd

from app.models import Calendar
from .base_model import BaseModel


class KlineBase(BaseModel):
    __fields__ = BaseModel.__fields__ + [
        ('stock_code', str),
        ('market', int),
        ('date', datetime),
        ('open', float),
        ('close', float),
        ('high', float),
        ('low', float),
        ('volume', int),
        ('amount', int),
    ]

    @classmethod
    def trans_data(cls, source_data):
        _ = dict()
        _['stock_code'] = source_data.get('stock_code', 'xxxxxx')
        _['market'] = source_data.get('market', 'unknow')
        dt = source_data.get('date').split(' ')
        r = re.search('(^\d{4})[./-]*(\d{1,2})[./-]*(\d{1,2}$)', dt[0])
        year, month, day = r.groups()
        _['date'] = datetime(year=int(year), month=int(month), day=int(day))
        _['open'] = float(source_data.get('open', -1))
        _['close'] = float(source_data.get('close', -1))
        _['high'] = float(source_data.get('high', -1))
        _['low'] = float(source_data.get('low', -1))
        _['volume'] = int(source_data.get('volume', -1))
        _['amount'] = int(float(source_data.get('amount', -1)))
        return _


class Day(KlineBase):
    pass


class Week(KlineBase):
    pass


class Month(KlineBase):
    pass


class Minute(KlineBase):
    __fields__ = KlineBase.__fields__ + [
        ('time', int)
    ]

    @classmethod
    def trans_data(cls, source_data):
        _ = KlineBase.trans_data(source_data)
        dt = source_data.get('date').split(' ')
        hour, minute = dt[1].split(':')
        _['time'] = int(hour + minute)
        return _


class Tick(BaseModel):
    __fields__ = BaseModel.__fields__ + [
        ('stock_code', str),
        ('date', datetime),
        ('time', int),
        ('market', str),
        ('price', float),
        ('volume', int),
        ('bs', int)
    ]

    @classmethod
    def trans_data(cls, stock_code, market, date, source_data):
        _ = list()
        for row in source_data:
            r = row.split('\t')
            try:
                t = r[0].split(':')
                _.append({
                    'date': date,
                    'stock_code': stock_code,
                    'market': market,
                    'time': int('{}{}'.format(t[0], t[1])),  # '10:56'
                    'price': float(r[1]),
                    'volume': int(r[2]),
                    'bs': int(r[3])
                })
            except Exception as e:
                continue
        return _

    def to_min(self, stock_code, day):
        ticks = list(self.query(date=Calendar.to('datetime', day), stock_code=stock_code))
        if len(ticks):
            ticks = sorted(ticks, key=lambda x: (x['time']))
            pd_ticks = pd.DataFrame(ticks)
            pd_ticks['open'] = pd_ticks.price
            pd_ticks['close'] = pd_ticks.price
            pd_ticks['high'] = pd_ticks.price
            pd_ticks['low'] = pd_ticks.price
            pd_ticks['volume'] *= 100
            pd_ticks['amount'] = pd_ticks['price'] * pd_ticks['volume']
            x1 = pd_ticks.groupby(by='time').agg(
                {'volume': 'sum', 'close': 'last', 'open': 'first', 'high': 'max', 'low': 'min', 'amount': 'sum'})
            tmp_data = x1.to_dict()
            min_data = list()
            open = tmp_data['open']
            close = tmp_data['close']
            high = tmp_data['high']
            low = tmp_data['low']
            volume = tmp_data['volume']
            amount = tmp_data['amount']
            times = sorted(open.keys())
            for t in times:
                min_data.append({
                    'stock_code': stock_code,
                    'date': day,
                    'time': int(t),
                    'open': round(open[t], 2),
                    'close': round(close[t], 2),
                    'high': round(high[t], 2),
                    'low': round(float(low[t]), 2),
                    'amount': int(amount[t]),
                    'volume': int(volume[t]),
                    'market': 1 if stock_code.startswith('60') else 0
                })
            return min_data
        else:
            return []
