import connexion
from connexion.middleware import MiddlewarePosition
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import Base
from event_logs import EventLogs

from helpers.read_config import get_sqlite_config, read_log_config

filename, seconds, url = get_sqlite_config()    
logger = read_log_config()

DB_ENGINE = create_engine("sqlite:///%s" %filename)
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def fetch_event_stats():
    logger.info("Starting ")
    return "", 200
    

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_middleware(CORSMiddleware, position=MiddlewarePosition.BEFORE_EXCEPTION, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_api("./config/openapi.yml", strict_validation=True, validate_response=True)

if __name__ == "__main__":
    # time.sleep(20)
    
    # init_scheduler()
    app.run(host="0.0.0.0", port=8120)


