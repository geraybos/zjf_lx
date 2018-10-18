from sklearn import tree

import pandas as pd
import datetime as dt

from Calf.models.base_model import BaseModel
from sklearn.metrics import classification_report

if __name__ == '__main__':
    curror = BaseModel('novel_Feature').query(sql=dict(stock_code=1,date={'$gte': dt.datetime(2018,4,15), '$lte': dt.datetime(2018, 4, 23)}))
    print(curror.count())
    data = pd.DataFrame(list(curror))

    data['change_r_next'] = data.change_r_next.map(lambda x: 1 if x > 0 else 0)
    data_test = data[data.date == dt.datetime(2018, 4, 23)]
    data = data[data.date < dt.datetime(2018, 4, 23)]

    y = data.loc[:, ['change_r_next']]
    X = data.drop(['_id', 'change_r_next', 'date'], axis=1)
    X_test = data_test.drop(['_id', 'change_r_next', 'date'], axis=1)
    y_test = data_test.loc[:, ['change_r_next']]
    clf = tree.DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=None,
                                      max_leaf_nodes=None, max_features=None,
                                      min_impurity_split=0.005,
                                      min_samples_split=2, min_weight_fraction_leaf=0.0,
                                      presort=False, random_state=1, splitter='random')
    clf = clf.fit(X, y)  # 此时完成训练
    y_pred = clf.predict(X_test)  # 预测
    # result=(classification_report(data_test.loc[:,['change_r_next']], y_pred))
    print(list(y_pred), '预测值')
    print(y_test.change_r_next.tolist(), '真实值')
