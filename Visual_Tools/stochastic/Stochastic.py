import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from Calf import BaseModel, ModelData
from Stock.Stock import Stock


class Stochastic:
    @classmethod
    def get_random(cls,sigma,sampleNo):
        s = sigma * np.random.standard_normal(sampleNo)
        return s

    @classmethod
    def get_k(cls,stock_code,sampleNo,kline,date,index_profit):
        # print(len(date))
        kline = "simulation_" +kline
        profit = Stochastic.get_random(sigma=0.01, sampleNo=sampleNo)
        high_increse = np.abs(Stochastic.get_random(sigma=0.005, sampleNo=sampleNo))
        low_increase = np.abs(Stochastic.get_random(sigma=0.005, sampleNo=sampleNo))
        resel = []
        reselh = []
        resell = []
        r = 1
        for i, ss in enumerate(profit):
            r *= 1 + profit[i]+index_profit[i]
            h=(r*1.1) if (1 + high_increse[i]) > 1.1 else r * (1 + high_increse[i])
            l=(r * 0.9) if r * (1 - low_increase[i]) < 0.9 else  r * (1 - low_increase[i])
            resel.append(r)
            reselh.append(h)
            resell.append(l)
        dd=pd.DataFrame({'stock_code':stock_code,'date':date,'low':resell,'high':reselh,'close':resel,'open':resel})
        ModelData.insert_data(table_name=kline,data=dd)
import datetime as dt

start_date=dt.datetime(2016,1,1)
end_date=dt.datetime(2018,6,20)
data = pd.DataFrame(list(BaseModel('calendar').query({'date': {'$gte': start_date, '$lte': end_date}})))
sampleNo = abs(data.num.iloc[0] - data.num.iloc[len(data) - 1]) + 1
index_profit = (Stochastic.get_random(sigma=0.03, sampleNo=sampleNo))
data2 = Stock.get_stock_code_list()
stocks = data2.stock_code.tolist()

for sc in stocks:
    Stochastic.get_k(stock_code=sc,kline="kline_day",date=data.date.tolist(),sampleNo=sampleNo,index_profit=index_profit)
