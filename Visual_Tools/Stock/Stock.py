# -*- coding: UTF-8 -*-
import tushare as ts
import pandas as pd

from Calf import project_dir, BaseModel
from Calf.models.calendar1 import Calendar


class Stock:
    @classmethod
    def get_stock_code_list(cls):
        t=Calendar.today()
        t = Calendar.calc(t,-1)['date']
        obj = BaseModel('kline_day')
        curror=obj.query({'date':t})
        data=pd.DataFrame(list(curror))
        data=data.sort_values(by=['stock_code'],ascending=True)
        return data
    @classmethod
    def get_index_stock_code_list(cls):
        data=['880302', '880303', '880306', '880307', '880308', '880311', '880312', '880313', '880319', '880320', '880321', '880325', '880326', '880327', '880328', '880329', '880330', '880336', '880337', '880338', '880339', '880340', '880345', '880346', '880347', '880348', '880350', '880351', '880355', '880361', '880362', '880363', '880364', '880366', '880368', '880369', '880373', '880374', '880375', '880381', '880382', '880383', '880387', '880391', '880392', '880393', '880394', '880398', '880399', '880401', '880402', '880403', '880407', '880408', '880409', '880410', '880411', '880412', '880413', '880414', '880419', '880420', '880421', '880422', '880423', '880425', '880426', '880430', '880431', '880432', '880438', '880439', '880441', '880442', '880443', '880444', '880445', '880446', '880447', '880448', '880452', '880453', '880454', '880455', '880456', '880460', '880461', '880462', '880463', '880464', '880466', '880467', '880468', '880471', '880472', '880473', '880474', '880477', '880478', '880483', '880484', '880485', '880486', '880489', '880490', '880491', '880492', '880493', '880494', '880497']
        data = list(set(data))
        data.sort()
        return data
    @classmethod
    def get_all_stock(cls):
        """
        #tushare的stock
        :rtype: object
        """
        df = ts.get_stock_basics()
        df['stock']=df.index
        df=df.sort_values(by=['stock'],ascending=True)
        # stocks = df.index.tolist()
        return df.stock.tolist()
    @classmethod
    def get_markets_stock(cls,market):
        pf = r'{}/Stock/{}'.format(project_dir, '{}.txt'.format(market))
        with open(pf) as f:
            sl = f.read().split('\n')
        return sl
    @classmethod
    def get_all_stock_outstanding(cls):
        df = ts.get_stock_basics()
        df = df.sort_values(by=['outstanding'], ascending=False)
        df['stock_code'] = df.index
        df = df.reset_index(drop=True)
        df['outstanding_num'] = df.index
        if len(df)==0:
            return pd.DataFrame()
        return df.loc[:, ['stock_code', 'outstanding', 'outstanding_num']]


