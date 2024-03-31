import sqlite3

from helpers.read_config import get_sqlite_config

filename, seconds, url = get_sqlite_config()

connection = sqlite3.connect(filename)

c = connection.cursor()

create_table1 = '''
                CREATE TABLE IF NOT EXISTS event_logs
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message TEXT NOT NULL,
                    message_code TEXT NOT NULL,
                    code_0001 INTEGER NOT NULL,
                    code_0002 INTEGER NOT NULL,
                    code_0003 INTEGER NOT NULL,
                    code_0004 INTEGER NOT NULL,
                    date_created DATETIME NOT NULL
                )
                '''

c.execute(create_table1)

connection.commit()
connection.close()

