# -*- coding: utf-8 -*-
from os.path import abspath, pardir, join
from sys import path

path.append(abspath(join(abspath(join(abspath(__file__), pardir)), pardir)))

import json

from . import project_dir

config_file = project_dir + '\config.json'

with open(config_file) as f:
    l = f.read()
    a = json.loads(l)
    db = a['db']
    dbname = db['dbname']
    print('db: {}'.format(dbname))
    ip = db['ip']
    port = db['port']
    username = db['username']
    password = db['password']
    dbauth = db['dbauth']

from pymongo import *

if username is None:
    uri = 'mongodb://{host}:{port}'
    connection = MongoClient(uri.format(host=ip, port=port))
else:
    uri = 'mongodb://{username}:{password}@{host}:{port}/{dbname}'
    if dbauth is not None and len(dbauth) > 0:
        uri += '?authSource={dbauth}'.format(dbauth=dbauth)

    connection = MongoClient(uri.format(username=username, password=password, host=ip, port=port, dbname=dbname))
mongodb = connection[dbname]
