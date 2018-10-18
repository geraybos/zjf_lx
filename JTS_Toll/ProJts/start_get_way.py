import datetime as dt
import subprocess
import threading
import time
from win32gui import IsWindow, IsWindowEnabled, IsWindowVisible, GetWindowText, SetForegroundWindow, EnumWindows

import pyautogui
from Calf.modelaction import ModelAction
from Calf import BaseModel, ModelRun
from app.local_models.dealer import Dealer
no='DU1162631'
no='DU1142167'
class JtsStart():
    def start(self, file):
        subprocess.call('taskkill /F /IM ibgateway.exe')
        subprocess.call('taskkill /F /IM tws.exe')
        subprocess.call(file)
    def stop(self):
        subprocess.call('taskkill /F /IM ibgateway.exe')
    def stop_delay(self):
        print('stop')
        subprocess.call('taskkill /F /IM tws.exe')
    def foo(self, hwnd, mouse):
        # 去掉下面这句就所有都输出了，但是我不需要那么多
        if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
            print(hwnd)
            if GetWindowText(hwnd) == 'IB Gateway':
                SetForegroundWindow(hwnd)
                print('ok')
                return
    def login(self):
        EnumWindows(self.foo, 0)
        pyautogui.PAUSE = 1
        pyautogui.FAILSAFE = True  # 启用自动防故障功能f
        pyautogui.typewrite(['right', '\t'], 0.1)
        pyautogui.typewrite('nwmdhk', 0.1)
        pyautogui.typewrite(['shiftleft'], 0.1)
        pyautogui.typewrite('715', 0.1)
        pyautogui.typewrite(['shiftleft', '\t'], 0.1)
        pyautogui.typewrite('MuLi', 0.1)
        pyautogui.typewrite(['shiftleft'], 0.1)
        pyautogui.typewrite('2018', 0.1)
        pyautogui.typewrite(['shiftleft', 'enter'], 0.1)
        time.sleep(10)
        pyautogui.typewrite(['space', 'space'], 0.1)
        # pyautogui.typewrite(['right', '\t'], 0.1)
        # pyautogui.typewrite('zjf', 0.1)
        # pyautogui.typewrite(['shiftleft'], 0.1)
        # pyautogui.typewrite('520520', 0.1)
        # pyautogui.typewrite(['shiftleft', '\t'], 0.1)
        # pyautogui.typewrite('zjf', 0.1)
        # pyautogui.typewrite(['shiftleft'], 0.1)
        # pyautogui.typewrite('804533125', 0.1)
        # pyautogui.typewrite(['shiftleft', 'enter'], 0.1)
        # time.sleep(10)
        # pyautogui.typewrite(['space', 'space'], 0.1)
        print('已经按下space')
        self.check()
    def check(self):
        app = Dealer('127.0.0.1', 4002, 4002)
        # x = app.get_accounting_values('DU1142167')
        x = app.get_accounting_values(no)
        BaseModel('jts_log').insert_batch(
            [{'date': dt.datetime.now(), 'event': 'login-ok', 'accounting_values': x,'user':no}])
        app.disconnect()
def exe():
    obj = JtsStart()
    app = Dealer('127.0.0.1', 4002, 4002)
    # x = app.get_accounting_values('DU1142167')
    x = app.get_accounting_values(no)
    try:
        app.disconnect()
    except Exception as e:
        print(e)
    if x is None:
        t1 = threading.Thread(target=obj.start, args=(u'C:\Jts\ibgateway\972/ibgateway.exe',))
        t2 = threading.Thread(target=obj.login)
        t1.start()
        time.sleep(10)
        t2.start()
    else:
        BaseModel('jts_log').insert_batch([{'date': dt.datetime.now(), 'event': '不用重启','accounting_values':x,'user':no}])
        print('状态不错不用重启')

class Min5Action(ModelAction):
    @classmethod
    def execute(cls, **kwargs):
        exe()

    @classmethod
    def is_trade_day(cls, date):
        return True

if __name__ == '__main__':
    exe()
    seconed=dt.datetime.now().minute
    ModelRun.DScheduler(Min5Action, execute_date='00:27:{}-23:59:00'.format(seconed), execute_interval=1 * 60)

