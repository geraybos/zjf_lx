# -*- coding: utf-8 -*-
from app.models.fundamentals import ZYBK_TTM, ZJH_TTM
from app.models.mark import kline_data_update_mark, Check_Data


class LazyProperty(object):
    def __init__(self, method):
        self.method = method
        self.method_name = method.__name__
        print('function overriden: {}'.format(self.method))
        print("function's name: {}".format(self.method_name))

    def __get__(self, obj, cls):
        if not obj:
            return None
        value = self.method(obj)
        print('value {}'.format(value))
        setattr(obj, self.method_name, value)
        return value


from .calendar import Calendar
from .feature import DayFeature, IndexFeature, Tushare, Capital, IndexMA, MinuteFeature
from .index import DayIndex, MintueIndex, WeekIndex, MonthIndex
from .kline import Day, Minute, Week, Month, Tick
from .market import Market
from .xdxr import XDXROffset, DayXDXR, MinuteXDXR, XDXR

model_list = {
    'tmp_kline_min5': Minute('tmp_kline_min5'),
    'kline_tick': Tick('kline_tick'),
    'kline_month': Month('kline_month'),
    'kline_week': Week('kline_week'),
    'kline_day': Day('kline_day'),
    'hk_kline_day': Day('hk_kline_day'),
    'hk_kline_min60': Minute('hk_kline_min60'),
    'usa_kline_day': Day('usa_kline_day'),
    'usa_kline_min60': Minute('usa_kline_min60'),
    'usa_kline_min5': Minute('usa_kline_min5'),
    'usa_kline_min15': Minute('usa_kline_min15'),
    'usa_kline_min30': Minute('usa_kline_min30'),
    'kline_min1': Minute('kline_min1'),
    'kline_min5': Minute('kline_min5'),
    'kline_min15': Minute('kline_min15'),
    'kline_min30': Minute('kline_min30'),
    'kline_min60': Minute('kline_min60'),
    'index_month': MonthIndex('index_month'),
    'index_week': WeekIndex('index_week'),
    'index_day': DayIndex('index_day'),
    'index_min5': MintueIndex('index_min5'),
    'index_min15': MintueIndex('index_min15'),
    'index_min30': MintueIndex('index_min30'),
    'index_min60': MintueIndex('index_min60'),
    'XDXR': XDXR('XDXR'),
    'XDXR_day': DayXDXR('XDXR_day'),
    'XDXR_min5': MinuteXDXR('XDXR_min5'),
    'XDXR_min15': MinuteXDXR('XDXR_min15'),
    'XDXR_min30': MinuteXDXR('XDXR_min30'),
    'XDXR_min60': MinuteXDXR('XDXR_min60'),
    'fund_zybk_ttm': ZYBK_TTM('fund_zybk_ttm'),
    'fund_zjh_ttm': ZJH_TTM('fund_zjh_ttm'),
    'fund_zz_ttm': ZJH_TTM('fund_zz_ttm'),
    'feature_day': DayFeature('feature_day'),
    'feature_min5': MinuteFeature('feature_min5'),
    'feature_index_day': IndexFeature('feature_index_day'),
    'feature_index_min5': IndexFeature('feature_index_min5'),
    'ma_index': IndexMA('ma_index'),
    'tushare': Tushare('tushare'),
    'capital': Capital('capital'),
    'kline_data_update_mark': kline_data_update_mark('kline_data_update_mark'),
    'check_data': Check_Data('check_data'),
    'calendar':Calendar('calendar')
}
