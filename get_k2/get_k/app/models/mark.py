# -*- coding: utf-8 -*-
from datetime import datetime

from app.models.base_model import BaseModel


class Kline_data_update_mark(BaseModel):
    __fields__ = BaseModel.__fields__ + [
        ('date', datetime, -1),
        ('status', int, 0),
        ('kline', str, ''),
        ('other',str,'')
    ]
    # send_date = "{'model': 'macd', 'status':1,'time':'%s','kline':%s}

class kline_data_update_mark(Kline_data_update_mark):
   # __tablename__ = 'kline_data_update_mark'
    pass

class Check_Data(BaseModel):
    __fields__ = BaseModel.__fields__ + [

    ]
    # send_date = "{'model': 'macd', 'status':1,'time':'%s','kline':%s}

class check_data(Check_Data):
   # __tablename__ = 'kline_data_update_mark'
    pass