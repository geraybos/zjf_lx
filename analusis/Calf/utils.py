# encoding: utf-8

"""
@version: 1.0
@author: LeungJain
@time: 2017/11/27 14:10
"""
import datetime as dt
import warnings
import time
# import pygame
import threading
import smtplib
import email.mime.multipart
import email.mime.text
from Calf import config
import sys
from business_calendar import Calendar, MO, TU, WE, TH, FR
from Calf import project_dir
from Calf.exception import ExceptionInfo

warnings.filterwarnings('ignore')


class fontcolor:
    F_RED = '\033[31m'
    F_GREEN = '\033[32m'
    F_YELLOW = '\033[33m'
    F_BLUE = '\033[34m'
    F_PURPLE = '\033[35m'
    F_GREEN_BLUE = '\033[36m'
    B_WHITE_F_BLACK = '\033[7;37;30m'
    END = '\033[0m'


def progress_bar(total, complete, **kwargs):
    isr = int(60 * complete / total)
    sr = ' ' * isr
    # print('\rRun:{0}\033[7;37;30m{1}\033[0m{2}/{3}'.format(kwargs, sr, complete, total), end='', flush=True)


def play_music(sound, second=10):
    """
    播放一段声音文件
    :param second: 播放的时间
    :param sound:文件名
    :return:
    """
    try:
        # sys.path[1]
        # file = project_dir + '\Calf\Files\\' + sound
        # pygame.mixer.init()
        # # print("播放音乐1")
        # track = pygame.mixer.music.load(file)
        # pygame.mixer.music.play()
        # time.sleep(second)
        # pygame.mixer.music.stop()
        pass
    except Exception as e:
        ExceptionInfo(e)
        pass


def sound_notice(sound_name):
    """
    以多线程的方式播放一段音频文件
    :param sound_name:
    :return:
    """
    try:
        t = threading.Thread(target=play_music, args=(sound_name,))
        return t
    except Exception as e:
        ExceptionInfo(e)


class trading:
    """
    关于交易所的一些基本概况
    ！！！适用于中国A股
    """
    # 2016 2017年非周末假日
    # holidays = ['2016-01-01', '2016-02-08', '2016-02-09', '2016-02-10', '2016-02-11',
    #             '2016-02-12', '2016-04-04', '2016-05-02', '2016-06-09', '2016-06-10',
    #             '2016-09-15', '2016-09-16', '2016-10-03', '2016-10-04', '2016-10-05',
    #             '2016-10-06', '2016-10-07',
    #             '2017-01-02', '2017-01-27', '2017-01-30', '2017-01-31', '2017-02-01',
    #             '2017-02-02', '2017-04-03', '2017-04-04', '2017-05-01', '2017-05-29',
    #             '2017-05-30', '2017-10-02', '2017-10-03', '2017-10-04', '2017-10-05',
    #             '2017-10-06',
    #             '2018-01-01', '2018-02-15', '2018-02-16', '2018-02-19', '2018-02-20',
    #             '2018-02-21', '2018-02-22', '2018-04-05', '2018-04-06', '2018-04-30',
    #             '2018-05-01', '2018-06-18', '2018-09-24', '2018-10-01', '2018-10-02',
    #             '2018-10-03', '2018-10-04', '2018-10-05']
    market = config.default_market_id(info_type='MarketHolidays')
    holidays = config.load_market_holidays(market=market) if market is not None else list()
    workdays = [MO, TU, WE, TH, FR]

    # fe_holidays = [[1, 1], [1, 2], [1, 3], [5, 1], [12, 25], [12, 26], [12, 27]]
    # d = dt.datetime.today()
    # fe_holidays = [lambda d:dt.datetime]
    def __init__(self, market=None):
        if market is not None:
            trading.market = market
            trading.holidays = config.load_market_holidays(market=market)

    @classmethod
    def trade_days(cls, start, end):
        """
        给定两个时间，计算这个时间段内有多少个交易日
        :param start:
        :param end:
        :return:
        """
        try:
            cal = Calendar(workdays=cls.workdays, holidays=cls.holidays)
            days = cal.busdaycount(start, end)
            return days
        except Exception as e:
            ExceptionInfo(e)
            return 0

    @classmethod
    def trade_period(cls, start, days, holidays=None):
        """
        计算某个时间x个交易日后的时间,或之前（days为一个负数）
        :param start:
        :param days:
        :return:
        """
        try:
            holidays = cls.holidays if holidays is None else holidays
            cal = Calendar(workdays=cls.workdays, holidays=holidays)
            end = cal.addbusdays(start, days)
            return end
        except Exception as e:
            ExceptionInfo(e)
            return start

    @classmethod
    def is_trade_day(cls, date, holidays=None):
        """
        判断给定的这个时间是否是交易日（以日记）
        :param date: 需要判断的时间
        :return:
        """
        try:
            holidays = cls.holidays if holidays is None else holidays
            cal = Calendar(workdays=cls.workdays, holidays=holidays)
            flag = cal.isbusday(dt.datetime(date.year, date.month, date.day))
            return flag
        except Exception as e:
            ExceptionInfo(e)
            return False

    @classmethod
    def fix_interval(cls, date, category, direction=-1):
        """
        为了取得足够量的数据，不同的K线应具有合理的间隔
        :param date:
        :param category:
        :param direction:
        :return:
        """

    @classmethod
    def fix_time(cls, kline, date):
        """
        基本kline表的time字段通常与实际不符，我们需要知道距
        某个时点最近的一条K线的time, 这个方法目前只适用于中国股票
        并且强烈建议只在不间歇的实时任务中使用
        :param kline:
        :param date:
        :return:
        """
        try:
            t = date.hour * 100 + date.minute
            if kline == 'kline_min30':
                if 1000 <= t < 1030:
                    return 1000
                elif 1030 <= t < 1100:
                    return 1030
                elif 1100 <= t < 1130:
                    return 1100
                elif 1130 <= t < 1330:
                    return 1300
                elif 1330 <= t < 1400:
                    return 1330
                elif 1400 <= t < 1430:
                    return 1400
                elif 1430 <= t < 1450:
                    return 1430
                else:
                    return 1500
            elif kline == 'kline_min60':
                if 1030 <= t < 1130:
                    return 1030
                elif 1130 <= t < 1400:
                    return 1300
                elif 1400 <= t < 1450:
                    return 1400
                else:
                    return 1500
            else:
                return 0
        except Exception as e:
            ExceptionInfo(e)
            return 0


class Email:
    @classmethod
    def send_email(cls, msgTo, content):
        try:
            msg = email.mime.multipart.MIMEMultipart()
            msgFrom = 'leungjain@163.com'  # 从该邮箱发送
            msgTo = msgTo  # 发送到该邮箱
            smtpSever = 'smtp.163.com'  # 163邮箱的smtp Sever地址
            smtpPort = '25'  # 开放的端口
            sqm = '7891190129lj'  # 在登录smtp时需要login中的密码应当使用授权码而非账户密码
            msg['from'] = msgFrom
            msg['to'] = msgTo
            msg['subject'] = '曲速智选'
            content = content

            txt = email.mime.text.MIMEText(content)
            msg.attach(txt)
            smtp = smtplib.SMTP()

            '''
            smtplib的connect（连接到邮件服务器）、login（登陆验证）、sendmail（发送邮件）
            '''
            smtp.connect(smtpSever, smtpPort)
            smtp.login(msgFrom, sqm)
            smtp.sendmail(msgFrom, msgTo, str(msg))
            smtp.quit()
            # print('发送成功')
            return True
        except Exception as e:
            print(e)
            # print('发送失败!')
            return False

# Email.send_email(msgTo='leungjain@qq.com', content='hhhhhh')
# date1 = dt.datetime(2017, 9, 29)
# print(trading.fix_time(kline='min60', date=date1))
# date2 = dt.datetime(2018, 4, 6)
# # print(trading.trade_days(date1, date2))
# r = trading.is_trade_day(date2)
# print(r)
# sound_notice('alert.wav').start()