import json

from datetime import datetime

def kafka_logger(producer):
    msg = {
        "datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3],
        "payload": {
            "message": "Processing service successfully started",
            "message_code": "0003"
        }
    }

    print(f"Message created: {msg}")

    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))


def kafka_max_count(producer, max_count):
    msg = {
        "datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3],
        "payload": {
            "message": f"Processing service has received more than {max_count} kafka messages",
            "message_code": "0004"
        }
    }

    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
