'''
Created on March 30, 2017
@author: Subhasis
'''

import ConfigParser
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

from HomeController import HomeController
from SearchController import SearchController

config = ConfigParser.ConfigParser()
configPath='../config/config.cnf'
config.read(configPath)

logger= logging.getLogger('log.application')
hdlr = logging.FileHandler(config.get('Logging', 'Logger.File'))
formatter = logging.Formatter('[%(levelname)s %(asctime)s -- %(module)s:%(lineno)d] %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging._levelNames[config.get('Logging', 'Logger.Level')])

define("port", default=config.get('ServerConnection', 'Server.Port'), help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeController),
            (r"/"+config.get('ServerConnection', 'Webservice.Search'), SearchController)
        ]
        logger.info('Handlers Set.')
        settings = dict(
            app_title=u""+config.get('ServerConnection', 'WebApp.title'),
            xsrf_cookies=False,
            debug=config.get('ServerConnection', 'Server.Debug'),
        )
        logger.info('Settings Variables Set.')
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    logger.info('Starting Server ....')
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    logger.info('Server Started. At Port 2121')
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()