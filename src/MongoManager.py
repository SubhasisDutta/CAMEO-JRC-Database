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

    def __init__(self):
        self.username = ""  # User name to connect to database
        self.password = ""  # password to connect to database
        self.schema = "JRC-Names"  # database
        self.resultTable = "Entities"  # collection
        self.batchSize = 1000  # This is the no of documents to be pushed in one go
        self.port = 27017  # Port to connect to database
        cluster_nodes = []
        cluster_nodes.append('localhost')
        self.client = MongoClient(cluster_nodes[0], self.port)
        self.db = self.client[self.schema]
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
