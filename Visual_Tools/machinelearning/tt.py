import math

from Calf.data import KlineData
from Calf.models import Calendar

from Calf.models.base_model import BaseModel
import datetime as dt
import pandas as pd
# data=pd.DataFrame(list(BaseModel('features_index_day').query({'kdj_30_max':{'$lte':108.175},'date':dt.datetime(2017, 6, 2)})))
# data2=pd.DataFrame(list(BaseModel('features_index_day').query({'kdj_30_max':{'$gte':108.175},'date':dt.datetime(2017, 6, 2)})))
# data3=pd.DataFrame(list(BaseModel('features_index_day').query({'kdj_30_max':{'$lte':108.175},'last_Close_dt_ma5':{'$lte':0.96},'date':dt.datetime(2017, 6, 2)})))
# data4=pd.DataFrame(list(BaseModel('features_index_day').query({'kdj_30_max':{'$gt':108.175},'last_Close_dt_ma5':{'$gt':0.96},'date':dt.datetime(2017, 6, 2)})))
# print(len(data))
# print(len(data2))
# print(len(data3))
# print(len(data4))
#
# import numpy as np
#
# x = [[0, 1, 2], [2, 3, 4]]
# x = np.array(x)
# x = x.T
# x = x[::-1].T
# print(x)
# x=math.log10(100)
# print(x)


# get_all_securities(date='2015-10-10')


import datetime as dt
# import pandas as pd
# data=BaseModel('kline_min5').query(sql={'date':Calendar.today(),'time':{'$lte':955}})
# data=pd.DataFrame(list(data))
# svg=data.volume.mean()
# print(svg)
#
# data=BaseModel('tmp_kline_min5').query(sql={'date':Calendar.today(),'time':{'$lte':955}})
# print(data.count())
# data=pd.DataFrame(list(data))
# svg=data.volume.mean()
# print(svg)


import pandas as pd

#
from Stock.Stock import Stock

data = pd.DataFrame({'a': [-100,0,0,0,-1,1, 2, 3, 4, 0],'b': [-200,0,0,0,-1,1, 2, 3, 4, 0]})
# columns = data.columns.values.tolist()
# print(columns)
# v=1.23
# x=type(v).__name__ =='float'
# print(x)
# i='a'
# data.loc[data[i] > 0, i] = (data.loc[data[i] > 0, i] - data.loc[data[i] > 0, i].min()) / (data.loc[data[i] > 0, i].max() - data.loc[data[i] > 0, i].min())
# print(data)
# data = pd.DataFrame(list(BaseModel('features_index_day').query({'stock_code':'880441'})))
# pass
# i='a'
# data.loc[data[i] != 0, i] = (data.loc[data[i] != 0, i] - data.loc[data[i] != 0, i].min()) / (
#                         data.loc[data[i] != 0, i].max() - data.loc[data[i] != 0, i].min())
#
# print(data)

# curror = BaseModel('features_index_day').query(
#     sql=dict(stock_code={'$in': model.li},
#              date={'$gte': start_date, '$lte': end_date}))


# print((data.a>0) & (data.a<4))

#
# data.loc[(data.a>0) & (data.a<4),['a','b']]=data.iloc[0].tolist()
# print(data)
# fund_data = pd.DataFrame(list(BaseModel('jq_fund_data').query({'code': '000001'})))
# print(fund_data.head())
# print(fund_data.columns.values.tolist())
# stocks=Stock.get_all_stock()
# result=[]
# dobj=BaseModel('kline_day')
# for sc in stocks:
#     print(sc)
#     c=dobj.query({'stock_code': sc})
#     if c.count():
#         print('enter')
#         data = list(dobj.asc(c, ['date']).limit(1))[0]['date']
#         result.append({'stock_code':sc,'date':data})
# BaseModel('LaunchDate').insert_batch(result)

import datetime as dt
date1=dt.datetime(2018,10,17)
date2=dt.datetime(2018,10,15)
date=(date1-date2)

print(date.days)