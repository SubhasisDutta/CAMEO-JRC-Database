'''
Created on Feb 20, 2017
@author: Subhasis
'''

import sys
from datetime import datetime
import argparse
import ConfigParser


from MongoManager import MongoManager
from CameoJRCRelationService import CameoJRCRelationService

if __name__ == '__main__':
    print "Starting @ ", str(datetime.now())
    parser = argparse.ArgumentParser(description='Script to load CAMEO and JRC data and find their relation and store them in a table.')
    parser.add_argument('--config', default='../config/config.cnf',
                        help='Location of Config File (default: ../config/config.cnf)')
    args = parser.parse_args()
    config = ConfigParser.ConfigParser()
    config_file = args.config

    config.read(config_file)

    db_config = {
        'host': config.get('MongoDBConnection', 'db.host'),
        'port': config.get('MongoDBConnection', 'db.port'),
        'username': config.get('MongoDBConnection', 'db.username'),
        'password': config.get('MongoDBConnection', 'db.password')
    }

    schema = config.get('MongoDBConnection', 'db.schema')
    target_table = config.get('CameoJRC', 'db.CameoJRCCountryActor')
    batch_size = config.get('MongoDBConnection', 'db.batch_limit')

    cameo_table = config.get('Cameo', 'db.Cameo')
    jrc_table = config.get('JRCNames', 'db.JRCNames')

    cleaner = MongoManager(schema, target_table, batch_size, db_config)
    cleaner.drop_collection()

    processor = CameoJRCRelationService(db_config, schema, target_table, batch_size, cameo_table, jrc_table)

    processComplete = processor.process()

    if processComplete:
        print "DONE"
    else:
        print "NOT FINISHED"
    print "Finished @ ", str(datetime.now())
