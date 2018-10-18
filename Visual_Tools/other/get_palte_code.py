import pandas as pd

from Calf import ModelData, BaseModel


class PlateStock:
    stock_code=[]
    hangye=[]

    def get_plate(self):
        f=open('plate_code.txt','r')
        for line in f:
            line=line.split('|')
            self.stock_code.append(line[1])
            self.hangye.append(line[2])
        data=pd.DataFrame(dict(stock_code=self.stock_code,hangye=self.hangye))
        return data


class PlateName:
    index_code=[]
    name=[]
    hangye=[]

    def get_plate(self):
        f=open('plate_name.txt','r')
        for line in f:
            line=line.split('|')
            self.index_code.append(line[1])
            self.name.append(line[0])
            self.hangye.append(line[5].replace('\n',''))
        data=pd.DataFrame(dict(index_code=self.index_code,name=self.name,hangye=self.hangye))
        return data

# obj=PlateName()
# data1=obj.get_plate()
# obj2=PlateStock()
# data2=obj2.get_plate()
# data=pd.merge(data1,data2,on=['hangye'])
# BaseModel('stock_code_plate').remove({})
# BaseModel('stock_code_plate').insert_batch(data.to_dict(orient='records'))

#===========================================================================
data=pd.DataFrame(list(BaseModel('stock_code_plate').query({})))
# print(data)
data=data.loc[:,['stock_code','index_code']].sort_values(by=['stock_code'])
index_dict={}
for i,r in data.iterrows():
    index_dict[r.stock_code]=r.index_code
print(index_dict)