import connexion
import time

from datetime import datetime
from connexion.middleware import MiddlewarePosition
from pykafka import KafkaClient
from pykafka.common import OffsetType
from starlette.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import Base
from stats import Stats

from helpers.log_message import start_request, end_request, data_found, data_not_found, start_periodic, end_periodic, updated_db, no_events
from helpers.kafka_message import kafka_logger
from helpers.query_database import row_counter, check_db, update_storage
from helpers.read_config import get_sqlite_config, read_log_config, get_kafka_config

filename, seconds, url = get_sqlite_config()    
kafka_hostname, kafka_port, kafka_topic = get_kafka_config()
logger = read_log_config()

DB_ENGINE = create_engine("sqlite:///%s" %filename)
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

time.sleep(10)

logs_connected = False

while not logs_connected:
    try:
        logs_client = KafkaClient(hosts=f'{kafka_hostname}:{kafka_port}')
        logs_topic = logs_client.topics[str.encode(kafka_topic)]
        logs_producer = logs_topic.get_sync_producer()
        
        logger.info("Successfully connected to Logger Kafka.")
        logs_connected = True
    except Exception as e:
        logger.error(e)
        logger.error("Failed to connect to logs Kafka, retrying in 5 seconds")
        time.sleep(5)


def get_stats():
    start_request(logger)

    session = DB_SESSION()

    response = row_counter(session, Stats)

    session.close()

    if response == None:
        data_not_found(logger, 400, "No new data")

        return "No Data Found", 400
    else:
        data_found(logger, response)
        end_request(logger)

        return response, 200


def populate_stats():
    start_periodic(logger)

    session = DB_SESSION()

    data = check_db(session, Stats)

    new_data = update_storage(logger, data, logs_producer)

    if new_data == "error":
        return

    if new_data['new_event']:
        updated_db(logger, new_data)
    else:
        last_updated = datetime.now()
        new_data['last_updated'] = last_updated

        no_events(logger, last_updated.strftime("%Y-%m-%d %H:%M:%S.%f"))

    pr = Stats(
        new_data['num_gun_stat_events'],
        new_data['head_shot_count'],
        new_data['bullet_shot_count'],
        new_data['num_purchase_history_events'],
        new_data['total_revenue'],
        new_data['last_updated'],
    )

    session.add(pr)

    session.commit()
    session.close()

    end_periodic(logger)
    

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats, 'interval', seconds=seconds)

    sched.start()


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_middleware(CORSMiddleware, position=MiddlewarePosition.BEFORE_EXCEPTION, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_api("./config/openapi.yml", strict_validation=True, validate_response=True)

if __name__ == "__main__":
    time.sleep(20)
    
    init_scheduler()
    kafka_logger()
    app.run(host="0.0.0.0", port=8100)


