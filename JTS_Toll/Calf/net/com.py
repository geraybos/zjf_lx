# encoding: utf-8

"""
@version: 1.0
@author: LeungJain
@time: 2018/2/26 17:21
"""
import socket
import sys
import datetime as dt
from ..net import STATUS


class ModelClient:
    @classmethod
    def ClientFrame(cls, info):
        cls.info = info
        try:
            # 获取本机电脑名
            cls.host = socket.getfqdn(socket.gethostname())
            # 获取本机ip
            cls.ip = socket.gethostbyname(cls.host)
            # create an AF_INET, STREAM socket (TCP)
            cls.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cls.socket.settimeout(10)
        except socket.error as msg:
            print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
            sys.exit()

    @classmethod
    def send(cls):
        try:
            cls.socket.connect((cls.info['ip'], cls.info['port']))
            m = cls.info['message']
            m['host'] = cls.host
            m['from'] = cls.ip
            message = bytes(str(m), encoding="utf8")
            # Set the whole string
            cls.socket.sendall(message)
            # print('Message send successfully')
            reply = str(cls.socket.recv(1024), encoding='utf-8')
            # print(reply)
            return reply
        except socket.error:
            print('Send failed')
            return 'Error'


def notice(address, **kw):
    """
    网络通知，address为需要通知的目的地址
    :param address: eg:{'ip':'127.0.0.1',port:50001}
    :param kw:
    :return:
    """
    now = dt.datetime.now()
    must_data = {'date': str(now), 'status': STATUS['success']}
    must_data = dict(must_data, **kw)
    message = {'message': must_data}
    info = dict(address, **message)
    ModelClient.ClientFrame(info)
    return ModelClient.send()

