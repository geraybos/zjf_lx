# -*- coding: utf-8 -*-

from os.path import abspath, pardir, join
from sys import path

from app import markets
from app.models import Calendar
from app.actions import get_stock_code_list, get_xdxr

path.append(abspath(join(abspath(join(abspath(__file__), pardir)), pardir)))

if __name__ == '__main__':
    if not Calendar.in_business(dt=Calendar.today(), day=True):
        exit()
    start_date = None
    end_date = None
    stock_code_list = []
    for m in ['sh', 'sz']:
        stock_code_list = get_stock_code_list(market=markets[m])
        get_xdxr(market_name=m, stock_code_list=stock_code_list, start_date=start_date, end_date=end_date)
