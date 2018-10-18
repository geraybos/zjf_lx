import tushare as ts
from Calf import ModelData
class Fundamental:
    @classmethod
    def get_stock_basics(cls):#上市公司基本情况
        data=ts.get_stock_basics()
        data['code']=data.index
        data.reset_index(drop=True,inplace=True)
        ModelData.remove_data(table_name='stock_basics')
        print('remove success')
        ModelData.insert_data(table_name='stock_basics', data=data)
        print('write success')
    @classmethod
    def get_report_data(cls,year,quarter):#业绩报表数据
        data=ts.get_report_data(year, quarter)
        data['year']=year
        data['quarter']=quarter
        data.reset_index(drop=True, inplace=True)
        ModelData.remove_data(table_name='report_data',year=year,quarter=quarter)
        print('remove success')
        ModelData.insert_data(table_name='report_data', data=data)
        print('write success')
        # print(data.head(5))
    @classmethod
    def get_profit_data(cls, year, quarter):#反应盈利能力的
        data = ts.get_profit_data(year, quarter)
        data['year'] = year
        data['quarter'] = quarter
        data.reset_index(drop=True, inplace=True)
        ModelData.remove_data(table_name='profit_data',year=year,quarter=quarter)
        print('remove success')
        ModelData.insert_data(table_name='profit_data', data=data)
        print('write success')
        print(data.head(5))

    @classmethod
    def get_operation_data(cls, year, quarter):  # 营运能力数据
        data = ts.get_operation_data(year, quarter)
        data['year'] = year
        data['quarter'] = quarter
        data.reset_index(drop=True, inplace=True)
        ModelData.remove_data(table_name='operation_data',year=year,quarter=quarter)
        print('remove success')
        ModelData.insert_data(table_name='operation_data', data=data)
        print('write success')
        # print(data.head(5))
    @classmethod
    def get_growth_data(cls, year, quarter):  # 营运能力数据
        data = ts.get_growth_data(year, quarter)
        data['year'] = year
        data['quarter'] = quarter
        data.reset_index(drop=True, inplace=True)
        ModelData.remove_data(table_name='growth_data',year=year,quarter=quarter)
        print('remove success')
        ModelData.insert_data(table_name='growth_data', data=data)
        print('write success')

    @classmethod
    def get_debtpaying_data(cls, year, quarter):  # 偿债能力数据
        data = ts.get_debtpaying_data(year, quarter)
        data['year'] = year
        data['quarter'] = quarter
        data.reset_index(drop=True, inplace=True)
        ModelData.remove_data(table_name='debtpaying_data',year=year,quarter=quarter)
        print('remove success')
        ModelData.insert_data(table_name='debtpaying_data', data=data)
        print('write success')
    @classmethod
    def get_cashflow_data(cls,year,quarter):
        data=ts.get_cashflow_data(year,quarter)
        data['year'] = year
        data['quarter'] = quarter
        data.reset_index(drop=True, inplace=True)
        ModelData.remove_data(table_name='cashflow_data',year=year,quarter=quarter)
        print('remove success')
        ModelData.insert_data(table_name='cashflow_data', data=data)
        print('write success')
        # print(data.head(5))

#
# all fund data from tushare
# Fundamental.get_stock_basics()
li=[2010,2011,2012,2013,2014,2015,2016,2017]

# ModelData.remove_data(table_name='report_data',year=2018,quarter=2)
# li=[2018]
for y in li:
    for q in [1,2,3,4]:
        Fundamental.get_cashflow_data(year=y,quarter=q)
        Fundamental.get_debtpaying_data(year=y,quarter=q)
        Fundamental.get_growth_data(year=y,quarter=q)
        Fundamental.get_operation_data(year=y,quarter=q)
        Fundamental.get_profit_data(year=y,quarter=q)
        Fundamental.get_report_data(year=y,quarter=q)


