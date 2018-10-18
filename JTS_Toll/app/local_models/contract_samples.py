# -*- coding: utf-8 -*-
from ibapi.contract import Contract


class ContractSamples(object):
    def __init__(self):
        self.c_f = {
            'HK': self.stock_HK,
            'CN': self.stock_CN,
            'US': self.stock_US,
            'UK': self.stock_UK,
            'FX': self.forex
        }

    def gene_contract(self, stock_code, market):
        return self.c_f[market](stock_code)

    @staticmethod
    def stock_HK(stock_code):
        contract = Contract()
        contract.currency = "HKD"
        contract.exchange = "SEHK"
        contract.secType = "STK"
        contract.symbol = stock_code
        return contract

    @staticmethod
    def stock_CN(stock_code):
        contract = Contract()
        contract.currency = "CNH"
        contract.exchange = "SEHKNTL" if stock_code[:2] == '60' else "SEHKSZSE"
        contract.secType = "STK"
        contract.symbol = stock_code
        return contract

    @staticmethod
    def stock_US(stock_code):
        contract = Contract()
        contract.currency = "USD"
        contract.exchange = "SMART"
        contract.secType = "STK"
        contract.symbol = stock_code
        return contract

    @staticmethod
    def stock_UK(stock_code):
        contract = Contract()
        contract.currency = "GBP"
        contract.exchange = "LSE"
        contract.secType = "STK"
        contract.symbol = stock_code
        return contract

    @staticmethod
    def forex(code):
        foreign, local = code[:3], code[3:]
        contract = Contract()
        contract.currency = local
        contract.secType = "CASH"
        contract.symbol = foreign
        contract.exchange = "IDEALPRO"
        return contract
