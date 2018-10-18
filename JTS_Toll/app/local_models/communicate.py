# -*- coding: utf-8 -*-
import json
import socket
import sys
from datetime import datetime


class OrderAction:
    """
    用来接受开仓请求的驱动
    """
    HOST = ''  # 默认监听地址（本地）
    PORT = 50014  # 默认监听端口
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # tcp

    @classmethod
    def run(cls, func, host=None, port=None):
        """
        接受TCP的端对端发送
        :param port: 除了使用默认的端口和地址之外还可以重新指定
        :param host:
        :param func: 接受到连接后的回调事件
        :return:
        """
        try:
            if host is None and port is None:
                cls.SERVER.bind((cls.HOST, cls.PORT))
            else:
                cls.SERVER.bind((host, port))
            cls.SERVER.listen(10)
            print('\033[32m' + '-' * 80)
            print('Model recommendation system started and listening '
                  'on {}'.format(port if port is not None else cls.PORT))
            print('Datetime:%s' % datetime.now())
            print('-' * 80 + '\033[0m')
        except Exception as e:
            print('\033[31m' + '-' * 80)
            print('Model recommendation system failed to start. error '
                  'code : ' + str(e))
            print('-' * 80 + '\033[0m')
            sys.exit()
        while 1:
            print('Waiting for a new request...')
            conn, address = cls.SERVER.accept()
            print('\033[32m' + '-' * 80)
            print('Received request from:' + address[0] + ':' + str(address[1])
                  + ' Datetime:', datetime.now())
            print('-' * 80 + '\033[0m')
            data = conn.recv(1024).decode('utf-8')
            data = data.replace("'", '"')

            # {'date': '2018-08-08 13:50:57.947806', 'status': 200, 'open_date': '2018-06-25 00:00:00', 'task': 102, 'model_from': 'macd_day_hk', 'host': 'PC-20170629ASUX', 'from': '192.168.1.103'}
            # print(data)
            data = json.loads(data)  # 一个字典：可以通过这个字典中的K-V在orders表中查询到数据
            try:
                conn.sendall(bytes(str(200), encoding='utf-8'))
                func(data)
            except Exception as e:
                print(e)
            finally:
                conn.close()
