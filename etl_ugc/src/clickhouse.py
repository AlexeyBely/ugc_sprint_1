from datetime import datetime
import logging
import uuid

from clickhouse_driver import Client


LOGGER = logging.getLogger(__name__)


class ClickHouseClient:

    def __init__(self, host: str, table: str):
        self.host = host
        self.table = table
        self.client = self.client()

    def client(self):
        LOGGER.info("Start ClickHouse client")
        return Client.from_url(self.host)

    @staticmethod
    def transform(value: bytes, key: bytes) -> dict:
        """Transform Kafka record into ClickHouse format."""
        key_kafka: str = key.decode('UTF-8')
        user_movie_ids = key_kafka.split('+')
        record = {}
        try:
            record["id"] = uuid.uuid4()
            record["user_id"] = user_movie_ids[0]
            record["movie_id"] = user_movie_ids[1]
            record["frame"] = int(value)
            record["event_time"] = datetime.now()
            return record
        except Exception as e:
            LOGGER.error(f"Error while preparing the message: {e}")
            raise

    def load(self, values: list) -> bool:
        try:
            self.client.execute(f"INSERT INTO {self.table} VALUES", values, types_check=True)
            LOGGER.info(f"{len(values)} rows upload successfully")
            return True
        except KeyError as ch_error:
            LOGGER.error(f"ClickHouse error encountered: {ch_error}")
            return False
