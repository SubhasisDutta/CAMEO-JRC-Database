'''
Created on Feb 20, 2017
@author: Subhasis
'''

from MongoManager import MongoManager
import editdistance


class CameoJRCRelationService(object):
    '''
    This class takes care of loading the cameo and JC data and do string match line by line and pushing it into MongoDB.
    '''

    def __init__(self, db_config, schema, table, batch_size, cameo_table, jrc_table):
        self.manager = MongoManager(schema, table, batch_size, db_config)
        self.cameo_manager = MongoManager(schema, cameo_table, batch_size, db_config)
        jrc_manager = MongoManager(schema, jrc_table, batch_size, db_config)
        jrc = jrc_manager.get_collection()
        jrc_data = jrc.find()
        self.jrc_cache = {}
        for jrc_record in jrc_data:
            jrc_compare_list = jrc_record['compare_strings']
            for name in jrc_compare_list:
                first_char = name[0]
                jrc_object = {
                    'name': name,
                    'jrc_id': jrc_record['id'],
                    '_id': jrc_record['_id']
                }
                if not first_char in self.jrc_cache.keys():
                    self.jrc_cache[first_char] = []
                self.jrc_cache[first_char].append(jrc_object)

    def process(self):
        cameo = self.cameo_manager.get_collection()

        cameo_data = cameo.find({}, no_cursor_timeout=True)
        counter = 0
        edit_distance_counter = [0, 0, 0, 0, 0, 0]
        for cameo_record in cameo_data:
            cameo_compare_list = cameo_record['compare_strings']
            for c in cameo_compare_list:
                if len(c) > 1:
                    first_char_cameo = c[0]
                    if first_char_cameo in self.jrc_cache.keys():
                        jrc_bucket = self.jrc_cache[first_char_cameo]
                        for j in jrc_bucket:
                            edit_distance = int(editdistance.eval(c, j['name']))
                            if edit_distance < 3:
                                counter += 1
                                edit_distance_counter[edit_distance] += 1
                                self.manager.pushRecords(self.getInsertObject(cameo_record['_id'], j['_id'],
                                                                              cameo_record['cameo_title'], j['jrc_id'],
                                                                              c, j['name'], edit_distance,
                                                                              cameo_record['record_type']))
        print "Total Matches Found : ", counter
        print "Edit Distance counter : ", edit_distance_counter
        cameo_data.close()
        return self.manager.flushBatch()

    def getInsertObject(self, cameo_id, jrc_id, cameo_title, jc_code, cameo_string, jrc_string, edit_distance,
                        record_type):
        d = {}
        d['cameo_id'] = cameo_id
        d['edit_distance'] = edit_distance
        d['jrc_id'] = jrc_id
        d['cameo_title'] = cameo_title
        d['jrc_code'] = jc_code
        d['cameo_string'] = cameo_string
        d['jrc_string'] = jrc_string
        d['record_type'] = record_type
        return d
