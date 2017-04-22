'''
Created on April 20, 2017
@author: Subhasis
'''

from MongoManager import MongoManager
from datetime import datetime
import httplib
import json
import ConfigParser
import FormatConverterUtil

class nameTranslatorService(object):
    def __init__(self, db_config, schema, table, batch_size, cameo_table, jrc_table, jrc_cameo_table):
        self.config = ConfigParser.ConfigParser()
        self.config.read('../config/config.cnf')
        self.translator_manager = MongoManager(schema, table, batch_size, db_config)
        self.cameo_manager = MongoManager(schema, cameo_table, batch_size, db_config)
        self.jrc_manager = MongoManager(schema, jrc_table, batch_size, db_config)
        self.jrc_cameo_table = MongoManager(schema, jrc_cameo_table, batch_size, db_config)
        self.translation = self.translator_manager.get_collection()

    def process(self, process_jrc, process_bable_net):
        cameo = self.cameo_manager.get_collection()
        jrc = self.jrc_manager.get_collection()
        jrc_cameo = self.jrc_cameo_table.get_collection()

        # Parse and get all JRC Names
        if process_jrc:
            cameo_data = cameo.find({}, no_cursor_timeout=True)
            counter = 0
            for cameo_record in cameo_data:
                cameo_compare_list = cameo_record['compare_strings']
                for c in cameo_compare_list:
                    if len(c) > 1:
                        jrc_cameo_data = jrc_cameo.find({"cameo_string": c})
                        for record_object in jrc_cameo_data:
                            jrc_data = jrc.find_one({"_id": record_object['jrc_id']})
                            for variation in jrc_data['variations']:
                                counter += 1
                                self.translator_manager.pushRecords(
                                    self.getInsertObject(c, "jrc", variation['lang'], variation['name']))
            print "Total Translation Found : ", counter
            cameo_data.close()
        # Parse and get all BableNet Names
        # To filter record to get web service - in produciton we can remove and run for all
        # {"record_type": "Cameo.Phoenix.Countries.actors", "cameo_title": "PRESIDENT_OF_THE_UNITED_STATES_"}
        if process_bable_net:
            cameo_data = cameo.find({"record_type": "Cameo.Phoenix.Countries.actors",
                                     "cameo_title": "PRESIDENT_OF_THE_UNITED_STATES_"},
                                    no_cursor_timeout=True)

            for cameo_record in cameo_data:
                cameo_compare_list = cameo_record['compare_strings']
                for c in cameo_compare_list:
                    if len(c) > 1:
                        self.get_bablenet_result(c, self.config.get('AccessParameters', 'Access.FilterLang'))

            cameo_data.close()
        return self.translator_manager.flushBatch()

    def get_bablenet_result(self, cameo_string, filter_lang):
        normalized_query = FormatConverterUtil.convertToCompareFormat(cameo_string.replace('+', ' ').strip(' '))
        cache_data = self.get_result_database(normalized_query, filter_lang, 'bablenet')
        if len(cache_data) < 1:
            # Get result from Bablenet and push to object
            lookup_lang = self.getFilterLang(filter_lang)
            conn = httplib.HTTPConnection('babelnet.io')
            headers = {"Accept": "application/json"}

            search_query = "/v4/getSenses?word=" + normalized_query + \
                           "&lang=EN&pos=NOUN&" + lookup_lang + "&key=" \
                           + self.config.get('BableNet', 'access.key')
            print search_query
            conn.request("GET", search_query, None, headers)
            raw_result = json.loads(conn.getresponse().read())
            #print raw_result
            conn.close()
            counter = 0
            is_flush = False
            for record in raw_result:
                counter += 1
                is_flush = True
                self.translator_manager.pushRecords(self.getInsertObject(normalized_query, "bablenet",
                                                                         record['language'].lower(),
                                                                         record['lemma'].replace('_', ' ')))
            print "Total Translation Found : ", counter
            if is_flush:
                self.translator_manager.flushBatch()
            cache_data = self.get_result_database(normalized_query, filter_lang, 'bablenet')
        return cache_data

    def getFilterLang(self, lookup_lang):
        filter_langs = ""
        langs = lookup_lang.upper().split(',')
        if len(langs) == 1:
            filter_langs = 'filterLangs=' + langs[0]
        elif len(langs) == 2:
            filter_langs = 'filterLangs=' + langs[0] + '&filterLangs=' + langs[1]
        elif len(langs) > 2:
            filter_langs = 'filterLangs=' + langs[0] + '&filterLangs=' + langs[1] + '&filterLangs=' + langs[3]
        return filter_langs

    def get_result_database(self, normalized_query, filter_lang, source):
        language_array = []
        f = filter_lang.lower().split(',')
        for r in f:
            d = {}
            d['lang'] = r
            language_array.append(d)

        translation_data = self.translation.find(
            {"$and": [{"cameo_name": normalized_query}, {"source": source}, {"$or": language_array}]})
        translation_result = list(translation_data)
        for data in translation_result:
            del data['cameo_name']
            del data['creation_timestamp']
            del data['_id']
        return translation_result

    def getInsertObject(self, cameo_name, source, lang, name):
        d = {}
        d['cameo_name'] = cameo_name
        d['source'] = source
        d['lang'] = lang
        d['name'] = name
        d['creation_timestamp'] = datetime.now()
        return d
