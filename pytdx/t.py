from pytdx.hq import TdxHq_API

api = TdxHq_API()
api = TdxHq_API(multithread=True)
api = TdxHq_API(heartbeat=True)
x=api.connect('119.147.212.81', 7709)


api.disconnect()