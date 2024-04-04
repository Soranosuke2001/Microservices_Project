import time

from logging import Logger

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pykafka import KafkaClient
from pykafka.common import OffsetType

from base import Base

from helpers.read_config import database_config, get_kafka_event_config, get_kafka_log_config

user, password, hostname, port, db = database_config()
kafka_events_hostname, kafka_events_port, kafka_events_topic = get_kafka_event_config()
kafka_logs_hostname, kafka_logs_port, kafka_logs_topic = get_kafka_log_config()


def mysql_connection(logger: Logger):
    MYSQL_CONNECTED = False
    # Attempt to connect to MySQL
    while not MYSQL_CONNECTED:
        try:
            logger.info("Connecting to DB. Hostname: %s, Port: %s", hostname, port)
            DB_ENGINE = create_engine(f'mysql+pymysql://{user}:{password}@{hostname}:{port}/{db}')
            Base.metadata.bind = DB_ENGINE
            DB_SESSION = sessionmaker(bind=DB_ENGINE)

            logger.info("Successfully connected to DB. Hostname: %s, Port: %s", hostname, port)
            MYSQL_CONNECTED = True
        except Exception as e:
            logger.error('Error: %s', e)
            logger.error("Failed to connect to MySQL, retrying in 5 seconds")
            time.sleep(5)

    return DB_SESSION


def events_kafka_connection(logger: Logger):
    EVENT_CONNECTED = False

    # Attempt to connect to Kafka for event processing
    while not EVENT_CONNECTED:
        try:
            events_client = KafkaClient(hosts=f'{kafka_events_hostname}:{kafka_events_port}')
            events_topic = events_client.topics[str.encode(kafka_events_topic)]
            events_consumer = events_topic.get_simple_consumer(
                consumer_group=b'event_group', 
                reset_offset_on_start=False, 
                auto_offset_reset=OffsetType.LATEST
            )

            logger.info("Successfully connected to Event Kafka")
            EVENT_CONNECTED = True
        except Exception as e:
            logger.error("Error: %s", e)
            logger.error("Failed to connect to events Kafka, retrying in 5 seconds")
            time.sleep(5)

    return events_consumer


def logs_kafka_connection(logger: Logger):
    LOG_CONNECTED = False

    # Attempt to connect to Kafka for logging
    while not LOG_CONNECTED:
        try:
            logs_client = KafkaClient(hosts=f'{kafka_logs_hostname}:{kafka_logs_port}')
            logs_topic = logs_client.topics[str.encode(kafka_logs_topic)]
            logs_producer = logs_topic.get_sync_producer()

            logger.info("Successfully connected to Logger Kafka")
            LOG_CONNECTED = True
        except Exception as e:
            logger.error("Error: %s", e)
            logger.error("Failed to connect to logs Kafka, retrying in 5 seconds")
            time.sleep(5)

    return logs_producer
