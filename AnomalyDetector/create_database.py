import sqlite3

from helpers.read_config import get_sqlite_config

filename = get_sqlite_config()

connection = sqlite3.connect(filename)

c = connection.cursor()

CREATE_TABLE = '''
                CREATE TABLE IF NOT EXISTS anomaly
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id VARCHAR(250) NOT NULL,
                    trace_id VARCHAR(250) NOT NULL,
                    event_type VARCHAR(100) NOT NULL,
                    anomaly_type VARCHAR(100) NOT NULL,
                    description VARCHAR(250) NOT NULL,
                    date_created DATETIME NOT NULL
                )
                '''

c.execute(CREATE_TABLE)

connection.commit()
connection.close()
