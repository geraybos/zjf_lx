# import pyqtgraph.examples
# pyqtgraph.examples.run()
# import matplotlib.pyplot as plt
# import numpy as np
#
# def check_chart(file_name):
#     x=np.load(file_name)
#     plt.matshow(x, cmap='hot')
#     plt.show()
# check_chart("//DESKTOP-4JKCMO0/zjf1/USA_boll_kline_day/2018-06-19_TWOU_-0.11759089423371627.npy")
import multiprocessing
from email.parser import Parser
from urllib.request import urlopen

import requests
from Calf.data import ModelData

from Calf.models.base_model import BaseModel
from lxml import etree
import datetime as dt

from Calf.models.calendar1 import Calendar
from Stock.Stock import Stock


class Fund:
    @classmethod
    def crawl(cls, url, params):
        return requests.get(url, params=params)

    @classmethod
    def get_ttm(cls, p_type):
        url = 'http://www.csindex.com.cn/zh-CN/downloads/industry-price-earnings-ratio'
        params = {'type': p_type + '2', 'date': dt.datetime(2018, 7, 30)}
        # obj = model_list['fund_{}_ttm'.format(p_type)]

        e = Fund.crawl(url, params)
        html = etree.HTML(e.text)
        name_data = html.xpath('//table[@class="list-div-table"]//span')
        list_name = [_.text for _ in name_data]
        sp_data = html.xpath('//table[@class="list-div-table"]//tbody//tr//td//div//a')
        list_sp = [_.text for _ in sp_data]
        normal_data = html.xpath('//table[@class="list-div-table"]//tbody//tr//td//div')
        list_normal = [_.text for _ in normal_data]
class SnWeb:
    url = 'https://hq.sinajs.cn/?_=0.06679163577256908&list=rt_hk00001'
    def crawl(self, url, params):
        return requests.get(url, params)
    def get_sina_data(self):
        e = self.crawl(url=self.url, params={})
        data = e.text
        # data=data.replace('\n','')
        print(data)
        # html = etree.HTML(data)
        # data=html.xpath('//div[@class="deta03 clearfix"]/ul')
        # data=data[0].xpath('./li')
        # list_name = [_.text for _ in data]
        # print(list_name)
    def get_sn_rt_data(self, codes):
        # http://hq.sinajs.cn/rn=1318986628214&list=USDCNY,USDHKD,EURCNY,GBPCNY,USDJPY,EURUSD,GBPUSD 外汇
        # http://hq.sinajs.cn/list=hk00001 港股
        # http://hq.sinajs.cn/list=sz000001 A股
        # http://hq.sinajs.cn/list=gb_tex 美股
        # rt_hk00001,rt_hk00700
        data_l = None
        try:
            html = urlopen('https://hq.sinajs.cn/?_=0.06679163577256908&list={}'.format(codes)).read()
            data_l = html.decode('gbk').split('\n')
        except Exception as e:
            print(e)
        i = 0

        codes = codes.split(',')
        date = Calendar.today()
        result = list()
        for data in data_l:
            if len(data):
                print(codes[i])
                d = data.split('="')
                vals = d[1][:-2].split(',')
                print(vals)
                result.append(dict(date=date, stock_code=codes[i][5:], volume=int(vals[12]),
                                   high=float(vals[4]), amount=float(vals[11]), low=float(vals[5]),
                                   close=float(vals[6]),
                                   open=float(vals[2])))
                i = i + 1
        return result


class IbData:
    def get_data(self, no):
        url = 'https://www.interactivebrokers.com/cn/index.php?f=2222&exch=ibfxpro&showcategories=FX&p=&cc=&limit=100&page=' + str(
            no)
        data = requests.get(url=url, params={}).content
        e = etree.HTML(data)
        data = e.xpath('//table[@class="table table-striped table-bordered"]')
        data = data[2].xpath('./tbody/tr')
        result = list()
        for idata in data:
            item = idata.xpath('./td')
            result.append(item[0].text)
        return (result)


# data=list()
# obj=IbData()
#
# x1=(obj.get_data(no=1))
# x2=obj.get_data(no=2)
# print(x1)
# print(x2)

class Outstanding:
    url = 'http://web-f10.gaotime.com/stock/{}/gbjg/lngbbd.html'
    def scrawl(self, url, parameter):
        return requests.get(url, parameter)

    def get_data(self, stock):
        url = self.url.format(stock)
        html = self.scrawl(url, parameter={})
        e = etree.HTML(html.content)
        text = e.xpath("//table[@class='tab01']/tbody/tr")
        result = list()
        for _text in text:
            temp = _text.xpath('./td')

            t=temp[0].text.split('-')
            if '-' not in temp[3].text:
             result.append(dict(
                               date=dt.datetime(int(t[0]),int(t[1]),int(t[2])),
                               all_capital=float(temp[1].text),
                               flow_capital=float(temp[2].text),
                               true_flow_capital=float(temp[3].text),
                               reason=temp[4].text,
                               stock_code=stock
                                )
                            )
        return result

def fun(stocks):
    obj=Outstanding()
    result=list()
    for sc in stocks:
        data=[]
        try:
            print('success', sc)
            data=(obj.get_data(stock=sc))
        except Exception as e:
            print('fail',sc)
            pass
        finally:
            result.extend(data)
    BaseModel('outstanding').remove({})
    BaseModel('outstanding').insert_batch(result)

if __name__ == '__main__':
    stocks = Stock.get_all_stock()
    pool = multiprocessing.Pool(processes=3)
    m = 10
    li = [stocks[i:i + m] for i in range(0, len(stocks), m)]
    result = pool.map(fun, li)


# Outstanding().get_data(stock='000001')
# start_date = dt.datetime.strptime("2018-05-05", "%Y-%m-%d")
# import pandas as pd
# ModelData(location='server_db',dbname='big-data').insert_data(table_name='userinfo',data=pd.DataFrame([{'name':'liuxiaoju','password':'liuxiaoju'}]))
# ModelData.insert_data(table_name='userinfo',data=pd.DataFrame([{'name':'zjf','password':'zjf'}]))
# data=['399001', '399106', '399005', '399101', '399006', '399102', '399303', '000001', '000300', '000905', '000016', '880578', '880579', '880577', '880574', '880575', '880572', '880573', '880570', '880571', '880400', '880368', '880503', '880502', '880501', '880507', '880506', '880505', '880504', '880489', '880482', '880483', '880486', '880361', '880484', '880485', '880409', '880477', '880476', '880474', '880473', '880472', '880471', '880374', '880375', '880372', '880373', '880626', '880627', '880624', '880625', '880622', '880623', '880620', '880621', '880628', '880629', '880394', '880392', '880393', '880390', '880391', '880398', '880399', '880530', '880653', '880652', '880651', '880650', '880657', '880656', '880655', '880654', '880929', '880659', '880658', '880928', '880431', '880430', '880921', '880228', '880211', '880210', '880219', '880990', '880991', '880992', '880661', '880448', '880446', '880447', '880444', '880445', '880442', '880443', '880440', '880441', '880533', '880439', '880438', '880536', '880537', '880534', '880535', '880925', '880432', '880927', '880926', '880437', '880920', '880923', '880922', '880213', '880212', '880668', '880669', '880217', '880216', '880215', '880214', '880662', '880663', '880660', '880218', '880666', '880667', '880664', '880665', '880327', '880326', '880325', '880324', '880321', '880320', '880329', '880328', '880569', '880568', '880564', '880567', '880566', '880560', '880563', '880468', '880318', '880319', '880312', '880313', '880310', '880311', '880491', '880490', '880493', '880492', '880494', '880497', '880402', '880403', '880369', '880401', '880406', '880407', '880363', '880362', '880408', '880360', '880367', '880366', '880364', '880635', '880634', '880637', '880636', '880631', '880630', '880633', '880632', '880639', '880638', '880387', '880229', '880381', '880380', '880383', '880382', '880222', '880223', '880220', '880221', '880226', '880227', '880224', '880225', '880478', '880462', '880541', '880540', '880424', '880425', '880426', '880420', '880421', '880930', '880548', '880594', '880595', '880596', '880597', '880459', '880591', '880989', '880988', '880455', '880986', '880985', '880984', '880983', '880599', '880453', '880452', '880909', '880855', '880202', '880203', '880918', '880919', '880523', '880522', '880525', '880524', '880527', '880526', '880910', '880911', '880912', '880913', '880915', '880916', '880917', '880679', '880678', '880671', '880670', '880673', '880672', '880675', '880674', '880677', '880676', '880588', '000001', '880350', '880351', '880355', '000300', '880558', '880559', '880550', '880551', '880552', '880553', '880554', '880556', '880557', '880954', '880950', '880951', '880952', '880953', '880308', '880305', '880307', '880306', '880301', '880303', '880302', '880411', '880410', '880413', '880412', '880414', '880419', '880418', '880600', '880601', '880602', '880603', '880604', '880605', '880606', '880607', '880608', '880609', '880231', '880230', '880232', '880592', '880593', '880987', '880454', '880456', '880598', '880982', '880981', '880590', '000905', '880583', '880582', '880581', '880580', '880587', '880586', '880585', '880584', '880460', '880461', '880589', '880463', '880464', '880465', '880466', '880467', '880907', '880906', '880905', '880904', '880903', '880902', '880901', '880862', '880908', '880519', '880515', '880516', '880513', '880521', '000016', '880520', '880613', '880340', '880345', '880344', '880347', '880346', '880348', '880612', '880529', '880528', '880644', '880645', '880646', '880647', '880640', '880641', '880642', '880643', '880648', '880649', '880949', '880948', '880943', '880942', '880941', '880940', '880947', '880946', '880945', '880944', '880338', '880339', '880330', '880335', '880336', '880337', '880423', '880547', '880546', '880545', '880544', '880542', '880938', '880939', '880936', '880937', '880531', '880935', '880932', '880933', '880422', '880931', '880204', '880205', '880206', '880207', '880201', '880619', '880618', '880617', '880616', '880615', '880614', '880208', '880209', '880610', '880680', '880681', '880682', '880683', '880684', '880685', '880549', '880993']
#
# print(len(data))

# li=['880511', '880532', '880538', '880539', '880543', '880562', '880565', '880576', '880801', '880802', '880803', '880804', '880805', '880806', '880807', '880808', '880809', '880810', '880811', '880812', '880813', '880821', '880823', '880824', '880826', '880827', '880829', '880833', '880834', '880835', '880836', '880837', '880842', '880843', '880844', '880845', '880846', '880847', '880848', '880849', '880850', '880851', '880852', '880853', '880854', '880856', '880857', '880858', '880859', '880860', '880861', '880863', '880864', '880865', '880866', '880867', '880868', '880869', '880870', '880871', '880872', '880873', '880874', '880875', '880876', '880877', '880878', '880879', '880880', '880881', '880882', '880883', '880884', '880885', '880886', '880887', '880889', '880890', '880891', '880892', '880893', '880895', '880896', '880897', '880894']
#
#
# BaseModel('A_MACD_left_right_index_min5_version4').remove({'stock_code':{'$in':li}})