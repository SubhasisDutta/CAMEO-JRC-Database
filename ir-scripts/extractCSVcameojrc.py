import unicodecsv as csv
from MongoManager import MongoManager
import argparse
import ConfigParser
import os

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

    manager = MongoManager(schema, cameo_table, batch_size, db_config)
    cameo = manager.get_collection()
    cameo_data = cameo.find()
    counter = 0
    result_file_cameo = config.get('Cameo', 'Cameo.CSV')
    os.remove(result_file_cameo)
    with open(result_file_cameo, 'ab') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        d = ['id','record_type','cameo_title','compare_strings']
        writer.writerow(d)
        for cameo_record in cameo_data:
            cameo_compare_list = cameo_record['compare_strings']
            for s in cameo_compare_list:
                dataList = []
                dataList.append(cameo_record['_id'])
                dataList.append(cameo_record['record_type'])
                dataList.append(cameo_record['cameo_title'])
                dataList.append(s)
                writer.writerow(dataList)
                counter += 1
    print "# of CAMEO entities extracted: ", counter

    manager2 = MongoManager(schema, jrc_table, batch_size, db_config)
    jrc = manager2.get_collection()
    jrc_data = jrc.find({})
    counter = 0
    result_file_jrc = config.get('JRCNames', 'Jrc.CSV')
    os.remove(result_file_jrc)
    with open(result_file_jrc, 'ab') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        d = ['id','jrc_id','type','compare_strings']
        writer.writerow(d)
        for jrc_record in jrc_data:
            jrc_compare_list = jrc_record['compare_strings']
            for s in jrc_compare_list:
                dataList = []
                dataList.append(jrc_record['_id'])
                dataList.append(jrc_record['id'])
                dataList.append(jrc_record['type'])
                dataList.append(s)
                writer.writerow(dataList)
                counter += 1
    print "# of JRC entities extracted: ", counter