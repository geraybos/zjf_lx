# -*- coding: utf-8 -*-
from .. import TradeX
import json
from time import sleep

from multiping import MultiPing

from . import LazyProperty
from .. import project_dir

class Market(object):
    config_file = project_dir + '\config.json'

    def __init__(self, TradeX, server_name):
        self.server_name = server_name
        self.ping()
        self.TX = TradeX
        self._connect = None

    @LazyProperty
    def connect(self):
        print('step connect')
        retry = True
        loop = 0
        flag = 0
        ip = None

        for ip in self.host_dict:
            try:
                if self.server_name == 'market_a_server':
                    self._connect = self.TX.TdxHq_Connect(ip, self.port)
                    # self._connect = self.TX.TdxHq_Connect('61.152.249.56',7709)
                else:
                    self._connect = self.TX.TdxExHq_Connect(ip, self.port)
                break  #zjf update 2018/6/11
            except Exception as e:
                flag += 1
                print(e.message.decode('gbk'))
                print('retry')
                continue
            # else:
            #     break
            finally:
                if loop >= 5:
                    exit()
                if flag >= 4:
                    loop += 1
                    flag = 0
                    self.ping()
        self._connect.SetTimeout(5000, 5000)
        print(u'\n\t连接成功\tServerName: {host}\t\t{ip}:{port}\n'.format(host=self.host_dict[ip], ip=ip, port=self.port))
        return self._connect

    def ping(self):
        print('step ping')
        with open(self.config_file) as f:
            server_json = json.loads(f.read())[self.server_name]

        mp = MultiPing(server_json['host_dict'].keys())
        mp.send()

        while True:
            try:
                res, no_res = mp.receive(1)
                if len(res):
                    print(u'{} 连接成功'.format(self.server_name))
                    break
                else:
                    print(u'{} 重连'.format(self.server_name))
            except:
                print(u'{} 重连'.format(self.server_name))
            sleep(2)
        self.ip_list = sorted(res.items(), key=lambda x: x[1])[:5]
        # self.ip_list = [min(res, key=lambda x: res[x])]   #20118/6/5  zjf  update
        self.host_dict = dict()
        for ip in self.ip_list:
            self.host_dict[ip[0]] = server_json['host_dict'][ip[0]]
        self.port = server_json['port']
        print(self.host_dict, self.port)
