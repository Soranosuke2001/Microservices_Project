from datetime import datetime
import json


def kafka_event_message(producer, body, event_type):
    msg = {
        "type": event_type,
        "datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": body
    }

    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))


def kafka_logger(producer):
    msg = {
        "datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": {
            "message": "Receiver service successfully started",
            "message_code": "0001"
        }
    }

    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    print("CONNECTED TO EVENT_LOG KAKFKA BULLSHIT")
