from Calf.models.base_model import BaseModel

print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.datasets import make_classification
from sklearn.ensemble import ExtraTreesClassifier




# Build a classification task using 3 informative features
# X, y = make_classification(n_samples=1000,
#                            n_features=10,
#                            n_informative=3,
#                            n_redundant=0,
#                            n_repeated=0,
#                            n_classes=2,
#                            random_state=0,
#                            shuffle=False)

li=[603993, 601989, 601988, 601881, 601878, 601857, 601818, 601800, 601766, 601688, 601668, 601628, 601601, 601398, 601390, 601360, 601336, 601328, 601318, 601288, 601229, 601211, 601186, 601169, 601166, 601088, 601006, 600999, 600958, 600887, 600703, 600690, 600606, 600585, 600547]
curror = BaseModel('novel_Feature').query(
    sql=dict(stock_code={'$in':li}, date={'$gte': dt.datetime(2016, 1, 1), '$lte': dt.datetime(2018, 9, 15)}))

data = pd.DataFrame(list(curror))
columns=['ADX', 'ADX1', 'ADX_50_DOWN', 'ADX_50_UP', 'ADX_z', 'AR', 'AR_50_DOWN', 'AR_50_UP', 'AR_z', 'BOLL', 'BR',
        'BR_AR_DOWN', 'BR_AR_UP', 'BR_z', 'CCI', 'CCI_-100_UP', 'CCI_100_DOWN', 'CCI_z', 'CR', 'CR_40_DOWN',
        'CR_40_UP', 'CR_MA1_DOWN', 'CR_MA1_UP', 'CR_MA2_DOWN', 'CR_MA2_UP', 'CR_MA3_DOWN', 'CR_MA3_UP', 'CR_z',
        'Close_dt_ma10', 'Close_dt_ma20', 'Close_dt_ma30', 'Close_dt_ma5', 'Close_dt_ma60', 'D', 'DMM', 'DMM1',
        'DMP', 'DMP1', 'D_z', 'HD', 'J', 'J_down_cross_100', 'J_less_20', 'J_over_80', 'J_up_cross_0', 'J_z', 'K',
        'LB', 'LB_z', 'LD', 'MA1', 'MA1_z', 'MA2', 'MA2_z', 'MA3', 'MA3_z', 'MDI', 'MDI_z', 'MTR', 'MTR_1', 'MTR_2',
        'MTR_D1', 'MTR_D2', 'MTR_D3', 'New_H_10', 'New_H_10_10', 'New_H_10_20', 'New_H_10_5', 'New_H_20',
        'New_H_20_10', 'New_H_20_20', 'New_H_20_5', 'New_H_30', 'New_H_30_10', 'New_H_30_20', 'New_H_30_5',
        'New_H_5', 'New_H_5_10', 'New_H_5_20', 'New_H_5_5', 'New_H_60', 'New_H_60_10', 'New_H_60_20', 'New_H_60_5',
        'New_Highest_10', 'New_Highest_20', 'New_Highest_30', 'New_Highest_5', 'New_Highest_60', 'New_Hl_10',
        'New_Hl_20', 'New_Hl_30', 'New_Hl_5', 'New_Hl_60', 'New_L_10', 'New_L_10_10', 'New_L_10_20', 'New_L_10_5',
        'New_L_20', 'New_L_20_10', 'New_L_20_20', 'New_L_20_5', 'New_L_30', 'New_L_30_10', 'New_L_30_20',
        'New_L_30_5', 'New_L_5', 'New_L_5_10', 'New_L_5_20', 'New_L_5_5', 'New_L_60', 'New_L_60_10', 'New_L_60_20',
        'New_L_60_5', 'New_Lh_10', 'New_Lh_20', 'New_Lh_30', 'New_Lh_5', 'New_Lh_60', 'New_Lowest_10',
        'New_Lowest_20', 'New_Lowest_30', 'New_Lowest_5', 'New_Lowest_60', 'PDI', 'PDI_MDI_DOWN', 'PDI_MDI_UP',
        'PDI_z', 'PSY', 'PSY_1', 'PSY_10_DOWN', 'PSY_90_UP', 'PSY_z', 'RSI1', 'RSI1_1', 'RSI1_2', 'RSI2', 'RSI2_1',
        'RSI2_2', 'RSI3', 'RSI3_1', 'RSI3_2', 'TH', 'TH_1', 'TL', 'TL_1', 'TQ', 'TQ_1', 'TYP', 'TYP_mean', 'UB',
        'UB_z', 'VR', 'VR_160_450', 'VR_40_70', 'VR_40_DOWN', 'VR_450_UP', 'VR_80_150', 'WR1', 'WR1_15_DOWN',
        'WR1_20_UP', 'WR1_50_DOWN', 'WR1_50_UP', 'WR1_80_DOWN', 'WR1_85_UP', 'WR1_WR2_DOWN', 'WR1_WR2_UP', 'WR1_z',
        'WR2', 'WR2_z', 'abs', 'amount', 'change_r', 'change_r_next16', 'change_r_next48', 'close',
        'close_LB_DOWN', 'close_UB_UP', 'close_down_ma10', 'close_down_ma20', 'close_down_ma30', 'close_down_ma5',
        'close_down_ma60', 'close_high', 'close_last_close', 'close_last_close_13', 'close_last_close_23',
        'close_last_close_34', 'close_last_close_45', 'close_last_high', 'close_last_high_13', 'close_last_high_23',
        'close_last_high_34', 'close_last_high_45', 'close_last_low', 'close_last_low_13', 'close_last_low_23',
        'close_last_low_34', 'close_last_low_45', 'close_last_open', 'close_last_open_13', 'close_last_open_23',
        'close_last_open_34', 'close_last_open_45', 'close_low', 'close_ma5', 'close_open', 'close_up_ma10',
        'close_up_ma20', 'close_up_ma30', 'close_up_ma5', 'close_up_ma60', 'dea', 'dea_down_cross_0',
        'dea_up_cross_0', 'dea_z', 'dif', 'dif_z', 'diff_down_cross_0', 'diff_down_cross_dea', 'diff_up_cross_0',
        'diff_up_cross_dea', 'duotou_5_10_20', 'h_10_20', 'h_20_30', 'h_30_60', 'h_5_10', 'high', 'high_last_close',
        'high_last_close_13', 'high_last_close_23', 'high_last_close_34', 'high_last_close_45', 'high_last_high',
        'high_last_high_13', 'high_last_high_23', 'high_last_high_34', 'high_last_high_45', 'high_last_low',
        'high_last_low_13', 'high_last_low_23', 'high_last_low_34', 'high_last_low_45', 'high_last_open',
        'high_last_open_13', 'high_last_open_23', 'high_last_open_34', 'high_last_open_45', 'high_list', 'high_low',
        'high_ma5', 'high_open', 'highest_10', 'highest_10_10', 'highest_10_20', 'highest_10_5', 'highest_20',
        'highest_20_10', 'highest_20_20', 'highest_20_5', 'highest_30', 'highest_30_10', 'highest_30_20',
        'highest_30_5', 'highest_5', 'highest_5_10', 'highest_5_20', 'highest_5_5', 'highest_60', 'highest_60_10',
        'highest_60_20', 'highest_60_5', 'highestl_10', 'highestl_20', 'highestl_30', 'highestl_5', 'highestl_60',
        'kdj_10_max', 'kdj_10_min', 'kdj_30_max', 'kdj_30_min', 'kdj_5_10_down', 'kdj_5_10_up', 'kdj_5_30_down',
        'kdj_5_30_up', 'kdj_5_60_down', 'kdj_5_60_up', 'kdj_5_max', 'kdj_5_min', 'kdj_60_max', 'kdj_60_min',
        'kongtou_5_10_20', 'lRSI_z', 'l_10_20', 'l_20_30', 'l_30_60', 'l_5_10', 'last10_high', 'last10_low',
        'last20_high', 'last20_low', 'last2_Close_dt_ma10', 'last2_Close_dt_ma20', 'last2_Close_dt_ma30',
        'last2_Close_dt_ma5', 'last2_Close_dt_ma60', 'last2_close', 'last2_close_high', 'last2_close_low',
        'last2_close_open', 'last2_high', 'last2_high_low', 'last2_high_open', 'last2_low', 'last2_low_open',
        'last2_open', 'last2_volume', 'last3_Close_dt_ma10', 'last3_Close_dt_ma20', 'last3_Close_dt_ma30',
        'last3_Close_dt_ma5', 'last3_Close_dt_ma60', 'last3_close', 'last3_high', 'last3_low', 'last3_open',
        'last3_volume', 'last4_Close_dt_ma10', 'last4_Close_dt_ma20', 'last4_Close_dt_ma30', 'last4_Close_dt_ma5',
        'last4_Close_dt_ma60', 'last4_close', 'last4_high', 'last4_low', 'last4_open', 'last4_volume', 'last5_high',
        'last5_low', 'last_Close_dt_ma10', 'last_Close_dt_ma20', 'last_Close_dt_ma30', 'last_Close_dt_ma5',
        'last_Close_dt_ma60', 'last_close', 'last_close_high', 'last_close_low', 'last_close_ma5',
        'last_close_open', 'last_high', 'last_high_low', 'last_high_ma5', 'last_high_open', 'last_low',
        'last_low_open', 'last_ma10_gt_ma20', 'last_ma20_gt_ma30', 'last_ma30_gt_ma60', 'last_ma5_gt_ma10',
        'last_open', 'last_open_ma5', 'last_volume', 'lastlow_ma5', 'lema', 'low', 'low_last_close',
        'low_last_close_13', 'low_last_close_23', 'low_last_close_34', 'low_last_close_45', 'low_last_high',
        'low_last_high_13', 'low_last_high_23', 'low_last_high_34', 'low_last_high_45', 'low_last_low',
        'low_last_low_13', 'low_last_low_23', 'low_last_low_34', 'low_last_low_45', 'low_last_open',
        'low_last_open_13', 'low_last_open_23', 'low_last_open_34', 'low_last_open_45', 'low_list', 'low_ma5',
        'low_open', 'lowest_10', 'lowest_10_10', 'lowest_10_20', 'lowest_10_5', 'lowest_20', 'lowest_20_10',
        'lowest_20_20', 'lowest_20_5', 'lowest_30', 'lowest_30_10', 'lowest_30_20', 'lowest_30_5', 'lowest_5',
        'lowest_5_10', 'lowest_5_20', 'lowest_5_5', 'lowest_60', 'lowest_60_10', 'lowest_60_20', 'lowest_60_5',
        'lowesth_10', 'lowesth_20', 'lowesth_30', 'lowesth_5', 'lowesth_60', 'm1', 'm2', 'm3', 'ma10', 'ma10_angle',
        'ma10_angle2', 'ma10_angle3', 'ma10_angle4', 'ma10_gt_ma20', 'ma10_z', 'ma10_z2', 'ma10_z3', 'ma10_z4',
        'ma20', 'ma20_angle', 'ma20_angle2', 'ma20_angle3', 'ma20_angle4', 'ma20_gt_ma30', 'ma20_z', 'ma20_z2',
        'ma20_z3', 'ma20_z4', 'ma30', 'ma30_angle', 'ma30_angle2', 'ma30_angle3', 'ma30_angle4', 'ma30_gt_ma60',
        'ma30_z', 'ma30_z2', 'ma30_z3', 'ma30_z4', 'ma5', 'ma5_angle', 'ma5_angle2', 'ma5_angle3', 'ma5_angle4',
        'ma5_down_ma10', 'ma5_down_ma10_2', 'ma5_down_ma10_3', 'ma5_down_ma10_4', 'ma5_down_ma20',
        'ma5_down_ma20_2', 'ma5_down_ma20_3', 'ma5_down_ma20_4', 'ma5_down_ma30', 'ma5_down_ma30_2',
        'ma5_down_ma30_3', 'ma5_down_ma30_4', 'ma5_down_ma60', 'ma5_down_ma60_2', 'ma5_down_ma60_3',
        'ma5_down_ma60_4', 'ma5_gt_ma10', 'ma5_up_ma10', 'ma5_up_ma10_2', 'ma5_up_ma10_3', 'ma5_up_ma10_4',
        'ma5_up_ma20', 'ma5_up_ma20_2', 'ma5_up_ma20_3', 'ma5_up_ma20_4', 'ma5_up_ma30', 'ma5_up_ma30_2',
        'ma5_up_ma30_3', 'ma5_up_ma30_4', 'ma5_up_ma60', 'ma5_up_ma60_2', 'ma5_up_ma60_3', 'ma5_up_ma60_4', 'ma5_z',
        'ma5_z2', 'ma5_z3', 'ma5_z4', 'ma60', 'ma60_angle', 'ma60_angle2', 'ma60_angle3', 'ma60_angle4', 'ma60_z',
        'ma60_z2', 'ma60_z3', 'ma60_z4', 'macd', 'macd_10_down_sum', 'macd_10_up_sum', 'macd_30_down_sum',
        'macd_30_up_sum', 'macd_5_10_down', 'macd_5_10_up', 'macd_5_30_down', 'macd_5_30_up', 'macd_5_60_down',
        'macd_5_60_up', 'macd_5_down_sum', 'macd_5_up_sum', 'macd_60_down_sum', 'macd_60_up_sum',
        'macd_over_last_macd', 'macd_q', 'macd_z', 'market', 'max', 'max2', 'mid', 'number_close_down_mean',
        'number_close_up_mean', 'open', 'open_last_close', 'open_last_close_13', 'open_last_close_23',
        'open_last_close_34', 'open_last_close_45', 'open_last_high', 'open_last_high_13', 'open_last_high_23',
        'open_last_high_34', 'open_last_high_45', 'open_last_low', 'open_last_low_13', 'open_last_low_23',
        'open_last_low_34', 'open_last_low_45', 'open_last_open', 'open_last_open_13', 'open_last_open_23',
        'open_last_open_34', 'open_last_open_45', 'open_ma5', 'p_close', 'p_close16', 'p_close48', 'rsv',
        'sRSI_20_cross_lRSI', 'sRSI_80_cross_lRSI', 'sRSI_down_cross_20', 'sRSI_down_cross_50', 'sRSI_up_cross_50',
        'sRSI_up_cross_80', 'sRSI_z', 'sema', 'std', 'std_std_z_DOWN', 'std_std_z_UP', 'std_z', 'stock_code',
        'sum1', 'sum2', 'sum3', 'sum4', 'v_dt_ma10', 'v_dt_ma20', 'v_dt_ma30', 'v_dt_ma5', 'v_dt_ma60', 'v_ma10',
        'v_ma20', 'v_ma30', 'v_ma5', 'v_ma60', 'volume', 'volume_r', 'vv_dt_ma10', 'vv_dt_ma20', 'vv_dt_ma30',
        'vv_dt_ma5', 'vv_dt_ma60', 'vv_ma10', 'vv_ma20', 'vv_ma30', 'vv_ma5', 'vv_ma60']
data['change_r_next'] = data.change_r_next.map(lambda x: 1 if x > 0 else 0)
data=data.dropna()



data_x = data.loc[:,columns]

data_y=data.loc[:,['change_r_next']]
X= np.array(data_x)
y= np.array(data_y)




# print(y)
# Build a forest and compute the feature importances
forest = ExtraTreesClassifier(n_estimators=250,
                              random_state=0)
#
forest.fit(X, y)
importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")
result=list()
for f in range(X.shape[1]):
    print("%d. feature %d  %s (%f)" % (f + 1, indices[f],columns[f], importances[indices[f]]))
    result.append(columns[f])
print(result)
# Plot the feature importances of the forest
plt.figure()
plt.title("Feature importances")
plt.bar(range(X.shape[1]), importances[indices],
       color="r", yerr=std[indices], align="center")
plt.xticks(range(X.shape[1]), indices)
plt.xlim([-1, X.shape[1]])
plt.show()