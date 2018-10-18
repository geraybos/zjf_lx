from app.models.base_model import BaseModel
from app.query_str_analyzer import analyzer
import pandas as pd
sql=analyzer('date = {}'.format(20180620))
# sql['time']={'$lte':955}
# data=BaseModel('tmp_kline_min5').remove(sql)
data=BaseModel('kline_min5').query(sql)
data=pd.DataFrame(list(data))
d=data.to_dict(orient='records')
BaseModel('tmp_kline_min5').insert_batch(d)