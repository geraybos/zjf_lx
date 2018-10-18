# -*- coding: utf-8 -*-

from pymongo import *
import json
from Calf import project_dir
# 构建一个默认的MongoDB对象置于项目运行的内存当中，避免频繁
# 的创建MongoDB对象


config_file = project_dir + '/Calf/db_config.json'
try:
    with open(config_file) as f:
        l = f.read()
        a = json.loads(l)
        # db = a['server_db']
        db = a['default']
    #     dbname = db['dbname']
    #     print('default db: {} have connected successfully'.format(dbname))
    #     ip = db['ip']
    #     port = db['port']
    #     username = db['username']
    #     password = db['password']
    #     dbauth = db['dbauth']
    # if username is None:
    #     uri = 'mongodb://{host}:{port}'
    #     connection = MongoClient(uri.format(host=ip, port=port))
    # else:
    #     uri = 'mongodb://{username}:{password}@{host}:{port}/{dbname}'
    #     if dbauth is not None and len(dbauth) > 0:
    #         uri += '?authSource={dbauth}'.format(dbauth=dbauth)
    #
    #     connection = MongoClient(uri.format(username=username, password=password,
    #                                         host=ip, port=port, dbname=dbname))
    # mongodb = connection[dbname]
    fields = db.keys()

    uri = 'mongodb://'
    if 'username' in fields and 'password' in fields:
        uri += '{username}:{password}@'.format(username=db['username'], password=db['password'])
    # ip是必须的
    uri += db['host']
    # if 'port' in fields:
    #     uri += ':%s' % db['port']
    uri += '/?connectTimeoutMS=2000'
    if 'replicaset' in fields:
        uri += ';replicaSet=%s' % db['replicaset']
    if 'dbauth' in fields:
        uri += ';authSource=%s' % db['dbauth']
    print('db-uri:', uri)
    connection = MongoClient(uri)
    if 'dbname' in fields:
        mongodb = connection[db['dbname']]
    else:
        mongodb = None
except Exception:
    raise Exception('connection MongoDB raise a error')


class MongoDB:
    """数据库对象"""
    connection_count = 0

    @classmethod
    def db_connection(cls, location, db_name=None):
        """
        连接到数据库
        :param db_name:
        :param location:
        :return:
        """
        try:
            with open(config_file) as cf:
                buffer = cf.read()
                jn = json.loads(buffer)
                db_ = jn[location]
                # dbname = db['dbname']
                # print('db: {}'.format(dbname))
            #     ip_ = db_['ip']
            #     port_ = db_['port']
            #     username_ = db_['username']
            #     password_ = db_['password']
            #     dbauth_ = db_['dbauth']
            # if username_ is None:
            #     uri_ = 'mongodb://{host}:{port}'
            #     connection_ = MongoClient(uri_.format(host=ip_, port=port_))
            # else:
            #     uri_ = 'mongodb://{username}:{password}@{host}:{port}/{dbname}'
            #     if dbauth_ is not None and len(dbauth_) > 0:
            #         uri_ += '?authSource={dbauth}'.format(dbauth=dbauth_)
            #
            #     connection_ = MongoClient(uri_.format(username=username_, password=password_,
            #                                           host=ip_, port=port_, dbname=db_name))
            #     cls.connection_count += 1
            # mongodb_object = connection_[db_name]
            # print('connection to %s successful' % db_name)
            # return mongodb_object
            fields = db_.keys()

            uri = 'mongodb://'
            if 'username' in fields and 'password' in fields:
                uri += '{username}:{password}@'.format(username=db_['username'], password=db_['password'])
            # ip是必须的
            uri += db_['host']
            # if 'port' in fields:
            #     uri += ':%s' % db_['port']
            uri += '/?connectTimeoutMS=2000'
            if 'replicaset' in fields:
                uri += ';replicaSet=%s' % db_['replicaset']
            if 'dbauth' in fields:
                uri += ';authSource=%s' % db_['dbauth']
            print('new db-uri:', uri)
            connection = MongoClient(uri)
            tn = db_name if db_name is not None else db_['dbname']
            return connection[tn]
        except Exception:
            raise Exception('connection MongoDB raise a error')
