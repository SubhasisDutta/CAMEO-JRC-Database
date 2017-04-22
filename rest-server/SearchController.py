#!/usr/bin/env python
#
# Copyright 2017 @author Subhasis

import ConfigParser
import logging
import tornado.web

import httplib
import json

from tornado.escape import json_encode

from MongoManager import MongoManager
import FormatConverterUtil

logger = logging.getLogger('log.application')


class SearchController(tornado.web.RequestHandler):
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
    cameo_jrc_table = config.get('CameoJRC', 'db.CameoJRCCountryActor')
    bablenet_cache = config.get('BableNet', 'db.BableNet.Cache')
    dbpedia_cache = config.get('DBPedia', 'db.DBPedia.Cache')

    cameo = MongoManager(schema, cameo_table, batch_size, db_config).get_collection()
    jrc = MongoManager(schema, jrc_table, batch_size, db_config).get_collection()
    cameo_jrc = MongoManager(schema, cameo_jrc_table, batch_size, db_config).get_collection()
    bablenet_cache = MongoManager(schema, bablenet_cache, batch_size, db_config).get_collection()
    dbpedia_cache = MongoManager(schema, dbpedia_cache, batch_size, db_config).get_collection()

    def get(self):
        logger.info(self.config.get('Logging', 'Logger.GetMessage1') + '' + self.request.remote_ip)
        query = self.get_argument(self.config.get('AccessParameters', 'Access.QueryString'))
        result = {}
        result['query'] = query
        normalized_query = FormatConverterUtil.convertToCompareFormat(query)

        # Get result from Bablenet and push to object
        conn = httplib.HTTPConnection('babelnet.io')
        headers = {"Accept": "application/json"}
        search_query = "/v4/getSenses?word=" + normalized_query + "&lang=EN&pos=NOUN&filterLangs=AR&filterLangs=ES&key=" + self.config.get('BableNet', 'access.key')
        conn.request("GET", search_query, None, headers)
        result['bablenet'] = json.loads(conn.getresponse().read())

        # Get result from DBpedia and push to object
        conn = httplib.HTTPConnection('lookup.dbpedia.org')
        headers = {"Accept": "application/json"}
        search_query = "/api/search/KeywordSearch?QueryString=" + normalized_query
        conn.request("GET", search_query, None, headers)
        result['dbpedia'] = json.loads(conn.getresponse().read())

        # get result from caameo and JRC and push to object
        result['cameojrc'] = self.get_cameo_jrc_result(normalized_query)

        result['status'] = self.config.get('GeneralMsg', 'Status.success')
        result['licence'] = self.config.get('GeneralMsg', 'Licence.Ack')

        self.write(json_encode(result))
        self.set_header("Content-Type", "application/json")

    def get_cameo_jrc_result(self, normalized_query):
        cameo_jrc_data = self.cameo_jrc.find(
            {"$or": [{"cameo_string": normalized_query}, {"jrc_string": normalized_query}]})

        cameo_jrc_result = list(cameo_jrc_data)
        for data in cameo_jrc_result:
            data['cameo_data'] = list(self.cameo.find({"_id": data['cameo_id']}, {"_id": 0, "compare_strings": 0}))
            data['jrc_data'] = list(self.jrc.find({"_id": data['jrc_id']}, {"_id": 0, "compare_strings": 0}))
            del data['cameo_id']
            del data['jrc_id']
            del data['_id']
        return cameo_jrc_result
