# -*- coding: utf-8 -*-
# tushare 数据，每日
from app.actions import tushare_to_db
from app.models import Calendar

if not Calendar.in_business(dt=Calendar.today(), day=True):
	exit()
tushare_to_db()
exit()
