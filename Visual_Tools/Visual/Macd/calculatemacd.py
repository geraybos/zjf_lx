# encoding: utf-8
import pandas as pd
import numpy as np

from Calf.indicators.public import EMA


class CalMacd:
    @classmethod
    def cal_profit(cls,data,interval):
        data = data.sort_values(by=['date'], ascending=True)
        data = data.reset_index(drop=True)
        data["close2"] = data.close.shift(-interval)
        # data["close3"] = data.close.shift(detal)
        data['profit'] = data.close2 / data.close - 1
        # data['profit_self'] = data.close / data.close3 - 1
        return data
    @classmethod
    def cal_macd(cls, data,interval,detal, short=12, long=26, mid=9):

        #传入data的顺序用取数据函（klinedata）数取出后的顺序
        data = data.sort_values(by=['date'],ascending=True)
        data = data.reset_index(drop=True)
        # data['s'] = EMA(list(data['close']), short)
        # data['l'] = EMA(list(data['close']), long)
        # data['dif'] = pd.eval('data.s - data.l')
        # data['dea'] = EMA(list(data['dif']), mid)
        # data['macd'] = pd.eval('2 * (data.dif - data.dea)')
        data['sema'] = pd.Series(data['close']).ewm(span=short).mean()
        # 计算长期的ema，方式同上
        data['lema'] = pd.Series(data['close']).ewm(span=long).mean()
        # 计算dif，加入新列data_dif
        data['dif'] = data['sema'] - data['lema']
        # 计算dea
        data['dea'] = pd.Series(data['dif']).ewm(span=mid).mean()
        # 计算macd
        data['macd'] = 2 * (data['dif'] - data['dea'])
        data["close2"] = data.close.shift(-interval)
        data["close3"] = data.close.shift(detal)
        data['profit'] = data.close2 / data.close - 1
        data['profit_self'] = data.close / data.close3 - 1
        return data

    @classmethod
    def data_normalization(cls,data,pixel):
        data = data.loc[:, ['dif', 'dea', 'macd']]
        a = np.array(data)
        amin, amax = a.min(), a.max()  # 求最大最小值
        max=-amax if abs(amax)>abs(amin) else amin
        a=a*(pixel/2-1)/max
        a=a+pixel/2
        data = pd.DataFrame(a, columns=['dif', 'dea', 'macd'])
        return data

    @classmethod
    def data_normalization_analysis(cls, data, pixel):
        data = data.loc[:, ['dif', 'dea', 'macd']]
        a = np.array(data)
        amin, amax = a.min(), a.max()  # 求最大最小值
        return amin,amax

    @classmethod
    def data_normalization2(cls, data, pixel):
        data = data.loc[:, ['dif', 'dea', 'macd']]
        a = np.array(data)
        amin, amax = a.min(), a.max()  # 求最大最小值
        max = -amax if abs(amax) > abs(amin) else amin
        a = a * (pixel / 2/2 - 1) / max
        a = a + pixel / 2/2
        data = pd.DataFrame(a, columns=['dif', 'dea', 'macd'])
        return data
    @classmethod
    def data_normalization3(cls, data, pixel,n,r):
        data = data.loc[:, ['dif', 'dea', 'macd']]
        a = np.array(data)
        amin, amax = a.min(), a.max()  # 求最大最小值
        max = -amax if abs(amax) > abs(amin) else amin
        a = a * (pixel / 2  - 1) / max
        a = a + pixel / 2
        data = pd.DataFrame(a, columns=['dif', 'dea', 'macd'])
        c = pixel - n*r
        temp=list()
        datat=data[len(data) - n:len(data)]
        data=data[0:c]
        for i,r in datat.iterrows():
            data.loc[c]=r
            c+=1
            data.loc[c] = r
            c += 1
            data.loc[c] = r
            c += 1
            data.loc[c] = r
            c += 1
        return data