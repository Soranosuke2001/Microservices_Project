import sqlite3

from helpers.read_config import get_sqlite_config

filename = get_sqlite_config('connection')

connection = sqlite3.connect(filename)

c = connection.cursor()

DROP_TABLE = 'DROP TABLE IF EXISTS stats'

c.execute(DROP_TABLE)

connection.commit()
connection.close()
