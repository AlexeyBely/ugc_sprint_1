import logging
import logging.config
from cfg import LOGGING

from clickhouse_driver import Client

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('create_clickhouse')


if __name__ == '__main__':
    logger.info('start')
    client = Client(host='localhost') 
    db = client.execute('CREATE DATABASE IF NOT EXISTS movies ON CLUSTER company_cluster')
    logger.info(f'nodes: {db}')
    sql_query = 'CREATE TABLE movies.stoped ON CLUSTER company_cluster '
    sql_query += '(id_user UUID, id_movie UUID, timestamp Int32)'
    sql_query += ' Engine=MergeTree() ORDER BY id'
    logger.info(f'query: {sql_query}')
    #client.execute(sql_query)





