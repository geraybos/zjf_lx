from Calf.data import KlineData
import datetime as dt
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt
from Calf.models.base_model import BaseModel
import pandas as pd
import numpy as np
data = KlineData.read_data(code='000001', start_date=dt.datetime(2016, 1, 1), end_date=dt.datetime(2018, 9, 2),
                           kline='index_min5', timemerge=True)
data = data.loc[:, ['date', 'close', 'open', 'high', 'low', 'volume']]
data['close2'] = data.close.shift(-48)
data['profit'] = data.close / data.close2 - 1
data = data.drop(['close2'], axis=1)
data = data.dropna()
y = data.loc[:, ['profit']]
X = data.loc[:, ['close', 'open', 'low', 'high', 'volume']]
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
print(X_train.shape)
print(y_test.shape)
from sklearn.linear_model import LinearRegression
linreg = LinearRegression()
linreg.fit(X_train, y_train)
a = (linreg.intercept_)
print(a)
print((linreg.coef_))
# 模型拟合测试集
y_pred = linreg.predict(X_test)
from sklearn import metrics
# 用scikit-learn计算MSE
print("MSE:", metrics.mean_squared_error(y_test, y_pred))
# 用scikit-learn计算RMSE
print("RMSE:", np.sqrt(metrics.mean_squared_error(y_test, y_pred)))


