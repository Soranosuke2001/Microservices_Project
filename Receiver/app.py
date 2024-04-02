from connexion import NoContent
import connexion, uuid, time
from pykafka import KafkaClient

from helpers.read_config import get_urls, read_log_config, get_kafka_config, get_kafka_event_logs_config
from helpers.kafka_message import kafka_event_message, kafka_logger

gun_stat_url, item_transaction_url = get_urls()
kafka_events_hostname, kafka_events_port, kafka_events_topic = get_kafka_config()
kafka_logs_hostname, kafka_logs_port, kafka_logs_topic = get_kafka_event_logs_config()
logger = read_log_config() 

time.sleep(10)

events_connected = False
logs_connected = False

while not events_connected:
    try:
        events_client = KafkaClient(hosts=f'{kafka_events_hostname}:{kafka_events_port}')
        events_topic = events_client.topics[str.encode(kafka_events_topic)]
        events_producer = events_topic.get_sync_producer()

        logger.info("Successfully connected to Events Kafka")
        events_connected = True
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.error("Failed to connect to events Kafka, retrying in 5 seconds")
        time.sleep(5)

while not logs_connected:
    try:
        logs_client = KafkaClient(hosts=f'{kafka_logs_hostname}:{kafka_logs_port}')
        logs_topic = logs_client.topics[str.encode(kafka_logs_topic)]
        logs_producer = logs_topic.get_sync_producer()
        
        logger.info("Successfully connected to Logger Kafka")
        logs_connected = True
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.error("Failed to connect to logs Kafka, retrying in 5 seconds")
        time.sleep(5)


def create_gun_stat(body):
    trace_id = gen_trace_id()
    body['trace_id'] = trace_id

    log_message(trace_id, "create_gun_stat", "receive")

    kafka_event_message(events_producer, body, "gun_stat")

    log_message(trace_id, "create_gun_stat", "return", 201)

    return NoContent, 201


def create_purchase_transaction(body):
    trace_id = gen_trace_id()
    body['trace_id'] = trace_id

    log_message(trace_id, "create_purchase_transaction", "receive")

    kafka_event_message(events_producer, body, "purchase_history")

    log_message(trace_id, "create_purchase_transaction", "return", 201)

    return NoContent, 201


def gen_trace_id():
    return str(uuid.uuid4())


def log_message(trace_id, event_name, event, status_code=400):
    if event == "receive":
        logger.info(f"Received event {event_name} request with a trace id of {trace_id}")
    else:
        logger.info(f"Returned event {event_name} response ID: {trace_id} with status {status_code}")


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("./config/openapi.yml", base_path="/receiver", strict_validation=True, validate_response=True)


if __name__ == "__main__":
    print("Running the service")
    kafka_logger(logs_producer)
    print("The kafka logs event message was sent")
    
    app.run(host="0.0.0.0", port=8080)