import gc

from Calf import ModelData
import datetime as dt

from Calf.models import Calendar
# table_names=['kline_day','kline_min30','kline_min60','index_min5','index_day','XDXR_day']
# table_names=['kline_day']
#
# for table_name in table_names:
#     print(table_name)
#     start=dt.datetime(2018,7,4)
#     # while start>dt.datetime(2018,7,4):
#     # print(start)
#     data0=ModelData(location='server_db',dbname='big-data').read_data(table_name=table_name,date={'$gte':start})
#     print('get ok')
#     ModelData(location='hk_server_db',dbname='big-data').insert_data(table_name=table_name,data=data0)
#     gc.collect()
#     # start=Calendar.calc(start,-1)['date']
#
