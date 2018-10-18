
class Industry:

    @classmethod
    def add_industry(cls,table):
        from Calf import ModelData
        import pymongo
        url = 'mongodb://limu:limu@192.168.1.104:27017/?connectTimeoutMS=2000;authSource=admin'
        industry = ModelData.read_data(table_name='platestock')
        dic = {}
        for i, r in industry.iterrows():
            dic[r.stock_code] = r.hangye
        myclient = pymongo.MongoClient(url)
        mydb = myclient["ppp"]
        mycol = mydb[table]
        for s_c in industry.stock_code.tolist():
            myquery = {"stock_code": s_c}
            newvalues = {"$set": {"hangye": dic[s_c]}}
            x = mycol.update_many(myquery, newvalues)
            print(x.modified_count, s_c + "文档已修改")
        myclient.close()
Industry.add_industry(table='AA_time_trends_kline_min1')


