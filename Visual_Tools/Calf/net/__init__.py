# encoding: utf-8

"""
@version: 1.0
@author: LeungJain
@time: 2018/2/26 17:16
"""
# 运行收益探测的服务器
MODEL_PROBE = {'ip': '127.0.0.1', 'port': 50012}

MODEL_REMOTE_SERVER = {'ip': '172.16.200.13', 'port': 50013}

# 传输状态说明
STATUS = {
    'success': 200,
    'error': 500,
    'loss': 404,
}

# 网络启动任务计划所对应的代码
TASK_CODE = {
    'to_signal': 100,
    'repair_signal': -100,
    'to_orders': 101,
    'repair_orders': -101,
    'profit_probing': 200,
    'close': 400
}