import sqlite3

from helpers.read_config import get_sqlite_config

filename = get_sqlite_config()

connection = sqlite3.connect(filename)

c = connection.cursor()

DROP_TABLE = 'DROP TABLE IF EXISTS anomaly;'

c.execute(DROP_TABLE)

connection.commit()
connection.close()
