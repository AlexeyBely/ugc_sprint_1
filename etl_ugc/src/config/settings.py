from pydantic import BaseSettings

class EtlSettings(BaseSettings):
    CH_HOST: str = 'clickhouse://clickhouse-node1'
    CH_TABLE: str = 'movies.frames'
    KAFKA_TOPIC: str = 'movies-frames'
    KAFKA_CONSUMER_GROUP: str = 'echo-messages-to-stdout'
    KAFKA_SERVERS: str = 'localhost:9092'
    FLUSH_SECONDS: float = 30
    FLUSH_COUNT: int = 1000

etl_settings = EtlSettings()