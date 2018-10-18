from pytdx.hq import TdxHq_API
api = TdxHq_API()
if api.connect('119.147.212.81', 7709):
    # ... same codes...
    data=api.get_security_list(0, 100)
    data=api.to_df(data)
    # data=data[(data.code<'39000')]
    # data=data[(data.code<'70000')]

    print(data)

    api.disconnect()