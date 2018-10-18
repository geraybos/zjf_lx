# -*- coding: utf-8 -*-
from ibapi.order import Order


class OrderSample(object):
    @staticmethod
    def sell_limit_price(volume, price, tp='OG'):
        order = Order()
        order.action = 'SELL'
        order.orderType = 'LMT'
        order.totalQuantity = volume
        order.lmtPrice = price
        order.transmit = True
        order.tif = 'DAY' if tp == 'OG' else 'GTC'
        return order

    @staticmethod
    def sell_market_price(volume):
        order = Order()
        order.action = 'SELL'
        order.orderType = 'MKT'
        order.totalQuantity = volume
        return order

    @staticmethod
    def buy_limit_price(volume, price, tp='OG'):
        order = Order()
        order.action = 'BUY'
        order.orderType = 'LMT'
        order.totalQuantity = volume
        order.lmtPrice = price
        order.transmit = True
        order.tif = 'DAY' if tp == 'OG' else 'GTC'
        return order

    @staticmethod
    def buy_market_price(volume):
        order = Order()
        order.action = 'BUY'
        order.orderType = 'MKT'
        order.totalQuantity = volume
        return order

    @staticmethod
    def stop(action: str, quantity: float, stopPrice: float):
        # ! [stop]
        order = Order()
        order.action = action
        order.orderType = "STP LMT"
        order.lmtPrice = stopPrice
        order.auxPrice = stopPrice
        order.totalQuantity = quantity
        order.tif = 'GTC'
        # ! [stop]
        return order
