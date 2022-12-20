import json
import time
import logging
import logging.config

import clickhouse_driver.errors
import kafka.errors

from clickhouse import ClickHouseClient
from kafka_consumer import Consumer

from config.settings import etl_settings as sett
from config.cfg import LOGGING

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


class Etl:

    def __init__(self):
        self.consumer = Consumer(
            sett.KAFKA_SERVERS,
            sett.KAFKA_TOPIC,
            sett.KAFKA_CONSUMER_GROUP
        )
        self.click_house = ClickHouseClient(
            sett.CH_HOST,
            sett.CH_TABLE
        )

    def execute(self):
        values_backup = []
        values: list = []
        while True:
            try:
                values = values_backup
                flush_start = time.time()
                for record in self.consumer.fetch():
                    values.append(self.click_house.transform(record.value, record.key))
                    if len(values) >= sett.FLUSH_COUNT or (time.time() - flush_start) >= sett.FLUSH_SECONDS:
                        res = self.click_house.load(values)
                        # if load fails, will try next time
                        if not res:
                            continue
                        values = []
                        flush_start = time.time()
            except clickhouse_driver.errors.Error as e:
                LOGGER.error(f"Error connecting ClickHouse: {e}")
            except kafka.errors.KafkaError as e:
                LOGGER.error(f"Error connecting Kafka: {e}")
            finally:
                values_backup = values


if __name__ == "__main__":
    LOGGER.info("Start ETL")
    Etl().execute()
