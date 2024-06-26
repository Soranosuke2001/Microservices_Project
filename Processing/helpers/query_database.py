from datetime import datetime
from sqlalchemy import func, desc
from sqlalchemy.orm import Session
import requests, time

from tables.gun_stats import GunStats
from tables.purchase_history import PurchaseHistory

from helpers.read_config import get_sqlite_config, get_kafka_threshold, read_request_config, read_log_config
from helpers.log_message import success_response, error_response, log_events
from helpers.kafka_message import kafka_max_count
from helpers.test_connection import mysql_connection

url = get_sqlite_config('query')
kafka_threshold = int(get_kafka_threshold())
request_timeout = read_request_config()
logger = read_log_config()

time.sleep(10)

DB_SESSION = mysql_connection(logger)


def check_prev_data():
    session = DB_SESSION()

    default_stats = {
        "num_gun_stat_events": 0,
        "head_shot_count": 0,
        "bullet_shot_count": 0,
        "num_purchase_history_events": 0,
        "total_revenue": 0,
    }
    
    gs_results = session.query(GunStats).all()
    ph_results = session.query(PurchaseHistory).all()

    session.close()
    
    if len(gs_results) > 0:
        default_stats['num_gun_stat_events'] = len(gs_results)
        default_stats['head_shot_count'] = count_sum_class(0, gs_results, "num_head_shots")
        default_stats['bullet_shot_count'] = count_sum_class(0, gs_results, "num_bullets_shot")    

    if len(ph_results) > 0:
        default_stats['num_purchase_history_events'] = len(ph_results)
        default_stats['total_revenue'] = count_sum_class(0, ph_results, "item_price")

    default_stats['last_updated'] = datetime.now()

    return default_stats


def row_counter(session: Session, table):
    result = session.query(func.count(table.id)).scalar()

    if result == 0:
        return None
    else:
        result = session.query(table).order_by(desc(table.last_updated)).first()
        return result.to_dict()


def fetch_recent(session: Session, table):
    result = session.query(table).order_by(desc(table.last_updated)).first()

    return result.to_dict()


def check_db(session: Session, table):
    result = session.query(func.count(table.id)).scalar()

    if result == 0:
        return check_prev_data()
    else:
        return fetch_recent(session, table)
    

def count_sum_class(count, events: list[GunStats | PurchaseHistory], property):
    for event in events:
        event = event.to_dict()
        count += event[property]
    
    return count


def count_sum(count, events, property):
    for event in events:
        count += event[property]

    return count


def update_last_updated(gs_events, ph_events, stats_last_updated):
    if len(gs_events) > 0 and len(ph_events) > 0:
        gs_last_updated = datetime.strptime(gs_events[-1]['date_created'], '%Y-%m-%dT%H:%M:%S.%fZ')
        ph_last_updated = datetime.strptime(ph_events[-1]['date_created'], '%Y-%m-%dT%H:%M:%S.%fZ')

        if gs_last_updated > ph_last_updated:
            last_updated = gs_last_updated
        else:
            last_updated = ph_last_updated
        
        return last_updated
    elif len(gs_events) > 0 and len(ph_events) == 0:
        last_updated = datetime.strptime(gs_events[-1]['date_created'], '%Y-%m-%dT%H:%M:%S.%fZ')

        return last_updated
    elif len(gs_events) == 0 and len(ph_events) > 0:
        last_updated = datetime.strptime(ph_events[-1]['date_created'], '%Y-%m-%dT%H:%M:%S.%fZ')

        return last_updated
    
    return stats_last_updated
    

def update_stats(producer, stats_data, gs_events, ph_events, new_event):
    total_messages = len(gs_events) + len(ph_events)

    if total_messages > kafka_threshold:
        kafka_max_count(producer, kafka_threshold)

    if len(ph_events) > 0:
        num_ph = stats_data['num_purchase_history_events'] + len(ph_events)
        total_revenue = count_sum(stats_data['total_revenue'], ph_events, "item_price")
    else:
        num_ph = stats_data['num_purchase_history_events']
        total_revenue = stats_data['total_revenue']

    if len(gs_events) > 0:
        num_gs = stats_data['num_gun_stat_events'] + len(gs_events)
        hs_count = count_sum(stats_data['head_shot_count'], gs_events, "num_head_shots")
        bs_count = count_sum(stats_data['bullet_shot_count'], gs_events, "num_bullets_shot")
    else:
        num_gs = stats_data['num_gun_stat_events']
        hs_count = stats_data['head_shot_count']
        bs_count = stats_data['bullet_shot_count']
    
    last_updated = update_last_updated(gs_events, ph_events, stats_data['last_updated'])

    return {
        "num_gun_stat_events": num_gs,
        "head_shot_count": hs_count,
        "bullet_shot_count": bs_count,
        "num_purchase_history_events": num_ph,
        "total_revenue": total_revenue,
        "last_updated": last_updated,
        "new_event": new_event
    }


def update_storage(logger, stats_data, producer):
    error = False

    params = {
        "start_timestamp": stats_data['last_updated'].strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        "end_timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    }

    logger.critical(f"Printing the params: {params}")

    gs_res = requests.get(f"{url}/get/gun_stats", params=params, timeout=request_timeout)
    ph_res = requests.get(f"{url}/get/purchase_transactions", params=params, timeout=request_timeout)

    if gs_res.status_code != 201:
        error_response(logger, "gs")
        error = True
    
    if ph_res.status_code != 201:
        error_response(logger, "ph")
        error = True

    if error:
        return "error"
    
    gs_events = gs_res.json()
    ph_events = ph_res.json()

    new_event = success_response(logger, len(gs_events), len(ph_events))

    log_events(logger, gs_events, ph_events)

    return update_stats(producer, stats_data, gs_events, ph_events, new_event)
