
import pandas as pd
from Calf import BaseModel
class PlateStock:
    @classmethod
    def get_all_info(cls):
        data=pd.DataFrame(list(BaseModel('platestock').query()))
        # print(data)
        if len(data)==0:
            return pd.DataFrame()
        return data.loc[:,['hangye','stock_code']]
    @classmethod
    def get_stock_code_plate(cls):
        data = pd.DataFrame(list(BaseModel('stock_code_plate').query()))
        data.drop_duplicates(['stock_code'],inplace=True)
        return data.loc[:, ['code', 'stock_code']]
        # print(len(data))
data=PlateStock.get_stock_code_plate()

# print(data)
# data=PlateStock.get_all_info()
# dic={}
# for i,r in data.iterrows():
#     dic[r.stock_code]=r.code
# print(dic)
