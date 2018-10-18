import requests

from Calf.data import ModelData

from Calf.models.base_model import BaseModel

class USStockCode:
    url = 'https://hq.sinajs.cn/?_=0.38256121247853314&list='
    # url = 'https://hq.sinajs.cn/'

    def crawl(self, code_list):
        code_list=','.join(code_list)
        data=requests.get(self.url+code_list, {})
        return data

    def get_sina_data(self,code_list):
        data=self.crawl(code_list=code_list)
        data=data.content
        data=data.decode('gbk')
        data=data.split('\n')[0:-1]
        result=list()
        i = 0
        for idata in data:
            # print(len(code_list),i)

            code=code_list[i]
            try:
                idata = idata.split('=')[1]
                idata = idata.split(',')
                result.append({'code':code,'value':float(idata[12])})
            except Exception as e:
                result.append({'code': code, 'value': 0})
            i+=1

        return result
# USStockCode().get_sina_data('gb_aapl,gb_ixic')

import pandas as pd
# data=ModelData(location='server_db',dbname='big-data').read_data(table_name='US_stock_code',field={'_id':0,'stock_type':0})
# data['code']=data.code.map(lambda x:'gb_'+str(x)[3:].lower())
# # print(data.head())
# stocks=data.code.tolist()
# m=100
# li=[stocks[i:i+m] for i in range(0,len(stocks),m)]
# result=list()
# obj=USStockCode()
# c=0
# for i in li:
#     print(c)
#     result.extend(obj.get_sina_data(i))
#     c+=1
# # print(result)
# data2=pd.DataFrame(result)
# data=pd.merge(data,data2,on=['code'])
# data=data[(data.value)>0]
# data=data.loc[:,['code','value']]
# data.to_csv('us_stock.csv')
# print(data.head())
import matplotlib.pyplot as plt
data=pd.read_csv('us_stock.csv')
data['code']=data.code.map(lambda x:x[3:])
data=(data[data.value>4000000000])
with open('usa2.txt','a+') as f:
    for i,r in data.iterrows():
        f.write(str(r.code).upper()+'\n')
# print(length/len(data))
# print(length)
# data['code']=data.code.map(lambda x:x[3:])
# data=data.dropna()
# plt.scatter(y=range(len(data)),x=data.value)
# plt.show()


