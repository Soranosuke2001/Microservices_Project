import json

from logging import Logger
from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from anomaly import Anomaly

from helpers.read_config import get_sqlite_config, get_threshold_config

filename = get_sqlite_config()
max_bullets, min_item_price = get_threshold_config()


def check_gun_stat_event(payload, logger: Logger, session: Session):
    bullet_count = payload['num_bullets_shot']

    if bullet_count > max_bullets:
        event_id = payload['gun_id']
        anomaly_value = bullet_count
        trace_id = payload['trace_id']
        event_type = 'gun_stat'
        anomaly_type = 'Exceeded max bullet count'
        description = f'The number of bullets shot, {anomaly_value}, exceeds the threshold value of {max_bullets}'

        logger.info(f"Anomaly detected in Gun Stats event: {description}")
        entry = Anomaly(
            event_id,
            trace_id,
            event_type,
            anomaly_type,
            description
        )

        session.add(entry)
        session.commit()


def check_purchase_history(payload, logger: Logger, session: Session):
    item_price = payload['item_price']

    if item_price < min_item_price:
        event_id = payload['transaction_id']
        anomaly_value = item_price
        trace_id = payload['trace_id']
        event_type = 'purchase_history'
        anomaly_type = 'Below minimum price'
        description = f'The item with the price of ${anomaly_value}, does not meet the minimum item price of ${min_item_price}'

        logger.info(f"Anomaly detected in Purchase History event: {description}")

        entry = Anomaly(
            event_id,
            trace_id,
            event_type,
            anomaly_type,
            description
        )

        session.add(entry)
        session.commit()


def read_kafka(consumer, logger: Logger, DB_SESSION):
    session: Session = DB_SESSION()

    logger.info(f"Checking anomalies: Gun Stats: {max_bullets} | Purchase History: {min_item_price}")

    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)

        logger.info(f"Checking for anomalies in the event: {msg['payload']}")

        if msg['type'] == 'gun_stat':
            check_gun_stat_event(msg['payload'], logger, session)
        elif msg['type']=='purchase_history':
            check_purchase_history(msg['payload'], logger, session)
        else:
            logger.error(f"Unable to process the following message: {msg}")
    
    consumer.commit_offsets()
    session.close()


def fetch_anomalies(anomaly_type, DB_SESSION):
    session: Session = DB_SESSION()
    return_list = []

    results = session.query(Anomaly).filter(Anomaly.anomaly_type == anomaly_type).order_by(desc(Anomaly.date_created)).all()

    print(f'type: {anomaly_type}')
    print(results)

    for result in results:
        entry = result.to_dict()
        return_list.append(entry)

    session.close()

    return return_list
    