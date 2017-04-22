'''
Created on Jan 30, 2017
@author: Subhasis
'''

import sys
from datetime import datetime
import argparse
import ConfigParser

from MongoManager import MongoManager
from nameTranslatorService import nameTranslatorService

if __name__ == '__main__':
    print "Starting @ ", str(datetime.now())
    parser = argparse.ArgumentParser(
        description='Script to load CAMEO and JRC data and find their relation and store them in a table.')
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

    batch_size = config.get('MongoDBConnection', 'db.batch_limit')

    cameo_table = config.get('Cameo', 'db.Cameo')
    jrc_table = config.get('JRCNames', 'db.JRCNames')
    jrc_cameo_table = config.get('CameoJRC', 'db.CameoJRCCountryActor')
    cameo_name_translation_table = config.get('NameTranslation','db.NameTranslation')

    # Uncomment this only to remove oldd data and build a new data table
    #cleaner = MongoManager(schema, cameo_name_translation_table, batch_size, db_config)
    #cleaner.drop_collection()

    processor = nameTranslatorService(db_config, schema, cameo_name_translation_table, batch_size, cameo_table,
                                      jrc_table, jrc_cameo_table)

    processComplete = processor.process(False,True)

    if processComplete:
        print "DONE"
    else:
        print "NOT FINISHED"
    print "Finished @ ", str(datetime.now())