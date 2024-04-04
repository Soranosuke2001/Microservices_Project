import time

from logging import Logger
from pykafka import KafkaClient

from helpers.read_config import get_kafka_config, get_kafka_event_logs_config

kafka_events_hostname, kafka_events_port, kafka_events_topic = get_kafka_config()
kafka_logs_hostname, kafka_logs_port, kafka_logs_topic = get_kafka_event_logs_config()

EVENTS_CONNECTED = False
LOGS_CONNECTED = False

def events_kafka_connection(logger: Logger):
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
    
    return events_producer


def logs_kafka_connection(logger: Logger):
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
    
    return logs_producer