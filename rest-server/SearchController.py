#!/usr/bin/env python
#
# Copyright 2017 @author Subhasis

import ConfigParser
import logging
import tornado.web

from tornado.options import options
from tornado.escape import json_encode

logger = logging.getLogger('log.application')


class SearchController(tornado.web.RequestHandler):
    config = ConfigParser.ConfigParser()

    def get(self):
        configPath = '../config/config.cnf'
        self.config.read(configPath)
        logger.info(self.config.get('Logging', 'Logger.GetMessage1') + '' + self.request.remote_ip)
        query = self.get_argument(self.config.get('AccessParameters', 'Access.QueryString'))
        result = {}
        result['query'] = query

        # Get result from Bablenet and push to object
        result['bablenet'] = {}

        # Get result from DBpedia and push to object
        result['dbpedia'] = {}
        # get result from caameo and JRC and push to object
        result['cameojrc'] = {}

        result['status'] = self.config.get('GeneralMsg', 'Status.success')
        result['licence'] = self.config.get('GeneralMsg', 'Licence.Ack')
        self.write(json_encode(result))
        self.set_header("Content-Type", "application/json")
