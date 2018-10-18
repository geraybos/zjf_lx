# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import datetime

import tushare as ts

from app import markets
from app.actions.utils import date_preprocess
from app.back_testing.novel_features import MA_s
from app.query_str_analyzer import analyzer
from app.utils import dict_combine
from . import data_client


def trans_tushare_data(y, s):
    dr = list()
    try:
        report_data = ts.get_report_data(y, s).to_dict()
        profit_data = ts.get_profit_data(y, s).to_dict()
        oper_data = ts.get_operation_data(y, s).to_dict()
        growth_data = ts.get_growth_data(y, s).to_dict()
        debtpay_data = ts.get_debtpaying_data(y, s).to_dict()
        cashflow_data = ts.get_cashflow_data(y, s).to_dict()
    except Exception as e:
        print(e)
    else:
        r_dict = dict()
        l_rd = len(report_data['code'])
        for i in range(l_rd):
            md = report_data['report_date'][i]
            try:
                d = Calendar.recent('{}-{}'.format(y, md), forward=True)['date']
            except Exception as e:
                d = Calendar.recent('{}-{}-01'.format(y, md.split('-')[0]), forward=True)['date']

            s_c = report_data['code'][i].strip()
            r_dict[i] = dict(
                stock_code=s_c,
                report_roe=float(report_data['roe'][i]) if pd.notnull(report_data['roe'][i]) and report_data['roe'][
                    i] != '--' else 0.0,
                report_eps=float(report_data['eps'][i]) if pd.notnull(report_data['eps'][i]) and report_data['eps'][
                    i] != '--' else 0.0,
                report_eps_yoy=float(report_data['eps_yoy'][i]) if pd.notnull(report_data['eps_yoy'][i]) and
                                                                   report_data['eps_yoy'][i] != '--' else 0.0,
                report_bvps=float(report_data['bvps'][i]) if pd.notnull(report_data['bvps'][i]) and report_data['bvps'][
                    i] != '--' else 0.0,
                report_epcf=float(report_data['epcf'][i]) if pd.notnull(report_data['epcf'][i]) and report_data['epcf'][
                    i] != '--' else 0.0,
                report_net_profits=float(report_data['net_profits'][i]) if pd.notnull(report_data['net_profits'][i]) and
                                                                           report_data['net_profits'][
                                                                               i] != '--' else 0.0,
                report_profits_yoy=float(report_data['profits_yoy'][i]) if pd.notnull(report_data['profits_yoy'][i]) and
                                                                           report_data['profits_yoy'][
                                                                               i] != '--' else 0.0,
                date=d
            )

        p_dict = dict()
        l_pd = len(profit_data['code'])
        for i in range(l_pd):
            s_c = profit_data['code'][i].strip()
            p_dict[i] = dict(
                stock_code=s_c,
                profit_roe=float(profit_data['roe'][i]) if pd.notnull(profit_data['roe'][i]) and profit_data['roe'][
                    i] != '--' else 0.0,
                profit_net_ratio=float(profit_data['net_profit_ratio'][i]) if pd.notnull(
                    profit_data['net_profit_ratio'][i]) and profit_data['net_profit_ratio'][i] != '--' else 0.0,
                profit_gross_rate=float(profit_data['gross_profit_rate'][i]) if pd.notnull(
                    profit_data['gross_profit_rate'][i]) and profit_data['gross_profit_rate'][i] != '--' else 0.0,
                profit_eps=float(profit_data['eps'][i]) if pd.notnull(profit_data['eps'][i]) and profit_data['eps'][
                    i] != '--' else 0.0,
                profit_business_income=float(profit_data['business_income'][i]) if pd.notnull(
                    profit_data['business_income'][i]) and profit_data['business_income'][i] != '--' else 0.0,
                profit_bips=float(profit_data['bips'][i]) if pd.notnull(profit_data['bips'][i]) and profit_data['bips'][
                    i] != '--' else 0.0
            )

        o_dict = dict()
        l_od = len(oper_data['code'])
        for i in range(l_od):
            s_c = oper_data['code'][i].strip()
            o_dict[i] = dict(
                stock_code=s_c,
                oper_arturnover=float(oper_data['arturnover'][i]) if pd.notnull(oper_data['arturnover'][i]) and
                                                                     oper_data['arturnover'][i] != '--' else 0.0,
                oper_arturndays=float(oper_data['arturndays'][i]) if pd.notnull(oper_data['arturndays'][i]) and
                                                                     oper_data['arturndays'][i] != '--' else 0.0,
                oper_inventory_turnover=float(oper_data['inventory_turnover'][i]) if pd.notnull(
                    oper_data['inventory_turnover'][i]) and oper_data['inventory_turnover'][i] != '--' else 0.0,
                oper_inventory_days=float(oper_data['inventory_days'][i]) if pd.notnull(
                    oper_data['inventory_days'][i]) and oper_data['inventory_days'][i] != '--' else 0.0,
                oper_currentasset_turnover=float(oper_data['currentasset_turnover'][i]) if pd.notnull(
                    oper_data['currentasset_turnover'][i]) and oper_data['currentasset_turnover'][i] != '--' else 0.0,
                oper_currentasset_days=float(oper_data['currentasset_days'][i]) if pd.notnull(
                    oper_data['currentasset_days'][i]) and oper_data['currentasset_days'][i] != '--' else 0.0
            )

        g_dict = dict()
        l_gd = len(growth_data['code'])
        for i in range(l_gd):
            s_c = growth_data['code'][i].strip()
            g_dict[i] = dict(
                stock_code=s_c,
                growth_mbrg=float(growth_data['mbrg'][i]) if pd.notnull(growth_data['mbrg'][i]) and growth_data['mbrg'][
                    i] != '--' else 0.0,
                growth_nprg=float(growth_data['nprg'][i]) if pd.notnull(growth_data['nprg'][i]) and growth_data['nprg'][
                    i] != '--' else 0.0,
                growth_nav=float(growth_data['nav'][i]) if pd.notnull(growth_data['nav'][i]) and growth_data['nav'][
                    i] != '--' else 0.0,
                growth_targ=float(growth_data['targ'][i]) if pd.notnull(growth_data['targ'][i]) and growth_data['targ'][
                    i] != '--' else 0.0,
                growth_epsg=float(growth_data['epsg'][i]) if pd.notnull(growth_data['epsg'][i]) and growth_data['epsg'][
                    i] != '--' else 0.0,
                growth_seg=float(growth_data['seg'][i]) if pd.notnull(growth_data['seg'][i]) and growth_data['seg'][
                    i] != '--' else 0.0
            )

        d_dict = dict()
        l_dd = len(debtpay_data['code'])
        for i in range(l_dd):
            s_c = debtpay_data['code'][i].strip()
            d_dict[i] = dict(
                stock_code=s_c,
                debtpay_currentratio=float(debtpay_data['currentratio'][i]) if pd.notnull(
                    debtpay_data['currentratio'][i]) and debtpay_data['currentratio'][i] != '--' else 0.0,
                debtpay_quickratio=float(debtpay_data['quickratio'][i]) if pd.notnull(debtpay_data['quickratio'][i]) and
                                                                           debtpay_data['quickratio'][
                                                                               i] != '--' else 0.0,
                debtpay_cashratio=float(debtpay_data['cashratio'][i]) if pd.notnull(debtpay_data['cashratio'][i]) and
                                                                         debtpay_data['cashratio'][i] != '--' else 0.0,
                debtpay_icratio=float(debtpay_data['icratio'][i]) if pd.notnull(debtpay_data['icratio'][i]) and
                                                                     debtpay_data['icratio'][i] != '--' else 0.0,
                debtpay_sheqratio=float(debtpay_data['sheqratio'][i]) if pd.notnull(debtpay_data['sheqratio'][i]) and
                                                                         debtpay_data['sheqratio'][i] != '--' else 0.0,
                debtpay_adratio=float(debtpay_data['adratio'][i]) if pd.notnull(debtpay_data['adratio'][i]) and
                                                                     debtpay_data['adratio'][i] != '--' else 0.0
            )

        c_dict = dict()
        l_cd = len(cashflow_data['code'])
        for i in range(l_cd):
            s_c = cashflow_data['code'][i].strip()
            c_dict[i] = dict(
                stock_code=s_c,
                cf_sales=float(cashflow_data['cf_sales'][i]) if pd.notnull(cashflow_data['cf_sales'][i]) and
                                                                cashflow_data['cf_sales'][i] != '--' else 0.0,
                cf_rateofreturn=float(cashflow_data['rateofreturn'][i]) if pd.notnull(
                    cashflow_data['rateofreturn'][i]) and cashflow_data['rateofreturn'][i] != '--' else 0.0,
                cf_nm=float(cashflow_data['cf_nm'][i]) if pd.notnull(cashflow_data['cf_nm'][i]) and
                                                          cashflow_data['cf_nm'][i] != '--' else 0.0,
                cf_liabilities=float(cashflow_data['cf_liabilities'][i]) if pd.notnull(
                    cashflow_data['cf_liabilities'][i]) and cashflow_data['cf_liabilities'][i] != '--' else 0.0,
                cf_ratio=float(cashflow_data['cashflowratio'][i]) if pd.notnull(cashflow_data['cashflowratio'][i]) and
                                                                     cashflow_data['cashflowratio'][i] != '--' else 0.0
            )

        dl = [c_dict, r_dict, g_dict, d_dict, p_dict, o_dict]
        s_c_l = list()
        for d in dl:
            s_c_l.extend(d.keys())

        s_c_l = set(s_c_l)
        for s_c in s_c_l:
            # report_esp,每股收益, report_eps_yoy,每股收益同比(%), report_bvps,每股净资产,
            # report_roe,净资产收益率(%), report_epcf,每股现金流量(元), report_net_profits,净利润(万元),
            # report_profits_yoy,净利润同比(%), report_distrib,分配方案
            # ------------------------------------------------------------------------
            # profit_roe,净资产收益率(%), profit_net_ratio,净利率(%), profit_gross_rate,毛利率(%), profit_net_profits,净利润(万元),
            # profit_esp,每股收益, profit_business_income,营业收入(百万元), profit_bips,每股主营业务收入(元)
            # ------------------------------------------------------------------------
            # oper_arturnover,应收账款周转率(次), oper_arturndays,应收账款周转天数(天), oper_inventory_turnover,存货周转率(次)
            # oper_inventory_days,存货周转天数(天), oper_currentasset_turnover,流动资产周转率(次), oper_currentasset_days,流动资产周转天数(天
            # ------------------------------------------------------------------------
            # groth_mbrg,主营业务收入增长率(%), groth_nprg,净利润增长率(%), groth_nav,净资产增长率, groth_targ,总资产增长率, groth_epsg,每股收益增长率, groth_seg,股东权益增长率
            # ------------------------------------------------------------------------
            # debtpay_currentratio,流动比率, debtpay_quickratio,速动比率, debtpay_cashratio,现金比率, debtpay_icratio,利息支付倍数, debtpay_sheqratio,股东权益比率, debtpay_adratio,股东权益增长率
            # ------------------------------------------------------------------------
            # cf_sales,经营现金净流量对销售收入比率, cf_rateofreturn,资产的经营现金流量回报率, cf_nm,经营现金净流量与净利润的比率
            # cf_liabilities,经营现金净流量对负债比率, cf_ratio,现金流量比率
            fmt = dict(stock_code=None, date=None,
                       report_roe=0, report_eps=0, report_eps_yoy=0, report_bvps=0, report_epcf=0, report_net_profits=0,
                       report_profits_yoy=0,
                       profit_roe=0, profit_net_ratio=0, profit_gross_rate=0, profit_eps=0, profit_business_income=0,
                       profit_bips=0,
                       oper_arturnover=0, oper_arturndays=0, oper_inventory_turnover=0, oper_inventory_days=0,
                       oper_currentasset_turnover=0, oper_currentasset_days=0,
                       growth_mbrg=0, growth_nprg=0, growth_nav=0, growth_targ=0, growth_epsg=0, growth_seg=0,
                       debtpay_currentratio=0, debtpay_quickratio=0, debtpay_cashratio=0, debtpay_icratio=0,
                       debtpay_sheqratio=0, debtpay_adratio=0,
                       cf_sales=0, cf_rateofreturn=0, cf_nm=0, cf_liabilities=0, cf_ratio=0
                       )
            for d in dl:
                dict_combine(fmt, d.get(s_c, {'date': Calendar.to('datetime', '{}{:02d}01'.format(y, s * 3 - 2))}))
            dr.append(fmt)
    return dr


def tushare_to_db(start_date=None, end_date=None):
    sd, ed = date_preprocess(start_date, end_date)
    obj = model_list['tushare']
    dr = list()
    if start_date:
        season = (sd.month - 1) // 3
        s1 = '{}{:02d}01'.format(sd.year, season * 3 if season > 0 else 1)
        cond = analyzer('date >= {}'.format(s1))
        obj.remove(cond)
        dr = trans_tushare_data(sd.year, season + 1)
    else:
        for y in range(sd.year, ed.year + 1):
            for s in range(1, 5):
                dr.extend(trans_tushare_data(y, s))
    obj.insert_batch(dr)


def capital_to_db(market_name, stock_list, start_date=None, end_date=None):
    market = markets[market_name]
    r_list = list()
    sd, ed = date_preprocess(start_date, end_date)
    for stock in stock_list:
        info = data_client.GetCompanyInfoCategory(market['id'], stock)  # 获取公司面板
        info = info[1].strip()
        if len(info):
            # print (info.decode('gbk'))
            info = info.split('\n')
            filename = ''
            start = 0
            length = 0
            for row in info:
                # print(row.decode('gbk'))
                if u'公司股本'.encode('gbk') in row:
                    ii = row.split()
                    filename = ii[1]
                    start = int(ii[2])
                    length = int(ii[3])
                    break

            result = data_client.GetCompanyInfoContent(market['id'], stock, filename, start, length)  # 获取公司详细信息-股本结构
            result = result[1]
            # print (result.decode('gbk'))
            result = result.split('\n')

            for line in result:
                # print(line.decode('gbk'))
                if u'｜2'.encode('gbk') == line[:3]:
                    # print (line.decode('gbk'))
                    cols = line.split(u'｜'.encode('gbk'))
                    if cols[3].decode('gbk').strip() == u'-':
                        break
                    val = {}
                    try:
                        val['date'] = Calendar.to('datetime', cols[1].decode('gbk').strip().decode('string_escape'))
                    except Exception as e:
                        print(u'{}\t| {}\t| {}'.format(stock, line.decode('gbk'), e.message))
                        continue
                    if sd <= val['date'] <= ed:
                        val['stock_code'] = stock

                        val['capital'] = float(cols[3].decode('gbk').strip())
                        val['capital_all'] = float(cols[2].decode('gbk').strip())
                        print(val)
                        r_list.append(val)
                        # print (r_list)
        print(stock, 'done')
    r = sorted(r_list, key=lambda x: (x['stock_code'], x['date']))
    Capital('capital').insert_batch(r)
    return r


def calc_feature(tn, stock_code, start_date, end_date):
    obj = model_list[tn]

    sd, ed = date_preprocess(start_date, end_date)
    sql = 'stock_code = {} and date >= {} and date <= {}'.format(stock_code, Calendar.to(str, sd), Calendar.to(str, ed))
    cond = analyzer(sql)
    raw_dl = list(obj.desc(obj.query(cond), ['date']))
    if len(raw_dl) < 2:
        return

    result = list()
    dl = MA_s(pd.DataFrame(raw_dl)).to_dict()
    l = len(dl['date'])
    sn = 0
    day1 = None
    for i in range(l):
        price_inc = 0
        dt = Calendar.to(str, raw_dl[i]['date'])

        # 确定该股是不是次新股
        if sn == 0:
            nc = analyzer('stock_code = {} and date <= {}'.format(raw_dl[i]['stock_code'], dt))
            ds = obj.query(nc)
            sn = ds.count()
            day1 = obj.asc(ds, ['date'])[0]

        if 0 < sn < 100:
            sub_new = True
            if 3 < sn < 100:
                price_inc = raw_dl[i]['close'] / day1['open']
            else:
                price_inc = 1
        else:
            sub_new = False
        sn -= 1

        d = dict(
            stock_code=raw_dl[i]['stock_code'],
            date=dl['date'][i],
            last_5=float(dl['last_5'][i]),
            last_10=float(dl['last_10'][i]),
            last_20=float(dl['last_20'][i]),
            last_30=float(dl['last_30'][i]),
            last_60=float(dl['last_60'][i]),
            ma5=float(dl['ma5'][i]),
            ma10=float(dl['ma10'][i]),
            ma20=float(dl['ma20'][i]),
            ma30=float(dl['ma30'][i]),
            ma60=float(dl['ma60'][i]),
            v_ma5=float(dl['v_ma5'][i]),
            v_ma10=float(dl['v_ma10'][i]),
            v_ma20=float(dl['v_ma20'][i]),
            v_ma30=float(dl['v_ma30'][i]),
            v_ma60=float(dl['v_ma60'][i]),
            close_z=float(dl['close_z'][i]),
            change_r=float(dl['change_r'][i]),
            volume_r=float(dl['volume_r'][i]),
            volume_z=float(dl['volume_z'][i]),
            v_dt_ma60=float(dl['v_dt_ma60'][i]),
            capital=0,
            price_inc=price_inc,
            sub_new=sub_new)
        d.update(raw_dl[i])
        result.append(d)
        # print(dt, raw_dl[i]['stock_code'], sn)

    if result is None:
        print(stock_code, ' calc_feature is None')
        return
    sr = sorted(result, key=lambda x: (x['stock_code'], x['date']))
    if sr is None:
        print(stock_code, ' calc_feature sort None')
        return
    return sr


def day_feature(stock_code, start_date, end_date, his=False):
    iobj = model_list['feature_day']

    offset = 0

    if end_date is None:
        end_date = Calendar.recent()
        if Calendar.in_business(datetime.now(), hard=False):
            end_date = Calendar.calc(end_date, -1)
    else:
        end_date = Calendar.recent(end_date)

    # 如果 start_date 为空，则定到 end_date 之前的60天
    # 这样刚好可以算出 end_date 那一天的 ma60
    # 实现了 daily update 的功能
    if his:
        start_date = Calendar.recent(start_date)
    else:
        if start_date is None:
            d = end_date
        else:
            d = start_date

        offset = Calendar.calc(end_date['date'], Calendar.to('datetime', d))
        start_date = Calendar.calc(d, -(offset + 60))['date']
        # num = 60

    sd, ed = date_preprocess(start_date, end_date)
    sql = 'stock_code = {} and date <= {}'.format(stock_code, Calendar.to(str, ed))
    cond = analyzer(sql)

    # print(1, stock_code)
    cobj = model_list['capital']
    cc = list(cobj.asc(cobj.query(cond), ['date']))
    # print(2, stock_code)
    tobj = model_list['tushare']
    tt = list(tobj.asc(tobj.query(cond), ['date']))
    # print(3, stock_code)
    dd = calc_feature('XDXR_day', stock_code, start_date, end_date)
    if dd:
        dd = dd[-offset:]
        dl = len(dd)
        cl = len(cc)
        tl = len(tt)
        ic = 0
        it = 0
        capital_all = 0
        capital = 0
        dr = deepcopy(dd)
        sub_t = dict()
        for j in range(dl):
            # print(4, stock_code)
            d = dr[j]
            for ti in range(it, tl):
                t = tt[ti]
                if t['date'] <= d['date']:
                    for k in t.keys():
                        if k == 'date':
                            continue
                        sub_t[k] = t[k] if pd.notnull(t[k]) else 0.0
                    it = ti + 1
                else:
                    break
            # print(5, stock_code)
            dict_combine(d, sub_t)
            # print(6, stock_code)
            for ci in range(ic, cl):
                c = cc[ci]
                if c['date'] <= d['date']:
                    capital_all = c['capital_all']
                    capital = c['capital']
                    ic = ci + 1
                else:
                    break
            d['capital'] = capital
            d['capital_all'] = capital_all

        iobj.insert_batch(dr)
        print('insertttt', stock_code)


from app.models import model_list, Calendar, Capital
import pandas as pd


# 收盘站上10， 20日均线的 CLOSE>MA10 MA20
# 收盘落下10，20日均线的
def close_ma1020(cond):
    fobj = model_list['feature_day']
    fdata = list(fobj.query(cond))
    fpd = pd.DataFrame(fdata)
    up_10 = fpd[fpd['close'] > fpd['ma10']]['volume'].count()
    up_20 = fpd[fpd['close'] > fpd['ma20']]['volume'].count()
    down_10 = fpd[fpd['close'] < fpd['ma10']]['volume'].count()
    down_20 = fpd[fpd['close'] < fpd['ma20']]['volume'].count()
    return up_10, up_20, down_10, down_20


def turnover_rate(cond):
    # 大盘每天的换手率（总的volume/capital）,按上证60开头的，深圳00，创业板30 分别统计（我晚点给你一个具体的列表）
    fobj = model_list['feature_day']

    fdata = list(fobj.query(cond))
    fl = len(fdata)
    print('fl: {}'.format(fl))
    if fl:
        fpd = pd.DataFrame(fdata)

        volume = fpd['volume'].sum()
        capital = fpd['capital'].sum()

        tor = volume / capital if capital != 0 else volume
    else:
        tor = 0
    return tor


def statistic(cond):
    fobj = model_list['feature_day']
    fdata = list(fobj.query(cond))
    fpd = pd.DataFrame(fdata)

    # 跌停的股票数量（change_r<0.905）的
    # 涨停的股票数量 change_r>1.097
    fup = fpd[(fpd.change_r > 1.097) & (fpd.sub_new == False)]['volume'].count()
    fdown = fpd[(fpd.change_r < 0.905)]['volume'].count()

    # 底部放量大涨的（volume>v_ma）1.5倍，change_r>1.05的数量
    # 顶部放量大跌的数量
    fpd['v_ma5_1_5'] = 1.5 * fpd['v_ma5']
    top_down_volum = fpd[(fpd['change_r'] > 1.05) & (fpd['volume'] > fpd['v_ma5_1_5'])]['volume'].count()
    bottom_up_volum = fpd[(fpd['change_r'] < 0.95) & (fpd['volume'] > fpd['v_ma5_1_5'])]['volume'].count()

    # 市场市值最小的
    fpd['cc'] = fpd['capital_all'] * fpd['close']
    min_value = fpd[(fpd['cc'] > 0) & (fpd['sub_new'] == False)]['cc'].min()
    return fup, fdown, top_down_volum, bottom_up_volum, min_value


def day_feature_index(cond, market):
    print(cond)
    dobj = model_list['feature_day']
    iobj = model_list['feature_index_day']
    raw_dl = list(dobj.query(cond))
    lrd = len(raw_dl)
    if lrd == 0:
        print('empty!!!!!!!!!!!!!!!!!')
        return
    tj = dict(up_03=0, up_35=0, up_57=0, up_79=0, up_95=0, down_03=0, down_35=0, down_57=0, down_79=0, down_95=0, eq=0)

    data = pd.DataFrame(raw_dl)
    flrd = float(lrd)
    tj['up_03'] = data[(data['change_r'] > 1.01) & (data['change_r'] <= 1.03)]['change_r'].count()
    tj['up_35'] = data[(data['change_r'] > 1.03) & (data['change_r'] <= 1.05)]['change_r'].count()
    tj['up_57'] = data[(data['change_r'] > 1.05) & (data['change_r'] <= 1.07)]['change_r'].count()
    tj['up_70'] = data[(data['change_r'] > 1.07)]['change_r'].count()
    tj['up'] = data[(data['change_r'] > 1)]['change_r'].count()

    tj['eq'] = data[(data['change_r'] >= 0.99) & (data['change_r'] <= 1.01)]['change_r'].count()

    tj['down_03'] = data[(data['change_r'] >= 0.97) & (data['change_r'] < 0.99)]['change_r'].count()
    tj['down_35'] = data[(data['change_r'] >= 0.95) & (data['change_r'] < 0.97)]['change_r'].count()
    tj['down_57'] = data[(data['change_r'] >= 0.93) & (data['change_r'] < 0.95)]['change_r'].count()
    tj['down_70'] = data[(data['change_r'] >= 0.9) & (data['change_r'] < 0.93)]['change_r'].count()
    tj['down'] = data[(data['change_r'] < 1)]['change_r'].count()

    sub_new = data[(data['sub_new'] == True)]

    if sub_new.empty:
        tj['sub_new_price_inc_down'] = 0
        tj['sub_new_price_inc_up'] = 0
    else:
        tj['sub_new_price_inc_down'] = float(sub_new['price_inc'].min())
        tj['sub_new_price_inc_up'] = float(sub_new['price_inc'].max())

    tj['date'] = raw_dl[0]['date']
    tj['market'] = market
    tj['total_stock'] = lrd
    tj['tor'] = turnover_rate(cond)
    tj['limit_up'], tj['limit_down'], tj['top_down_volum_num'], tj['bottom_up_volume_num'], tj['min_value'] = statistic(
        cond)
    tj['close_up_10'], tj['close_up_20'], tj['close_down_10'], tj['close_down_20'] = close_ma1020(cond)
    for i in ['limit_up', 'limit_down', 'top_down_volum_num', 'bottom_up_volume_num',
              'close_up_10', 'close_up_20', 'close_down_10', 'close_down_20',
              'eq', 'up', 'down', 'up_35', 'down_35', 'up_57', 'down_57',
              'up_70', 'down_70']:
        tj[i + '_rate'] = tj[i] / flrd
    iobj.insert(tj)


def close_ma1020_n(fdata):
    # fobj = model_list[category]
    # fdata = list(fobj.query(cond))
    fpd = pd.DataFrame(fdata)
    up_10 = fpd[fpd['close'] > fpd['ma10']]['volume'].count()
    up_20 = fpd[fpd['close'] > fpd['ma20']]['volume'].count()
    down_10 = fpd[fpd['close'] < fpd['ma10']]['volume'].count()
    down_20 = fpd[fpd['close'] < fpd['ma20']]['volume'].count()
    return up_10, up_20, down_10, down_20


def turnover_rate_n(fdata):
    # 大盘每天的换手率（总的volume/capital）,按上证60开头的，深圳00，创业板30 分别统计（我晚点给你一个具体的列表）
    # fobj = model_list[category]

    # fdata = list(fobj.query(cond))
    fl = len(fdata)
    print('fl: {}'.format(fl))
    if fl:
        fpd = pd.DataFrame(fdata)

        volume = fpd['volume'].sum()
        capital = fpd['capital'].sum()

        tor = volume / capital if capital != 0 else volume
    else:
        tor = 0
    return tor


def statistic_n(fdata):
    # fobj = model_list[category]
    # fdata = list(fobj.query(cond))
    fpd = pd.DataFrame(fdata)

    # 跌停的股票数量（change_r<0.905）的
    # 涨停的股票数量 change_r>1.097
    fup = fpd[(fpd.change_r > 1.097) & (fpd.sub_new == False)]['volume'].count()
    fdown = fpd[(fpd.change_r < 0.905)]['volume'].count()

    # 底部放量大涨的（volume>v_ma）1.5倍，change_r>1.05的数量
    # 顶部放量大跌的数量
    fpd['v_ma5_1_5'] = 1.5 * fpd['v_ma5']
    top_down_volum = fpd[(fpd['change_r'] > 1.05) & (fpd['volume'] > fpd['v_ma5_1_5'])]['volume'].count()
    bottom_up_volum = fpd[(fpd['change_r'] < 0.95) & (fpd['volume'] > fpd['v_ma5_1_5'])]['volume'].count()

    # 市场市值最小的
    fpd['cc'] = fpd['capital_all'] * fpd['close']
    min_value = fpd[(fpd['cc'] > 0) & (fpd['sub_new'] == False)]['cc'].min()
    return fup, fdown, top_down_volum, bottom_up_volum, min_value


def minute_feature_index(raw_dl, market):
    # dobj = model_list[category]
    # iobj = model_list['feature_index_day']
    # raw_dl = list(dobj.query(cond))
    lrd = len(raw_dl)
    if lrd == 0:
        print('empty!!!!!!!!!!!!!!!!!')
        return
    tj = dict(up_03=0, up_35=0, up_57=0, up_79=0, up_95=0, down_03=0, down_35=0, down_57=0, down_79=0, down_95=0, eq=0)

    data = pd.DataFrame(raw_dl)
    flrd = float(lrd)
    tj['up_03'] = data[(data['change_r'] > 1.01) & (data['change_r'] <= 1.03)]['change_r'].count()
    tj['up_35'] = data[(data['change_r'] > 1.03) & (data['change_r'] <= 1.05)]['change_r'].count()
    tj['up_57'] = data[(data['change_r'] > 1.05) & (data['change_r'] <= 1.07)]['change_r'].count()
    tj['up_70'] = data[(data['change_r'] > 1.07)]['change_r'].count()
    tj['up'] = data[(data['change_r'] > 1)]['change_r'].count()

    tj['eq'] = data[(data['change_r'] >= 0.99) & (data['change_r'] <= 1.01)]['change_r'].count()

    tj['down_03'] = data[(data['change_r'] >= 0.97) & (data['change_r'] < 0.99)]['change_r'].count()
    tj['down_35'] = data[(data['change_r'] >= 0.95) & (data['change_r'] < 0.97)]['change_r'].count()
    tj['down_57'] = data[(data['change_r'] >= 0.93) & (data['change_r'] < 0.95)]['change_r'].count()
    tj['down_70'] = data[(data['change_r'] >= 0.9) & (data['change_r'] < 0.93)]['change_r'].count()
    tj['down'] = data[(data['change_r'] < 1)]['change_r'].count()

    sub_new = data[(data['sub_new'] == True)]

    if sub_new.empty:
        tj['sub_new_price_inc_down'] = 0
        tj['sub_new_price_inc_up'] = 0
    else:
        tj['sub_new_price_inc_down'] = float(sub_new['price_inc'].min())
        tj['sub_new_price_inc_up'] = float(sub_new['price_inc'].max())

    tj['date'] = raw_dl[0]['date']
    tj['market'] = market
    tj['total_stock'] = lrd
    # tj['tor'] = turnover_rate_n(raw_dl)
    # tj['limit_up'], tj['limit_down'], tj['top_down_volum_num'], tj['bottom_up_volume_num'], tj['min_value'] = statistic_n(raw_dl)
    tj['close_up_10'], tj['close_up_20'], tj['close_down_10'], tj['close_down_20'] = close_ma1020_n(raw_dl)
    for i in ['close_up_10', 'close_up_20', 'close_down_10', 'close_down_20',
              'eq', 'up', 'down', 'up_35', 'down_35', 'up_57', 'down_57',
              'up_70', 'down_70']:
        tj[i + '_rate'] = tj[i] / flrd
    # iobj.insert(tj)
    return (tj)
