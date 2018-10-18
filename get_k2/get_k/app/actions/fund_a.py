# -*- coding: utf-8 -*-
from random import randint
from time import sleep

from lxml import etree

from app.actions.utils import crawl, date_range, date_preprocess
from app.models import Calendar, model_list

url = 'http://www.csindex.com.cn/zh-CN/downloads/industry-price-earnings-ratio'


def get_zybk_ttm(start_date=None, end_date=None):
    obj = model_list['fund_zybk_ttm']
    start_date, end_date = date_preprocess(start_date, end_date)
    calendar = date_range(start_date, end_date)
    print('calendar', len(calendar))

    i_l = 0

    result = list()
    cl = len(calendar)

    for ci in range(cl):
        c = calendar[ci]
        t = randint(1, 2)
        params = {'type': 'zy2', 'date': Calendar.to(str, c, _format='%Y-%m-%d')}
        try:
            e = crawl(url, params)

            html = etree.HTML(e.text)
            html_tbody_tr = html.xpath('//tbody//tr/td')
            tr_list = [_.text for _ in html_tbody_tr]
            for i in range(6):
                sub_tr = tr_list[8 * i:8 * (1 + i)]
                sub_tr.append(c['date'])
                data = obj.trans_data(sub_tr)
                result.append(data)
        except Exception as e:
            print(e)
        finally:
            params['t'] = t
            print(params)
            i_l += 1
            if i_l > 500 or ci == cl - 1:
                print('insert')
                obj.insert_batch(result)
                i_l = 0
                result = list()

            sleep(t)


def get_ttm(p_type='zz', start_date=None, end_date=None):
    start_date, end_date = date_preprocess(start_date, end_date)
    calendar = date_range(start_date, end_date)
    print('calendar', len(calendar))
    for c in calendar:
        t = randint(1, 2)
        params = {'type': p_type + '2', 'date': Calendar.to(str, c, _format='%Y-%m-%d')}
        obj = model_list['fund_{}_ttm'.format(p_type)]
        try:
            e = crawl(url, params)

            html = etree.HTML(e.text)
            name_data = html.xpath('//table[@class="list-div-table"]//span')
            list_name = [_.text for _ in name_data]
            sp_data = html.xpath('//table[@class="list-div-table"]//tbody//tr//td//div//a')
            list_sp = [_.text for _ in sp_data]
            normal_data = html.xpath('//table[@class="list-div-table"]//tbody//tr//td//div')
            list_normal = [_.text for _ in normal_data]

            lnl = len(list_normal) / 9
            name_loop = 0
            sp_loop = 0

            for i in range(lnl):
                sub_normal = list_normal[9 * i: 9 * (i + 1)]
                name = list_name[name_loop]
                name_loop += 1

                code = sub_normal[0]
                cl = len(code)

                def sll(sp_loop):
                    lv = cl / 2
                    s_n = list_sp[sp_loop]
                    if s_n is None:
                        sp_loop += 1
                        s_n = list_sp[sp_loop]
                    sp_loop += 1
                    l_n = list_sp[sp_loop]
                    sp_loop += 1
                    return s_n, l_n, lv, sp_loop

                # if cl == 2:
                #     lv = 1
                #     stock_num = list_sp[sp_loop]
                #     if stock_num is None:
                #         sp_loop += 1
                #         stock_num = list_sp[sp_loop]
                #     sp_loop += 1
                #     loss_num = list_sp[sp_loop]
                #     sp_loop += 1
                # elif cl == 4:
                #     lv = 2
                #     stock_num = list_sp[sp_loop]
                #     if stock_num is None:
                #         sp_loop += 1
                #         stock_num = list_sp[sp_loop]
                #     sp_loop += 1
                #     loss_num = list_sp[sp_loop]
                #     sp_loop += 1
                # elif cl == 6:
                #     lv = 3
                #     stock_num = list_sp[sp_loop]
                #     if stock_num is None:
                #         sp_loop += 1
                #         stock_num = list_sp[sp_loop]
                #     sp_loop += 1
                #     loss_num = list_sp[sp_loop]
                #     sp_loop += 1
                # elif cl == 8:
                #     lv = 4
                #     stock_num = list_sp[sp_loop]
                #     if stock_num is None:
                #         sp_loop += 1
                #         stock_num = list_sp[sp_loop]
                #     sp_loop += 1
                #     loss_num = list_sp[sp_loop]
                #     sp_loop += 1
                # else:
                #     continue

                stock_num, loss_num, lv, sp_loop = sll(sp_loop)

                data = obj.trans_data([
                    name,
                    sub_normal[2],
                    stock_num,
                    loss_num,
                    sub_normal[5],
                    sub_normal[6],
                    sub_normal[7],
                    sub_normal[8],
                    code,
                    lv,
                    c['date']
                ])
                obj.insert(data)
        except Exception as e:
            print(e)
        finally:
            params['t'] = t
            print(params)
            sleep(t)
