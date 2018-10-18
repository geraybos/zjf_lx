from Calf.data import KlineData
import datetime as dt
import matplotlib.pyplot as plt
from Visual.DMI.caculate import Caculate

data=KlineData().read_data(code='001979',start_date=dt.datetime(2018,5,1),end_date=dt.datetime(2018,9,1),kline='kline_day')
data=data.sort_values(by=['date'],ascending=True)
data=Caculate.n_DMI(data)
data=data[::-1]
print(data.date.tolist())
fig=plt.figure(figsize=(9,6))
plt.plot(data.date,data['PDI'])
plt.plot(data.date,data['MDI'])
plt.plot(data.date,data['ADX'])
plt.show()