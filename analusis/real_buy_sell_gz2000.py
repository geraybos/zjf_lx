import datetime as dt
import multiprocessing

import pandas as pd
from urllib.request import urlopen

from Calf.models.base_model import BaseModel

from Calf.modelrun import ModelRun

from Calf.modelaction import ModelAction


class RealData:
    """
    从各个行情服务器读取实时数据
    """
    # 新浪A股返回的数据结构
    columns = {0: 'stock_name', 1: 'open', 2: 'last_close', 3: 'price', 4: 'high',
               5: 'low', 6: 'buy_', 7: 'sell_', 8: 'volume', 9: 'amount',
               10: 'B1_V', 11: 'B1', 12: 'B2_V', 13: 'B2', 14: 'B3_V', 15: 'B3',
               16: 'B4_V', 17: 'B4', 18: 'B5_V', 19: 'B5', 20: 'S1_V',
               21: 'S1', 22: 'S2_V', 23: 'S2', 24: 'S3_V', 25: 'S3', 26: 'S4_V', 27: 'S4',
               28: 'S5_V', 29: 'S5', 30: 'datetime', 31: 'time', 32: 'other'}

    @classmethod
    def market_judge(cls, stock_code):
        """
        根据股票的代码判断其所属市场，并返回带市场标示前缀的股票代码
        :param stock_code:
        :return:
        """
        if stock_code[0:1] == '6':
            stock_code = 'sh' + stock_code
        else:
            stock_code = 'sz' + stock_code
        return stock_code

    @classmethod
    def get_stock_data(cls, stock_code):
        """
        读取一止股票的实时数据
        :param stock_code:
        :return:
        """
        _code = RealData.market_judge(stock_code)
        html = urlopen('http://hq.sinajs.cn/list={}'.format(_code)).read()
        data_l = html.decode('gbk').split('\n')
        i = 0
        res = dict()
        for data in data_l:
            if len(data):
                d = data.split('="')
                key = stock_code
                i = i + 1
                res[key] = d[1][:-2].split(',')

        # print(res, len(res['601088']))
        return res

    @classmethod
    def get_stocks_data(cls, stocks_code):
        """
        根据所给的股票代码列表，从新浪接口读取实时数据并打包成一个df
        注意：在交易时间之外价格数据可能不符合实际
        :param stocks_code:
        :return:
        """
        try:
            _codes = ['sh' + c if c[0:1] == '6' else 'sz' + c for c in stocks_code]

            # _codes = [RealData.market_judge(x) for x in stocks_code]
            _codes = ','.join(_codes)
            html = urlopen('http://hq.sinajs.cn/list={}'.format(_codes)).read()
            data_l = html.decode('gbk').split('\n')
            i = 0
            res = dict()
            for data in data_l:
                if len(data):
                    d = data.split('="')
                    key = stocks_code[i]
                    i += 1
                    res[key] = d[1][:-2].split(',')
            data = pd.DataFrame(res).T
            data[30] = data[30] + ' ' + data[31]
            data = data.rename(columns=RealData.columns)
            data['datetime'] = pd.to_datetime(data.datetime)
            data['stock_code'] = data.index
            _ = 'float'
            dtypes = dict(open=_, last_close=_, price=_, high=_, low=_, buy_=_, sell_=_,
                          volume=_, amount=_, B1=_, B2=_, B3=_, B4=_, B5=_, S1=_, S2=_, S3=_, S4=_, S5=_,
                          B1_V=_, B2_V=_, B3_V=_, B4_V=_, B5_V=_, S1_V=_, S2_V=_, S3_V=_, S4_V=_, S5_V=_, )
            data = data.astype(dtypes)
            # print(data.T)
            return data
        except Exception as e:
            print(e)
            return None


def exe():
    data = list()
    with open('gz2000cons.txt') as f:
        for line in f.read().split('\n'):
            data.append(line)
    # data=data[1500:2000]
    m=300
    data=[data[i:m+i] for i in range(0,len(data),m)]
    # pool = multiprocessing.Pool(processes=3)
    # result = pool.map(fun, data)
    for idata in data:
        # print(idata)
        x = RealData.get_stocks_data(idata)
        if len(x):
            x = x.drop(['time', 'other'], axis=1)
            idata = x.to_dict(orient='records')
            BaseModel('real_buy_sell_gz2000').insert_batch(idata)
#
def fun(idata):
    x = RealData.get_stocks_data(idata)
    x = x.drop(['time', 'other'], axis=1)
    idata = x.to_dict(orient='records')
    BaseModel('real_buy_sell_gz2000').insert_batch(idata)

class Min5Action(ModelAction):
    @classmethod
    def execute(cls, **kwargs):
        exe()

    @classmethod
    def is_trade_day(cls, date):
        return True


if __name__ == '__main__':
    # exe()
    ModelRun.DScheduler(Min5Action, execute_date='9:29:00-11:30:00 13:00:00-15:00:30', execute_interval=3)
