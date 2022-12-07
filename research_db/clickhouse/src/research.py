import logging
import logging.config
import uuid
import random
from datetime import datetime

from cfg import LOGGING
from clickhouse_driver import Client
import clickhouse_driver

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('research_clickhouse')
client = Client(host='localhost')


sql_querys = [
    ('SHOW DATABASES', True),
    ('SELECT count() FROM movies.frames', True),
    ('SELECT user_id, uniq(movie_id) FROM movies.frames WHERE frame > 100 GROUP by user_id', False),
    ('SELECT movie_id, min(frame), max(frame) FROM movies.frames GROUP by movie_id', False),
]

if __name__ == '__main__':
    logger.info('start research')
    for query, visible in sql_querys:    
        try:
            response = client.execute(query)
        except clickhouse_driver.errors.Error as e:
            logger.error(f'({e.code}) {e.message}')
        finally:
            if visible is True:
                logger.info(f'<{query}> {response}')
            else:
                logger.info(f'<{query}>')        
    logger.info('research OK')




