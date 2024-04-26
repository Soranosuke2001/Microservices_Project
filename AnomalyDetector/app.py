"""
This module defines the main functionality for the Anomaly Detector application.
It sets up the web server, defines routes, and handles anomaly data fetching.
"""

import time
import os
from threading import Thread

import connexion
from connexion.middleware import MiddlewarePosition
from starlette.middleware.cors import CORSMiddleware

from helpers.read_config import read_flask_config, read_log_config
from helpers.query_database import read_kafka, fetch_anomalies
from helpers.test_connection import sqlite_connection, kafka_connection

# Read configuration for Flask and logging
flask_host, flask_port = read_flask_config()
logger = read_log_config()

# Ensure all services are ready before proceeding
time.sleep(10)

# Establish database session and Kafka consumer connection
DB_SESSION = sqlite_connection(logger)
events_consumer = kafka_connection(logger)

def get_anomalies(anomaly_type):
    """
    Fetch and return anomalies for a given type.
    :param anomaly_type: The type of anomaly to fetch
    :return: A tuple of the list of anomalies and HTTP status code
    """
    try:
        logger.info("Fetching detected anomalies for the event type: %s", anomaly_type)

        anomalies = fetch_anomalies(anomaly_type, DB_SESSION)

        results_len = len(anomalies)

        logger.info("Successfully fetched %d anomalies for the event type: %s", results_len, anomaly_type)

        return anomalies, 200
    except Exception as e:
        logger.error("There was an error fetching the anomalies: %s", e)

        return {'message': str(e)}, 400

def check_anomalies():
    """
    Checks for new anomalies by reading from Kafka and updates the database.
    """
    read_kafka(events_consumer, logger, DB_SESSION)

app = connexion.FlaskApp(__name__, specification_dir='')

# Configure CORS middleware
if "TARGET_ENV" not in os.environ or os.environ["TARGET_ENV"] != "test":
    app.add_middleware(CORSMiddleware,
                       position=MiddlewarePosition.BEFORE_EXCEPTION,
                       allow_origins=["*"],
                       allow_credentials=True,
                       allow_methods=["*"],
                       allow_headers=["*"])
    app.app.config['CORS_HEADERS'] = 'Content-Type'

# Add OpenAPI configuration
app.add_api("./config/openapi.yml",
            base_path="/anomaly_detector",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    t1 = Thread(target=check_anomalies)
    t1.daemon = True  # Use the property setter for modern Python versions
    t1.start()

    app.run(host=flask_host, port=flask_port)
