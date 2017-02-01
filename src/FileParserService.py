'''
Created on Jan 30, 2017
@author: Subhasis
'''

import csv
from MongoManager import MongoManager


class FileParserService(object):
    '''
    This class takes care of reading the input file parsing the text line by line and pushing it into MongoDB.
    '''

    def __init__(self, file_path):
        self.file_path = file_path
        self.manager = MongoManager()

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
                    self.manager.pushRecords(similar_record)
                    entity_count += 1
                    similar_record = []
                similar_record.append(row)
                previous_record_id = row[0]
                count_record += 1
            self.manager.pushRecords(similar_record)
        print "Records Processed ", count_record
        print "Entity Processed ", entity_count
        return self.manager.flushBatch()
