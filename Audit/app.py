"""
This module provides a Flask app for auditing purposes, with endpoints to fetch gun statistics
and purchase transactions from a Kafka topic.
"""

import connexion

from helpers.read_config import read_log_config, get_kafka_config, read_flask_config
from helpers.kafka_fetch import kafka_fetch

kafka_hostname, kafka_port, kafka_topic = get_kafka_config()
flask_host, flask_port = read_flask_config()
logger = read_log_config()

def fetch_gun_stat(index):
    """Fetches gun statistic events from Kafka based on the provided index."""
    logger.info("Retrieving Gun Statistic event at index: %s", index)
    
    message, status_code = kafka_fetch(kafka_hostname,
                                       kafka_port,
                                       kafka_topic,
                                       "gun_stat",
                                       index,
                                       logger)
    
    return message, status_code

def fetch_purchase_transaction(index):
    """Fetches purchase transaction events from Kafka based on the provided index."""
    logger.info("Retrieving Purchase History event at index: %s", index)
    
    message, status_code = kafka_fetch(kafka_hostname,
                                       kafka_port,
                                       kafka_topic,
                                       "purchase_history",
                                       index,
                                       logger)
    
    return message, status_code

def log_info(event_type, start_timestamp, end_timestamp, result_len):
    """Logs information about query results for a specific event type."""
    logger.info(
        "Query for %s events after %s, until %s return %s results",
        event_type, start_timestamp, end_timestamp, result_len)

app = connexion.FlaskApp(__name__, specification_dir='')

app.add_api("./config/openapi.yml", base_path="/audit_log",
            strict_validation=True, validate_response=True)

if __name__ == "__main__":
    app.run(host=flask_host, port=flask_port)
