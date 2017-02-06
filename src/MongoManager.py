'''
Created on Jan 30, 2017
@author: Subhasis
'''

import pymongo
from pymongo.mongo_client import MongoClient


class MongoManager(object):
    '''
    This class takes care of setting up the connection to Mongo DB and pushing data into database.
    '''

    def __init__(self, schema, table, batch_size, db_config):
        self.username = db_config['username']  # User name to connect to database
        self.password = db_config['password']  # password to connect to database
        self.schema = schema  # database
        self.resultTable = table  # collection
        self.batchSize = batch_size  # This is the no of documents to be pushed in one go
        self.port = int(db_config['port'])  # Port to connect to database
        cluster_nodes = []
        cluster_nodes.append(db_config['host'])
        self.client = MongoClient(cluster_nodes[0], self.port)
        self.db = self.client[self.schema]
        if len(self.username) > 1 and len(self.password) > 1:
            self.db.authenticate(self.username, self.password, mechanism='MONGODB-CR')
        self.collection = self.db[self.resultTable]
        self.insert_batch = []
        self.batch_count = 0

    def getInsertObject(self, data_list):
        d = {}
        d['id'] = int(data_list[0][0])
        d['type'] = 'UNKNOWN'
        if data_list[0][1] == 'P':
            d['type'] = 'PERSON'
        if data_list[0][1] == 'O':
            d['type'] = 'ORGANIZATION'
        variations = []
        for r in data_list:
            v = {}
            v['lang'] = r[2]
            v['name'] = r[3]
            variations.append(v)
        d['variations'] = variations
        return d

    def pushRecords(self, data_list):
        return self.batchQuery(data_list)

    def batchQuery(self, data_list):
        if self.batch_count < self.batchSize:
            data_dict = self.getInsertObject(data_list)
            self.insert_batch.append(data_dict)
            self.batch_count += 1
        else:
            data_dict = self.getInsertObject(data_list)
            self.insert_batch.append(data_dict)
            self.collection.insert_many(self.insert_batch)
            self.batch_count = 0
            self.insert_batch = []
        return True

    def flushBatch(self):
        print "Flushed"
        self.collection.insert_many(self.insert_batch)
        self.batch_count = 0
        self.insert_batch = []
        return True

    def drop_collection(self):
        self.collection.drop()
        print "Clean Up Complete"
