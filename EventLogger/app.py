import connexion
import time

from threading import Thread
from connexion.middleware import MiddlewarePosition
from starlette.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pykafka import KafkaClient
from pykafka.common import OffsetType

from base import Base

from helpers.read_config import get_sqlite_config, read_log_config, get_kafka_config
from helpers.query_database import check_prev_data, update_db

filename, seconds, url = get_sqlite_config()
kafka_hostname, kafka_port, kafka_topic = get_kafka_config()
logger = read_log_config()

time.sleep(10)

kafka_connected = False
sqlite_connected = False

while not kafka_connected:
    try:
        events_client = KafkaClient(hosts=f'{kafka_hostname}:{kafka_port}')
        events_topic = events_client.topics[str.encode(kafka_topic)]

        events_consumer = events_topic.get_simple_consumer(
            consumer_group=b'event_group', 
            reset_offset_on_start=False, 
            auto_offset_reset=OffsetType.LATEST
        )

        logger.info("Successfully connected to Kafka")
        kafka_connected = True
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.error("Failed to connect to events Kafka, retrying in 5 seconds")
        time.sleep(5)

while not sqlite_connected:
    try:
        DB_ENGINE = create_engine("sqlite:///%s" %filename)
        Base.metadata.bind = DB_ENGINE
        DB_SESSION = sessionmaker(bind=DB_ENGINE)

        logger.info("Successfully connected to SQLite")
        sqlite_connected = True
    except Exception as e:
        logger.error("Failed to connect to SQLite database, retrying in 5 seconds")
        time.sleep(5)


def fetch_event_stats():
    logger.info("Fetching logged events")

    try:
        prev_entry = check_prev_data(DB_SESSION)

        data = {
            "0001": prev_entry['0001'],
            "0002": prev_entry['0002'],
            "0003": prev_entry['0003'],
            "0004": prev_entry['0004'],
        }

        logger.info("Successfully fetched logged events")

        return data, 200
    except Exception as e:
        logger.error("There was an error fetching the data entry from SQLite database.")
        return { 'message': e }, 400


def update_logs():
    logger.info("Started periodic event logging")

    prev_data = check_prev_data(DB_SESSION)

    update_db(prev_data, events_consumer, logger, DB_SESSION)

    logger.info("Ended periodic event logging")


# def init_scheduler():
#     sched = BackgroundScheduler(daemon=True)
#     sched.add_job(update_logs, 'interval', seconds=seconds)

#     sched.start()
    

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_middleware(CORSMiddleware, position=MiddlewarePosition.BEFORE_EXCEPTION, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_api("./config/openapi.yml", strict_validation=True, validate_response=True)

if __name__ == "__main__":
    # init_scheduler()
    t1 = Thread(target=update_logs)
    t1.setDaemon(True)
    t1.start()

    app.run(host="0.0.0.0", port=8120)
