from urllib.request import urlopen

from Calf.models.calendar1 import Calendar
from Calf.models.base_model import BaseModel
import pandas as pd
import datetime as dt

class fundmental:
    def get_sn_now_price_data(self, codes):
        #http://hq.sinajs.cn/rn=1318986628214&list=USDCNY,USDHKD,EURCNY,GBPCNY,USDJPY,EURUSD,GBPUSD 外汇
        #http://hq.sinajs.cn/list=hk00001 港股
        #http://hq.sinajs.cn/list=sz000001 A股
        #http://hq.sinajs.cn/list=gb_tex 美股
        try:
            html = urlopen('http://hq.sinajs.cn/list={}'.format(codes)).read()
            data_l = html.decode('gbk').split('\n')
        except Exception as e:
            print(e)
        i = 0
        res = list()
        res2 = list()
        codes=codes.split(',')
        for data in data_l:
            if len(data):
                d = data.split('="')
                vals = d[1][:-2].split(',')
                res.append(float(vals[self.jug_market(codes[i])]))
                res2.append((vals[self.jug_market_for_name(codes[i])]))
                i = i + 1
        return res,res2

    def get_stock_basics(self,condition):
        curror = BaseModel('stock_basics').query(condition, {'_id': 0, 'classtype': 0})
        return pd.DataFrame(list(curror))

    def get_report_data(self,condition):
        curror=BaseModel('report_data').query(condition,{'_id':0,'classtype':0})
        return pd.DataFrame(list(curror))

    def chose_report_data(self):
        data = self.get_report_data(condition=dict(year={'$gte': 2018}))
        print(data.code.count())
        data = data[data['net_profits'] > 300000]
        print(data.code.count())
        data = data[data['profits_yoy'] > 10]
        print(data.code.count())
        data = data[data['roe'] > 5]
        print(data.code.count())
        # data['distrib']=data.distrib.map(lambda x:len(str(x))>3)
        # data=data[data['distrib']==True]
        data = data.sort_values(by=['roe'], ascending=False)
        print(data.head(20))
        print(data.code.count())
        print(data.code.tolist())

    def get_growth_data(self, condition):
        curror = BaseModel('growth_data').query(condition, {'_id': 0, 'classtype': 0})
        return pd.DataFrame(list(curror))

    def chose_growth_data(self):
        data=self.get_growth_data(condition=dict(year={'$gte': 2018}))
        print(data.code.count())
        data=data[data['mbrg']>50]
        data=data[data['nav']>30]
        data=data[data['targ']>30]
        data=data[data['epsg']>100]
        data=data[data['seg']>30]
        data=data.sort_values(by=['nprg'],ascending=False)
        data=data.loc[:,['year','quarter','code']]
        print(data.head(20))
        print(data.code.count())

    def get_profit_data(self, condition):
        curror = BaseModel('profit_data').query(condition, {'_id': 0, 'classtype': 0})
        return pd.DataFrame(list(curror))

    def chose_profit_data(self):
        data=self.get_profit_data(condition=dict(year={'$gte': 2018}))
        print(data.code.count())
        data = data[data['net_profit_ratio'] > 10]
        data = data[data['gross_profit_rate'] > 30]
        data = data[data['net_profits'] > 30000/4]
        data = data[data['business_income'] > 3000/4]
        data = data.sort_values(by=['roe'], ascending=False)
        print(data.head(20))
        print(data.code.count())

    def get_cashflow_data(self,condition):
        curror = BaseModel('cashflow_data').query(condition, {'_id': 0, 'classtype': 0})
        return pd.DataFrame(list(curror))

    def chose_cashflow_data(self):
        obj = BaseModel('cashflow_data')
        condition = dict(year={'$gte': 2018}, quarter=2)
        curror = BaseModel('cashflow_data').query(condition, {'_id': 0, 'classtype': 0})
        data = list(curror)
        data = sorted(data, key=lambda x: (x['cf_sales']), reverse=True)
        data = sorted(data, key=lambda x: (x['rateofreturn']), reverse=True)
        data = sorted(data, key=lambda x: (x['cf_nm']), reverse=True)
        data = sorted(data, key=lambda x: (x['cf_liabilities']), reverse=True)
        data = sorted(data, key=lambda x: (x['cashflowratio']), reverse=True)
        data = pd.DataFrame(data)
        print(data.code.tolist()[0:21])

    def chose_report_data2(self):

        data0 = self.get_report_data(condition=dict(year={'$gte': 2018}, quarter=2))
        data = self.get_report_data(condition=dict(year={'$gte': 2017}))
        data1 = self.get_stock_basics(condition={})
        # print(data1.head())

        data['is_distrib'] = data.distrib.map(lambda x: True if len(str(x)) > 3 else False)
        data = data.groupby(by=['code'], as_index=False).agg({'is_distrib': 'sum'})
        data = data[data.is_distrib >= 1]
        data = pd.merge(data, data0, on=['code'])
        # print(data1.columns.values)
        data = pd.merge(data, data1.loc[:, ['code', 'pe', 'undp', 'industry']], on=['code'])
        data = data[data.pe < 10]
        data = data[data.pe > 0]
        data = data[data.profits_yoy > 1.5]
        # print(data.columns.values)
        data = data.sort_values(by=['roe'], ascending=False)
        data = data.loc[:, ['code', 'industry']]
        print(data.head(20))
        print(data.code.count())

    def jug_market(self, code):
        if 'gb' in code:
            return 1
        elif 'hk' in code:
            return 6
        else:
            return 3

    def jug_market_for_name(self, code):
       return  1 if 'hk' in code else 0

    def cal_profit(self,data):
        obj2 = BaseModel('kline_day')
        data['buy_price'] = None
        data['now_price'] = None

        for i, r in data.iterrows():
            date = Calendar.recent(r.date)['date']
            curror=obj2.query(dict(date=date, stock_code=r.code))
            if curror.count():
                data.at[i, ['buy_price']] = list(obj2.query(dict(date=date, stock_code=r.code)))[0]['close']
            else:
                data.at[i, ['buy_price']] = 0.000000000001

        stocks = data.code.tolist()
        stocks = list(map(lambda x: 'sh' + str(x) if str(x).startswith('6') else 'sz' + x, stocks))
        stocklist, names = self.get_sn_now_price_data(','.join(stocks))
        data['now_price'] = stocklist
        data['name'] = names
        data['profit'] = data.now_price / data.buy_price - 1
        return data

    def report_data_analysis(self):

        data0 = self.get_report_data(condition=dict(year={'$gte': 2018}, quarter=2))
        data = self.get_report_data(condition=dict(year={'$gte': 2016}))

        data['is_distrib'] = data.distrib.map(lambda x: True if len(str(x)) > 3 else False)
        data = data.groupby(by=['code'], as_index=False).agg({'is_distrib': 'sum'})
        data = data[data.is_distrib >= 3]
        data = pd.merge(data, data0, on=['code'])
        data = data[data['profits_yoy'] > 0]
        data = data[data['eps_yoy'] > 0]
        data = data.sort_values(by=['roe'], ascending=False)

        data['date'] = data.report_date.map(lambda x: dt.datetime(2018, int(x.split('-')[0]), int(x.split('-')[1])))
        # data['date']=data.report_date.map(lambda x:Calendar.recent(_date=x)['date'])
        data = data.loc[:, ['code', 'date']]
        data = self.cal_profit(data=data)
        print(data.head(20))
        print(data.code.count())




if __name__ == '__main__':
    # fundmental().chose_report_data()  #季报
    # fundmental().chose_growth_data()  #成长能力
    # fundmental().chose_profit_data()    #盈利能力
    # fundmental().chose_cashflow_data()  #现金流量
    fundmental().report_data_analysis()  #基本面

    # from jqdatasdk import *
    # auth('18623166973', 'zjf950613')
    # # q = query(valuation).filter(valuation.code == '000001.XSHE')
    # # df = get_fundamentals(q, '2015-10-15')
    # # # 打印出总市值
    # # print(df['market_cap'][0])
    # df = get_fundamentals(query(
    #     valuation.code,
    #     indicator.inc_revenue_year_on_year,
    #     indicator.operation_profit_to_total_revenue,
    #     indicator.inc_revenue_annual,
    #     indicator.inc_net_profit_annual,
    #     indicator.gross_profit_margin,
    #     valuation.circulating_market_cap
    # ).filter(
    #     valuation.circulating_market_cap > 300,
    #     indicator.inc_revenue_year_on_year >=0.25,
    #     indicator.operation_profit_to_total_revenue>=0.20,
    #     indicator.inc_revenue_annual >=0.15,
    #     indicator.inc_net_profit_annual >=0.15,
    #     indicator.gross_profit_margin >=0.25,
    #
    # ).order_by(
    #     # 按市值降序排列
    #     valuation.circulating_market_cap.desc()
    # ).limit(
    #     # 最多返回100个
    #     100
    # ), statDate='2018q2')
    # df['code']=df.code.map(lambda x:str(x)[0:-5])
    # print(df.loc[:,['code']])









