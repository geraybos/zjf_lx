# -*- coding: utf-8 -*-

FINISHED = object()
NO_ATTRIBUTES_SET = object()
TIME_OUT = object()
STARTED = object()
FILL_CODE = -1
DEFAULT_MARKET_DATA_ID = 50
DEFAULT_GET_CONTRACT_ID = 43
DEFAULT_EXEC_TICKER = 78
ACCOUNT_UPDATE_FLAG = "update"
ACCOUNT_VALUE_FLAG = "value"
ACCOUNT_TIME_FLAG = "time"

from .contract_samples import *
from .deal_client import *
from .deal_wrapper import *
from .order_sample import *
from .util_objects import *
