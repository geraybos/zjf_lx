import pandas as pd

from Calf.models import Calendar
from Calf.models.base_model import BaseModel

code='000001'

# fund_data = pd.DataFrame(list(BaseModel('jq_fund_data').query({'code': code})))
# data=fund_data[fund_data.day == '2015-12-31'].circulating_market_cap.iloc[0]
# print(data)
def min30(time):
    min30_times = [1000, 1030, 1100, 1130, 1330, 1400, 1500]
    if time in min30_times:
        temp = time // 100 * 60 + time % 100 - 30
        temp = temp // 60 * 100 + temp % 60
        print(temp)
        sql = {'time': {'$gt': temp, '$lte': time}, 'date': Calendar.today()}
        curror = BaseModel('real_kline_min5').query(sql=sql)
        if curror.count():
            data = pd.DataFrame(list(curror))

            data = data.sort_values(by=['time'], ascending=True)
            data = data.groupby(by=['stock_code'], as_index=False).agg(
                {'volume': 'sum', 'amount': 'sum', 'open': 'first',
                 'close': 'last', 'high': 'max', 'low': 'min'})

            data['time'] = time
            data['date'] = Calendar.today()
            BaseModel('real_kline_min30').insert_batch(data.to_dict(orient='records'))
            print('min30 ok')


# min30(time=1000)
def min60(time):
    min60_times = [1030,  1130,  1400, 1500]
    if time in min60_times:
        temp = time // 100 * 60 + time % 100 - 60
        temp = temp // 60 * 100 + temp % 60
        print(temp)
        sql = {'time': {'$gt': temp, '$lte': time}, 'date': Calendar.today()}
        curror = BaseModel('real_kline_min5').query(sql=sql)
        if curror.count():
            data = pd.DataFrame(list(curror))

            data = data.sort_values(by=['time'], ascending=True)
            data = data.groupby(by=['stock_code'], as_index=False).agg(
                {'volume': 'sum', 'amount': 'sum', 'open': 'first',
                 'close': 'last', 'high': 'max', 'low': 'min'})

            data['time'] = time
            data['date'] = Calendar.today()
            BaseModel('real_kline_min60').insert_batch(data.to_dict(orient='records'))
            print('min60 ok')
# min60(time=1030)