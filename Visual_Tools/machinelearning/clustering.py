import datetime as dt
import os

import pydot as pydot
from sklearn.cluster import DBSCAN
from sklearn.tree import export_graphviz
from sklearn import tree
import pydotplus
from sklearn import tree
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.externals import joblib
from sklearn.externals.six import StringIO
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier

from Calf.models.base_model import BaseModel
from Stock.Stock import Stock


class model:
    #初始names
    names=['ADX', 'ADX1', 'ADX_50_DOWN', 'ADX_50_UP', 'ADX_z', 'AR', 'AR_50_DOWN', 'AR_50_UP', 'AR_z', 'BOLL', 'BR', 'BR_AR_DOWN', 'BR_AR_UP', 'BR_z', 'CCI', 'CCI_-100_UP', 'CCI_100_DOWN', 'CCI_z', 'CR', 'CR_40_DOWN', 'CR_40_UP', 'CR_MA1_DOWN', 'CR_MA1_UP', 'CR_MA2_DOWN', 'CR_MA2_UP', 'CR_MA3_DOWN', 'CR_MA3_UP', 'CR_z', 'Close_dt_ma10', 'Close_dt_ma20', 'Close_dt_ma30', 'Close_dt_ma5', 'Close_dt_ma60', 'D', 'DMM', 'DMM1', 'DMP', 'DMP1', 'D_z', 'HD', 'J', 'J_down_cross_100', 'J_less_20', 'J_over_80', 'J_up_cross_0', 'J_z', 'K', 'LB', 'LB_z', 'LD', 'MA1', 'MA1_z', 'MA2', 'MA2_z', 'MA3', 'MA3_z', 'MDI', 'MDI_z', 'MTR', 'MTR_1', 'MTR_2', 'MTR_D1', 'MTR_D2', 'MTR_D3', 'New_H_10', 'New_H_10_10', 'New_H_10_20', 'New_H_10_5', 'New_H_20', 'New_H_20_10', 'New_H_20_20', 'New_H_20_5', 'New_H_30', 'New_H_30_10', 'New_H_30_20', 'New_H_30_5', 'New_H_5', 'New_H_5_10', 'New_H_5_20', 'New_H_5_5', 'New_H_60', 'New_H_60_10', 'New_H_60_20', 'New_H_60_5', 'New_Highest_10', 'New_Highest_20', 'New_Highest_30', 'New_Highest_5', 'New_Highest_60', 'New_Hl_10', 'New_Hl_20', 'New_Hl_30', 'New_Hl_5', 'New_Hl_60', 'New_L_10', 'New_L_10_10', 'New_L_10_20', 'New_L_10_5', 'New_L_20', 'New_L_20_10', 'New_L_20_20', 'New_L_20_5', 'New_L_30', 'New_L_30_10', 'New_L_30_20', 'New_L_30_5', 'New_L_5', 'New_L_5_10', 'New_L_5_20', 'New_L_5_5', 'New_L_60', 'New_L_60_10', 'New_L_60_20', 'New_L_60_5', 'New_Lh_10', 'New_Lh_20', 'New_Lh_30', 'New_Lh_5', 'New_Lh_60', 'New_Lowest_10', 'New_Lowest_20', 'New_Lowest_30', 'New_Lowest_5', 'New_Lowest_60', 'PDI', 'PDI_MDI_DOWN', 'PDI_MDI_UP', 'PDI_z', 'PSY', 'PSY_1', 'PSY_10_DOWN', 'PSY_90_UP', 'PSY_z', 'RSI1', 'RSI1_1', 'RSI1_2', 'RSI2', 'RSI2_1', 'RSI2_2', 'RSI3', 'RSI3_1', 'RSI3_2', 'TH', 'TH_1', 'TL', 'TL_1', 'TQ', 'TQ_1', 'TYP', 'TYP_mean', 'UB', 'UB_z', 'VR', 'VR_160_450', 'VR_40_70', 'VR_40_DOWN', 'VR_450_UP', 'VR_80_150', 'WR1', 'WR1_15_DOWN', 'WR1_20_UP', 'WR1_50_DOWN', 'WR1_50_UP', 'WR1_80_DOWN', 'WR1_85_UP', 'WR1_WR2_DOWN', 'WR1_WR2_UP', 'WR1_z', 'WR2', 'WR2_z', '_id', 'abs', 'amount', 'change_r', 'change_r_next', 'change_r_next16', 'change_r_next48', 'close', 'close_LB_DOWN', 'close_UB_UP', 'close_down_ma10', 'close_down_ma20', 'close_down_ma30', 'close_down_ma5', 'close_down_ma60', 'close_high', 'close_last_close', 'close_last_close_13', 'close_last_close_23', 'close_last_close_34', 'close_last_close_45', 'close_last_high', 'close_last_high_13', 'close_last_high_23', 'close_last_high_34', 'close_last_high_45', 'close_last_low', 'close_last_low_13', 'close_last_low_23', 'close_last_low_34', 'close_last_low_45', 'close_last_open', 'close_last_open_13', 'close_last_open_23', 'close_last_open_34', 'close_last_open_45', 'close_low', 'close_ma5', 'close_open', 'close_up_ma10', 'close_up_ma20', 'close_up_ma30', 'close_up_ma5', 'close_up_ma60', 'date', 'dea', 'dea_down_cross_0', 'dea_up_cross_0', 'dea_z', 'dif', 'dif_z', 'diff_down_cross_0', 'diff_down_cross_dea', 'diff_up_cross_0', 'diff_up_cross_dea', 'duotou_5_10_20', 'h_10_20', 'h_20_30', 'h_30_60', 'h_5_10', 'high', 'high_last_close', 'high_last_close_13', 'high_last_close_23', 'high_last_close_34', 'high_last_close_45', 'high_last_high', 'high_last_high_13', 'high_last_high_23', 'high_last_high_34', 'high_last_high_45', 'high_last_low', 'high_last_low_13', 'high_last_low_23', 'high_last_low_34', 'high_last_low_45', 'high_last_open', 'high_last_open_13', 'high_last_open_23', 'high_last_open_34', 'high_last_open_45', 'high_list', 'high_low', 'high_ma5', 'high_open', 'highest_10', 'highest_10_10', 'highest_10_20', 'highest_10_5', 'highest_20', 'highest_20_10', 'highest_20_20', 'highest_20_5', 'highest_30', 'highest_30_10', 'highest_30_20', 'highest_30_5', 'highest_5', 'highest_5_10', 'highest_5_20', 'highest_5_5', 'highest_60', 'highest_60_10', 'highest_60_20', 'highest_60_5', 'highestl_10', 'highestl_20', 'highestl_30', 'highestl_5', 'highestl_60', 'kdj_10_max', 'kdj_10_min', 'kdj_30_max', 'kdj_30_min', 'kdj_5_10_down', 'kdj_5_10_up', 'kdj_5_30_down', 'kdj_5_30_up', 'kdj_5_60_down', 'kdj_5_60_up', 'kdj_5_max', 'kdj_5_min', 'kdj_60_max', 'kdj_60_min', 'kongtou_5_10_20', 'lRSI_z', 'l_10_20', 'l_20_30', 'l_30_60', 'l_5_10', 'last10_high', 'last10_low', 'last20_high', 'last20_low', 'last2_Close_dt_ma10', 'last2_Close_dt_ma20', 'last2_Close_dt_ma30', 'last2_Close_dt_ma5', 'last2_Close_dt_ma60', 'last2_close', 'last2_close_high', 'last2_close_low', 'last2_close_open', 'last2_high', 'last2_high_low', 'last2_high_open', 'last2_low', 'last2_low_open', 'last2_open', 'last2_volume', 'last3_Close_dt_ma10', 'last3_Close_dt_ma20', 'last3_Close_dt_ma30', 'last3_Close_dt_ma5', 'last3_Close_dt_ma60', 'last3_close', 'last3_high', 'last3_low', 'last3_open', 'last3_volume', 'last4_Close_dt_ma10', 'last4_Close_dt_ma20', 'last4_Close_dt_ma30', 'last4_Close_dt_ma5', 'last4_Close_dt_ma60', 'last4_close', 'last4_high', 'last4_low', 'last4_open', 'last4_volume', 'last5_high', 'last5_low', 'last_Close_dt_ma10', 'last_Close_dt_ma20', 'last_Close_dt_ma30', 'last_Close_dt_ma5', 'last_Close_dt_ma60', 'last_close', 'last_close_high', 'last_close_low', 'last_close_ma5', 'last_close_open', 'last_high', 'last_high_low', 'last_high_ma5', 'last_high_open', 'last_low', 'last_low_open', 'last_ma10_gt_ma20', 'last_ma20_gt_ma30', 'last_ma30_gt_ma60', 'last_ma5_gt_ma10', 'last_open', 'last_open_ma5', 'last_volume', 'lastlow_ma5', 'lema', 'low', 'low_last_close', 'low_last_close_13', 'low_last_close_23', 'low_last_close_34', 'low_last_close_45', 'low_last_high', 'low_last_high_13', 'low_last_high_23', 'low_last_high_34', 'low_last_high_45', 'low_last_low', 'low_last_low_13', 'low_last_low_23', 'low_last_low_34', 'low_last_low_45', 'low_last_open', 'low_last_open_13', 'low_last_open_23', 'low_last_open_34', 'low_last_open_45', 'low_list', 'low_ma5', 'low_open', 'lowest_10', 'lowest_10_10', 'lowest_10_20', 'lowest_10_5', 'lowest_20', 'lowest_20_10', 'lowest_20_20', 'lowest_20_5', 'lowest_30', 'lowest_30_10', 'lowest_30_20', 'lowest_30_5', 'lowest_5', 'lowest_5_10', 'lowest_5_20', 'lowest_5_5', 'lowest_60', 'lowest_60_10', 'lowest_60_20', 'lowest_60_5', 'lowesth_10', 'lowesth_20', 'lowesth_30', 'lowesth_5', 'lowesth_60', 'm1', 'm2', 'm3', 'ma10', 'ma10_angle', 'ma10_angle2', 'ma10_angle3', 'ma10_angle4', 'ma10_gt_ma20', 'ma10_z', 'ma10_z2', 'ma10_z3', 'ma10_z4', 'ma20', 'ma20_angle', 'ma20_angle2', 'ma20_angle3', 'ma20_angle4', 'ma20_gt_ma30', 'ma20_z', 'ma20_z2', 'ma20_z3', 'ma20_z4', 'ma30', 'ma30_angle', 'ma30_angle2', 'ma30_angle3', 'ma30_angle4', 'ma30_gt_ma60', 'ma30_z', 'ma30_z2', 'ma30_z3', 'ma30_z4', 'ma5', 'ma5_angle', 'ma5_angle2', 'ma5_angle3', 'ma5_angle4', 'ma5_down_ma10', 'ma5_down_ma10_2', 'ma5_down_ma10_3', 'ma5_down_ma10_4', 'ma5_down_ma20', 'ma5_down_ma20_2', 'ma5_down_ma20_3', 'ma5_down_ma20_4', 'ma5_down_ma30', 'ma5_down_ma30_2', 'ma5_down_ma30_3', 'ma5_down_ma30_4', 'ma5_down_ma60', 'ma5_down_ma60_2', 'ma5_down_ma60_3', 'ma5_down_ma60_4', 'ma5_gt_ma10', 'ma5_up_ma10', 'ma5_up_ma10_2', 'ma5_up_ma10_3', 'ma5_up_ma10_4', 'ma5_up_ma20', 'ma5_up_ma20_2', 'ma5_up_ma20_3', 'ma5_up_ma20_4', 'ma5_up_ma30', 'ma5_up_ma30_2', 'ma5_up_ma30_3', 'ma5_up_ma30_4', 'ma5_up_ma60', 'ma5_up_ma60_2', 'ma5_up_ma60_3', 'ma5_up_ma60_4', 'ma5_z', 'ma5_z2', 'ma5_z3', 'ma5_z4', 'ma60', 'ma60_angle', 'ma60_angle2', 'ma60_angle3', 'ma60_angle4', 'ma60_z', 'ma60_z2', 'ma60_z3', 'ma60_z4', 'macd', 'macd_10_down_sum', 'macd_10_up_sum', 'macd_30_down_sum', 'macd_30_up_sum', 'macd_5_10_down', 'macd_5_10_up', 'macd_5_30_down', 'macd_5_30_up', 'macd_5_60_down', 'macd_5_60_up', 'macd_5_down_sum', 'macd_5_up_sum', 'macd_60_down_sum', 'macd_60_up_sum', 'macd_over_last_macd', 'macd_q', 'macd_z', 'market', 'max', 'max2', 'mid', 'number_close_down_mean', 'number_close_up_mean', 'open', 'open_last_close', 'open_last_close_13', 'open_last_close_23', 'open_last_close_34', 'open_last_close_45', 'open_last_high', 'open_last_high_13', 'open_last_high_23', 'open_last_high_34', 'open_last_high_45', 'open_last_low', 'open_last_low_13', 'open_last_low_23', 'open_last_low_34', 'open_last_low_45', 'open_last_open', 'open_last_open_13', 'open_last_open_23', 'open_last_open_34', 'open_last_open_45', 'open_ma5', 'p_close', 'p_close16', 'p_close48', 'rsv', 'sRSI_20_cross_lRSI', 'sRSI_80_cross_lRSI', 'sRSI_down_cross_20', 'sRSI_down_cross_50', 'sRSI_up_cross_50', 'sRSI_up_cross_80', 'sRSI_z', 'sema', 'std', 'std_std_z_DOWN', 'std_std_z_UP', 'std_z', 'stock_code', 'sum1', 'sum2', 'sum3', 'sum4', 'v_dt_ma10', 'v_dt_ma20', 'v_dt_ma30', 'v_dt_ma5', 'v_dt_ma60', 'v_ma10', 'v_ma20', 'v_ma30', 'v_ma5', 'v_ma60', 'volume', 'volume_r', 'vv_dt_ma10', 'vv_dt_ma20', 'vv_dt_ma30', 'vv_dt_ma5', 'vv_dt_ma60', 'vv_ma10', 'vv_ma20', 'vv_ma30', 'vv_ma5', 'vv_ma60']
    #select rank names
    names=['New_H_20_5', 'New_L_10_5', 'ma10_angle2', 'low_last_open', 'ADX1', 'last_Close_dt_ma5', 'ma20_angle', 'high_last_high_23', 'CCI_z', 'kdj_30_min', 'MDI_z', 'highest_20_10', 'high_last_low_45', 'last_low_open', 'RSI1', 'low_last_high_13', 'high_last_open_13', 'ma30_angle2', 'kdj_30_max', 'AR', 'l_10_20', 'lema', 'low_last_close_23', 'kdj_60_min', 'PDI_z', 'high_last_low_34', 'MTR_D2', 'last3_open', 'New_L_10', 'low_last_close_13', 'RSI2', 'highestl_30', 'VR', 'low_last_low_34', 'D_z', 'last_close_high', 'ma5_z3', 'number_close_down_mean', 'New_L_20_20', 'close_last_high_13', 'v_ma5', 'New_Hl_20', 'kdj_10_max', 'New_H_30_20', 'New_H_60_10', 'last_high_ma5', 'New_Hl_60', 'New_H_30_10', 'MA2_z', 'PSY', 'New_Hl_5', 'New_L_20', 'CCI', 'kdj_5_30_up', 'highestl_5', 'Close_dt_ma5', 'ma5', 'New_H_30', 'last_close', 'high_last_open', 'ma30_z4', 'h_5_10', 'lastlow_ma5', 'close_last_low_45', 'New_H_20', 'New_L_30_10', 'low_last_low', 'close_last_low_23', 'ma10', 'New_L_20_10', 'open_last_high_34', 'ma30_z3', 'last5_low', 'ma20', 'p_close', 'New_Lh_5', 'low_last_high_45', 'open_last_low_45', 'low_last_close', 'lowesth_5', 'MA1', 'open_last_open_13', 'New_H_10_10', 'RSI1_1', 'dea_down_cross_0', 'open_last_high_23', 'last4_Close_dt_ma10', 'last3_volume', 'amount', 'm3', 'sum2', 'last_ma30_gt_ma60', 'ma5_z4', 'BR', 'ma60', 'New_L_10_10', 'high_last_close_34', 'New_H_60_5', 'close_last_open_34', 'New_L_30_5', 'abs', 'low_last_close_34', 'low_last_open_45', 'last_high_open', 'v_dt_ma20', 'macd_5_30_down', 'h_30_60', 'New_H_5_10', 'last3_low', 'kdj_5_60_up', 'high_last_high_45', 'New_L_5_20', 'last3_high', 'last4_volume', 'last_Close_dt_ma20', 'New_Lh_20', 'kdj_5_max', 'last_ma5_gt_ma10', 'close_last_close_45', 'TH_1', 'New_L_60_10', 'close_last_open_23', 'low_last_high_23', 'low_last_low_45', 'v_ma30', 'New_H_10', 'duotou_5_10_20', 'macd_5_60_down', 'New_H_20_20', 'ma20_z4', 'highestl_60', 'ma30_angle', 'high', 'std_std_z_UP', 'WR2', 'low_last_high', 'kdj_5_10_up', 'MA3', 'high_last_high_34', 'low_last_open_13', 'volume', 'close_last_close_13', 'last2_Close_dt_ma10', 'high_last_close_45', 'v_dt_ma5', 'New_L_5', 'MA1_z', 'last3_Close_dt_ma10', 'New_Lh_10', 'D', 'Close_dt_ma60', 'last2_high_low', 'open_last_high_13', 'open_last_high_45', 'New_H_30_5', 'New_H_5_5', 'MA3_z', 'open_last_close_34', 'ma20_z3', 'number_close_up_mean', 'ma10_z4', 'New_H_5', 'Close_dt_ma20', 'macd_5_10_down', 'PDI', 'New_Hl_30', 'close_last_high', 'high_last_open_45', 'CR_z', 'vv_dt_ma20', 'low_last_open_34', 'MTR_D3', 'close_last_low', 'New_L_60_5', 'lowesth_60', 'high_last_high', 'macd_5_down_sum', 'close_high', 'CR', 'open_last_low_23', 'New_H_60', 'J_z', 'DMP1', 'low_last_high_34', 'last10_low', 'high_list', 'change_r_next', 'open', 'New_H_60_20', 'New_L_60_20', 'MA2', 'kdj_60_max', 'last_close_ma5', 'last2_close_low', 'last_ma10_gt_ma20', 'kdj_5_60_down', 'last2_Close_dt_ma60', 'J', 'ma60_z4', 'WR2_z', 'New_L_5_10', 'PSY_1', 'close_last_open_13', 'sRSI_down_cross_50', 'v_dt_ma10', 'ma5_down_ma60_2', 'kdj_5_30_down', 'last2_low_open', 'macd_60_up_sum', 'std', 'highest_60', 'K', '_id', 'ma30', 'open_last_low_13', 'close_down_ma5', 'ma20_angle2', 'l_5_10', 'LD', 'h_10_20', 'std_z', 'DMM', 'vv_ma10', 'close_last_close', 'high_last_low_23', 'Close_dt_ma10', 'WR1', 'lRSI_z', 'last2_low', 'MDI', 'last20_low', 'ADX', 'New_L_30', 'high_last_close_23', 'diff_up_cross_dea', 'open_last_close_13', 'lowest_20_5', 'low_last_close_45', 'macd_q', 'm2', 'close_last_close_34', 'dea', 'last_Close_dt_ma60', 'BR_z', 'change_r', 'high_last_open_34', 'TL', 'last_low', 'New_L_20_5', 'last20_high', 'high_last_close_13', 'v_ma20', 'last2_close_open', 'ma60_z', 'ma10_angle', 'v_dt_ma30', 'macd_60_down_sum', 'open_last_close', 'open_last_open', 'ma60_angle', 'low_last_low_13', 'last_close_open', 'close_last_open_45', 'high_last_low_13', 'stock_code', 'l_30_60', 'high_last_close', 'v_ma10', 'RSI2_2', 'v_ma60', 'close_last_low_13', 'close_last_high_34', 'sema', 'last2_Close_dt_ma5', 'low_last_low_23', 'last3_Close_dt_ma20', 'open_last_low_34', 'New_Lh_60', 'vv_ma20', 'New_Hl_10', 'ma10_z3', 'high_last_high_13', 'open_last_close_45', 'low', 'New_H_10_5', 'last4_Close_dt_ma20', 'open_last_high', 'diff_down_cross_dea', 'ADX_z', 'WR1_z', 'last_high', 'highest_5_20', 'DMM1', 'PSY_z', 'New_L_5_5', 'close_down_ma60', 'macd_10_down_sum', 'vv_dt_ma60', 'open_last_low', 'highestl_20', 'New_H_10_20', 'open_last_open_23', 'close_last_low_34', 'last_open', 'kdj_5_10_down', 'highest_10_5', 'open_last_close_23', 'New_Lh_30', 'lowest_5_5', 'New_H_20_10', 'highest_10', 'New_L_10_20', 'close_last_open', 'last3_Close_dt_ma30', 'close_low', 'last_Close_dt_ma10', 'v_dt_ma60', 'vv_dt_ma10', 'last4_high', 'lowesth_30', 'RSI2_1', 'close_last_close_23', 'MTR_1', 'lowest_5_10', 'highest_30', 'RSI1_2', 'New_Highest_5', 'AR_z', 'ma60_z2', 'last5_high', 'close_last_high_45', 'last_volume', 'TQ', 'ma5_angle', 'high_last_low', 'sum4', 'highest_5_5', 'RSI3', 'last2_open', 'close_last_high_23', 'dea_up_cross_0', 'last4_Close_dt_ma60', 'close_up_ma5', 'lowest_60', 'New_L_60', 'lowest_10_5', 'open_ma5', 'sum3', 'volume_r', 'diff_up_cross_0', 'MTR_D1', 'highest_30_20', 'New_H_5_20', 'vv_dt_ma5', 'ma20_gt_ma30', 'vv_dt_ma30', 'Close_dt_ma30', 'last_Close_dt_ma30', 'DMP', 'sRSI_up_cross_80', 'lowesth_20', 'VR_80_150', 'ma60_angle3', 'last2_close', 'highest_20', 'ma5_z', 'm1', 'last2_volume', 'kdj_10_min', 'sum1', 'high_low', 'VR_160_450', 'last3_Close_dt_ma60', 'highest_5_10', 'h_20_30', 'lowest_30_5', 'last2_Close_dt_ma30', 'lowest_20_10', 'last2_Close_dt_ma20', 'lowest_30_20', 'high_open', 'ma30_angle4', 'last_open_ma5', 'highest_60_5', 'low_open', 'macd_z', 'ma60_angle4', 'last4_low', 'open_last_open_34', 'kdj_5_min', 'ma20_angle4', 'ma10_gt_ma20', 'TH', 'UB_z', 'lowest_5_20', 'lowest_10_10', 'RSI3_1', 'high_ma5', 'MTR_2', 'BOLL', 'TL_1', 'last4_close', 'high_last_open_23', 'highest_20_20', 'highest_30_5', 'macd_30_down_sum', 'LB', 'RSI3_2', 'New_L_30_20', 'last2_high_open', 'lowest_30', 'last_high_low', 'last3_close', 'last2_close_high', 'last_close_low', 'LB_z', 'last10_high', 'TYP', 'last4_Close_dt_ma5', 'highest_30_10', 'HD', 'ma20_angle3', 'MTR', 'sRSI_z', 'lowest_10', 'New_Highest_10', 'lowest_20', 'last3_Close_dt_ma5', 'highest_20_5', 'ma10_angle3', 'highest_10_10', 'highest_60_20', 'ma5_up_ma60_2', 'l_20_30', 'lowest_60_5', 'lowest_30_10', 'open_last_open_45', 'low_ma5', 'highest_60_10', 'macd_5_60_up', 'change_r_next16', 'ma30_angle3', 'last4_open', 'last4_Close_dt_ma30', 'ma5_z2', 'ma60_angle2', 'lowest_60_10', 'ma10_angle4', 'TYP_mean', 'macd_10_up_sum', 'ma10_z', 'ma30_z2', 'lowest_20_20', 'WR1_15_DOWN', 'mid', 'lowest_10_20', 'highestl_10', 'last_ma20_gt_ma30', 'kongtou_5_10_20', 'ma5_up_ma60_4', 'ma30_z', 'New_Highest_20', 'ma10_z2', 'ma60_z3', 'lowest_5', 'lowest_60_20', 'ma20_z2', 'highest_5', 'sRSI_up_cross_50', 'lowesth_10', 'ma30_gt_ma60', 'ma5_up_ma60_3', 'max2', 'ma20_z', 'New_Lowest_5', 'New_Highest_30', 'highest_10_20', 'macd_5_30_up', 'UB', 'low_last_open_23', 'sRSI_down_cross_20', 'last2_high', 'market', 'macd_30_up_sum', 'close_down_ma20', 'macd', 'max', 'macd_5_10_up', 'WR1_20_UP', 'low_list', 'New_Highest_60', 'close_up_ma20', 'ma5_up_ma20_4', 'WR1_85_UP', 'ma5_up_ma10', 'New_Lowest_10', 'CCI_100_DOWN', 'VR_40_70', 'sRSI_80_cross_lRSI', 'close_LB_DOWN', 'sRSI_20_cross_lRSI', 'ma5_down_ma60_4', 'close_open', 'WR1_80_DOWN', 'WR1_50_UP', 'ma5_down_ma60_3', 'macd_over_last_macd', 'J_down_cross_100', 'WR1_50_DOWN', 'J_over_80', 'CR_MA1_UP', 'ma5_down_ma10_2', 'ma5_angle4', 'close_UB_UP', 'close', 'ma5_down_ma10', 'ma5_up_ma60', 'CR_MA3_UP', 'CR_MA1_DOWN', 'ma5_angle2', 'ma5_up_ma30', 'dif', 'WR1_WR2_UP', 'BR_AR_UP', 'New_Lowest_20', 'New_Lowest_30', 'CCI_-100_UP', 'close_ma5', 'J_up_cross_0', 'ma5_down_ma20_2', 'close_up_ma30', 'date', 'ma5_down_ma30_4', 'close_down_ma30', 'PDI_MDI_UP', 'ma5_up_ma20', 'ma5_down_ma10_4', 'J_less_20', 'ma5_up_ma10_3', 'TQ_1', 'ADX_50_UP', 'dif_z', 'ma5_down_ma20_3', 'close_up_ma10', 'ma5_up_ma20_3', 'rsv', 'PDI_MDI_DOWN', 'ma5_down_ma20_4', 'ma5_up_ma10_4', 'ma5_angle3', 'ma5_up_ma10_2', 'ma5_up_ma30_2', 'ma5_up_ma20_2', 'VR_40_DOWN', 'VR_450_UP', 'dea_z', 'ma5_up_ma30_3', 'close_down_ma10', 'CR_40_UP', 'ma5_down_ma60', 'New_Lowest_60', 'AR_50_DOWN', 'ma5_down_ma10_3', 'CR_MA2_UP', 'p_close16', 'PSY_90_UP', 'ma5_gt_ma10', 'ma5_down_ma30_2', 'CR_MA3_DOWN', 'std_std_z_DOWN', 'PSY_10_DOWN', 'diff_down_cross_0', 'BR_AR_DOWN', 'ma5_down_ma30', 'ma5_down_ma20', 'AR_50_UP', 'ADX_50_DOWN', 'CR_40_DOWN', 'ma5_up_ma30_4', 'WR1_WR2_DOWN', 'CR_MA2_DOWN', 'p_close48', 'macd_5_up_sum', 'change_r_next48', 'close_up_ma60', 'ma5_down_ma30_3']

    # try  No20.
    names=names[0:20]
    li = [600000, 600008, 600009, 600010, 600011, 600015, 600016, 600018, 600019, 600023, 600025, 600028, 600029,
          600030,
          600031, 600036, 600038, 600048, 600050, 600061, 600066, 600068, 600085, 600089, 600100, 600104, 600109,
          600111,
          600115, 600118, 600153, 600157, 600170, 600176, 600177, 600188, 600196, 600208, 600219, 600221, 600233,
          600271,
          600276, 600297, 600309, 600332, 600339, 600340, 600346, 600352, 600362, 600369, 600372, 600373, 600376,
          600383,
          600390, 600398, 600406, 600415, 600436, 600438, 600482, 600487, 600489, 600498, 600516, 600518, 600519,
          600522,
          600535, 600547, 600549, 600570, 600583, 600585, 600588, 600606, 600637, 600660, 600663, 600674, 600682,
          600688,
          600690, 600703, 600704, 600705, 600739, 600741, 600795, 600804, 600809, 600816, 600820, 600837, 600867,
          600886,
          600887, 600893, 600900, 600909, 600919, 600926, 600958, 600959, 600977, 600999, 601006, 601009, 601012,
          601018,
          601021, 601088, 601099, 601108, 601111, 601117, 601155, 601166, 601169, 601186, 601198, 601211, 601212,
          601216,
          601225, 601228, 601229, 601238, 601288, 601318, 601328, 601333, 601336, 601360, 601377, 601390, 601398,
          601555,
          601600, 601601, 601607, 601611, 601618, 601628, 601633, 601668, 601669, 601688, 601718, 601727, 601766,
          601788,
          601800, 601808, 601818, 601828, 601838, 601857, 601866, 601877, 601878, 601881, 601888, 601898, 601899,
          601901,
          601919, 601933, 601939, 601958, 601985, 601988, 601989, 601991, 601992, 601997, 601998, 603160, 603260,
          603288,
          603799, 603833, 603858, 603993, 1, 2, 60, 63, 69, 100, 157, 166, 333, 338, 402, 413, 415, 423, 425, 503, 538,
          540,
          559, 568, 623, 625, 627, 630, 651, 671, 709, 723, 725, 728, 768, 776, 783, 786, 792, 826, 839, 858, 876, 895,
          898,
          938, 959, 961, 963, 983, 1965, 1979, 2007, 2008, 2024, 2027, 2044, 2050, 2065, 2074, 2081, 2085, 2142, 2146,
          2153,
          2202, 2230, 2236, 2241, 2252, 2294, 2304, 2310, 2352, 2385, 2411, 2415, 2450, 2456, 2460, 2466, 2468, 2470,
          2475,
          2493, 2500, 2508, 2555, 2558, 2572, 2594, 2601, 2602, 2608, 2624, 2625, 2673, 2714, 2736, 2739, 2797, 2925,
          300003, 300015, 300017, 300024, 300027, 300033, 300059, 300070, 300072, 300122, 300124, 300136, 300144,
          300251,
          300408, 300433]
    li = Stock.get_index_stock_code_list()
    # label='change_r_next16'
    label='change_r_next'

    def classify(self, x):
        return x // 50
    def get_data(self, start_date, end_date):
        print(start_date)
        curror = BaseModel('features_index_day').query(
            sql=dict(stock_code={'$in': model.li},
                     date={'$gte': start_date, '$lte': end_date}))
        if curror.count():
            data = pd.DataFrame(list(curror))

            data=data.loc[:,model.names+[model.label]]
            data = data.replace(to_replace=np.Infinity, value=np.NaN).dropna()
            # data['change_r_next16'] = data.change_r_next16.map(lambda x: 1 if x > 0 else 0)
            for cl in model.names:
                v=data[cl].iloc[0]
                # if type(v).__name__ !='bool':

                  # data[cl] = data.sort_values(by=[cl], ascending=False).index
                  # temp = data[cl].mean()
                  # data[cl] = data[cl].map(lambda x:1 if x>len(data)//2 else 0)
                  # pass
            y = data.loc[:, [model.label]]
            y['sort'] = y.sort_values(by=[model.label], ascending=False).index
            y = y.drop([model.label], axis=1)
            y['sort'] = y.sort.map(lambda x: self.classify(x))
            # y['sort'] = y.sort.map(lambda x:1 if x>len(y)/2 else 0)
            X=data.drop([model.label],axis=1)
            # X = data.loc[:, model.names]
            # X_test = data_test.loc[:, model.names]
            # y_test = data_test.loc[:, ['change_r_next16']]

            return X, y
        else:
            return pd.DataFrame([]), pd.DataFrame([])

    def get_data_for_selection(self, start_date, end_date):
        curror = BaseModel('novel_Feature').query(
            sql=dict(stock_code={'$in': model.li},
                     date={'$gte': start_date, '$lte': end_date}))
        if curror.count():
            data = pd.DataFrame(list(curror))

            data=data.loc[:,model.names]
            data = data.replace(to_replace=np.Infinity, value=np.NaN).dropna()
            # data['change_r_next16'] = data.change_r_next16.map(lambda x: 1 if x > 0 else 0)
            for cl in model.names:
                v=data[cl].iloc[0]
                # tp=type(v)
                # if type(v).__name__ !='bool':

                  # data[cl] = data.sort_values(by=[cl], ascending=False).index
            #       # temp = data[cl].mean()
            #       data[cl] = data[cl].map(lambda x:1 if x>len(data)//2 else 0)
            #       pass
            y = data.loc[:, [model.label]]
            y['sort'] = y.sort_values(by=[model.label], ascending=False).index
            y = y.drop([model.label], axis=1)
            y['sort'] = y.sort.map(lambda x: 1 if x > len(y) / 2 else 0)
            X = data.drop([model.label, 'date', '_id'], axis=1)
            return X, y
        else:
            return [], []

    def model_select(self, start_date, end_date):
        curror = BaseModel('calendar').query(sql=dict(date={'$gte': start_date, '$lte': end_date}))
        date_list = list(curror)

        n = 0
        x, y = list(), list()
        for i in range(len(date_list) - n):
            print(date_list[i]['date'])
            temp1, temp2 = self.get_data_for_selection(date_list[i]['date'], date_list[i + n]['date'])
            x.append(temp1)
            y.append(temp2)
        X = pd.concat(x)
        y = pd.concat(y)
        X = np.array(X)
        y = np.array(y)
        # Build a forest and compute the feature importances
        forest = ExtraTreesClassifier(criterion='entropy',n_estimators=250,
                                      random_state=0)
        forest.fit(X, y)
        importances = forest.feature_importances_
        std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                     axis=0)
        indices = np.argsort(importances)[::-1]

        # Print the feature ranking
        print("Feature ranking:")
        result = list()
        for f in range(X.shape[1]):
            print("%d. feature %d  %s (%f)" % (f + 1, indices[f], model.names[ indices[f]], importances[indices[f]]))
            result.append(model.names[ indices[f]])
        print(result)
        # Plot the feature importances of the forest
        plt.figure()
        plt.title("Feature importances")
        plt.bar(range(X.shape[1]), importances[indices],
                color="r", yerr=std[indices], align="center")
        plt.xticks(range(X.shape[1]), indices)
        plt.xlim([-1, X.shape[1]])
        plt.show()

    def train(self, clf, X, y):
        print('x_t', len(X))
        clf = clf.fit(X, y)  # 此时完成训练
        return clf

    def save(self, clf, train_model_name):
        joblib.dump(clf, train_model_name)

    def is_exist(self, train_model_name):
        return os.path.exists(train_model_name)

    def get(self, train_model_name):
        if self.is_exist(train_model_name):
            clf = joblib.load(train_model_name)
        else:
            clf = None
        return clf

    def exe(self, clf, start_date, end_date):
        # clf = self.get(train_model_name)
        X, y = self.get_data(start_date, end_date)
        if len(X):
            clf = self.train(clf, X, y)
        return clf
            # self.save(clf, train_model_name)
            # model().report(train_model_name,  dt.datetime(2018, 1, 3),  dt.datetime(2018, 1, 3))

    def report(self, clf, start_date, end_date):
        curror = BaseModel('calendar').query(sql=dict(date={'$gte': start_date, '$lte': end_date}))
        date_list = list(curror)

        n = 0
        x, y = list(), list()
        for i in range(len(date_list) - n):
            print(date_list[i]['date'])
            temp1, temp2 = self.get_data(date_list[i]['date'], date_list[i + n]['date'])
            x.append(temp1)
            y.append(temp2)

        X_test, y_test = pd.concat(x), pd.concat(y)
        y_pred = clf.predict(X_test)  # 预测
        result = classification_report(y_test, y_pred)
        print(result)
        print(clf.score(X_test, y_test))

    def visualization(self, clf):
        dot_data = tree.export_graphviz(clf, out_file=None)
        graph = pydotplus.graph_from_dot_data(dot_data)
        graph.write_png("tree.png")  # 生成png文件

def gt():
    start_date = dt.datetime(2018, 5, 24)
    end_date = dt.datetime(2018, 6, 2)
    curror = BaseModel('calendar').query(sql=dict(date={'$gte': start_date, '$lte': end_date}))
    date_list = list(curror)
    obj = model()
    n = 0
    # clf = SGDClassifier()
    # clf = DecisionTreeClassifier(min_samples_leaf=20)
    X = list()
    Y = list()
    for i in range(len(date_list) - n):
        # print(date_list[i]['date'])
        temp1, temp2 = obj.get_data(date_list[i]['date'], date_list[i]['date'])
        X.append(temp1)
        Y.append(temp2)
    X_train = pd.concat(X)
    Y_train = pd.concat(Y)
    return  np.array(X_train),np.array(Y_train)

if __name__ == '__main__':
    pass
    # feature select===========================================================================
    # start_date = dt.datetime(2018, 1, 1)
    # end_date = dt.datetime(2018, 1, 23)
    # model().model_select(start_date, end_date)
    # feature select===========================================================================
    print(__doc__)
    from time import time

    import numpy as np
    from scipy import ndimage
    from matplotlib import pyplot as plt
    from sklearn import manifold, datasets
    # digits = datasets.load_digits(n_class=10)
    # X = digits.data
    # y = digits.target

    data=BaseModel('a_ma_index_min5_gru_128').query(sql={'date':{'$lte':dt.datetime(2018,8,9,9,55),'$gte':dt.datetime(2018,1,1,9,55)}})
    data=pd.DataFrame(list(data))
    data2=data.groupby(by=['type']).agg({'profit':'mean'})
    data2=data2.sort_values(by=['profit'],ascending=False)

    X=np.array(data.encode.tolist())
    y=np.array(data.type)
    # X,y=gt()
    # y=np.array(300)
    n_samples, n_features = X.shape
    np.random.seed(0)
    def nudge_images(X, y):
        # Having a larger dataset shows more clearly the behavior of the
        # methods, but we multiply the size of the dataset only by 2, as the
        # cost of the hierarchical clustering methods are strongly
        # super-linear in n_samples
        shift = lambda x: ndimage.shift(x.reshape((8, 8)),
                                        .3 * np.random.normal(size=2),
                                        mode='constant',
                                        ).ravel()
        X = np.concatenate([X, np.apply_along_axis(shift, 1, X)])
        Y = np.concatenate([y, y], axis=0)
        return X, Y
    # X, y = nudge_images(X, y)


    # ----------------------------------------------------------------------
    # Visualize the clustering

    def plot_clustering(X_red, X, labels, title=None):
        x_min, x_max = np.min(X_red, axis=0), np.max(X_red, axis=0)
        X_red = (X_red - x_min) / (x_max - x_min)
        plt.figure(figsize=(6, 4))
        result={}
        for i in range(X_red.shape[0]):

            itype=(plt.cm.nipy_spectral(labels[i] / 10.))
            itype=str(itype[0])+'_'+str(itype[1])+'_'+str(itype[2])
            itype=itype.replace('.','')
            plt.text(X_red[i, 0], X_red[i, 1], str(y[i]),
                     color=plt.cm.nipy_spectral(labels[i] / 10.),
                     fontdict={'weight': 'bold', 'size': 9})
            if itype not in result.keys():
                # print(itype,result.keys())
                result[itype] = [i]
            else:

                result[itype].append(i)

        li=[]
        for key in result:
            sum=0
            for i in result[key]:
                sum+=data[data.index==i].profit.iloc[0]
            li.append(sum/len(result[key]))
        # print(len(li),len(data2))
        data3=pd.DataFrame([])
        li.sort(reverse=True)
        data3['profit2']=li
        li2=list(data2.profit)
        li2.sort(reverse=True)
        data3['profit']=li2+['-']*(len(li)-len(li2))

        print(data3)
        plt.xticks([])
        plt.yticks([])
        if title is not None:
            plt.title(title, size=17)
        plt.axis('off')
        plt.tight_layout()

    # ----------------------------------------------------------------------
    # 2D embedding of the digits dataset
    print("Computing embedding")
    X_red = manifold.SpectralEmbedding(n_components=2).fit_transform(X)
    # X_red = manifold.TSNE(n_components=2).fit_transform(X)
    print("Done.")
    from sklearn.cluster import AgglomerativeClustering
    # name= ('ward', 'average', 'complete')
    for linkage in ['ward']:
        clustering = AgglomerativeClustering(linkage=linkage, n_clusters=10)
        t0 = time()
        clustering.fit(X_red)
        print("%s : %.2fs" % (linkage, time() - t0))
        plot_clustering(X_red, X, clustering.labels_, "%s linkage" % linkage)
    # plt.show()