'''
Created on Feb 20, 2017
@author: Subhasis
'''

import argparse
import ConfigParser
from MongoManager import MongoManager

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Script to find data stats.')
    parser.add_argument('--config', default='../config/config.cnf',
                        help='Location of Config File (default: ../config/config.cnf)')
    args = parser.parse_args()
    config = ConfigParser.ConfigParser()
    config_file = args.config
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
    target_table = config.get('CameoJRC', 'db.CameoJRCCountryActor')

    #No of entities in Cameo.Phoenix.Countries.actors
    manager = MongoManager(schema, cameo_table, batch_size, db_config)
    cameo = manager.get_collection()
    cameo_data = cameo.find({"record_type": "Cameo.Phoenix.Countries.actors"})
    counter = 0
    for cameo_record in cameo_data:
        cameo_compare_list = cameo_record['compare_strings']
        counter+= len(cameo_compare_list)
    print "# of entities in Cameo.Phoenix.Countries.actors: ", counter

    cameo_data = cameo.find({"record_type": "Cameo.Phoenix.International.actors"})
    counter = 0
    for cameo_record in cameo_data:
        cameo_compare_list = cameo_record['compare_strings']
        counter += len(cameo_compare_list)
    print "# of entities in Cameo.Phoenix.International.actors: ", counter

    cameo_data = cameo.find({"record_type": "Cameo.Phoenix.MilNonState.actors"})
    counter = 0
    for cameo_record in cameo_data:
        cameo_compare_list = cameo_record['compare_strings']
        counter += len(cameo_compare_list)
    print "# of entities in Cameo.Phoenix.MilNonState.actors: ", counter

    cameo_data = cameo.find({"record_type": "Cameo.Phoenix.agents"})
    counter = 0
    for cameo_record in cameo_data:
        cameo_compare_list = cameo_record['compare_strings']
        counter += len(cameo_compare_list)
    print "# of entities in Cameo.Phoenix.agents: ", counter

    manager2 = MongoManager(schema, jrc_table, batch_size, db_config)
    jrc = manager2.get_collection()
    jrc_data = jrc.find({})
    counter = 0
    for jrc_record in jrc_data:
        jrc_compare_list = jrc_record['compare_strings']
        counter += len(jrc_compare_list)
    print "# of entities in JRC Data: ", counter

    manager3 = MongoManager(schema, target_table, batch_size, db_config)
    jrc_cameo = manager3.get_collection()
    jrc_cameo_data = jrc_cameo.find({})
    counter = 0
    for jrc_record in jrc_cameo_data:
        #jrc_compare_list = jrc_record['compare_strings']
        counter += 1
    print "# of entities in JRC CAMEO Relation Data: ", counter

    print ""
