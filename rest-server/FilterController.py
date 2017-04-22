#!/usr/bin/env python
#
# Copyright 2017 @author Subhasis

import ConfigParser
import logging
import tornado.web
from tornado.web import MissingArgumentError

import httplib
import json

from tornado.escape import json_encode

from MongoManager import MongoManager
import FormatConverterUtil
from datetime import datetime

logger = logging.getLogger('log.application')


class FilterController(tornado.web.RequestHandler):
    config = ConfigParser.ConfigParser()
    configPath = '../config/config.cnf'
    config.read(configPath)

    db_config = {
        'host': config.get('MongoDBConnection', 'db.host'),
        'port': config.get('MongoDBConnection', 'db.port'),
        'username': config.get('MongoDBConnection', 'db.username'),
        'password': config.get('MongoDBConnection', 'db.password')
    }
    schema = config.get('MongoDBConnection', 'db.schema')
    batch_size = config.get('MongoDBConnection', 'db.batch_limit')

    cameo_table = config.get('Cameo', 'db.Cameo')
    jrc_table = config.get('JRCNames', 'db.JRCNames')
    translation_table = config.get('NameTranslation', 'db.NameTranslation')

    translation_manager = MongoManager(schema, translation_table, batch_size, db_config)
    translation = translation_manager.get_collection()

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

    def get(self):
        logger.info(self.config.get('Logging', 'Logger.GetMessage2') + '' + self.request.remote_ip)
        try:
            query = self.get_argument(self.config.get('AccessParameters', 'Access.QueryString'))
            source = self.get_argument(self.config.get('AccessParameters', 'Access.Source'), default='both')
            filter_lang = self.get_argument(self.config.get('AccessParameters', 'Access.LookupLang'),
                                            default=self.config.get('AccessParameters', 'Access.FilterLang'))

            result = {}
            result['query'] = query
            normalized_query = FormatConverterUtil.convertToCompareFormat(query)

            if source == 'jrc':
                result['jrc'] = self.get_jrc_result(normalized_query, filter_lang)
                # return only jrc result
            elif source == 'bablenet':
                result['bablenet'] = self.get_bablenet_result(normalized_query, filter_lang)
                # return only bablenet result
            else:
                result['jrc'] = self.get_jrc_result(normalized_query, filter_lang)
                result['bablenet'] = self.get_bablenet_result(normalized_query, filter_lang)

            result['status'] = self.config.get('GeneralMsg', 'Status.success')
            result['licence'] = self.config.get('GeneralMsg', 'Licence.Ack')
        except MissingArgumentError:
            result = {"status": "Failed", "Message": "The query string is wrong on not present."}
        self.write(json_encode(result))
        self.set_header("Content-Type", "application/json")

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

    def get_bablenet_result(self, normalized_query, filter_lang):
        cache_data = self.get_result_database(normalized_query, filter_lang, 'bablenet')
        if len(cache_data) < 1:
            # Get result from Bablenet and push to object
            lookup_lang = self.getFilterLang(filter_lang)
            conn = httplib.HTTPConnection('babelnet.io')
            headers = {"Accept": "application/json"}

            search_query = "/v4/getSenses?word=" + normalized_query + \
                           "&lang=EN&pos=NOUN&" + lookup_lang + "&key=" \
                           + self.config.get('BableNet', 'access.key')
            conn.request("GET", search_query, None, headers)
            raw_result = json.loads(conn.getresponse().read())
            #print raw_result
            conn.close()
            is_flush = False
            for record in raw_result:
                is_flush = True
                self.translation_manager.pushRecords(self.getInsertObject(normalized_query, "bablenet",
                                                                         record['language'].lower(),
                                                                         record['lemma'].replace('_', ' ')))
            if is_flush:
                self.translation_manager.flushBatch()
            cache_data = self.get_result_database(normalized_query, filter_lang, 'bablenet')
            logger.info(self.config.get('Logging', 'Logger.GetMessage3') + '' + normalized_query)
        return cache_data

    def getInsertObject(self, cameo_name, source, lang, name):
        d = {}
        d['cameo_name'] = cameo_name
        d['source'] = source
        d['lang'] = lang
        d['name'] = name
        d['creation_timestamp'] = datetime.now()
        return d

    def get_jrc_result(self, normalized_query, filter_lang):
        result = self.get_result_database(normalized_query, filter_lang, 'jrc')
        for r in result:
            r['names'] = r['names'].replace('+', ' ')
        return result
