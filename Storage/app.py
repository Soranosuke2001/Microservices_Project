"""
This module sets up a Flask application that interfaces with both a MySQL database and Kafka
to process and store gun statistics and purchase history. It ensures connections to MySQL and Kafka
before starting the Flask application and listens for incoming Kafka messages in a separate thread.
"""

import time
import connexion
from threading import Thread

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pykafka import KafkaClient
from pykafka.common import OffsetType

from base import Base
from gun_stats import GunStats
from purchase_history import PurchaseHistory

from helpers.read_config import database_config, read_log_config, get_kafka_event_config, get_kafka_log_config, read_flask_config
from helpers.query_database import fetch_timestamp_results
from helpers.kafka_message import kafka_message, kafka_logger

# Configuration setup
user, password, hostname, port, db = database_config()
kafka_events_hostname, kafka_events_port, kafka_events_topic = get_kafka_event_config()
kafka_logs_hostname, kafka_logs_port, kafka_logs_topic = get_kafka_log_config()
flask_host, flask_port = read_flask_config()
logger = read_log_config()

time.sleep(10)

MYSQL_CONNECTED = False
EVENT_CONNECTED = False
LOG_CONNECTED = False

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


def fetch_gun_stat(start_timestamp, end_timestamp):
    """Fetch gun statistics within a specified time range."""

    session = DB_SESSION()
    results = fetch_timestamp_results(start_timestamp, end_timestamp, session, GunStats)
    session.close()

    log_info("Gun Statistics", start_timestamp, end_timestamp, len(results))
    return results, 201


def fetch_purchase_transaction(start_timestamp, end_timestamp):
    """Fetch purchase transactions within a specified time range."""

    session = DB_SESSION()
    results = fetch_timestamp_results(start_timestamp, end_timestamp, session, PurchaseHistory)
    session.close()

    log_info("Purchase History", start_timestamp, end_timestamp, len(results))
    return results, 201


def log_info(event_type, start_timestamp, end_timestamp, result_len):
    """Log information about a query."""

    logger.info("Query for %s events after %s, until %s return %s results", event_type, start_timestamp, end_timestamp, result_len)


def process_messages():
    """Process incoming Kafka messages."""

    kafka_message(DB_SESSION, events_consumer, logger)


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("./config/openapi.yml", base_path="/storage", strict_validation=True, validate_response=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.daemon = True
    t1.start()

    kafka_logger(logs_producer)

    app.run(host=flask_host, port=flask_port)
