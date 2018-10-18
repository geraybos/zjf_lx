import datetime as dt
import subprocess
import threading
import time
import pyautogui
from Calf.modelaction import ModelAction
from Calf import BaseModel, ModelRun
from app.local_models.dealer import Dealer
class JtsStart():
    def start(self,file):
        status = subprocess.call('taskkill /F /IM tws.exe')
        status = subprocess.call(file)
    def stop(self):
        status = subprocess.call('taskkill /F /IM tws.exe')
    def stop_delay(self):
        print('stop')
        status = subprocess.call('taskkill /F /IM tws.exe')
    def check(self):
        app = None
        # time.sleep(1)
        count=1
        while True:
            try:
                app= Dealer('127.0.0.1', 7497, 1)
                time.sleep(1)
                # accounting_values = app.get_accounting_values('DU1162631')
                accounting_values = app.get_accounting_values('DU1142167')

                if accounting_values is not None:
                    BaseModel('jts_log').insert_batch(
                        [{'date': dt.datetime.now(), 'event': 'login-ok', 'accounting_values': accounting_values}])
                    print(count)
                    break
                else:
                    BaseModel('jts_log').insert_batch(
                        [{'date': dt.datetime.now(), 'event': 'login-ok', 'accounting_values': accounting_values}])
                    print('fail',accounting_values)

            except Exception as e:
                print('av failed')
            count += 1
    def login(self):

        BaseModel('jts_log').insert_batch([{'date':dt.datetime.now(),'event':'login-start'}])
        pyautogui.PAUSE = 1
        pyautogui.FAILSAFE = True  # 启用自动防故障功能f
        # pyautogui.click(100, 100)
        # pyautogui.typewrite('zjf', 0.1)
        # pyautogui.typewrite(['shiftleft'], 0.1)
        # pyautogui.typewrite('520520', 0.1)
        # pyautogui.typewrite(['shiftleft','\t'], 0.1)
        # pyautogui.typewrite('zjf', 0.1)
        # pyautogui.typewrite(['shiftleft'], 0.1)
        # pyautogui.typewrite('804533125', 0.1)
        # pyautogui.typewrite(['shiftleft', '\t'], 0.1)
        # pyautogui.typewrite(['down','down','\n'], 0.1)
        # pyautogui.typewrite(['\t','\t','\t','\t','\t','\t','\t','\t','\n'], 0.1)


        pyautogui.typewrite('nwmdhk', 0.1)
        pyautogui.typewrite(['shiftleft'], 0.1)
        pyautogui.typewrite('715', 0.1)
        pyautogui.typewrite(['shiftleft', '\t'], 0.1)
        pyautogui.typewrite('MuLi', 0.1)
        pyautogui.typewrite(['shiftleft'], 0.1)
        pyautogui.typewrite('2018', 0.1)
        pyautogui.typewrite(['shiftleft', '\t'], 0.1)
        pyautogui.typewrite(['down', 'down', '\n'], 0.1)
        pyautogui.typewrite(['\t','\t','\t','\t','\t','\t','\t','\t','\n'], 0.1)


        # self.check()
def exe():
    obj=JtsStart()
    t1 = threading.Thread(target=obj.start,args=(u'C:\Jts/tws.exe',))
    t2 = threading.Thread(target=obj.login)
    # t3 = threading.Thread(target=obj.stop_delay())
    # obj.start('C:\Jts/tws.exe')
    # obj.login()
    t1.start()
    time.sleep(10)
    t2.start()

    # lockwork='rundll32.exe user32.dll,LockWorkStation'
    # pyautogui.PAUSE = 1
    # pyautogui.FAILSAFE = False  # 启用自动防故障功能f
    # pyautogui.hotkey('winleft', 'r')
    # pyautogui.hotkey('ctrl', 'a')
    # pyautogui.hotkey('delete')
    # pyautogui.typewrite('rundll')
    # pyautogui.typewrite(['shift'])
    # pyautogui.typewrite('32.exe')
    # pyautogui.typewrite(['shift'])
    # pyautogui.typewrite(' user')
    # pyautogui.typewrite(['shift'])
    #
    # pyautogui.typewrite('32.dll,LockWorkStation')
    # pyautogui.typewrite(['shift'],1)
    # pyautogui.typewrite(['\n'])
    # print('suole ok?')8
class Min5Action(ModelAction):
    @classmethod
    def execute(cls, **kwargs):
        exe()
    @classmethod
    def is_trade_day(cls, date):
        return True
if __name__ == '__main__':
    # exe(),
    # time.sleep(60)
    # JtsStart().check()
    # # ModelRun.DScheduler(Min5Action, execute_date='0:1:00-23:59:00', execute_interval=30*60)
    app = Dealer('127.0.0.1', 4002,1)
    # app.disconnect()
    print(app)
    # app.conn=None
    # accounting_values = app.get_accounting_values('DU1142167')
    # print(accounting_values)
    # accounting_values = app.get_current_positions()
    # print(accounting_values)