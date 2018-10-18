from Calf.models.base_model import BaseModel
from jqdatasdk import *

auth('18623166973', 'zjf950613')
# q = query(valuation).filter(valuation.code == '000001.XSHE')
# df = get_fundamentals(q, '2015-10-15')
# # 打印出总市值
# print(df['market_cap'][0])
name=['2016q1','2016q2','2016q3','2016q4','2017q1','2017q2','2017q3','2017q4','2018q1','2018q2']
for i in ['2015q4']:
    df = get_fundamentals(query(
    valuation.code,
    valuation.day,
    valuation.capitalization,
    valuation.circulating_cap,
    valuation.market_cap,
    valuation.circulating_market_cap,
    valuation.turnover_ratio,
    valuation.pe_ratio,
    valuation.pe_ratio_lyr,
    valuation.pb_ratio,
    valuation.ps_ratio,
    valuation.pcf_ratio,
    ), statDate=i)
    df['code']=df.code.map(lambda x:x[0:6])
    df['date']=i

    BaseModel('jq_fund_data').insert_batch(df.to_dict(orient='records'))
