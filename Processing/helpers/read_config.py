import yaml
import logging.config
import logging
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


def get_mysql_config():
    app_config = read_app_config()

    hostname = app_config['mysql']['url']
    user = app_config['mysql']['user']
    password = app_config['mysql']['password']
    port = app_config['mysql']['port']
    db = app_config['mysql']['db']

    return hostname, user, password, port, db


def get_sqlite_config():
    app_config = read_app_config()

    filename = app_config['datastore']['filename']
    seconds = app_config['scheduler']['period_sec']
    url = app_config['eventstore']['url']

    return filename, seconds, url


def get_kafka_config():
    app_config = conf_filename('app')

    hostname = app_config['events']['hostname']
    port = app_config['events']['port']
    topic = app_config['events']['topic']

    return hostname, port, topic


def get_kafka_threshold():
    app_config = conf_filename('app')

    threshold = app_config['events']['threshold']

    return threshold


def read_log_config():
    log_conf_file = conf_filename('log')

    with open(log_conf_file, 'r') as file:
        log_config = yaml.safe_load(file.read())
        logging.config.dictConfig(log_config)

    logger = logging.getLogger('basicLogger')

    return logger
