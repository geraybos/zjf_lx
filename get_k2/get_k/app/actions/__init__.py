# -*- coding: utf-8 -*-

from .. import TradeX
from ..models import Calendar, Market

__today = Calendar.today()

market_a = Market(TradeX, 'market_a_server')
# market_ex = Market(TradeX, 'market_ex_server')

data_client = market_a.connect
print("data_client:"+str(data_client))
# data_client_ex = market_ex.connect
data_client_ex = None

from .utils import get_stock_code_list
from .index_market_a import get_realtime as i_realtime_a
from .index_market_a import get_history as i_history_a
from .index_market_a import get_specified as i_specified_a
from .kline_market_a import get_realtime as k_realtime_a
from .kline_market_a import get_history as k_history_a
from .kline_market_a import get_specified as k_specified_a
from .kline_market_a import get_history_tick as k_tick_a
from .kline_market_a import generate_min_by_tick
from .kline_market_ex import get_realtime as k_realtime_ex
from .kline_market_ex import get_history as k_history_ex
from .kline_market_ex import get_specified as k_specified_ex
from .calendar import get_trade_cal
from .xdxr_market_a import get_xdxr, calc_xdxr_specified
from .fund_a import get_zybk_ttm as f_zybk_ttm_a
from .fund_a import get_ttm as f_zz_ttm_a
from .fund_a import get_ttm as f_zjh_ttm_a
from .feature_a import capital_to_db
from .feature_a import tushare_to_db
from .feature_a import day_feature, day_feature_index, calc_feature, minute_feature_index
from .ma import calc_ma