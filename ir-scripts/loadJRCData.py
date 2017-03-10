'''
Created on Jan 30, 2017
@author: Subhasis
'''

import sys
from datetime import datetime
import argparse
import ConfigParser

from MongoManager import MongoManager

from JRCFileParserService import JRCFileParserService

if __name__ == '__main__':
    print "Starting @ ", str(datetime.now())
    parser = argparse.ArgumentParser(description='Script to process JRC data and push it into MongoDB collection.')
    parser.add_argument('--config', default='../config/config.cnf',
                        help='Location of Config File (default: ../config/config.cnf)')
    args = parser.parse_args()
    config = ConfigParser.ConfigParser()
    config_file = args.config

    config.read(config_file)

    input_file = config.get('JRCNames', 'JRCNames.entityfile')

    db_config = {
        'host': config.get('MongoDBConnection', 'db.host'),
        'port': config.get('MongoDBConnection', 'db.port'),
        'username': config.get('MongoDBConnection', 'db.username'),
        'password': config.get('MongoDBConnection', 'db.password')
    }

    schema = config.get('MongoDBConnection', 'db.schema')
    table = config.get('JRCNames', 'db.JRCNames')
    batch_size = config.get('MongoDBConnection', 'db.batch_limit')

    cleaner = MongoManager(schema, table, batch_size, db_config)
    cleaner.drop_collection()

    processor = JRCFileParserService(input_file, db_config, schema, table, batch_size)

    processComplete = processor.process()

    if processComplete:
        print "DONE"
    else:
        print "NOT FINISHED"
    print "Finished @ ", str(datetime.now())
