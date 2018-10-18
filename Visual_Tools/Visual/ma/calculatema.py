import pandas as pd
import numpy as np


class CalMa:
    @classmethod
    def cal_ma(cls, data, interval,detal):
        data = data.sort_values(by=['date'],ascending=True )
        data['ma5'] = data.close.rolling(5).mean()
        data['ma10'] = data.close.rolling(10).mean()
        data['ma20'] = data.close.rolling(20).mean()
        data['ma60'] = data.close.rolling(60).mean()
        data['ma120'] = data.close.rolling(120).mean()
        data['ma200'] = data.close.rolling(200).mean()
        data["close2"] = data.close.shift(-interval)
        data["close3"] = data.close.shift(detal)
        data['profit'] = data.close2 / data.close - 1
        data['profit_self'] = data.close / data.close3 - 1
        return data


    @classmethod
    def cal_profit(cls, data, interval,detal):
        data = data.sort_values(by=['date'], ascending=True)
        data = data.reset_index(drop=True)
        data["close2"] = data.close.shift(-interval)
        data["close3"] = data.close.shift(detal)
        data['profit'] = data.close2 / data.close - 1
        data['profit_self'] = data.close / data.close3 - 1
        return data

    @classmethod
    def cal_jsut_ma(cls, data):
        data = data.sort_values(by=['date'],ascending=True )
        data['ma5'] = data.close.rolling(5).mean()
        data['ma10'] = data.close.rolling(10).mean()
        data['ma20'] = data.close.rolling(20).mean()
        data['ma60'] = data.close.rolling(60).mean()
        data['ma120'] = data.close.rolling(120).mean()
        data['ma200'] = data.close.rolling(200).mean()
        return data

    @classmethod
    def cal_ma_stub(cls, data, interval, detal):
        data = data.sort_values(by=['date'], ascending=True)
        data['ma5'] = data.close.rolling(5).mean()
        data['ma10'] = data.close.rolling(10).mean()
        data['ma20'] = data.close.rolling(20).mean()
        data['ma60'] = data.close.rolling(60).mean()
        data['ma120'] = data.close.rolling(120).mean()
        data['ma200'] = data.close.rolling(200).mean()
        data["close2"] = data.close.shift(-interval)
        data["close3"] = data.close.shift(detal)
        data['profit'] = data.close2 / data.close - 1
        data['profit_self'] = data.close / data.close3 - 1
        return data

    @classmethod
    def data_normalization_one_four(cls, datax,pixel):
        date1=datax.date

        data = datax.loc[:, ['close_x', 'open_x', 'high_x', 'low_x', 'ma5_x', 'ma10_x', 'ma20_x', 'ma60_x', 'ma120_x']]
        a = np.array(data)
        amin, amax = a.min(), a.max()  # 求最大最小值
        a = (a - amin) / (amax - amin) * (pixel*2-2)
        data = pd.DataFrame(a, columns=['close', 'open', 'high', 'low', 'ma5', 'ma10', 'ma20', 'ma60', 'ma120'])
        data['date']=date1

        data_index = datax.loc[:, ['close_y', 'open_y', 'high_y', 'low_y', 'ma5_y', 'ma10_y', 'ma20_y', 'ma60_y', 'ma120_y']]
        a = np.array(data_index)
        amin, amax = a.min(), a.max()  # 求最大最小值
        a = (a - amin) / (amax - amin) * (pixel*2 - 2)
        data_index = pd.DataFrame(a, columns=['close_index', 'open_index', 'high_index', 'low_index', 'ma5_index', 'ma10_index', 'ma20_index', 'ma60_index', 'ma120_index'])
        data_index['date']=date1
        datas=pd.merge(data,data_index,on=['date'])
        datas=datas.tail(pixel)
        return datas

    @classmethod
    def data_normalization2(self, data, pixel):

        data = data.loc[:, ['close', 'open', 'high', 'low', 'ma5', 'ma10', 'ma20', 'ma60', 'ma120']]
        a = np.array(data)
        amin, amax = a.min(), a.max()  # 求最大最小值
        a = (a - amin) / (amax - amin) * (pixel/2 - 2)
        data = pd.DataFrame(a, columns=['close', 'open', 'high', 'low', 'ma5', 'ma10', 'ma20', 'ma60', 'ma120'])
        return data

    @classmethod
    def data_normalization(self, data, pixel):
        # pixel=pixel-border/2
        data = data.loc[:, ['close', 'open', 'high', 'low', 'ma5', 'ma10', 'ma20', 'ma60', 'ma120']]
        a = np.array(data)
        amin, amax = a.min(), a.max()  # 求最大最小值
        a = (a - amin) / (amax - amin) * (pixel-3)+2
        data2 = pd.DataFrame(a, columns=['close', 'open', 'high', 'low', 'ma5', 'ma10', 'ma20', 'ma60', 'ma120'])
        return data2

    @classmethod
    def data_normalization_ok(self, data, pixel):
        # pixel=pixel-border/2
        data = data.loc[:, ['close', 'open', 'high', 'low', 'ma5', 'ma10', 'ma20','ma60','ma120','ma200']]
        a = np.array(data)
        amin, amax = a.min(), a.max()  # 求最大最小值
        a = (a - amin) / (amax - amin) * (pixel - 3) + 2
        data2 = pd.DataFrame(a, columns=['close', 'open', 'high', 'low', 'ma5', 'ma10', 'ma20','ma60','ma120','ma200'])
        return data2

    @classmethod
    def data_stub_normalization(self, data, pixel):
        # pixel=pixel-border/2
        data = data.loc[:, ['close', 'open', 'high', 'low']]
        a = np.array(data)
        amin, amax = a.min(), a.max()  # 求最大最小值
        a = (a - amin) / (amax - amin) * (pixel - 3) + 2
        data2 = pd.DataFrame(a, columns=['close', 'open', 'high', 'low'])
        return data2

    @classmethod
    def data_stub_normalization2(self, data, pixel):
        # pixel=pixel-border/2
        data = data.loc[:, ['close', 'open', 'high', 'low', 'ma5', 'ma10', 'ma20']]
        a = np.array(data)
        amin, amax = a.min(), a.max()  # 求最大最小值
        a = (a - amin) / (amax - amin) * (pixel - 3) + 2
        a=a/2
        data2 = pd.DataFrame(a, columns=['close', 'open', 'high', 'low', 'ma5', 'ma10', 'ma20'])
        return data2

    @classmethod
    def data_normalization3(self, data, pixel):
        # pixel=pixel-border/2
        data = data.loc[:, ['close', 'open', 'high', 'low', 'ma5', 'ma10', 'ma20', 'ma60', 'ma120','ma200']]
        a = np.array(data)
        amin, amax = a.min(), a.max()  # 求最大最小值
        a = (a - amin) / (amax - amin) * (pixel - 3) + 2
        data2 = pd.DataFrame(a, columns=['close', 'open', 'high', 'low', 'ma5', 'ma10', 'ma20', 'ma60', 'ma120','ma200'])
        return data2

    @classmethod
    def data_normalization_volume(cls,data,pixel):
        data = data.loc[:, ['volume']]
        a = np.array(data)
        amin, amax = a.min(), a.max()  # 求最大最小值
        a = (a - amin) / (amax - amin) * (pixel - 3) + 2
        data2 = pd.DataFrame(a,
                             columns=['volume'])
        return data2

    @classmethod
    def data_normalization_volume2(cls, data, pixel,amax):
        data['temp']=data.close-data.open
        data['temp']=data.temp.map(lambda x:1 if x>0 else -1)
        data['volume']=data.volume*data.temp
        data = data.loc[:, ['volume']]
        data['volume']=data['volume']* (pixel/2-1)/amax+(pixel/2)
        return data.loc[:,['volume']]


