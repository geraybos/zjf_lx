
from pytdx.hq import TdxHq_API
from pytdx.pool.hqpool import TdxHqPool_API
from pytdx.pool.ippool import AvailableIPPool
from pytdx.config.hosts import hq_hosts
import random
import logging
import pprint

import tushare as ts
def get_all_stock():
    df = ts.get_stock_basics()
    df['stock'] = df.index
    df = df.sort_values(by=['stock'], ascending=True)
    df['stock']=df.stock.map(lambda x:(1if str(x).startswith('60')else 0,x))
    return df['stock'].tolist()


if __name__ == '__main__':
    stocks=get_all_stock()
    api = TdxHq_API()
    if api.connect('119.147.212.81', 7709):
        data=api.get_security_quotes(stocks[0:200])
        print(data)
        api.disconnect()

    # ips = [(v[1], v[2]) for v in hq_hosts]
    # # 获取5个随机ip作为ip池
    # random.shuffle(ips)
    # ips5 = ips[:5]
    #
    # ## IP 池对象
    # ippool = AvailableIPPool(TdxHq_API, ips5)
    #
    # ## 选出M, H
    # primary_ip, hot_backup_ip = ippool.sync_get_top_n(2)
    #
    # print("make pool api")
    # ## 生成hqpool对象，第一个参数为TdxHq_API后者 TdxExHq_API里的一个，第二个参数为ip池对象。
    # api = TdxHqPool_API(TdxHq_API, ippool)
    #
    # ## connect 函数的参数为M, H 两组 (ip, port) 元组
    # with api.connect(primary_ip, hot_backup_ip):
    #     ## 这里的借口和对应TdxHq_API 或者 TdxExHq_API里的一样，我们通过反射调用正确的接口
    #     ret = api.get_security_quotes(stocks)
    #
    #     print("send api call done")
    #     pprint.pprint(ret)



