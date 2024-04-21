import time

from logging import Logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pykafka import KafkaClient
from pykafka.common import OffsetType

from base import Base

from helpers.read_config import get_sqlite_config, get_kafka_config

filename = get_sqlite_config()
kafka_hostname, kafka_port, kafka_topic = get_kafka_config()

def sqlite_connection(logger: Logger):
    SQLITE_CONNECTED = False

    while not SQLITE_CONNECTED:
        try:
            DB_ENGINE = create_engine(f"sqlite:///{filename}")
            Base.metadata.bind = DB_ENGINE
            DB_SESSION = sessionmaker(bind=DB_ENGINE)

            logger.info("Successfully connected to SQLite")
            SQLITE_CONNECTED = True
        except Exception as sqlite_error:
            logger.error(sqlite_error)
            logger.error(
                "Failed to connect to SQLite database, retrying in 5 seconds")
            time.sleep(5)
    
    return DB_SESSION


def kafka_connection(logger: Logger):
    KAFKA_CONNECTED = False

    while not KAFKA_CONNECTED:
        try:
            events_client = KafkaClient(hosts=f'{kafka_hostname}:{kafka_port}')
            events_topic = events_client.topics[str.encode(kafka_topic)]

            events_consumer = events_topic.get_simple_consumer(
                consumer_group=b'log_group',
                reset_offset_on_start=False,
                auto_offset_reset=OffsetType.LATEST
            )

            logger.info("Successfully connected to Kafka")
            KAFKA_CONNECTED = True
        except Exception as kafka_error:
            logger.error(kafka_error)
            logger.error(
                "Failed to connect to events Kafka, retrying in 5 seconds")
            time.sleep(5)

    return events_consumer
