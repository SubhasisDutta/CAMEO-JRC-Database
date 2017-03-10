'''
Created on Jan 30, 2017
@author: Subhasis
'''

import sys
from datetime import datetime
import argparse
import ConfigParser

from MongoManager import MongoManager

from CAMEOFileParserService import CAMEOFileParserService

if __name__ == '__main__':
    print "Starting @ ", str(datetime.now())
    parser = argparse.ArgumentParser(description='Script to process CAMEO data and push it into MongoDB collection.')
    parser.add_argument('--config', default='../config/config.cnf',
                        help='Location of Config File (default: ../config/config.cnf)')
    args = parser.parse_args()
    config = ConfigParser.ConfigParser()
    config_file = args.config

    config.read(config_file)

    input_files = {}
    input_files['Cameo.Phoenix.agents'] = config.get('Cameo', 'Cameo.Phoenix.agents')
    input_files['Cameo.Phoenix.Countries.actors'] = config.get('Cameo', 'Cameo.Phoenix.Countries.actors')
    input_files['Cameo.Phoenix.International.actors'] = config.get('Cameo', 'Cameo.Phoenix.International.actors')
    input_files['Cameo.Phoenix.MilNonState.actors'] = config.get('Cameo', 'Cameo.Phoenix.MilNonState.actors')

    db_config = {
        'host': config.get('MongoDBConnection', 'db.host'),
        'port': config.get('MongoDBConnection', 'db.port'),
        'username': config.get('MongoDBConnection', 'db.username'),
        'password': config.get('MongoDBConnection', 'db.password')
    }

    schema = config.get('MongoDBConnection', 'db.schema')
    table = config.get('Cameo', 'db.Cameo')
    batch_size = config.get('MongoDBConnection', 'db.batch_limit')

    cleaner = MongoManager(schema, table, batch_size, db_config)
    cleaner.drop_collection()

    processor = CAMEOFileParserService(input_files, db_config, schema, table, batch_size)

    processComplete = processor.process()

    if processComplete:
        print "DONE"
    else:
        print "NOT FINISHED"
    print "Finished @ ", str(datetime.now())
