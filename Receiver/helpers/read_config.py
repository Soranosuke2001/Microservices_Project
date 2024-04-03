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


def get_urls():
    app_config = read_app_config()

    return app_config['newGunStat']['url'], app_config['newItemTransaction']['url']


def read_log_config():
    log_conf_file = conf_filename('log')

    with open(log_conf_file, 'r') as file:
        log_config = yaml.safe_load(file.read())
        logging.config.dictConfig(log_config)

    logger = logging.getLogger('basicLogger')

    return logger


def get_kafka_config():
    app_config = read_app_config()

    return app_config['events']['hostname'], app_config['events']['port'], app_config['events']['topic']


def get_kafka_event_logs_config():
    app_config = read_app_config()

    hostname = app_config['event_logs']['hostname']
    port = app_config['event_logs']['port']
    topic = app_config['event_logs']['topic']

    return hostname, port, topic


def read_flask_config():
    app_config = read_app_config()

    host = str(app_config['app']['host'])
    port = app_config['app']['port']

    return host, port