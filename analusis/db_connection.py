import pymongo


class DBConnection:
    connection=None
    def connect(self,port=27017,db_name='ppp'):

        db_url='mongodb://limu:limu@192.168.3.249:{}/?connectTimeoutMS=2000;authSource=admin'.format(port)
        myclient=pymongo.MongoClient(db_url)
        self.connection=myclient
        mydb=myclient[db_name]
        return mydb

    def connect2(self, port=40000, db_name='ttt'):
        #'mongodb://localhost:27017/'
        db_url = 'mongodb://192.168.3.221:{}/?connectTimeoutMS=2000;authSource=admin'.format(port)
        myclient = pymongo.MongoClient(db_url)
        self.connection = myclient
        mydb = myclient[db_name]
        return mydb

# obj=DBConnection()
# mydb=obj.connect2()
# mydb['t1'].insert_many([{'name':'234'}])
#
# obj.connection.close()
