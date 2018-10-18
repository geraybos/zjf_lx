from futuquant import SubType, OpenQuoteContext


def get_quote(code_list,quote_ctx):
    quote_dict = dict()
    quote_ctx.subscribe(list(code_list), [SubType.ORDER_BOOK])
    for code in code_list:
        a = quote_ctx.get_order_book(code)
        a =   a[1]
        quote_dict[code] = dict(buy_1_price=a['Bid'][0][0], buy_1_volume=a['Bid'][0][1],
                                buy_1_order_num=a['Bid'][0][2],
                                sell_1_price=a['Ask'][0][0], sell_1_volume=a['Ask'][0][1],
                                sell_1_order_num=a['Ask'][0][2],
                                buy_2_price=a['Bid'][1][0], buy_2_volume=a['Bid'][1][1],
                                buy_2_order_num=a['Bid'][1][2],
                                sell_2_price=a['Ask'][1][0], sell_2_volume=a['Ask'][1][1],
                                sell_2_order_num=a['Ask'][1][2],
                                buy_3_price=a['Bid'][2][0], buy_3_volume=a['Bid'][2][1],
                                buy_3_order_num=a['Bid'][2][2],
                                sell_3_price=a['Ask'][2][0], sell_3_volume=a['Ask'][2][1],
                                sell_3_order_num=a['Ask'][2][2],
                                buy_4_price=a['Bid'][3][0], buy_4_volume=a['Bid'][3][1],
                                buy_4_order_num=a['Bid'][3][2],
                                sell_4_price=a['Ask'][3][0], sell_4_volume=a['Ask'][3][1],
                                sell_4_order_num=a['Ask'][3][2],
                                buy_5_price=a['Bid'][4][0], buy_5_volume=a['Bid'][4][1],
                                buy_5_order_num=a['Bid'][4][2],
                                sell_5_price=a['Ask'][4][0], sell_5_volume=a['Ask'][4][1],
                                sell_5_order_num=a['Ask'][4][2],
                                buy_6_price=a['Bid'][5][0], buy_6_volume=a['Bid'][5][1],
                                buy_6_order_num=a['Bid'][5][2],
                                sell_6_price=a['Ask'][5][0], sell_6_volume=a['Ask'][5][1],
                                sell_6_order_num=a['Ask'][5][2],
                                buy_7_price=a['Bid'][6][0], buy_7_volume=a['Bid'][6][1],
                                buy_7_order_num=a['Bid'][6][2],
                                sell_7_price=a['Ask'][6][0], sell_7_volume=a['Ask'][6][1],
                                sell_7_order_num=a['Ask'][6][2],
                                buy_8_price=a['Bid'][7][0], buy_8_volume=a['Bid'][7][1],
                                buy_8_order_num=a['Bid'][7][2],
                                sell_8_price=a['Ask'][7][0], sell_8_volume=a['Ask'][7][1],
                                sell_8_order_num=a['Ask'][7][2],
                                buy_9_price=a['Bid'][8][0], buy_9_volume=a['Bid'][8][1],
                                buy_9_order_num=a['Bid'][8][2],
                                sell_9_price=a['Ask'][8][0], sell_9_volume=a['Ask'][8][1],
                                sell_9_order_num=a['Ask'][8][2],
                                buy_10_price=a['Bid'][9][0], buy_10_volume=a['Bid'][9][1],
                                buy_10_order_num=a['Bid'][9][2],
                                sell_10_price=a['Ask'][9][0], sell_10_volume=a['Ask'][9][1],
                                sell_10_order_num=a['Ask'][9][2])

    return quote_dict
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
x=get_quote(code_list=['HK.00700'],quote_ctx=quote_ctx)
print(x)
quote_ctx.close()