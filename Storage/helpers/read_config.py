import yaml
import logging
import logging.config
import os


def conf_filename(service):
    if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
        print("In Testing Environment")

        conf_file = f"/config/{service}_conf.yml"
    else:
        conf_file = f"{service}_conf.yml"
    
    return conf_file


def read_app_config():
    app_conf_file = conf_filename('app')

    with open(app_conf_file, 'r') as file:
        app_config = yaml.safe_load(file.read())

    return app_config


def database_config():
    app_config = read_app_config()

    user = app_config["datastore"]["user"]
    password = app_config["datastore"]["password"]
    hostname = app_config["datastore"]["hostname"]
    port = app_config["datastore"]["port"]
    db = app_config["datastore"]["db"]

    return user, password, hostname, port, db


def read_log_config():
    log_conf_file = conf_filename('log')

    with open(log_conf_file, 'r') as file:
        log_config = yaml.safe_load(file.read())
        logging.config.dictConfig(log_config)

    logger = logging.getLogger('basicLogger')

    return logger


def get_kafka_event_config():
    app_config = read_app_config()

    hostname = app_config['events']['hostname']
    port = app_config['events']['port']
    topic = app_config['events']['topic']

    return hostname, port, topic


def get_kafka_log_config():
    app_config = read_app_config()

    hostname = app_config['event_logs']['hostname']
    port = app_config['event_logs']['port']
    topic = app_config['event_logs']['topic']

    return hostname, port, topic
