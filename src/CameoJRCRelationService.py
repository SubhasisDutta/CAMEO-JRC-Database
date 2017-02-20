'''
Created on Feb 20, 2017
@author: Subhasis
'''

from MongoManager import MongoManager


class CameoJRCRelationService(object):
    '''
    This class takes care of loading the cameo and JC data and do string match line by line and pushing it into MongoDB.
    '''

    def __init__(self, db_config, schema, table, batch_size, cameo_table, jrc_table):
        self.manager = MongoManager(schema, table, batch_size, db_config)
        self.cameo_manager = MongoManager(schema, cameo_table, batch_size, db_config)
        self.jrc_manager = MongoManager(schema, jrc_table, batch_size, db_config)

    def process(self):
        cameo = self.cameo_manager.get_collection()
        jrc = self.jrc_manager.get_collection()
        cameo_data = cameo.find({}, no_cursor_timeout=True)
        counter = 0
        for cameo_record in cameo_data:
            #print cameo_record['cameo_title'], "    ", len(cameo_record['compare_strings'])
            #print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            cameo_compare_list = cameo_record['compare_strings']
            jrc_data = jrc.find()
            for jrc_record in jrc_data:
                # print jrc_record['id'], "  ", len(jrc_record['compare_strings'])
                jrc_compare_list = jrc_record['compare_strings']
                for c in cameo_compare_list:
                    for j in jrc_compare_list:
                        if c == j:
                            counter += 1
                            self.manager.pushRecords(self.getInsertObject(cameo_record['_id'], jrc_record['_id'],
                                                                          cameo_record['cameo_title'], jrc_record['id'],
                                                                          c))
                            #print cameo_record['_id'], ",", jrc_record['_id'], ",", \
                            #    cameo_record['cameo_title'], ",", jrc_record['id'], ",", c, ",", \
                            #    len(jrc_record['compare_strings'])
        print "Total Matches Found : ", counter
        cameo_data.close()
        return self.manager.flushBatch()

    def getInsertObject(self, cameo_id, jrc_id, cameo_title, jc_code, compare_string):
        d = {}
        d['cameo_id'] = cameo_id
        d['jrc_id'] = jrc_id
        d['cameo_title'] = cameo_title
        d['jrc_code'] = jc_code
        d['compare_string'] = compare_string
        return d
