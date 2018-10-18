#step one  get-data
from sklearn import tree

from Calf.data import KlineData
import datetime as dt
import pandas as pd
class Alphas:
    def get_data(self):
        data=KlineData.read_data(code='000001',kline='kline_day',start_date=dt.datetime(2015,1,1),end_date=dt.datetime(2018,9,3))
        # print(data.loc[:,['date']])
        return data
    def caculate(self):
        data=self.get_data()

        data['close-1']=data.close.shift(1)

        data['profit']=data['close-1']/data.close-1
        data['close1']=data.close.shift(-1)
        data['close2']=data.close.shift(-2)
        data['close3']=data.close.shift(-3)
        data['close4']=data.close.shift(-4)
        data['close5']=data.close.shift(-5)
        data['close6'] = data.close.shift(-6)
        data['close9']=data.close.shift(-9)
        data['close20'] = data.close.shift(-20)

        data['return_6'] = data.close / data.close6 -1#
        data['return_20'] = data.close / data.close20-1#

        data['volume_mean3']=data.volume.rolling(3).mean()

        data['high_0/low_0'] = data.high/data.low#
        data['close_1/open_0'] = data.close1/data.open#
        data['open_0/close_0'] = data.open/data.close#
        data['close_0/open_0'] = data.close/data.open#
        data['high_0/close_1'] = data.high/data.close1#
        data['close_9/close_0'] = data.close9/data.close#
        data['close_4/close_0'] = data.close4/data.close#
        data['close_6/close_0'] = data.close6/data.close#
        data['close_2/close_0'] = data.close2/data.close#
        data['close_3/close_0'] = data.close3/data.close#
        data['close_5/close_0'] = data.close5/data.close#
        data['close_1/close_0'] = data.close1/data.close#
        data['volume_0/mean(volume_0, 3)*100'] = data.volume/data.volume_mean3#



        data=data.dropna()

        data=data.loc[:,['return_6','return_20','high_0/low_0','close_1/open_0','close_0/open_0','open_0/close_0',
             'high_0/close_1','close_9/close_0','close_4/close_0','close_6/close_0','close_2/close_0','close_5/close_0',
             'close_1/close_0','date','profit']
             ]
        print(data.head())
        return data

    def set(self):
        data=self.caculate()
        data['profit'] = data.profit.map(lambda x: 1 if x > 0 else 0)
        data_test = data[data.date >= dt.datetime(2018, 1, 1)]
        data = data[data.date < dt.datetime(2018, 1, 1)]
        y = data.loc[:, ['profit']]
        X = data.drop([ 'profit', 'date'], axis=1)
        X_test = data_test.drop([ 'profit', 'date'], axis=1)
        y_test = data_test.loc[:, ['profit']]
        clf = tree.DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=None,
                                          max_leaf_nodes=None, max_features=None,
                                          min_impurity_split=0.005,
                                          min_samples_split=2, min_weight_fraction_leaf=0.0,
                                          presort=False, random_state=1, splitter='random')
        clf = clf.fit(X, y)  # 此时完成训练
        y_pred = clf.predict(X_test)  # 预测
        print(clf.score(X_test,y_test))
        print(y_pred)


if __name__ == '__main__':
    Alphas().set()