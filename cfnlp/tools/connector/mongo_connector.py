# coding=utf-8
"""
@ license: Apache Licence
@ github: invoker4zoo
@ author: invoker/cc
@ wechart: whatshowlove
@ software: PyCharm
@ file: mongo_connector.py
@ time: $19-2-21 上午9:24
"""
import sys
sys.path.append('..')
from pymongo import MongoClient
from cfnlp.tools.logger import logger
import os
from pymongo.errors import ConnectionFailure

class mongoConnector(object):

    def __init__(self,MONGODB_SERVER,MONGODB_PORT,MONGODB_DB,MONGODB_COLLECTION):
        try:
            self.connection = MongoClient(
                MONGODB_SERVER,
                MONGODB_PORT
            )
            self.db = self.connection[MONGODB_DB] # Getting a databse
            self.collection = self.db[MONGODB_COLLECTION]  # Getting a collection
        except ConnectionFailure, e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)


if __name__ == "__main__":
    # MONGODB_SERVER = "127.0.0.1"
    MONGODB_SERVER = "192.168.155.125"
    MONGODB_PORT = 27017
    MONGODB_DB = "gov_finace"
    MONGODB_COLLECTION = "country"
    db = mongoConnector(MONGODB_SERVER,MONGODB_PORT,MONGODB_DB,MONGODB_COLLECTION)
    for i in db.collection.find():
        print type(i)
    result = db.collection.find({'noticeTitle': '关于开展三大粮食作物完全成本保险和收入保险试点工作的通知'})
    print result