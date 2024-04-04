import sqlite3

from helpers.read_config import get_sqlite_config

filename = get_sqlite_config('app')

connection = sqlite3.connect(filename)

c = connection.cursor()

CREATE_TABLE = '''
                CREATE TABLE IF NOT EXISTS stats
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    num_gun_stat_events INTEGER NOT NULL,
                    head_shot_count INTEGER NOT NULL,
                    bullet_shot_count INTEGER NOT NULL,
                    num_purchase_history_events INTEGER NOT NULL,
                    total_revenue INTEGER NOT NULL,
                    last_updated DATETIME NOT NULL
                )
                '''

c.execute(CREATE_TABLE)

connection.commit()
connection.close()
