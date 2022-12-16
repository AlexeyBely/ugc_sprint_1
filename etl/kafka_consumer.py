from kafka import KafkaConsumer


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

    def fetch(self):
        consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.hosts,
            group_id=self.group_id,
            enable_auto_commit=self.auto_commit,
            auto_offset_reset='earliest',
        )
        for message in consumer:
            yield message
