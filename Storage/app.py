"""
This module sets up a Flask application that interfaces with both a MySQL database and Kafka
to process and store gun statistics and purchase history. It ensures connections to MySQL and Kafka
before starting the Flask application and listens for incoming Kafka messages in a separate thread.
"""

import time
import connexion
from threading import Thread

from gun_stats import GunStats
from purchase_history import PurchaseHistory

from helpers.read_config import read_log_config, read_flask_config
from helpers.query_database import fetch_timestamp_results
from helpers.kafka_message import kafka_message, kafka_logger
from helpers.test_connection import mysql_connection, events_kafka_connection, logs_kafka_connection

# Configuration setup
flask_host, flask_port = read_flask_config()
logger = read_log_config()

time.sleep(10)

DB_SESSION = mysql_connection(logger)
events_consumer = events_kafka_connection(logger)
logs_producer = logs_kafka_connection(logger)


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
