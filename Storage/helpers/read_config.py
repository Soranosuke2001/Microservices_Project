import yaml, logging, logging.config


def read_app_config():
    with open('./config/app_conf.yml', 'r') as file:
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
    

def read_log_config():
    with open('./config/log_conf.yml', 'r') as file:
        log_config = yaml.safe_load(file.read())
        logging.config.dictConfig(log_config)

    logger = logging.getLogger('basicLogger')

    return logger