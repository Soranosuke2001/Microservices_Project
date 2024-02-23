from pykafka import KafkaClient
from pykafka.common import OffsetType
import json

from logging import Logger
from sqlalchemy.orm import Session

from gun_stats import GunStats
from purchase_history import PurchaseHistory


def log_debug(logger: Logger, event_name, trace_id):
    logger.debug(f"Stored event {event_name} request with a trace id of {trace_id}")


def session_commit(DB_SESSION, entry):
    session: Session = DB_SESSION()

    session.add(entry)

    session.commit()
    session.close()


def kafka_message(DB_SESSION, consumer, logger: Logger):
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)

        logger.info(f'Message: {msg}')

        payload = msg["payload"]

        if msg["type"] == "gun_stat":
            entry = GunStats(
                payload['trace_id'],
                payload['gun_id'],
                payload['game_id'],
                payload['user_id'],
                payload['num_bullets_shot'],
                payload['num_body_shots'],
                payload['num_head_shots'],
                payload['num_missed_shots']
            )

            session_commit(DB_SESSION, entry)

            log_debug(logger, "create_gun_stat", payload['trace_id'])
        elif msg["type"] == "purchase_history":
            entry = PurchaseHistory(
                payload['trace_id'],
                payload['transaction_id'],
                payload['item_id'],
                payload['user_id'],
                payload['item_price'],
                payload['transaction_date']
            )

            session_commit(DB_SESSION, entry)

            log_debug(logger, "create_gun_stat", payload['trace_id'])
        
        consumer.commit_offsets()
