'''
Created on Jan 30, 2017
@author: Subhasis
'''

import csv
from MongoManager import MongoManager


class CAMEOFileParserService(object):
    '''
    This class takes care of reading the input file parsing the text line by line and pushing it into MongoDB.
    '''

    def __init__(self, file_dict, db_config, schema, table, batch_size):
        self.file_paths = file_dict
        self.manager = MongoManager(schema, table, batch_size, db_config)

    def process(self):
        for k, v in self.file_paths.iteritems():
            print "Reading File ", v
            count_record = 0
            entity_count = 0
            with open(v, 'rb') as fileObj:
                lines = fileObj.readlines()
                for row in lines:
                    if row[0] == '#':  # Ignore line if start with comment
                        continue
                    count_record += 1
                    if k == 'Cameo.Phoenix.agents':
                        if row[0] == '!':  # Ignore line if start with !
                            continue
                        data_list = row.rstrip('\n').split(' ')
                        if len(data_list) < 2:  # Ignore lines that are blank
                            continue
                        self.manager.pushRecords(self.getInsertObject(data_list, k))
                        entity_count += 1
                    elif k == 'Cameo.Phoenix.Countries.actors':
                        pass
                    elif k == 'Cameo.Phoenix.International.actors':
                        pass
                    elif k == 'Cameo.Phoenix.MilNonState.actors':
                        pass
                print "Lines Processed for ", k, " is : ", count_record
                print "Records created for ", k, " is : ", entity_count
        return self.manager.flushBatch()

    def getInsertObject(self, data_list, type):
        d = {}
        d['record_type'] = type
        d['cameo_title'] = data_list[0]
        t = data_list[1].replace('[~', '')
        t = t.replace(']', '')
        d['cameo_code_category'] = t
        d['compare_strings'] = []
        for data in data_list:
            tmp_str = data.lower().replace('_', '+').replace(' ', '+')
            d['compare_strings'].append(tmp_str)
        return d
