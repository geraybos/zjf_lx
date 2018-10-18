# encoding=utf-8
import gc

from boto import sns
from matplotlib.finance import candlestick2_ohlc
from pylab import *  # 支持中文
import pandas as pd
import matplotlib.pyplot as plt

from Calf.data import klinedata
from Calf.models import Calendar
from File.file import File
from Stock.Stock import Stock
from Stock.klinebase import KlineBase
from Stock.platestock import PlateStock
from Visual.Macd.calculatemacd import CalMacd


class visualization:
    @classmethod
    def drow_boll_line(cls, date, data, code='000001', kline='kline_day', interval=4):
        """
        这部分是boll线的可视化部分
        :param date: date是后续label使用
        :param data: 计算好的data
        :param code:股票号码
        :param kline:kline_min5等
        :param interval:间隔日期，默认是4
        :return:
        """
        if len(data) < 92:
            # print('这个股票没有数据')
            return 0
        profits = (data.close.iloc[0] - data.close.iloc[interval]) / data.close.iloc[interval]
        if abs(profits) < 0.02:
            return
        data = data.drop(['_id', 'classtype'], axis=1)
        data = data.sort_values(by=['date'], ascending=True)
        data = data.reset_index()
        data['mid'] = data['close'].rolling(26).mean()
        data['tmp2'] = data['close'].rolling(20).std()
        data['top'] = data['mid'] + 2 * data['tmp2']
        data['bottom'] = data['mid'] - 2 * data['tmp2']
        data = data.iloc[30:-interval]

        names = list(data.date)
        y = list(data.top)
        y1 = list(data.bottom)
        y2 = list(data.mid)
        x = range(len(names))
        fig, ax = plt.subplots(figsize=(12*1.2,8*1.2))
        fig.subplots_adjust()
        plt.plot(x, y,mec='r', mfc='w')
        plt.plot(x, y1,mec='r', mfc='w')
        plt.plot(x, y2,ms=5)
        # plt.legend()  # 让图例生效
        # plt.xticks(x, names, rotation=90)
        # plt.margins(0)
        plt.subplots_adjust(bottom=0.15)
        # plt.xlabel(u"时间轴")  # X轴标签
        # plt.ylabel(u"数据")  # Y轴标签
        # title = str(code) + 'BOLL轨道'
        # plt.title(title)  # 标题
        ax.set_yticks([])
        ax.set_xticks([])
        open1 = list(data['open'])
        high1 = list(data['high'])
        low1 = list(data['low'])
        close1 = list(data['close'])
        # 画图
        # candlestick2_ohlc(ax, open1, high1, low1, close1, width=0.6, colorup='red', colordown='green')
        # plt.show()
        title = 'boll' + '_' + str(date)[0:10] + '_' + code + '_' + str(profits)
        # plt.title(title)  # 标题
        # plt.legend() #图例
        # plt.show()
        up = ''
        if profits >= 0:
            up = '/up'
        else:
            up = '/down'
        path = 'F:/zjf/images/boll2/' + kline + "/" + str(date)[0:10] + up
        File.check_file(path=path)
        file_name = path + '/' + title + '.png'
        plt.savefig(fname=file_name, format='png', dpi=50)
        # plt.clf()
        plt.close()

    @classmethod
    def draw_ma_line(cls, data, profits, date, code,path):


        fig, ax = plt.subplots()
        open1 = list(data['open'])
        high1 = list(data['high'])
        low1 = list(data['low'])
        close1 = list(data['close'])
        candlestick2_ohlc(ax, open1, high1, low1, close1, width=0.6, colorup='black', colordown='black')
        plt.plot(list(data['ma5']),c='black')
        # MA10
        plt.plot(list(data['ma10']),c='black')
        # MA20
        plt.plot(list(data['ma20']),c='black')
        # MA40
        plt.plot(list(data['ma60']),c='black')

        plt.plot(list(data['ma120']), c='black')
        title = str(date)[0:10] + '_' + code + '_' + str(profits)
        # plt.title(title)  # 标题
        # plt.legend() #图例
        # plt.show()

        # path = path + "/" + str(date)[0:10]
        File.check_file(path=path)
        file_name = path + '/' + title + '.png'
        plt.axis('off')
        plt.savefig(fname=file_name, format='png', transparent=True)
        # plt.clf()
        plt.close()
        gc.collect()
        return ''
        # basedata.add_file_address(
        # {'file_name': file_name, 'date': date, 'profits': profits, 'property': 'ma', 'code': code})

    @classmethod
    def draw_ma_min5_line(cls, date, data,kline,length,start_time=None, end_time=None, code='000001', interval=48):
        if start_time == None or end_time == None:
            print('时间必须要有')
            return 0
        data=data.reset_index(drop=True)
        # 前60被截断，后四用来计算涨跌

        if len(data) < length:
            # print(len(data))
            # print('data is no ok')
            return 0

        date = data.date.iloc[interval]
        profits = (data.close.iloc[0] - data.close.iloc[interval]) / data.close.iloc[interval]
        # if abs(profits) < 0.005:
        #     return
        data=data[::-1]
        # 画图
        data['ma5'] = pd.rolling_mean(data['close'], 5)
        data['ma10'] = pd.rolling_mean(data['close'], 10)
        data['ma20'] = pd.rolling_mean(data['close'], 20)
        data['ma60'] = pd.rolling_mean(data['close'], 60)
        data['ma120'] = pd.rolling_mean(data['close'], 120)
        data['ma200'] = pd.rolling_mean(data['close'], 200)

        # fig, ax = plt.subplots(figsize=(18 * (len(data) / 164), 12))
        data = data.iloc[-(48+interval):-interval]
        data = data.reset_index()
        fig, ax = plt.subplots()
        open1 = list(data['open'])
        high1 = list(data['high'])
        low1 = list(data['low'])
        close1 = list(data['close'])
        # candlestick2_ohlc(ax, open1, high1, low1, close1, width=0.6, colorup='red', colordown='green')
        # mpl.rcParams['font.sans-serif'] = ['SimHei']
        # plt.title(str(date)+'p='+str(profits))
        plt.plot(list(data['ma5']))
        # MA10
        plt.plot(list(data['ma10']))
        # MA20
        plt.plot(list(data['ma20']))
        # MA40
        plt.plot(list(data['ma60']))
        plt.plot(list(data['ma120']))
        plt.plot(list(data['ma200']))
        title = 'MA' + '_' + str(date).split(' ')[0] + '_' + code+'_'+ str(date).split(' ')[1].replace(':','-')+ '_' + str(profits)
        # plt.title(title)  # 标题
        # plt.legend() #图例
        # plt.show()
        ax.set_yticks([])
        ax.set_xticks([])
        up = ''
        path = 'F:/zjf/images/Ma_new/399303'
        File.check_file(path=path)
        file_name = path + '/' + title + '.png'
        plt.savefig(fname=file_name, format='png', dpi=100)
        plt.close()
        gc.collect()
        return ''
        # basedata.add_file_address(
        # {'file_name': file_name, 'date': date, 'profits': profits, 'property': 'ma', 'code': code})

    @classmethod
    def draw_macd_line(cls, date, data,profits,start_time=None, end_time=None, code='000001', kline='kline_day',path="f:/zjf/image/macd"):
        """
        :param date: lable,作为图片的标签日期
        :param start_time: 开始日期
        :param end_time: 结束日期
        :param code: 股票号
        :param kline: 数据库表
        :param interval: 间隔几日的收益率
        :return:
        """
        diff = list(data['dif'])
        dea = list(data['dea'])
        fig, ax = plt.subplots()
        plt.plot(diff, 'black')
        plt.plot(dea, 'black')
        macd = list(data.macd)
        x = range(0, len(list(data['macd'])), 1)
        li = list()
        li2 = list()
        for i in macd:
            if i > 0:
                li.append(i)
                li2.append(0)
            else:
                li.append(0)
                li2.append(i)
        plt.bar(left=x, height=li, width=0.4, color=('black'), align="center")  # yerr=0.1
        plt.bar(left=x, height=li2, width=0.4, color=('black'), align="center")  # yerr=0.1

        File.check_file(path=path)
        title = 'macd' + '_' + str(date)[0:10] + '_' + code + '_' + str(profits)
        file_name = path + '/' + title + '.png'
        plt.axis('off')
        plt.savefig(fname=file_name, format='png',transparent=True)
        plt.close()
        gc.collect()
        return ''

    @classmethod
    def handler_data(cls):
        code1 = Stock.get_all_stock_outstanding()
        code2 = PlateStock.get_all_info()
        data = pd.merge(code1, code2, on=['stock_code'])
        data = data.sort_values(by=['hangye'], ascending=True)
        data = data.reset_index(drop=True)
        data['hangye_num'] = data.index
        return data

    @classmethod
    def draw_rl_pic(cls, data, date, time):

        code3 = KlineBase.get_all_stock_code_info(date, time)
        if len(code3) == 0:
            return pd.DataFrame()
        data = pd.merge(data, code3, on=['stock_code'])

        # data['pro'] =data.close_x/data.open_x-1
        pro=data.pro.mean()
        data = data[0:2500]
        arr = np.zeros((51, 51))
        y = 0
        for i, r in data.iterrows():
            if (i + 1) % 50 != 0:
                # print((i + 1) % 50)
                arr[y, i % 50] = r['pro']
            else:
                y = y + 1
                # print('y', y)
                arr[y, i % 50] = r['pro']
        proifit = data.profit.mean()
        if abs(proifit) < 0.0005:
            return


        ax = sns.heatmap(arr, vmin=-0.03, vmax=0.03,cbar=False)
        # plt.matshow(arr, cmap='hot')
        ax.set_yticks([])
        ax.set_xticks([])
        # plt.show()
        # plt.showbar(False)

        if proifit >= 0:
            up = '/up'
        else:
            up = '/down'
        title = str(data.date_x.iloc[0])[0:10] + '_' + str(data.time_x.iloc[0]) +'_'+str(pro)+ '_' + str(proifit)
        path = 'F:/zjf/images/hot/' + str(data.date_x.iloc[0])[0:10] + '/' + up + '/'
        File.check_file(path=path)
        file_name = path + title + '.png'
        plt.savefig(fname=file_name, format='png', dpi=50)
        plt.close()
        gc.collect()

    @classmethod
    def draw_rl_pic_for_day(cls, data,end_date):

        code3 = KlineBase.get_all_stock_code_info_for_day(start_date=Calendar.calc(end_date,-1)['date'],end_date=end_date)
        if len(code3) == 0:
            return pd.DataFrame()
        data = pd.merge(data, code3, on=['stock_code'])
        # data['pro'] =data.close_x/data.open_x-1
        pro=data.pro.mean()
        data = data[0:2500]
        arr = np.zeros((51, 51))
        y = 0
        for i, r in data.iterrows():
            if (i + 1) % 50 != 0:
                # print((i + 1) % 50)
                arr[y, i % 50] = r['pro']
            else:
                y = y + 1
                # print('y', y)
                arr[y, i % 50] = r['pro']
        proifit = data.profit.mean()
        if abs(proifit) < 0.005:
            return

        ax = sns.heatmap(arr, vmin=-0.03, vmax=0.03,cbar=False)
        # plt.matshow(arr, cmap='hot')
        ax.set_yticks([])
        ax.set_xticks([])
        # plt.show()
        # plt.showbar(False)
        if proifit >= 0:
            up = '/up'
        else:
            up = '/down'
        title = str(data.date_x.iloc[0])[0:10]  +'_'+str(pro)+ '_' + str(proifit)
        path = 'F:/zjf/images/hot_day/'  + up + '/'
        File.check_file(path=path)
        file_name = path + title + '.png'
        plt.savefig(fname=file_name, format='png', dpi=50)
        plt.close()
        gc.collect()


