import vertica_python

import logging
import logging.config
import uuid
import random

from datetime import datetime
from cfg import LOGGING
from setting import connection_info


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('load_data')

user_ids = [str(uuid.uuid4()) for x in range(1000)]
movie_ids = [str(uuid.uuid4()) for x in range(1000)]

def create_database(connection_info):
    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS frames (
            id IDENTITY,
            user_id VARCHAR(36) NOT NULL,
            movie_id VARCHAR(36) NOT NULL,
            frame INTEGER NOT NULL,
            event_time DATETIME NOT NULL
        );
        """)


if __name__ == '__main__':
    create_database()
    logger.info('start')
    values = []
    counter: int = 0    
    for i in range(1, 10000001):
        data = {
            'id': i,
            'user_id': random.choice(user_ids),
            'movie_id': random.choice(movie_ids),
            'frame': random.randint(1, 200),
            'event_time': datetime.now(),
        }
        values.append(data)

        if len(values) >= 1000:
            try:
                client.execute('INSERT INTO movies.frames VALUES', values)
            except clickhouse_driver.errors.Error as e:
                logger.error(f'({e.code}) {e.message}')
            finally:
                values = []
                counter += 1000
                logger.info(f'insert {counter} records')
    logger.info('load OK')





