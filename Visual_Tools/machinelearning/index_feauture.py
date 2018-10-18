
# t = time.clock()
import multiprocessing

from Calf.models import Calendar
from Calf.models.base_model import BaseModel

from Calf.data import KlineData
from Stock.Stock import Stock

from novel_features import n_KDJ, n_MA, n_MACD, n_RSI, n_DMI, n_BRAR, n_CR, n_VR, n_WR, n_CCI, n_BOLL, n_PSY
import datetime as dt
import pandas as pd
import numpy as np
def normal(employment):
    mean = employment.mean()  # 计算平均数
    deviation = employment.std()  # 计算标准差
    # 标准化数据的公式: (数据值 - 平均数) / 标准差
    standardized_employment = (employment - mean) / deviation
    return standardized_employment

def deal_data(code):
    data = KlineData.read_data(code=code, start_date=dt.datetime(2016, 1, 1), end_date=dt.datetime(2018, 9, 18),
                               kline='index_min5',timemerge=True)
    if len(data):
        data = n_KDJ(data, 9, 3)
        # t1 = time.clock()
        # print(t1-t)
        # t = time.clock()
        data = n_MA(data)
        # t1 = time.clock()
        # print(t1 - t)
        # t = time.clock()
        data = n_MACD(data, 12, 26, 9)
        # t1 = time.clock()
        # print(t1 - t)
        # t = time.clock()
        data = n_RSI(data, 6, 12, 24)
        # t1 = time.clock()
        # print(t1 - t)
        # t = time.clock()
        data = n_DMI(data, 14, 6)
        # t1 = time.clock()
        # print(t1 - t)
        # t = time.clock()
        data = n_BRAR(data, 26)
        # t1 = time.clock()
        # print(t1 - t)
        # t = time.clock()
        data = n_CR(data, 26, 10, 20, 40)
        # t1 = time.clock()
        # print(t1 - t)
        # t = time.clock()
        data = n_VR(data, 26)
        # t1 = time.clock()
        # print(t1 - t)
        # t = time.clock()
        data = n_WR(data, 10, 6)
        # t1 = time.clock()
        # print(t1 - t)
        # t = time.clock()
        data = n_CCI(data, 14)
        # t1 = time.clock()
        # print(t1 - t)
        # t = time.clock()
        data = n_BOLL(data, 20)
        # t1 = time.clock()
        # print(t1 - t)
        # t = time.clock()
        data = n_PSY(data, 12)


        data.dropna(inplace=True)
        data=data[data.time==955]

        BaseModel('features_index_min5').insert_batch(data.to_dict(orient='records'))


import datetime as dt
def similarity():
    index_features= pd.DataFrame(list(BaseModel('index_feature_temp').query({})))
    print(index_features.columns.values)
    x_columns = [x for x in index_features.columns if
                 x in ["ma5_angle","ma10_angle","ma20_angle","close_open","high_low",'high_close','Close_dt_ma5','Close_dt_ma10',"Close_dt_ma20"]]#"ma10_angle", "ma20_angle","ma30_angle", "ma60_angle",'close_ma5','open_ma5','high_open','high_low','high_close','close_open'
    index_features=index_features.loc[:,x_columns+['date']]

    index_features=index_features.replace(to_replace=np.Infinity, value=np.NaN)
    index_features=index_features.dropna()
    index_features=index_features.sort_values(by=['date'],ascending=False)
    index_features=index_features.reset_index(drop=True)




    # index_features_=index_features.loc[:,x_columns].apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))
    # index_features_['date']=index_features['date']
    # index_features=index_features_
    from sklearn import preprocessing
    #=============================================================================标准化
    index_features_=index_features.loc[:,x_columns]
    index_features_=np.array(index_features_)
    index_features_=preprocessing.scale(index_features_)
    index_features_=pd.DataFrame(index_features_,columns=x_columns)
    index_features_['date']=index_features['date']
    index_features=index_features_
    # =============================================================================标准化
    target_date = dt.datetime(2017, 7, 17)
    target=index_features[index_features.date==target_date]
    other=index_features[index_features.date<target_date]
    date_list = other.date.tolist()
    print('date len',len(date_list))
    target=target.drop(['date'],axis=1)
    other=other.drop(['date'],axis=1)
    target_arr=np.array(target)
    other_arr=np.array(other)
    print('other_arr len', len(other_arr))
    result=target_arr-other_arr
    print('result len', len(result))
    result=result**2
    result=np.sum(result,axis=1)
    result=np.sqrt(result)


    #===============================================================================余弦
    # from scipy.spatial.distance import pdist
    # result=list()
    # for i in range(len(date_list)):result
    #     result.append(pdist(np.vstack([target_arr,other_arr[i][:]]), 'cosine')[0])
    # print(result)
    # ===============================================================================余弦

    data=pd.DataFrame({'result':result,'date':date_list})
    print('target',target_date)
    print('result',data[data.result==data.result.min()])
    # position_index=np.argsort(result)
    # position_index=pd.DataFrame(result)
    # no1_index=position_index[position_index[0]==0].index.tolist()[0]
    # no2_index=position_index[position_index[0]==1].index.tolist()[0]
    # no3_index=position_index[position_index[0]==2].index.tolist()[0]
    # no4_index=position_index[position_index[0]==3].index.tolist()[0]
    # pass
    # date=[date_list[i] for i in [no1_index,no2_index,no3_index,no4_index]]
    # print('target',target_date)
    # print('similarity',date)
    # print(index_features[index_features.date==date[0]])
    # print(index_features[index_features.date==date[1]])
# deal_data(code='399303')
# similarity()
# c=BaseModel('index_min5').query(sql={'date':dt.datetime(2018,9,17),'time':1500})
# data=pd.DataFrame(list(c))
# print(data.stock_code.tolist())
def fun(codes):
    for i in codes:
        BaseModel('features_index_min5').remove(stock_code=i)
        deal_data(i)
        print(i,'over')
if __name__ == '__main__':
    stocks = Stock.get_index_stock_code_list()
    pool = multiprocessing.Pool(processes=3)
    m = 10
    li = [stocks[i:i + m] for i in range(0, len(stocks), m)]
    result = pool.map(fun, li)