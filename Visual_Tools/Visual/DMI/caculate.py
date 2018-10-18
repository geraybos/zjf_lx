class Caculate:
    @classmethod
    def n_DMI(clf,data, interval,detal,N1=14, M1=6):
        data["close2"] = data.close.shift(-interval)
        data["close3"] = data.close.shift(detal)
        data['profit'] = data.close2 / data.close - 1
        data['profit_self'] = data.close / data.close3 - 1

        data['last_close']=data.close.shift(1)
        data['last_high']=data.high.shift(1)
        data['last_low']=data.low.shift(1)



        data['MTR_D1'] = data['high'] - data['low']
        data['MTR_D2'] = abs(data['high'] - data.last_close)
        data['MTR_D3'] = abs(data.last_close - data['low'])
        data['MTR_1'] = data['MTR_D2']
        data.loc[data['MTR_D1'] > data['MTR_D2'], 'MTR_1'] = data['MTR_D1']
        # data['MTR_1'] = data.apply(lambda x: x['MTR_D1'] if x['MTR_D1'] > x['MTR_D2']  else x['MTR_D2'], axis=1)

        # 要删除的第一个属性
        data['MTR_2'] = data['MTR_D3']
        data.loc[data['MTR_1'] > data['MTR_D3'], 'MTR_2'] = data['MTR_1']
        # data['MTR_2'] = data.apply(lambda x: x['MTR_1'] if x['MTR_1'] > x['MTR_D3']  else x['MTR_D3'], axis=1)

        # roolling 必须依赖于 transform 才行，只能是先生成一列，然后在抛弃
        # roolling 操作要先进行反转才能。因为rolling操作会空前N行
        # data = data[::-1]

        data['MTR'] = data['MTR_2'].rolling(window=N1).sum()

        data['HD'] = data['high'] - data.last_high
        data['LD'] = data.last_low - data['low']

        # HD1 = np.where(HD <= 0, 0, HD)
        # data['DMP1'] = np.where(HD1 <= LD, 0, HD1)
        data['DMP1'] = 0
        data.loc[(data['HD'] > 0) & (data['HD'] > data['LD']), 'DMP1'] = data['HD']

        data['DMP'] = data['DMP1'].rolling(window=N1).sum()

        # LD1 = np.where(LD <= 0, 0, LD)
        # data['DMM1'] = np.where(LD1 <= HD, 0, LD1)
        data['DMM1'] = 0
        data.loc[(data['LD'] > 0) & (data['LD'] > data['HD']), 'DMM1'] = data['LD']

        data['DMM'] = data['DMM1'].rolling(window=N1).sum()

        data['PDI'] = data['DMP'] * 100 / data['MTR']
        data['MDI'] = data['DMM'] * 100 / data['MTR']

        # 要删除的第4个属性
        data['ADX1'] = abs(data['MDI'] - data['PDI']) / (data['MDI'] + data['PDI']) * 100

        data['ADX'] = data['ADX1'].rolling(window=M1).mean()
        # data = data[::-1]

        # data['PDI_z'] = last_n(data, 1, 'PDI')
        # data['MDI_z'] = last_n(data, 1, 'MDI')
        # data['ADX_z'] = last_n(data, 1, 'ADX')
        #
        # data = cross(data, 'PDI_z', 'MDI_z', 'PDI', 'MDI', 'PDI_MDI_UP', 'PDI_MDI_DOWN')
        #
        # data['ADX_50_DOWN'] = (data.ADX < 50) & (50 < data.ADX_z)
        # data['ADX_50_UP'] = (data.ADX > 50) & (50 > data.ADX_z)

        # data.drop(
        #     ['MTR_2', 'MTR', 'HD', 'LD', 'MTR_D1', 'MTR_D2', 'MTR_1', 'MTR_D3', 'DMP1', 'DMP', 'DMM', 'DMM1', 'ADX1', 'PDI',
        #      'MDI', 'ADX', 'PDI_z', 'MDI_z', 'ADX_z'],
        #     axis=1, inplace=True)
        # data.fillna(0, inplace=True)
        data.dropna(inplace=True)
        return data

