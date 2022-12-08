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
    create_database(connection_info)
    logger.info('start')
    values = []
    counter: int = 0
    connection = vertica_python.connect(**connection_info)
    cursor = connection.cursor()
    query = 'INSERT INTO frames (user_id, movie_id, frame, event_time) VALUES (%s,%s,%s,%s)'    
    for i in range(1, 10000001):
        data = (
            random.choice(user_ids),
            random.choice(movie_ids),
            random.randint(1, 200),
            datetime.now(),
        )
        values.append(data)

        if len(values) >= 1000:
            try:
                cursor.executemany(query, values)
            except Exception as e:
                logger.error(f'{type(e)}: {e}')
                break
            finally:
                values = []
                counter += 1000
                logger.info(f'insert {counter} records')
    cursor.close()
    connection.close()
    logger.info('load OK')





