from sklearn.externals import joblib
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier

from Calf.models.base_model import BaseModel
import datetime as dt
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


def fund_data_normalizing(data):
    names = ['capitalization', 'circulating_cap', 'circulating_market_cap',
             'market_cap', 'pb_ratio', 'pcf_ratio', 'pe_ratio', 'pe_ratio_lyr', 'ps_ratio', 'turnover_ratio']
    for i in names:
        data[i] = (data[i] - data[i].min()) / (data[i].max() - data[i].min())
    return data


if __name__ == '__main__':
    # clf = DecisionTreeClassifier()
    # clf = LogisticRegression()
    table = 'features_index_day'
    clf = RandomForestClassifier(n_estimators=200, n_jobs=2)
    label = 'change_r_next2'
    curror = BaseModel(table).query(sql={'date': {'$gte': dt.datetime(2018, 1, 5), '$lte': dt.datetime(2018, 7, 25)}})

    print(curror.count())
    if curror.count():

        data = pd.DataFrame(list(curror))

        data = data.replace(to_replace=np.Infinity, value=np.NaN).dropna()
        name = data.columns.values.tolist()
        names = list()

        # data=data.sample(frac=0.2)

        for i in name:
            if i not in ['stock_code', 'date', 'time', 'change_r', 'change_r_next', 'change_r_next16', 'change_r_next2',
                         'change_r_next3', 'change_r_next4', 'change_r_next48', '_id', 'classtype', 'p_close',
                         'p_close2', 'p_close3',
                         'p_close4', 'p_close16', 'p_close48', 'lable']:
                names.append(i)

        # data=fund_data_normalizing(data)
        data_x = data.loc[:, names]

        # data['change_r_next2_sort']=data.sort_values(by=['change_r_next2'],ascending=False).reset_index(drop=True).index

        data[label] = data[label].map(lambda x: 1 if x > 0 else 0)
        data_y = data.loc[:, [label]]
        # data_y=data_y.map(lambda x:1 if x>0 else 0)
        X = np.array(data_x)
        y = np.array(data_y)
        clf.fit(X, y)
        joblib.dump(clf, 'kline_features.m')

    sdate = dt.datetime(2018, 7, 26)
    edate = dt.datetime(2018, 8, 6)
    calendar_list = list(
        BaseModel('calendar').query({'date': {'$gte': sdate, '$lte': edate}}))
    for idate in calendar_list:
        curror = BaseModel(table).query(
            sql={'date': idate['date']})
        date = idate['date']
        if curror.count():
            data = pd.DataFrame(list(curror))
            data = data.replace(to_replace=np.Infinity, value=np.NaN).dropna()
            name = data.columns.values.tolist()
            names = list()
            for i in name:
                if i not in ['stock_code', 'date', 'time', 'change_r', 'change_r_next', 'change_r_next16',
                             'change_r_next2',
                             'change_r_next3', 'change_r_next4', 'change_r_next48', '_id', 'classtype', 'p_close',
                             'p_close2', 'p_close3',
                             'p_close4', 'p_close16', 'p_close48', 'lable']:
                    names.append(i)
            label_data = data.loc[:, ['stock_code', 'date', label]]
            data_x = data.loc[:, names]
            # data['change_r_next2_sort'] = data.sort_values(by=['change_r_next2'], ascending=False).reset_index(
            #     drop=True).index
            data[label] = data[label].map(lambda x: 1 if x > 0 else 0)
            data_y = data.loc[:, [label]]
            # data_y=data_y.map(lambda x:1 if x>0 else 0)
            X_test = np.array(data_x)
            y_test = np.array(data_y)
            y_pred = clf.predict(X_test)  # 预测
            y_prob = clf.predict_proba(X_test)[:, 1]  # 预测
            result = classification_report(y_test, y_pred)
            y_prob = np.argsort(y_prob)
            print('#=======================================================', idate['date'])
            # print(result)
            label_data = label_data[label_data.date == date]
            pre = data.loc[:, ['change_r_next2', 'stock_code']].iloc[y_prob[0:10]]
            last = data.loc[:, ['change_r_next2', 'stock_code']].iloc[y_prob[-10:]]
            # print(data.loc[:, ['change_r_next2', 'stock_code']].iloc[y_prob[0:10]])
            # print(data.loc[:, ['change_r_next2', 'stock_code',]].iloc[y_prob[-10:]])
            pre = pd.merge(pre, label_data, on=['stock_code'])
            last = pd.merge(last, label_data, on=['stock_code'])
            # print('pre_data',pre)
            # print('last_data',last)
            print('pre', pre[label + '_y'].sum() / 10)
            print('last', last[label + '_y'].sum() / 10)
            print('all', last[label + '_y'].mean() - pre[label + '_y'].mean())
            # print('all',pre[label+'_y'].sum()+last[label+'_y'].sum())
            # print('all',(pre[label+'_y'].sum()+last[label+'_y'].sum())/20)
            # print(data_y.iloc[y_prob[-10:]])
            # print('#=======================================================')
            # print(y_prob)
