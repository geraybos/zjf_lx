import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from Calf import BaseModel, ModelData, klinedata, KlineData
from Calf.models.calendar1 import Calendar
from File.file import File
import datetime as dt
class CheckData:
    @classmethod
    def check_npy_file(cls,file_name):
        x = np.load(file_name)
        plt.matshow(x, cmap='hot')
        plt.show()

    @classmethod
    def check_database(cls,table,condtion,num,path):
        data=BaseModel(table).query(condtion).limit(num)
        data=pd.DataFrame(list(data))
        # data=data[0:num]
        names = data.columns.values.tolist()
        File.check_file(path)
        for i,r in data.iterrows():
            time = r.time if 'time' in names else ''
            plt.grid(False)
            plt.matshow(r.value,cmap='hot')
            plt.savefig(fname=path+"/"+str(r.date)[0:10]+'_'+str(r.date.minute)+".png",transparent=True)
        print('complete')

    @classmethod
    def check_database_by_type(cls, table, condtion,pre_table, num, path):
        data = BaseModel(table).query(condtion)
        data = pd.DataFrame(list(data))
        data = data[0:num]


        File.check_file(path)
        for i, r in data.iterrows():

            data0=pd.DataFrame(list(BaseModel(pre_table).query({'date':r.date,'stock_code':r.stock_code})))
            plt.matshow(data0.value.iloc[0], cmap='hot')
            plt.savefig(fname=path + "/" + str(r.date)[0:10] + ".png")
        print('complete')

    @classmethod
    def insert_data(cls,tablename,data):
        ModelData.insert_data(tablename,data)

    @classmethod
    def add_industry(cls, table):
        from Calf import ModelData
        import pymongo
        url = 'mongodb://limu:limu@192.168.1.104:27017/?connectTimeoutMS=2000;authSource=admin'
        industry = ModelData.read_data(table_name='platestock')
        dic = {}
        for i, r in industry.iterrows():
            dic[r.stock_code] = r.hangye
        myclient = pymongo.MongoClient(url)
        mydb = myclient["ppp"]
        mycol = mydb[table]
        for s_c in industry.stock_code.tolist():
            myquery = {"stock_code": s_c}
            newvalues = {"$set": {"hangye": dic[s_c]}}
            x = mycol.update_many(myquery, newvalues)
            print(x.modified_count, s_c + "文档已修改")
        myclient.close()
    @classmethod
    def draw_399303(cls,path,start_date,end_date,table):
        print(start_date,end_date)
        data=ModelData.read_data(table_name=table,stock_code={'$in':['399303','000001','399001','399006']},date={'$gte':start_date,'$lte':end_date})
        data=data.sort_values(by=['date'],ascending=True)

        # print(data.head())
        while len(data):
            date=data.date.iloc[-1]
            data0=data[data.date==date]
            # plt.grid(False)
            plt.figure()
            plt.title(str(date))
            ax1=plt.subplot(221)

            ax1.matshow(data0[data0.stock_code=='399303'].value.iloc[0], cmap='hot')
            ax1.set_xticks([])
            ax1.set_yticks([])
            plt.title(str(399303))
            ax2=plt.subplot(222)
            ax2.matshow(data0[data0.stock_code=='000001'].value.iloc[0], cmap='hot')
            ax2.set_xticks([])
            ax2.set_yticks([])
            plt.title('000001')
            ax3 = plt.subplot(223)
            ax3.matshow(data0[data0.stock_code=='399001'].value.iloc[0], cmap='hot')
            ax3.set_xticks([])
            ax3.set_yticks([])
            plt.title('399001')
            ax4 = plt.subplot(224)
            ax4.matshow(data0[data0.stock_code=='399006'].value.iloc[0], cmap='hot')
            plt.title('399006')
            ax4.set_xticks([])
            ax4.set_yticks([])
            # plt.show()
            # break
            File.check_file(path=path)
            plt.savefig(fname=path + "/" + str(date)[0:10] + ".png")
            data=data[data.date<date]

    @classmethod
    def draw_399303(cls, path, start_date, end_date, table,kline):
        print(start_date, end_date)
        data = ModelData.read_data(table_name=table, stock_code={'$in': ['399303', '000001', '399001', '399006']},
                                   date={'$gte': start_date, '$lte': end_date})
        data = data.sort_values(by=['date'], ascending=True)

        for i,r in data.iterrows():
            plt.matshow(r.value, cmap='hot')
            File.check_file(path + "/" +r.stock_code+'/'+kline)
            plt.savefig(fname=path + "/" +r.stock_code+'/'+kline+ '/'+str(r.date)[0:10]+'-'+str(r.date.minute) + ".png")
            plt.close()


#==================================================================================================

# table='A_MACD_left_right_index_min5_version3'
# path='f:/zjf/data/data'
# kline='index_min5'
# end_date=dt.datetime(2018,8,10)
# while end_date>dt.datetime(2017,1,1):
#     start=Calendar.calc(end_date,-10)['date']
#     start=dt.datetime(2017,1,1) if start<dt.datetime(2017,1,1) else start
#     CheckData.draw_399303(path=path,start_date=start,end_date=end_date,table=table,kline=kline)
#     end_date=Calendar.calc(start,-1)['date']

#==================================================================================================


#exmpale
#======================================================================================================
table="A_MA_H512_W64_index_min5"
CheckData.check_database(table=table,condtion={'stock_code':'880302'},num=10,path="f:/item/"+table)
#======================================================================================================
#exmpale
#======================================================================================================
# sql={
#     "stock_code":'000001'
# }
# data=pd.DataFrame(list(BaseModel('boll_A_kline_min30').query(sql)))
# print(data)
# data['type']=1
# CheckData.insert_data(tablename='item',data=data)
# CheckData.check_database_by_type(table='item',condtion={'type':1},pre_table="boll_A_kline_min30",num=10,path="f:/item")
#======================================================================================================
#exmple
#======================================================================================================
# CheckData.add_industry(table='AA_time_trends_kline_min1')
#======================================================================================================

# #exmple
#======================================================================================================
# table="hot_min5_version2"
# CheckData.check_database(table=table,condtion={},num=10,path="f:/item/"+table)
#======================================================================================================
