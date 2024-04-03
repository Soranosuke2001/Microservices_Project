"""
This module sets up a Flask app with Connexion for handling requests related to gun statistics
and purchase transactions, sending events to Kafka topics.
"""

import uuid
import time
import connexion
from pykafka import KafkaClient
from connexion import NoContent

from helpers.read_config import get_urls, read_log_config, get_kafka_config, \
    get_kafka_event_logs_config, read_flask_config
from helpers.kafka_message import kafka_event_message, kafka_logger

# Retrieve configuration settings
gun_stat_url, item_transaction_url = get_urls()
kafka_events_hostname, kafka_events_port, kafka_events_topic = get_kafka_config()
kafka_logs_hostname, kafka_logs_port, kafka_logs_topic = get_kafka_event_logs_config()
flask_host, flask_port = read_flask_config()
logger = read_log_config()

# Wait for external services to be available
time.sleep(20)

EVENTS_CONNECTED = False
LOGS_CONNECTED = False

# Connect to Kafka for events
while not EVENTS_CONNECTED:
    try:
        events_client = KafkaClient(hosts=f'{kafka_events_hostname}:{kafka_events_port}')
        events_topic = events_client.topics[str.encode(kafka_events_topic)]
        events_producer = events_topic.get_sync_producer()
        logger.info("Successfully connected to Events Kafka")
        EVENTS_CONNECTED = True
    except Exception as e:
        logger.error("Error: %s", e)
        logger.error("Failed to connect to events Kafka, retrying in 5 seconds")
        time.sleep(5)

# Connect to Kafka for logs
while not LOGS_CONNECTED:
    try:
        logs_client = KafkaClient(hosts=f'{kafka_logs_hostname}:{kafka_logs_port}')
        logs_topic = logs_client.topics[str.encode(kafka_logs_topic)]
        logs_producer = logs_topic.get_sync_producer()
        logger.info("Successfully connected to Logger Kafka")
        LOGS_CONNECTED = True
    except Exception as e:
        logger.error("Error: %s", e)
        logger.error("Failed to connect to logs Kafka, retrying in 5 seconds")
        time.sleep(5)

def create_gun_stat(body):
    """Creates a gun stat record."""
    trace_id = gen_trace_id()
    body['trace_id'] = trace_id

    log_message(trace_id, "create_gun_stat", "receive")

    kafka_event_message(events_producer, body, "gun_stat")

    log_message(trace_id, "create_gun_stat", "return", 201)

    return NoContent, 201

def create_purchase_transaction(body):
    """Creates a purchase transaction record."""
    trace_id = gen_trace_id()
    body['trace_id'] = trace_id

    log_message(trace_id, "create_purchase_transaction", "receive")

    kafka_event_message(events_producer, body, "purchase_history")

    log_message(trace_id, "create_purchase_transaction", "return", 201)

    return NoContent, 201

def gen_trace_id():
    """Generates a unique trace ID."""
    return str(uuid.uuid4())

def log_message(trace_id, event_name, event, status_code=400):
    """Logs messages with a specific format."""
    if event == "receive":
        logger.info("Received event %s request with a trace id of %s", event_name, trace_id)
    else:
        logger.info("Returned event %s response ID: %s with status %s", event_name, trace_id, status_code)

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("./config/openapi.yml", base_path="/receiver", strict_validation=True, validate_response=True)

if __name__ == "__main__":
    kafka_logger(logs_producer)
    app.run(host=flask_host, port=flask_port)
