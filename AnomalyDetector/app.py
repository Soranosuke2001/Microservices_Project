import time
import os
from threading import Thread

import connexion
from connexion.middleware import MiddlewarePosition
from starlette.middleware.cors import CORSMiddleware

from helpers.read_config import read_flask_config, read_log_config
from helpers.query_database import read_kafka, fetch_anomalies
from helpers.test_connection import sqlite_connection, kafka_connection

flask_host, flask_port = read_flask_config()
logger = read_log_config()

time.sleep(10)

DB_SESSION = sqlite_connection(logger)
events_consumer = kafka_connection(logger)


def get_anomalies(anomaly_type):
    try:
        logger.info(f"Fetching detected anomalies for the event type: {anomaly_type}")

        anomalies = fetch_anomalies(anomaly_type)

        results_len = len(anomalies)

        logger.info(f"Successfully fetched {results_len} anomalies for the event type: {anomaly_type}")

        return anomalies, 200
    except Exception as e:
        logger.error(f"There was an error fetching the anomalies: {e}")

        return { 'message': e }, 400


def check_anomalies():
    read_kafka(events_consumer, logger, DB_SESSION)


app = connexion.FlaskApp(__name__, specification_dir='')

if "TARGET_ENV" not in os.environ or os.environ["TARGET_ENV"] != "test":
    app.add_middleware(CORSMiddleware,
                       position=MiddlewarePosition.BEFORE_EXCEPTION,
                       allow_origins=["*"],
                       allow_credentials=True,
                       allow_methods=["*"],
                       allow_headers=["*"])
    app.app.config['CORS_HEADERS'] = 'Content-Type'

app.add_api("./config/openapi.yml",
            base_path="/event_logger",
            strict_validation=True,
            validate_response=True)

if __name__ == "__main__":
    t1 = Thread(target=check_anomalies)
    t1.setDaemon(True)
    t1.start()

    app.run(host=flask_host, port=flask_port)
