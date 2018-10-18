
import pandas as pd
if __name__ == '__main__':
    stock_code=list()
    hangye_code=list()
    index_stock=list()
    hy=list()
    with open('tdxhy.cfg','r') as f:
        for i in (f.read().split('\n')):
            temp=(i.split('|'))
            # print(temp)
            if len(temp)>2:

                stock_code.append(temp[1])
                hangye_code.append(temp[2])

    with open('tdxzs.cfg','r') as f:
        for i in (f.read().split('\n')):
            temp=i.split('|')
            if len(temp)>2:

                index_stock.append(temp[1])
                hy.append(temp[5])
    data1=pd.DataFrame({'stock_code':stock_code,'hangye_code':hangye_code})
    data2=pd.DataFrame({'index_code':index_stock,'hangye_code':hy})

    data=pd.merge(data1,data2,on=['hangye_code'])
    # print(data.stock_code.tolist())
    data=data.groupby(['hangye_code'], as_index=False).agg({'stock_code': lambda x: sorted(list(x)), 'index_code': 'first'})

    # data=data.sort_values(by=['index_code'])
    # data['stock_code']=data.stock_code.astype('str')
    # print(len(data))
    # data=data.drop_duplicates(['stock_code'])
    # print(len(data))
    print(data.index_code.tolist())
    pass