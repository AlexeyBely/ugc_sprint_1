import logging
import logging.config
import uuid
import random
from datetime import datetime

from cfg import LOGGING
from clickhouse_driver import Client
import clickhouse_driver

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('load_data')
client = Client(host='localhost')

user_ids = [str(uuid.uuid4()) for x in range(1000)]
movie_ids = [str(uuid.uuid4()) for x in range(1000)]


if __name__ == '__main__':
    logger.info('start')
    values = []
    counter: int = 0
    for i in range(1, 10000001):
        data = {
            'id': uuid.uuid4(),
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





