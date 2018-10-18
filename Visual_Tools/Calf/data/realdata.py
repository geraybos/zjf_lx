# encoding: utf-8

"""
@version: 1.0
@author: LeungJain
@time: 2017/12/26 9:43
"""
import pandas as pd
from urllib.request import urlopen
from pandas_datareader import data as pdr


class RealData:
    """
    从各个行情服务器读取实时数据
    """
    # 新浪A股返回的数据结构
    columns = {0: 'stock_name', 1: 'open', 2: 'last_close', 3: 'price', 4: 'high',
               5: 'low', 6: 'buy_', 7: 'sell_', 8: 'volume', 9: 'amount',
               10: 'B1_V', 11: 'B1', 12: 'B2_V', 13: 'B2', 14: 'B3_V', 15: 'B3',
               16: 'B4_V', 17: 'B4', 18: 'B5_V', 19: 'B5', 20: 'B1_V',
               21: 'S1', 22: 'S2_V', 23: 'S2', 24: 'S3_V', 25: 'S3', 26: 'S4_V', 27: 'S4',
               28: 'S5_V', 29: 'S5', 30: 'datetime', 31: 'time'}

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
            # print(data.T)
            return data
        except Exception as e:
            print(e)
            return None

    @classmethod
    def yahoo_stock_data(cls, stock_code):
        """

        :param stock_code:
        :return:
        """
        html = urlopen('http://finance.yahoo.com/d/quotes.csv?s=XOM+BBDb.TO+JNJ+MSFT&f=snd1l1yr').read()
        data_l = html.decode('gbk').split('\n')
        print(data_l)

    @classmethod
    def usa_stock_data(cls, stock_code):
        """
        获取美股的实时数据
        :param stock_code:
        :return:
        """
        try:
            data = pdr.DataReader(stock_code, 'iex-last')
            data = data.T
            if len(data) > 1:
                data = data.T
            elif len(data) == 1:
                pass
            else:
                return None
            data = data.rename(columns={'symbol': 'stock_code', 'time': 'datetime'})
            data['datetime'] = pd.to_datetime(data.datetime, unit='ms', utc=True)
            data['datetime'] = data.datetime + pd.Timedelta(hours=-4)
            data['datetime'] = data.datetime.map(lambda d: d.replace(tzinfo=None))
            return data
        except Exception as e:
            print(e)
            return None
    
    @classmethod
    def hk_stock_data(cls, stock_code):
        try:
            if isinstance(stock_code, str):
                _code = 'hk' + stock_code
                stock_code = [stock_code]
            elif isinstance(stock_code, list):
                _code = ['hk' + c  for c in stock_code]
                _code = ','.join(_code)
            else:
                raise TypeError('This stock code type must in (str, list)')
            html = urlopen('http://hq.sinajs.cn/list={}'.format(_code)).read()
            data_l = html.decode('gbk').split('\n')
            i = 0
            res = dict()
            for data in data_l:
                if len(data):
                    d = data.split('="')
                    key = stock_code[i]
                    res[i] = [stock_code[i]] + d[1][:-2].split(',')
                    i += 1
            data = pd.DataFrame(res).T
            data[18] = data[18] + ' ' + data[19]
            data = data.loc[:, [0, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 18]]
            columns = {0: 'stock_code', 2: 'stock_name', 3: 'open', 4: 'last_close',
                       5: 'price', 6: 'low', 7: 'high', 9: 'gains', 10: 'B1', 11: 'S1',
                       12: 'amount', 13: 'volume', 18: 'datetime'}
            data = data.rename(columns=columns)
            data['datetime'] = pd.to_datetime(data.datetime)
            # data['stock_code'] = data.index
            # print(data.T)
            return data
        except Exception as e:
            print(e)
            return None

# realdata.get_stocks_data(['601088', '002427'])
# RealData.yahoo_stock_data('aa')
# print(RealData.hk_stock_data('00700'))