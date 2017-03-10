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
                entity_list = []
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
                        if row == '\n':
                            if len(entity_list) > 1:
                                self.manager.pushRecords(self.getInsertObject(entity_list, k))
                                entity_count += 1
                                entity_list = []
                        record = row.rstrip('\n')
                        data_list = []
                        if len(record) > 1 and record[0] == '\t':
                            data_list.append(record.replace('\t', ''))
                        else:
                            data_list = record.replace('  # CountryInfo.txt', '#ACTOR#').split(' ')
                        for d in data_list:
                            if len(d) > 0:
                                entity_list.append(d)
                    elif k == 'Cameo.Phoenix.International.actors' or k == 'Cameo.Phoenix.MilNonState.actors':
                        record = row.rstrip('\n')
                        if len(record) > 2 and record[0] != '+':
                            if record[0] == '\t': #ignore tab lines
                                continue
                            if len(entity_list) > 1:
                                self.manager.pushRecords(self.getInsertObject(entity_list, k))
                                entity_count += 1
                                entity_list = []
                        data_list = []
                        if len(record) > 1:
                            data_list = record.replace(' ','').replace('#','#$').split('#')
                        for d in data_list:
                            if len(d) > 0:
                                entity_list.append(d)
                    # elif k == 'Cameo.Phoenix.MilNonState.actors':
                    #     pass
                print "Lines Processed for ", k, " is : ", count_record
                print "Records created for ", k, " is : ", entity_count
        return self.manager.flushBatch()

    def getInsertObject(self, data_list, type):
        d = {}
        d['record_type'] = type
        d['cameo_title'] = data_list[0]
        if type == 'Cameo.Phoenix.agents' and len(data_list) > 1:
            t = data_list[1].replace('[~', '')
            t = t.replace(']', '')
            d['cameo_code_category'] = t
            del data_list[1]
        elif type == 'Cameo.Phoenix.Countries.actors':
            # Setup Country code
            t = data_list[1].replace('[', '')
            t = t.replace(']', '')
            d['cameo_country_code'] = t
            del data_list[1]
            # setup variation of country name
            country_name_variation = []
            for data in data_list:
                if data[0] == '+':
                    data = data[1:]
                    country_name_variation.append(data)
            d['cameo_country_name_variation'] = country_name_variation
            # setup county actors and their position
            country_actors = []
            a = {}
            actor_period = []
            for index, val in enumerate(data_list):
                if val.endswith('#ACTOR#'):
                    if len(a) > 0:
                        a['cameo_actor_period'] = actor_period
                        country_actors.append(a)
                        actor_period = []
                        a = {}
                    a['cameo_actor_name'] = val.replace('#ACTOR#', '')
                if val[0] == '[' and val[-1] == ']':
                    actor_period.append(val)
            d['cameo_country_actors'] = country_actors
        elif type == 'Cameo.Phoenix.International.actors' or type == 'Cameo.Phoenix.MilNonState.actors':
            # setup variation of country name
            actor_name_variation = []
            for data in data_list:
                if data[0] == '+':
                    data = data[1:]
                    actor_name_variation.append(data)
            d['cameo_actor_name_variation'] = actor_name_variation
            actor_orgs = []
            for data in data_list:
                if len(data) > 2 and data[0] == '$':
                    actor_orgs.append(data[1:])
            d['cameo_actor_orgs'] = actor_orgs
        #This is common for all types
        d['compare_strings'] = []
        for data in data_list:
            if len(data) > 1:
                if data[0] == '[' and data[-1] == ']':
                    continue
                tmp_str = data.replace('#ACTOR#', '').lower().replace('_', '+').replace(' ', '+').replace('\t', '')
                tmp_str = self.remove_text_paranthesis(tmp_str)
                if len(tmp_str) > 2 and tmp_str[0] == '+':
                    tmp_str = tmp_str[1:]
                elif len(tmp_str) > 2 and tmp_str[-1] == '+':
                    tmp_str = tmp_str[:-1]
                elif len(tmp_str) > 2 and tmp_str[0] == '$':
                    continue
                d['compare_strings'].append(tmp_str)
        return d

    def remove_text_paranthesis(self,sentence):
        ret = ''
        skip1c = 0
        skip2c = 0
        for i in sentence:
            if i == '[':
                skip1c += 1
            elif i == '(':
                skip2c += 1
            elif i == ']' and skip1c > 0:
                skip1c -= 1
            elif i == ')'and skip2c > 0:
                skip2c -= 1
            elif skip1c == 0 and skip2c == 0:
                ret += i
        return ret