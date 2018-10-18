from Calf.indicators.public import EMA
import numpy as np
import pandas as pd
class calculate:
    @classmethod
    def calculate_data(cls,data,interval,detal, short=12, long=26, mid=9):
        data = data.sort_values(by=['date'], ascending=True)
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



        data['ma5'] = data.close.rolling(5).mean()
        data['ma10'] = data.close.rolling(10).mean()
        data['ma20'] = data.close.rolling(20).mean()
        data['ma60'] = data.close.rolling(60).mean()
        data['ma120'] = data.close.rolling(120).mean()
        data["close2"] = data.close.shift(-interval)
        data["close3"] = data.close.shift(detal)
        data['profit'] = data.close2 / data.close - 1
        data['profit_self'] = data.close / data.close3 - 1




        return data

    @classmethod
    def calculate_data2(cls, data, data_index,interval, detal, short=12, long=26, mid=9):
        data = data.sort_values(by=['date'], ascending=True)
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
        # data_index=data_index.rename({'close_i':'close','low_index':'low','high_index':'high'})


        data_index['low_index']=data_index.low
        data_index['high_index']=data_index.high
        data_index['close_index'] = data_index.close
        # print(data_index['close_index'].iloc[0])
        # print(data.tail(16))
        # print(data_index.loc[-16:-1,['date','close_index']])
        # print(data_index['close_index'].iloc[0])
        # print(data_index['date'].iloc[0])
        # print(data_index.loc[0:10,['date','close_index']])
        print(data.loc[len(data)-10:len(data)-1,['date']])
        md=pd.merge(data.loc[:,['date','profit','profit_self','dif', 'dea', 'macd']],data_index.loc[:,['date','close_index','low_index','high_index']],on=['date'])
        # print(md.loc[len(md) - 10:len(md) - 1, ['date']])
        md = md.sort_values(by=['date'], ascending=True)
        md['ma5'] = md.close_index.rolling(5).mean()
        md['ma10'] = md.close_index.rolling(10).mean()
        md['ma20'] = md.close_index.rolling(20).mean()
        md['ma60'] = md.close_index.rolling(60).mean()
        md['ma120'] = md.close_index.rolling(120).mean()
        md['low'] = md.low_index
        md['high'] = md.high_index
        md['close'] = md.close_index
        del md['low_index']
        del md['high_index']
        del md['close_index']

        # print(data.head(10))
        # print(data.tail(10))

        return md

    @classmethod
    def data_normalization(cls,data,pixel,length):

        data0 = data.loc[:, ['close', 'open', 'high', 'low', 'ma5', 'ma10', 'ma20', 'ma60', 'ma120']]
        a = np.array(data0)
        amin, amax = a.min(), a.max()  # 求最大最小值
        a = (a - amin) / (amax - amin) * (pixel/2 - 2)
        data0 = pd.DataFrame(a, columns=['close', 'open', 'high', 'low', 'ma5', 'ma10', 'ma20', 'ma60', 'ma120'])


        data1 = data.loc[:, ['dif', 'dea', 'macd']]
        a = np.array(data1)
        amin, amax = a.min(), a.max()  # 求最大最小值
        max = -amax if abs(amax) > abs(amin) else amin
        a = a * (pixel / 4 - 2) / max
        a = a + pixel*3/4
        data2 = pd.DataFrame(a, columns=['dif', 'dea', 'macd'])
        data0['dif']=data2.dif
        data0['dea']=data2.dea
        data0['macd']=data2.macd
        return data0

    @classmethod
    def data_normalization2(cls, data, pixel, length):
        data0 = data.loc[:, [ 'high', 'low', 'ma5', 'ma10', 'ma20', 'ma60', 'ma120']]
        a = np.array(data0)
        amin, amax = a.min(), a.max()  # 求最大最小值
        a = (a - amin) / (amax - amin) * (pixel/2 - 2)
        data0 = pd.DataFrame(a, columns=[ 'high', 'low', 'ma5', 'ma10', 'ma20', 'ma60', 'ma120'])

        data1 = data.loc[:, ['dif', 'dea', 'macd']]
        a = np.array(data1)
        amin, amax = a.min(), a.max()  # 求最大最小值
        max = -amax if abs(amax) > abs(amin) else amin
        a = a * (pixel / 4 - 1) / max
        a = a + length * 3 / 4
        data2 = pd.DataFrame(a, columns=['dif', 'dea', 'macd'])
        data0['dif'] = data2.dif
        data0['dea'] = data2.dea
        data0['macd'] = data2.macd
        return data0