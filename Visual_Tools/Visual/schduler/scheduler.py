from Calf import ModelAction, BaseModel, ModelRun
from Calf.models import Calendar
from Visual.Macd.macdAstock import macd_exe
from Visual.ma.maklineday import start_exe


class Action_other(ModelAction):
    @classmethod
    def start(cls, **kwargs):
        start_exe()
        macd_exe()
        start_exe(kline='kline_day')
        macd_exe(kline='kline_day')

    @classmethod
    def is_trade_day(cls, date):
        curror=BaseModel('calendar').query(dict(date=Calendar.today()))
        return True if curror.count() else False
if __name__ == '__main__':
    ModelRun.DScheduler(Action_other, start_date='16:23:00')