import connexion, time
from threading import Thread

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pykafka import KafkaClient
from pykafka.common import OffsetType

from base import Base
from gun_stats import GunStats
from purchase_history import PurchaseHistory

from helpers.read_config import database_config, read_log_config, get_kafka_event_config, get_kafka_log_config
from helpers.query_database import fetch_timestamp_results
from helpers.kafka_message import kafka_message


user, password, hostname, port, db = database_config()
events_hostname, events_port, events_topic = get_kafka_event_config()
logs_hostname, logs_port, logs_topic = get_kafka_log_config()
logger = read_log_config()

time.sleep(10)

mysql_connected = False
event_connected = False
log_connected = False

while not mysql_connected:
    try:
        logger.info(f"Connecting to DB. Hostname: {hostname}, Port: {port}")

        DB_ENGINE = create_engine(f'mysql+pymysql://{user}:{password}@{hostname}:{port}/{db}')
        Base.metadata.bind = DB_ENGINE
        DB_SESSION = sessionmaker(bind=DB_ENGINE)

        logger.info(f"Successfully connected to DB. Hostname: {hostname}, Port: {port}")
    except:
        logger.error("Failed to connect to MySQL, retrying in 5 seconds")
        time.sleep(5)
        
while not event_connected:
    try:
        events_client = KafkaClient(hosts=f'{events_hostname}:{events_port}')
        events_topic = events_client.topics[str.encode(events_topic)]

        events_consumer = events_topic.get_simple_consumer(
            consumer_group=b'event_group', 
            reset_offset_on_start=False, 
            auto_offset_reset=OffsetType.LATEST
        )
    except:
        logger.error("Failed to connect to events Kafka, retrying in 5 seconds")
        time.sleep(5)

while not log_connected:
    try:
        logs_client = KafkaClient(hosts=f'{logs_hostname}:{logs_port}')
        logs_topic = logs_client.topics[str.encode(logs_topic)]

        logs_consumer = logs_topic.get_simple_consumer(
            consumer_group=b'event_group', 
            reset_offset_on_start=False, 
            auto_offset_reset=OffsetType.LATEST
        )
    except:
        logger.error("Failed to connect to logs Kafka, retrying in 5 seconds")
        time.sleep(5)


def fetch_gun_stat(start_timestamp, end_timestamp):
    session = DB_SESSION()

    results = fetch_timestamp_results(start_timestamp, end_timestamp, session, GunStats)

    session.close()

    log_info("Gun Statistics", start_timestamp, end_timestamp, len(results))

    return results, 201


def fetch_purchase_transaction(start_timestamp, end_timestamp):
    session = DB_SESSION()

    results = fetch_timestamp_results(start_timestamp, end_timestamp, session, PurchaseHistory)

    session.close()

    log_info("Purchase History", start_timestamp, end_timestamp, len(results))

    return results, 201


def log_info(event_type, start_timestamp, end_timestamp, result_len):
    logger.info(f"Query for {event_type} events after {start_timestamp}, until {end_timestamp} return {result_len} results")


def process_messages():
    kafka_message(DB_SESSION, events_consumer, logger)

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("./config/openapi.yml", strict_validation=True, validate_response=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()

    app.run(host="0.0.0.0", port=8090)

