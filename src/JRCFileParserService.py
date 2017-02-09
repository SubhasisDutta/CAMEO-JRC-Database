'''
Created on Jan 30, 2017
@author: Subhasis
'''

import csv
from MongoManager import MongoManager


class JRCFileParserService(object):
    '''
    This class takes care of reading the input file parsing the text line by line and pushing it into MongoDB.
    '''

    def __init__(self, file_path, db_config, schema, table, batch_size):
        self.file_path = file_path
        self.manager = MongoManager(schema, table, batch_size, db_config)

    def process(self):
        print "Reading File ", self.file_path
        count_record = 0
        entity_count = 0
        similar_record = []
        previous_record_id = '0'
        with open(self.file_path, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            for row in reader:
                if previous_record_id != row[0]:
                    self.manager.pushRecords(self.getInsertObject(similar_record))
                    entity_count += 1
                    similar_record = []
                similar_record.append(row)
                previous_record_id = row[0]
                count_record += 1
            self.manager.pushRecords(self.getInsertObject(similar_record))
        print "Records Processed ", count_record
        print "Entity Processed ", entity_count
        return self.manager.flushBatch()

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
