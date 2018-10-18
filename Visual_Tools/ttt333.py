from Calf.data import KlineData
import datetime as dt

def deal(data):
    columns = data.columns.values.tolist()

    for i in columns:
        if i not in ['_id', 'classtype']:
            v = data[i].iloc[0]
            if type(v).__name__ not in ['bool_','str'] :
                data[i] = (data[i] - data[i].min()) / (data[i].max() - data[i].min())
    return data
data = KlineData.read_data(code='000001',start_date=dt.datetime(2018,9,1),end_date=dt.datetime(2018,10,10),kline='kline_day')
data=deal(data)
print(data.head(10))
