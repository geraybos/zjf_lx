from Calf import KlineData
from matplotlib.finance import candlestick2_ohlc
import matplotlib.pyplot as plt

from Calf.models.calendar1 import Calendar
from File.file import File
from kline.klineInfo import KlineInfo


class DbData:
    def __init__(self):
        pass
    @classmethod
    def get_code(cls,kline):
        if 'hk' in kline:
            return '00700'
        elif 'usa' in kline:
            return 'AAPL'
        elif 'index' in kline:
            return '399303'
        else:
            return '000555'
    @classmethod
    def check_db_data(cls, code,start_date,end_date,table, db='server_db',dbname='big-data',db2='server_db',dbname2='big-data',path='f://zjf//check_data//'):
        if table == None: raise Exception("table can't be empty")
        data=KlineData(location=db,dbname=dbname).read_data(code=code,start_date=start_date,end_date=end_date,kline=table,timemerge=True)
        data=data.sort_values(by=['date'],ascending=True)

        data2 = KlineData(location=db2, dbname=dbname2).read_data(code=code, start_date=start_date, end_date=end_date,
                                                               kline=table, timemerge=True)
        data2 = data2.sort_values(by=['date'], ascending=True)
        print('start draw.......')
        # fig, ax = plt.subplots()
        # fig.subplots_adjust(bottom=0.2)
        ax=plt.subplot(211)
        # plt.title('本地')
        ax.set_xticks([])
        candlestick2_ohlc(ax, data.open, data.high, data.low, data.close, width=1, colorup='red', colordown='green')
        plt.title(db+'--'+ table + '--' + code)
        ax=plt.subplot(212)
        # plt.title('远程')
        plt.title(db2+'--' + table + '--' + code)
        candlestick2_ohlc(ax, data2.open, data2.high, data2.low, data2.close, width=1, colorup='red', colordown='green')
        # plt.show()
        File.check_file(path=path)
        ax.set_xticks([])
        plt.savefig(path+table+'.png',transparent=True)
        plt.close()
# import datetime as dt
# table_list=['kline_day','kline_min5','kline_min30','kline_min60','index_min5','index_day','XDXR_day','hk_kline_day','usa_kline_day']
#
#
# for table in table_list:
#     end_date=Calendar.calc(Calendar.today(),0)['date']
#     off=-KlineInfo.get_general(kline=table)
#     print(table,off)
#     DbData.check_db_data(code=DbData.get_code(table),start_date=Calendar.calc(end_date,off)['date'],end_date=end_date,table=table,db2='hk_server_db')


