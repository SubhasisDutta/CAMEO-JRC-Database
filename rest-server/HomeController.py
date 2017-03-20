#!/usr/bin/env python
#
# Copyright 2017 @author Subhasis

import logging
import ConfigParser
import tornado.web

logger = logging.getLogger('log.application')


class HomeController(tornado.web.RequestHandler):
    config = ConfigParser.ConfigParser()

    def get(self):
        configPath = '../config/config.cnf'
        self.config.read(configPath)
        logger.info(self.config.get('Logging', 'Logger.HomeMessage') + '' + self.request.remote_ip)
        self.write({"multilangAPI": "Welcome", "Status": "Server Running"})
        self.set_header("Content-Type", "application/json")
