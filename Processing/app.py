"""Main module for handling statistic updates and serving the processing API."""

import os
import time
from datetime import datetime

import connexion
from apscheduler.schedulers.background import BackgroundScheduler

from connexion.middleware import MiddlewarePosition
from starlette.middleware.cors import CORSMiddleware

from stats import Stats

from helpers.log_message import (
    start_request, end_request, data_found, data_not_found,
    start_periodic, end_periodic, updated_db, no_events
)
from helpers.kafka_message import kafka_logger
from helpers.query_database import row_counter, check_db, update_storage
from helpers.read_config import get_sqlite_config, read_log_config, read_flask_config
from helpers.test_connection import sqlite_connection, kafka_connection

seconds = get_sqlite_config('app')
flask_host, flask_port = read_flask_config()
logger = read_log_config()

time.sleep(10)

DB_SESSION = sqlite_connection(logger)
logs_producer = kafka_connection(logger)


def get_stats():
    """Fetches and returns current statistics."""
    start_request(logger)

    session = DB_SESSION()

    response = row_counter(session, Stats)

    session.close()

    if response is None:
        data_not_found(logger, 400, "No new data")
        return "No Data Found", 400
    else:
        data_found(logger, response)
        end_request(logger)
        return response, 200


def populate_stats():
    """Populates the database with new stats periodically."""
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
    """Initializes the scheduler for periodic tasks."""
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats, 'interval', seconds=seconds)
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir='')

if "TARGET_ENV" not in os.environ or os.environ["TARGET_ENV"] != "test":
    app.add_middleware(
        CORSMiddleware, position=MiddlewarePosition.BEFORE_EXCEPTION,
        allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
    )
    app.app.config['CORS_HEADERS'] = 'Content-Type'

app.add_api("./config/openapi.yml", base_path="/processing", strict_validation=True, validate_response=True)

if __name__ == "__main__":
    time.sleep(20)

    init_scheduler()
    kafka_logger(logs_producer)
    app.run(host=flask_host, port=flask_port)
