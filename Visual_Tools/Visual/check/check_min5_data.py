from matplotlib.finance import candlestick2_ohlc

from Calf.data import KlineData
from Calf.models.calendar1 import Calendar
import matplotlib.pyplot as plt
from File.file import File
from Stock.Stock import Stock
class CheckMin5Data:
    @classmethod
    def check(cls, code, start_date, end_date):
        table = 'kline_min5'
        table2 = 'tmp_kline_min5'
        path = 'f:/zjf/data/check6/'
        data = KlineData.read_data(code=code, start_date=start_date,
                                   end_date=end_date, kline=table,
                                   timemerge=True)
        if len(data) <= 0:
            return
        data = data.sort_values(by=['date'], ascending=True)
        data = data[data.time <= 955]
        data2 = KlineData.read_data(code=code, start_date=start_date,
                                    end_date=end_date,
                                    kline=table2, timemerge=True)
        if len(data2) <= 0:
            return
        data2 = data2.sort_values(by=['date'], ascending=True)
        data2 = data2[data2.time <= 955]
        print('start draw.......')
        # fig, ax = plt.subplots()
        # fig.subplots_adjust(bottom=0.2)
        ax = plt.subplot(211)
        # plt.title('本地')
        ax.set_xticks([])
        candlestick2_ohlc(ax, data.open, data.high, data.low, data.close, width=1, colorup='red', colordown='green')
        plt.title(table + '--' + code)
        ax = plt.subplot(212)
        # plt.title('远程')
        plt.title(table2 + '--' + code)
        candlestick2_ohlc(ax, data2.open, data2.high, data2.low, data2.close, width=1, colorup='red', colordown='green')
        File.check_file(path=path)
        ax.set_xticks([])
        plt.savefig(path + code + '.png', transparent=True)
        plt.close()


data = Stock.get_stock_code_list()
stocks = data.stock_code.tolist()
import datetime as dt
start_date = dt.datetime(2018,8,6)
end_date = start_date
for sc in stocks:CheckMin5Data.check(code=sc, start_date=start_date, end_date=end_date)

