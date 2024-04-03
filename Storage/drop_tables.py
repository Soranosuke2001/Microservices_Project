import mysql.connector
from helpers.read_config import database_config

user, password, hostname, port, db = database_config()

connection = mysql.connector.connect(host=hostname, user=user, password=password, database=db)

c = connection.cursor()

DROP_TABLE = "DROP TABLE IF EXISTS gun_stats, purchase_history"

c.execute(DROP_TABLE)

connection.commit()
connection.close()
