import json

# from Calf import ModelData
# import datetime as dt
# table_name='kline_min1'
# date=dt.datetime(2018,6,8)
# data0 = ModelData.read_data(table_name=table_name, date=date)
# data0=data0.drop_duplicates(['stock_code'])
# data0=data0.sort_values(by=['stock_code'],ascending=True)
# data0.to_csv('xxx.csv')
# from Calf.net.com import ModelClient
# ModelClient.ClientFrame(info={'ip':'192.168.1.0','port':50014,'message':{'d':'我日'}})
# ModelClient.send()

# udp_gb_server.py

#
import socket

from Calf import ModelData


class Messages:
    @classmethod
    def send(cls,messages):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            PORT = 50015
            network = '<broadcast>'
            x=json.dumps(messages)
            s.sendto(x.encode('utf-8'), (network, PORT))
            print('广播成功：'+str(messages))
        except Exception as e:
            print('广播失败')
    @classmethod
    def receive(cls):
        import json
        import socket
        import datetime as dt

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        PORT = 50015
        s.bind(('', PORT))
        print('Listening for broadcast at ', s.getsockname())
        result = {'kline_min5': False, 'index_min5': False}
        while True:
            try:
                data, address = s.recvfrom(65535)
                data = data.decode('utf-8')
                print('Server received from {}:{}'.format(address, data))
                data = json.loads(data)
                if data['identification'] == 'getdata':
                    result[data['kline']] = True
                    if result['index_min5'] and result['kline_min5']:
                        print('start')
                        # dosomething
                        # your function
                        result = {'kline_min5': False, 'index_min5': False}
            except Exception as e:
                print(e)
# Messages.receive()
# import datetime as dt
# date=dt.datetime.now()
# # messages = {'identification': 'getdata', 'status': 200, 'kline': 'index_min5', 'other': 'ok','datetime':date}
# messages2 = {'identification': 'getdata', 'status': 200, 'kline': 'kline_min30', 'other': 'ok','datetime':str(date)}
# # Messages.send(messages)
# Messages.send(messages2)
import datetime as dt
kline='kline_min5'
date=dt.datetime(2018,8,6)
data = ModelData.read_data(table_name=kline, field=['stock_code', 'close', 'open'], date=date, time=1130)
print(data.stock_code.tolist())