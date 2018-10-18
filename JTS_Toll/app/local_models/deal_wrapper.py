# -*- coding: utf-8 -*-
from queue import Queue, Empty

from ibapi.wrapper import EWrapper

from . import FINISHED, ACCOUNT_VALUE_FLAG, ACCOUNT_UPDATE_FLAG, ACCOUNT_TIME_FLAG, FILL_CODE
from .account import identifed_as
from .util_objects import orderInformation, execInformation


class DealWrapper(EWrapper):
    def __init__(self):
        self._my_contract_details = {}
        self._my_requested_execution = {}
        self._my_accounts = {}

        ## We set these up as we could get things coming along before we run an init
        self._my_executions_stream = Queue()
        self._my_commission_stream = Queue()
        self._my_open_orders = Queue()
        self._my_positions = Queue()

    def init_error(self):
        error_queue = Queue()
        self._my_errors = error_queue

    def get_error(self, timeout=10):
        if self.is_error():
            try:
                return self._my_errors.get(timeout=timeout)
            except Empty as e:
                raise e
        return None

    def is_error(self):
        return not self._my_errors.empty()

    def error(self, id, error_code, error_str):
        self._my_errors.put("IB error id %d errorcode %d string %s" % (id, error_code, error_str))

    ## get positions code
    def init_positions(self):
        positions_queue = self._my_positions = Queue()

        return positions_queue

    def position(self, account, contract, position,
                 avgCost):

        ## uses a simple tuple, but you could do other, fancier, things here
        self._my_positions.put((account, contract, position,
                                avgCost))

    def positionEnd(self):
        ## overriden method

        self._my_positions.put(FINISHED)

    def init_accounts(self, accountName):
        self.accountName = accountName
        self._my_accounts[accountName] = Queue()

        return self._my_accounts[accountName]

    def updateAccountValue(self, key: str, val: str, currency: str,
                           accountName: str):

        ## use this to seperate out different account data
        data = identifed_as(ACCOUNT_VALUE_FLAG, (key, val, currency))
        self._my_accounts[accountName].put(data)

    def updatePortfolio(self, contract, position: float,
                        marketPrice: float, marketValue: float,
                        averageCost: float, unrealizedPNL: float,
                        realizedPNL: float, accountName: str):

        ## use this to seperate out different account data
        data = identifed_as(ACCOUNT_UPDATE_FLAG, (contract, position, marketPrice, marketValue, averageCost,
                                                  unrealizedPNL, realizedPNL))
        self._my_accounts[accountName].put(data)

    def updateAccountTime(self, timeStamp: str):

        ## use this to seperate out different account data
        data = identifed_as(ACCOUNT_TIME_FLAG, timeStamp)
        self._my_accounts[self.accountName].put(data)

    def accountDownloadEnd(self, accountName: str):
        self._my_accounts[accountName].put(FINISHED)

    def init_contractdetails(self, contract_id):
        self._my_contract_details[contract_id] = Queue()
        return self._my_contract_details[contract_id]

    def contractDetails(self, contract_id, contract_details):
        ## overridden method

        if contract_id not in self._my_contract_details.keys():
            self.init_contractdetails(contract_id)

        self._my_contract_details[contract_id].put(contract_details)

    def contractDetailsEnd(self, contract_id):
        ## overriden method
        if contract_id not in self._my_contract_details.keys():
            self.init_contractdetails(contract_id)

        self._my_contract_details[contract_id].put(FINISHED)

    # orders
    def init_open_orders(self):
        open_orders_queue = self._my_open_orders = Queue()

        return open_orders_queue

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permid,
                    parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):

        order_details = orderInformation(orderId, status=status, filled=filled,
                                         avgFillPrice=avgFillPrice, permid=permid,
                                         parentId=parentId, lastFillPrice=lastFillPrice, clientId=clientId,
                                         whyHeld=whyHeld, mktCapPrice=mktCapPrice)

        self._my_open_orders.put(order_details)

    def openOrder(self, orderId, contract, order, orderstate):
        """
        Tells us about any orders we are working now
        overriden method
        """

        order_details = orderInformation(orderId, contract=contract, order=order, orderstate=orderstate)
        self._my_open_orders.put(order_details)

    def openOrderEnd(self):
        """
        Finished getting open orders
        Overriden method
        """

        self._my_open_orders.put(FINISHED)

    """ Executions and commissions
    requested executions get dropped into single queue: self._my_requested_execution[reqId]
    Those that arrive as orders are completed without a relevant reqId go into self._my_executions_stream
    All commissions go into self._my_commission_stream (could be requested or not)
    The *_stream queues are permanent, and init when the TestWrapper instance is created
    """

    def init_requested_execution_data(self, reqId):
        execution_queue = self._my_requested_execution[reqId] = Queue()

        return execution_queue

    def access_commission_stream(self):
        ## Access to the 'permanent' queue for commissions

        return self._my_commission_stream

    def access_executions_stream(self):
        ## Access to the 'permanent' queue for executions

        return self._my_executions_stream

    def commissionReport(self, commreport):
        """
        This is called if
        a) we have submitted an order and a fill has come back
        b) We have asked for recent fills to be given to us
        However no reqid is ever passed
        overriden method
        :param commreport:
        :return:
        """

        commdata = execInformation(commreport.execId, Commission=commreport.commission,
                                   commission_currency=commreport.currency,
                                   realisedpnl=commreport.realizedPNL)

        ## there are some other things in commreport you could add
        ## make sure you add them to the .attributes() field of the execInformation class

        ## These always go into the 'stream' as could be from a request, or a fill thats just happened
        self._my_commission_stream.put(commdata)

    def execDetails(self, reqId, contract, execution):
        """
        This is called if
        a) we have submitted an order and a fill has come back (in which case reqId will be FILL_CODE)
        b) We have asked for recent fills to be given to us (reqId will be
        See API docs for more details
        """
        ## overriden method

        execdata = execInformation(execution.execId, contract=contract,
                                   ClientId=execution.clientId, OrderId=execution.orderId,
                                   time=execution.time, AvgPrice=execution.avgPrice,
                                   AcctNumber=execution.acctNumber, Shares=execution.shares,
                                   Price=execution.price)

        ## there are some other things in execution you could add
        ## make sure you add them to the .attributes() field of the execInformation class

        reqId = int(reqId)

        ## We eithier put this into a stream if its just happened, or store it for a specific request
        if reqId == FILL_CODE:
            self._my_executions_stream.put(execdata)
        else:
            self._my_requested_execution[reqId].put(execdata)

    def execDetailsEnd(self, reqId):
        """
        No more orders to look at if execution details requested
        """
        self._my_requested_execution[reqId].put(FINISHED)

    ## order ids
    def init_nextvalidid(self):

        orderid_queue = self._my_orderid_data = Queue()

        return orderid_queue

    def nextValidId(self, orderId):
        """
        Give the next valid order id
        Note this doesn't 'burn' the ID; if you call again without executing the next ID will be the same
        If you're executing through multiple clients you are probably better off having an explicit counter
        """
        if getattr(self, '_my_orderid_data', None) is None:
            ## getting an ID which we haven't asked for
            ## this happens, IB server just sends this along occassionally
            self.init_nextvalidid()

        self._my_orderid_data.put(orderId)
