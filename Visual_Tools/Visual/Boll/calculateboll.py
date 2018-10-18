# encoding: utf-8
import numpy as np
import pandas as pd
class CalBoll:
    @classmethod
    def cal_boll(cls, data,interval,p1=20,p2=2,mid=26):
        data = data.sort_values(by=['date'], ascending=True)#保证数据按照时间由远及近的顺序
        data = data.reset_index()#重置索引
        data['mid'] = data['close'].rolling(mid).mean()#按照ma26的计算方式  这就是中轨线
        data['tmp2'] = data['close'].rolling(p1).std()
        data['top'] = data['mid'] + p2 * data['tmp2']   #上轨线
        data['bottom' ] = data['mid'] - p2 * data['tmp2']  #下轨线数据
        data["close2"] = data.close.shift(-interval)
        data['profit'] = data.close2 / data.close - 1
        return data
    @classmethod
    def data_normalization(cls,data,pixel):
        data = data.loc[:, ['mid', 'top', 'bottom','low','high']]
        a = np.array(data)
        amin, amax = a.min(), a.max()  # 求最大最小值
        a = (a - amin) / (amax - amin) * (pixel-2)#减一的目的是为了让四舍五入不会到下面去
        data = pd.DataFrame(a, columns=['mid', 'top', 'bottom','low','high'])
        return data