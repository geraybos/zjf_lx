from Calf import KlineData
import pandas as pd

class MacdData:
    @classmethod
    def get_macd_data(cls, sc, start_time, end_time, kline,length):#length 限定获取数据的长度
        data = KlineData.read_data(code=sc, start_date=start_time, end_date=end_time, kline=kline)
        if len(data) < length:
            print('data is no ok')
            return pd.DataFrame([])
        data = data.drop(['_id', 'classtype'], axis=1)
        return data
