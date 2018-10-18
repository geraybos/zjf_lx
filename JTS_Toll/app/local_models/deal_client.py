# -*- coding: utf-8 -*-
from datetime import datetime
from queue import Empty

from ibapi.client import EClient
from ibapi.execution import ExecutionFilter

from . import ACCOUNT_VALUE_FLAG, ACCOUNT_UPDATE_FLAG, ACCOUNT_TIME_FLAG, DEFAULT_GET_CONTRACT_ID, DEFAULT_EXEC_TICKER, \
    TIME_OUT
from .account import simpleCache
from .util_objects import list_of_execInformation, finishableQueue, list_of_identified_items, list_of_orderInformation


class DealClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)
        self._account_cache = simpleCache(max_staleness_seconds=5 * 60)
        self._account_cache.update_data = self._update_accounting_data
        self._market_data_q_dict = {}
        self._commissions = list_of_execInformation()

    def get_current_positions(self):
        """
        Current positions held

        :return:
        """

        ## Make a place to store the data we're going to return
        positions_queue = finishableQueue(self.wrapper.init_positions())

        ## ask for the data
        self.reqPositions()

        ## poll until we get a termination or die of boredom
        MAX_WAIT_SECONDS = 1
        positions_list = positions_queue.get(timeout=MAX_WAIT_SECONDS)

        while self.wrapper.is_error():
            print(self.wrapper.get_error())

        if positions_queue.timed_out():
            print("Exceeded maximum wait for wrapper to confirm finished whilst getting positions")

        return positions_list

    def _update_accounting_data(self, accountName):
        """
        Update the accounting data in the cache

        :param accountName: account we want to get data for
        :return: nothing
        """

        ## Make a place to store the data we're going to return
        accounting_queue = finishableQueue(self.wrapper.init_accounts(accountName))

        ## ask for the data
        self.reqAccountUpdates(True, accountName)

        ## poll until we get a termination or die of boredom
        MAX_WAIT_SECONDS = 1
        accounting_list = accounting_queue.get(timeout=MAX_WAIT_SECONDS)

        while self.wrapper.is_error():
            print(self.wrapper.get_error())

        if accounting_queue.timed_out():
            print("Exceeded maximum wait for wrapper to confirm finished whilst getting accounting data")

        # seperate things out, because this is one big queue of data with different things in it
        accounting_list = list_of_identified_items(accounting_list)
        seperated_accounting_data = accounting_list.seperate_into_dict()

        ## update the cache with different elements
        self._account_cache.update_cache(accountName, seperated_accounting_data)

        ## return nothing, information is accessed via get_... methods

    def get_accounting_time_from_server(self, accountName):
        """
        Get the accounting time from IB server

        :return: accounting time as served up by IB
        """

        # All these functions follow the same pattern: check if stale or missing, if not return cache, else update values

        return self._account_cache.get_updated_cache(accountName, ACCOUNT_TIME_FLAG)

    def get_accounting_values(self, accountName):
        """
        Get the accounting values from IB server

        :return: accounting values as served up by IB
        """

        # All these functions follow the same pattern: check if stale, if not return cache, else update values

        return self._account_cache.get_updated_cache(accountName, ACCOUNT_VALUE_FLAG)

    def get_accounting_updates(self, accountName):
        """
        Get the accounting updates from IB server

        :return: accounting updates as served up by IB
        """

        # All these functions follow the same pattern: check if stale, if not return cache, else update values

        return self._account_cache.get_updated_cache(accountName, ACCOUNT_UPDATE_FLAG)

    def resolve_ib_contract(self, ibcontract, reqId=DEFAULT_GET_CONTRACT_ID):

        """
        From a partially formed contract, returns a fully fledged version
        :returns fully resolved IB contract
        """

        ## Make a place to store the data we're going to return
        contract_details_queue = finishableQueue(self.wrapper.init_contractdetails(reqId))

        print("Getting full contract details from the server... ")

        self.reqContractDetails(reqId, ibcontract)

        ## Run until we get a valid contract(s) or get bored waiting
        MAX_WAIT_SECONDS = 1
        new_contract_details = contract_details_queue.get(timeout=MAX_WAIT_SECONDS)

        while self.wrapper.is_error():
            print(self.wrapper.get_error())

        if contract_details_queue.timed_out():
            print("Exceeded maximum wait for wrapper to confirm finished - seems to be normal behaviour")

        if len(new_contract_details) == 0:
            print("Failed to get additional contract details: returning unresolved contract")
            return ibcontract

        if len(new_contract_details) > 1:
            print("got multiple contracts using first one")

        new_contract_details = new_contract_details[0]

        resolved_ibcontract = new_contract_details.contract

        return resolved_ibcontract

    def get_next_brokerorderid(self):
        """
        Get next broker order id
        :return: broker order id, int; or TIME_OUT if unavailable
        """

        ## Make a place to store the data we're going to return
        orderid_q = self.wrapper.init_nextvalidid()

        self.reqIds(-1)  # -1 is irrelevant apparently (see IB API docs)

        ## Run until we get a valid contract(s) or get bored waiting
        MAX_WAIT_SECONDS = 1
        try:
            brokerorderid = orderid_q.get(timeout=MAX_WAIT_SECONDS)
        except Empty:
            print("Wrapper timeout waiting for broker orderid")
            brokerorderid = TIME_OUT

        while self.wrapper.is_error():
            print(self.wrapper.get_error(timeout=MAX_WAIT_SECONDS))

        return brokerorderid

    def place_new_IB_order(self, ibcontract, order, orderid=None, poid=None, order_type=None):
        """
        Places an order
        Returns brokerorderid
        """

        ## We can eithier supply our own ID or ask IB to give us the next valid one
        if order_type != 'OG':
            if poid is not None and isinstance(poid, int):
                order.parentId=poid
            else:
                raise Exception
        if orderid is None:
            print("Getting orderid from IB")
            orderid = self.get_next_brokerorderid()

            if orderid is TIME_OUT:
                raise Exception("I couldn't get an orderid from IB, and you didn't provide an orderid")

        print("Using order id of %d" % orderid)

        ## Note: It's possible if you have multiple traidng instances for orderids to be submitted out of sequence
        ##   in which case IB will break

        # Place the order
        self.placeOrder(
            orderid,  # orderId,
            ibcontract,  # contract,
            order  # order
        )

        return orderid

    def any_open_orders(self):
        """
        Simple wrapper to tell us if we have any open orders
        """

        return len(self.get_open_orders()) > 0

    def get_open_orders(self):
        """
        Returns a list of any open orders
        """

        ## store the orders somewhere
        open_orders_queue = finishableQueue(self.wrapper.init_open_orders())

        ## You may prefer to use reqOpenOrders() which only retrieves orders for this client
        self.reqAllOpenOrders()

        ## Run until we get a terimination or get bored waiting
        MAX_WAIT_SECONDS = 1
        open_orders_list = list_of_orderInformation(open_orders_queue.get(timeout=MAX_WAIT_SECONDS))

        while self.wrapper.is_error():
            print(self.wrapper.get_error())

        if open_orders_queue.timed_out():
            print("Exceeded maximum wait for wrapper to confirm finished whilst getting orders")

        ## open orders queue will be a jumble of order details, turn into a tidy dict with no duplicates
        open_orders_dict = open_orders_list.merged_dict()

        return open_orders_dict

    def get_executions_and_commissions(self, reqId=DEFAULT_EXEC_TICKER, execution_filter=ExecutionFilter()):
        """
        Returns a list of all executions done today with commission data
        """

        ## store somewhere
        execution_queue = finishableQueue(self.wrapper.init_requested_execution_data(reqId))

        ## We can change ExecutionFilter to subset different orders
        ## note this will also pull in commissions but we would use get_executions_with_commissions
        self.reqExecutions(reqId, execution_filter)

        ## Run until we get a terimination or get bored waiting
        MAX_WAIT_SECONDS = 1
        exec_list = list_of_execInformation(execution_queue.get(timeout=MAX_WAIT_SECONDS))

        while self.wrapper.is_error():
            print(self.wrapper.get_error())

        if execution_queue.timed_out():
            print("Exceeded maximum wait for wrapper to confirm finished whilst getting exec / commissions")

        ## Commissions will arrive seperately. We get all of them, but will only use those relevant for us
        commissions = self._all_commissions()

        ## glue them together, create a dict, remove duplicates
        all_data = exec_list.blended_dict(commissions)

        return all_data

    def _recent_fills(self):
        """
        Returns any fills since we last called recent_fills
        :return: list of executions as execInformation objects
        """

        ## we don't set up a queue but access the permanent one
        fill_queue = self.wrapper.access_executions_stream()

        list_of_fills = list_of_execInformation()

        while not fill_queue.empty():
            MAX_WAIT_SECONDS = 1
            try:
                next_fill = fill_queue.get(timeout=MAX_WAIT_SECONDS)
                list_of_fills.append(next_fill)
            except Empty:
                ## corner case where Q emptied since we last checked if empty at top of while loop
                pass

        ## note this could include duplicates and is a list
        return list_of_fills

    def recent_fills_and_commissions(self):
        """
        Return recent fills, with commissions added in
        :return: dict of execInformation objects, keys are execids
        """

        recent_fills = self._recent_fills()
        commissions = self._all_commissions()  ## we want all commissions

        ## glue them together, create a dict, remove duplicates
        all_data = recent_fills.blended_dict(commissions)

        return all_data

    def _recent_commissions(self):
        """
        Returns any commissions that are in the queue since we last checked
        :return: list of commissions as execInformation objects
        """

        ## we don't set up a queue, as there is a permanent one
        comm_queue = self.wrapper.access_commission_stream()

        list_of_comm = list_of_execInformation()

        while not comm_queue.empty():
            MAX_WAIT_SECONDS = 5
            try:
                next_comm = comm_queue.get(timeout=MAX_WAIT_SECONDS)
                list_of_comm.append(next_comm)
            except Empty:
                ## corner case where Q emptied since we last checked if empty at top of while loop
                pass

        ## note this could include duplicates and is a list
        return list_of_comm

    def _all_commissions(self):
        """
        Returns all commissions since we created this instance
        :return: list of commissions as execInformation objects
        """

        original_commissions = self._commissions
        latest_commissions = self._recent_commissions()

        all_commissions = list_of_execInformation(original_commissions + latest_commissions)

        self._commissions = all_commissions

        # note this could include duplicates and is a list
        return all_commissions

    def cancel_order(self, orderid):

        ## Has to be an order placed by this client. I don't check this here -
        ## If you have multiple IDs then you you need to check this yourself.

        self.cancelOrder(orderid)

        ## Wait until order is cancelled
        start_time = datetime.now()
        MAX_WAIT_TIME_SECONDS = 10

        finished = False

        while not finished:
            if orderid not in self.get_open_orders():
                ## finally cancelled
                finished = True

            if (datetime.now() - start_time).seconds > MAX_WAIT_TIME_SECONDS:
                print("Wrapper didn't come back with confirmation that order was cancelled!")
                finished = True

        ## return nothing

    def cancel_all_orders(self):

        ## Cancels all orders, from all client ids.
        ## if you don't want to do this, then instead run .cancel_order over named IDs
        self.reqGlobalCancel()

        start_time = datetime.now()
        MAX_WAIT_TIME_SECONDS = 10

        finished = False

        while not finished:
            if not self.any_open_orders():
                ## all orders finally cancelled
                finished = True
            if (datetime.now() - start_time).seconds > MAX_WAIT_TIME_SECONDS:
                print("Wrapper didn't come back with confirmation that all orders were cancelled!")
                finished = True

        ## return nothing
