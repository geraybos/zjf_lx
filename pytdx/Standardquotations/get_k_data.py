from pytdx.hq import TdxHq_API
api = TdxHq_API()
if api.connect('119.147.212.81', 7709):
    # ... same codes...
    data=api.get_k_data('000001','2015-07-03','2018-07-10')
    print(data)

    api.disconnect()