# -*- coding: utf-8 -*-
from copy import deepcopy
from queue import Empty

from . import STARTED, FINISHED, TIME_OUT, NO_ATTRIBUTES_SET


class finishableQueue(object):
    """
    Creates a queue which will finish at some point
    """

    def __init__(self, queue_to_finish):

        self._queue = queue_to_finish
        self.status = STARTED

    def get(self, timeout):
        """
        Returns a list of queue elements once timeout is finished, or a FINISHED flag is received in the queue

        :param timeout: how long to wait before giving up
        :return: list of queue elements
        """
        contents_of_queue = []
        finished = False

        while not finished:
            try:
                current_element = self._queue.get(timeout=timeout)
                if current_element is FINISHED:
                    finished = True
                    self.status = FINISHED
                else:
                    contents_of_queue.append(current_element)
                    ## keep going and try and get more data

            except Empty:
                ## If we hit a time out it's most probable we're not getting a finished element any time soon
                ## give up and return what we have
                finished = True
                self.status = TIME_OUT

        return contents_of_queue

    def timed_out(self):
        return self.status is TIME_OUT


class mergableObject(object):
    """
    Generic object to make it easier to munge together incomplete information about orders and executions
    """

    def __init__(self, id, **kwargs):
        """
        :param id: master reference, has to be an immutable type
        :param kwargs: other attributes which will appear in list returned by attributes() method
        """

        self.id = id
        attr_to_use = self.attributes()

        for argname in kwargs:
            if argname in attr_to_use:
                setattr(self, argname, kwargs[argname])
            else:
                print(
                    "Ignoring argument passed %s: is this the right kind of object? If so, add to .attributes() method" % argname)

    def attributes(self):
        ## should return a list of str here
        ## eg return ["thingone", "thingtwo"]
        return NO_ATTRIBUTES_SET

    def _name(self):
        return "Generic Mergable object - "

    def __repr__(self):

        attr_list = self.attributes()
        if attr_list is NO_ATTRIBUTES_SET:
            return self._name()

        return self._name() + " ".join(["%s: %s" % (attrname, str(getattr(self, attrname))) for attrname in attr_list
                                        if getattr(self, attrname, None) is not None])

    def merge(self, details_to_merge, overwrite=True):
        """
        Merge two things
        self.id must match
        :param details_to_merge: thing to merge into current one
        :param overwrite: if True then overwrite current values, otherwise keep current values
        :return: merged thing
        """

        if self.id != details_to_merge.id:
            raise Exception("Can't merge details with different IDS %d and %d!" % (self.id, details_to_merge.id))

        arg_list = self.attributes()
        if arg_list is NO_ATTRIBUTES_SET:
            ## self is a generic, empty, object.
            ## I can just replace it wholesale with the new object

            new_object = details_to_merge

            return new_object

        new_object = deepcopy(self)

        for argname in arg_list:
            my_arg_value = getattr(self, argname, None)
            new_arg_value = getattr(details_to_merge, argname, None)

            if new_arg_value is not None:
                ## have something to merge
                if my_arg_value is not None and not overwrite:
                    ## conflict with current value, don't want to overwrite, skip
                    pass
                else:
                    setattr(new_object, argname, new_arg_value)

        return new_object


class orderInformation(mergableObject):
    """
    Collect information about orders
    master ID will be the orderID
    eg you'd do order_details = orderInformation(orderID, contract=....)
    """

    def _name(self):
        return "Order - "

    def attributes(self):
        return ['contract', 'order', 'orderstate', 'status',
                'filled', 'remaining', 'avgFillPrice', 'permid',
                'parentId', 'lastFillPrice', 'clientId', 'whyHeld',
                'mktCapPrice']


class execInformation(mergableObject):
    """
    Collect information about executions
    master ID will be the execid
    eg you'd do exec_info = execInformation(execid, contract= ... )
    """

    def _name(self):
        return "Execution - "

    def attributes(self):
        return ['contract', 'ClientId', 'OrderId', 'time', 'AvgPrice', 'Price', 'AcctNumber',
                'Shares', 'Commission', 'commission_currency', 'realisedpnl']


class list_of_mergables(list):
    """
    A list of mergable objects, like execution details or order information
    """

    def merged_dict(self):
        """
        Merge and remove duplicates of a stack of mergable objects with unique ID
        Essentially creates the union of the objects in the stack
        :return: dict of mergableObjects, keynames .id
        """

        ## We create a new stack of order details which will contain merged order or execution details
        new_stack_dict = {}

        for stack_member in self:
            id = stack_member.id

            if id not in new_stack_dict.keys():
                ## not in new stack yet, create a 'blank' object
                ## Note this will have no attributes, so will be replaced when merged with a proper object
                new_stack_dict[id] = mergableObject(id)

            existing_stack_member = new_stack_dict[id]

            ## add on the new information by merging
            ## if this was an empty 'blank' object it will just be replaced with stack_member
            new_stack_dict[id] = existing_stack_member.merge(stack_member)

        return new_stack_dict

    def blended_dict(self, stack_to_merge):
        """
        Merges any objects in new_stack with the same ID as those in the original_stack
        :param self: list of mergableObject or inheritors thereof
        :param stack_to_merge: list of mergableObject or inheritors thereof
        :return: dict of mergableObjects, keynames .id
        """

        ## We create a new dict stack of order details which will contain merged details

        new_stack = {}

        ## convert the thing we're merging into a dictionary
        stack_to_merge_dict = stack_to_merge.merged_dict()

        for stack_member in self:
            id = stack_member.id
            new_stack[id] = deepcopy(stack_member)

            if id in stack_to_merge_dict.keys():
                ## add on the new information by merging without overwriting
                new_stack[id] = stack_member.merge(stack_to_merge_dict[id], overwrite=False)

        return new_stack


class list_of_execInformation(list_of_mergables):
    pass


class list_of_orderInformation(list_of_mergables):
    pass


class list_of_identified_items(list):
    """
    A list of elements, each of class identified_as (or duck equivalent)

    Used to seperate out accounting data
    """

    def seperate_into_dict(self):
        """

        :return: dict, keys are labels, each element is a list of items matching label
        """

        all_labels = [element.label for element in self]
        dict_data = dict([
            (label,
             [element.data for element in self if element.label == label])
            for label in all_labels])

        return dict_data
