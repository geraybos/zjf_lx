# -*- coding: utf-8 -*-
from threading import Thread

from . import DealWrapper, DealClient


class Dealer(DealWrapper, DealClient):
    def __init__(self, host, port, clent_id):
        DealWrapper.__init__(self)
        DealClient.__init__(self, wrapper=self)
        self.init_error()
        self.connect(host, port, clent_id)
        thread = Thread(target=self.run)
        thread.start()
        setattr(self, '_thread', thread)
