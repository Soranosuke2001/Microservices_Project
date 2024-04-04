import time

from pykafka import KafkaClient
from logging import Logger

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import Base

from helpers.read_config import get_kafka_config, get_sqlite_config, get_mysql_config

filename = get_sqlite_config('connection')
hostname, user, password, port, db = get_mysql_config()
kafka_hostname, kafka_port, kafka_topic = get_kafka_config()


def sqlite_connection(logger: Logger):
    SQLITE_CONNECTED = False

    while not SQLITE_CONNECTED:
        try:
            DB_ENGINE = create_engine("sqlite:///%s" %filename)
            Base.metadata.bind = DB_ENGINE
            DB_SESSION = sessionmaker(bind=DB_ENGINE)
            
            logger.info("Successfully connected to SQLite database.")
            SQLITE_CONNECTED = True
        except Exception as e:
            logger.error(e)
            logger.error("Failed to connect to SQLite database, retrying in 5 seconds")
            time.sleep(5)
    
    return DB_SESSION


def kafka_connection(logger: Logger):
    LOGS_CONNECTED = False

    while not LOGS_CONNECTED:
        try:
            logs_client = KafkaClient(hosts=f'{kafka_hostname}:{kafka_port}')
            logs_topic = logs_client.topics[kafka_topic.encode('utf-8')]
            logs_producer = logs_topic.get_sync_producer()
            
            logger.info("Successfully connected to Logger Kafka.")
            LOGS_CONNECTED = True
        except Exception as e:
            logger.error(e)
            logger.error("Failed to connect to Logger Kafka, retrying in 5 seconds")
            time.sleep(5)
    
    return logs_producer


def mysql_connection(logger: Logger):
    CONNECTED = False

    while not CONNECTED:
        try:
            DB_ENGINE = create_engine(f'mysql+pymysql://{user}:{password}@{hostname}:{port}/{db}')
            Base.metadata.bind = DB_ENGINE
            DB_SESSION = sessionmaker(bind=DB_ENGINE)

            logger.info("Successfully connected to MySQL.")
            CONNECTED = True
        except Exception as e:
            logger.error("Failed to connect to MySQL, retrying in 5 seconds")
            time.sleep(5)

    return DB_SESSION