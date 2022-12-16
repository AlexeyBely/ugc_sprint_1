import json
import time
import logging

import clickhouse_driver.errors
import kafka.errors

from clickhouse import ClickHouseClient
from kafka_consumer import Consumer

from config.settings import CH_HOST, CH_TABLE, KAFKA_TOPIC, KAFKA_CONSUMER_GROUP, KAFKA_SERVERS, FLUSH_SECONDS, FLUSH_COUNT

LOGGER = logging.getLogger(__name__)


class Etl:

    def __init__(self):
        self.consumer = Consumer(KAFKA_SERVERS, KAFKA_TOPIC, KAFKA_CONSUMER_GROUP)
        self.click_house = ClickHouseClient(CH_HOST, CH_TABLE)

    @staticmethod
    def _parse_key(key):
        key = key.decode('utf-8')
        return key.split('+')

    def execute(self):
        values_backup = []
        values: list = []
        while True:
            try:
                values = values_backup
                flush_start = time.time()
                for record in self.consumer.fetch():
                    value = json.loads(record.value)
                    values.append(self.click_house.transform(value))
                    if len(values) >= FLUSH_COUNT or (time.time() - flush_start) >= FLUSH_SECONDS:
                        res = self.click_house.load(values)
                        # if load fails, will try next time
                        if not res:
                            continue
                        values = []
                        flush_start = time.time()
            except clickhouse_driver.errors.Error as e:
                LOGGER.error(f'Error connecting ClickHouse: {e}')
            except kafka.errors.KafkaError as e:
                LOGGER.error(f'Ошибка в соединении с Kafka: {e}')
            finally:
                values_backup = values


if __name__ == '__main__':
    LOGGER.info('Start ETL')
    Etl().execute()
