import pandas as pd
import numpy as np
import datetime as dt


class CalOneData:
    @classmethod
    def cal_data(cls, data, interval, detal):
        # 传入data的顺序用取数据函（klinedata）数取出后的顺序
        data = data.sort_values(by=['date'], ascending=True)
        # data = data.reset_index(drop=True)
        # data["close2"] = data.close.shift(-interval)
        # data["close3"] = data.close.shift(detal)
        # # data['profit'] = data.close2 / data.close - 1
        # data['profit_self'] = data.close / data.close3 - 1
        return data

    @classmethod
    def data_normalization(cls, data, pixel, detal):
        date = data.date.iloc[len(data) - detal]
        temp = data[data.time == 1500]

        ps=temp.close.iloc[len(temp) - 2] / temp.close.iloc[len(temp) - 3] - 1
        data['profit_self'] = ps
        data['profit'] = temp.close.iloc[len(temp) - 1] / temp.close.iloc[len(temp) - 2] - 1
        y=temp.close.iloc[len(temp) - 3]
        data['up'] = data.close /  y- 1
        data = data[data.date2 == dt.datetime(date.year, date.month, date.day)]
        data = data.reset_index(drop=False)
        data0 = data.loc[:, ['volume']]
        data1 = data.loc[:, ['up']]

        a = np.array(data0)
        amax, amin = a.max(), a.min()
        a = (a - amin) / (amax - amin) * (pixel / 2 - 1)
        result0 = pd.DataFrame(a, columns=['volume'])
        a = np.array(data1)

        amax, amin = a.max(), a.min()
        max = -amax if abs(amax) > abs(amin) else amin
        a0 = a * (pixel / 4 - 1) / max* abs(max)/0.097
        a = a0 + pixel / 4
        result = pd.DataFrame(a, columns=['up'])
        result['volume'] = result0['volume']
        result['date'] = data.date
        result['profit'] = data.profit
        result['profit_self'] = data.profit_self
        return result
