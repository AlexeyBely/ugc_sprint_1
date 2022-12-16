from kafka import KafkaConsumer
import logging

LOGGER = logging.getLogger(__name__)


class Consumer:

    def __init__(
            self,
            hosts: list[str],
            topic: str,
            group_id: str,
            auto_commit: bool = False,
    ):
        self.hosts = hosts
        self.topic = topic
        self.group_id = group_id
        self.auto_commit = auto_commit
        self.consumer = self.consumer()

    def consumer(self):
        LOGGER.info("Start Kafka consumer")
        return KafkaConsumer(
            self.topic,
            bootstrap_servers=self.hosts,
            group_id=self.group_id,
            enable_auto_commit=self.auto_commit,
            auto_offset_reset="earliest",
        )

    def fetch(self):
        for message in self.consumer:
            yield message
