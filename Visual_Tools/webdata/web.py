import requests
from lxml import etree
import datetime as dt



class Fund:
    @classmethod
    def crawl(cls,url, params):
        return requests.get(url, params=params)
    @classmethod
    def get_ttm(cls,p_type ):
        url = 'http://www.csindex.com.cn/zh-CN/downloads/industry-price-earnings-ratio'
        params = {'type': p_type + '2', 'date':dt.datetime(2018,7,30)}
            # obj = model_list['fund_{}_ttm'.format(p_type)]

        e = Fund.crawl(url, params)
        html = etree.HTML(e.text)
        name_data = html.xpath('//table[@class="list-div-table"]//span')
        list_name = [_.text for _ in name_data]
        sp_data = html.xpath('//table[@class="list-div-table"]//tbody//tr//td//div//a')
        list_sp = [_.text for _ in sp_data]
        normal_data = html.xpath('//table[@class="list-div-table"]//tbody//tr//td//div')
        list_normal = [_.text for _ in normal_data]


Fund.get_ttm(p_type='zz')

