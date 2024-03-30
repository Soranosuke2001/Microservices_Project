import json

from logging import Logger
from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from base import Base
from event_logs import EventLogs

from helpers.read_config import get_sqlite_config

filename, seconds, url = get_sqlite_config()

def check_prev_data(DB_SESSION):
    session: Session = DB_SESSION()

    results = session.query(EventLogs).order_by(desc(EventLogs.date_created)).first()

    session.close()
    
    if results:
        return results.to_dict()

    return {
        'id': 'default',
        'message': "There was no data found, creating default values.",
        'message_code': 'Default Values',
        '0001': 0,
        '0002': 0,
        '0003': 0,
        '0004': 0
    }


def insert_default(DB_SESSION, data):
    session: Session = DB_SESSION()

    entry = EventLogs(
        data['message'],
        data['message_code'],
        data['0001'],
        data['0002'],
        data['0003'],
        data['0004']
    )

    session.add(entry)
    session.commit()

    session.close()

    return check_prev_data(DB_SESSION)


def update_db(prev_data, consumer, logger: Logger, DB_SESSION):
    if prev_data['id'] == 'default':
        prev_data = insert_default(DB_SESSION, prev_data)

    session: Session = DB_SESSION()

    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)

        logger.info(f'Message: {msg}')

        payload = msg['payload']
        code_received = msg['message_code']

        prev_data[code_received] += 1

        entry = EventLogs(
            payload['message'],
            payload['message_code'],
            prev_data['0001'],
            prev_data['0002'],
            prev_data['0003'],
            prev_data['0004'],
        )

        session.add(entry)
        session.commit()

        logger.debug(f"Added event log {code_received} with an ID of {entry.id} - {entry.date_created}")
        consumer.commit_offsets()
    
    session.close()
