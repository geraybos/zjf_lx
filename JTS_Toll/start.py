import datetime as dt
import subprocess
import threading
import time

import pyautogui
from Calf import BaseModel

from app.local_models.dealer import Dealer


class JtsStart():
    def start(self,file):

        print('strat')
        status = subprocess.call('taskkill /F /IM tws.exe')
        status = subprocess.call(file)
        BaseModel('jts_log').insert_batch(
            [{'date': dt.datetime.now(), 'event': 'login-pre','accounting_values': status}])

    def stop(self):
        status = subprocess.call('taskkill /F /IM tws.exe')

    def stop_delay(self):
        print('stop')
        status = subprocess.call('taskkill /F /IM tws.exe')
    def check(self):
        app = Dealer('127.0.0.1', 7497, 1)
        # time.sleep(1)
        while True:
            try:
                time.sleep(1)
                accounting_values = app.get_accounting_values('DU1162631')
                if accounting_values is not None:
                    BaseModel('jts_log').insert_batch(
                        [{'date': dt.datetime.now(), 'event': 'login-ok', 'accounting_values': accounting_values}])
                    break
                else:
                    BaseModel('jts_log').insert_batch(
                        [{'date': dt.datetime.now(), 'event': 'login-ok', 'accounting_values': accounting_values}])

                    print('accounting_values None')
            except Exception as e:
                print('av failed')

    def login(self):

        BaseModel('jts_log').insert_batch([{'date':dt.datetime.now(),'event':'login-start'}])
        pyautogui.PAUSE = 1
        pyautogui.FAILSAFE = True  # 启用自动防故障功能f
        # pyautogui.click(100, 100)
        pyautogui.typewrite('zjf', 0.1)
        pyautogui.typewrite(['shiftleft'], 0.1)
        pyautogui.typewrite('520520', 0.1)
        pyautogui.typewrite(['shiftleft','\t'], 0.1)

        pyautogui.typewrite('zjf', 0.1)
        pyautogui.typewrite(['shiftleft'], 0.1)
        pyautogui.typewrite('804533125', 0.1)
        pyautogui.typewrite(['shiftleft', '\t'], 0.1)
        pyautogui.typewrite(['down','down','\n'], 0.1)
        pyautogui.typewrite(['\t','\t','\t','\t','\t','\t','\t','\t','\n'], 0.1)
        time.sleep(30)
        self.check()











if __name__ == '__main__':
    obj=JtsStart()
    t1 = threading.Thread(target=obj.start,args=(u'C:\Jts/tws.exe',))
    t2 = threading.Thread(target=obj.login)
    # t3 = threading.Thread(target=obj.stop_delay())
    # obj.start('C:\Jts/tws.exe')
    # obj.login()
    t1.start()
    time.sleep(10)
    t2.start()
