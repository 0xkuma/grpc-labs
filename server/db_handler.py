import logging
from psycopg2 import connect

db_name = "Users"
user = "admin"
password = "admin"
host = "localhost"
port = "5432"


class Database():
    def __init__(self):
        self.conn = connect(f"dbname=%s user=%s password=%s host=%s port=%s" % (
            db_name, user, password, host, port))
        self.cur = self.conn.cursor()

    def close_connection(self):
        self.cur.close()
        self.conn.close()

    def execute(self, query: str, params: tuple = None):
        try:
            if params:
                self.cur.execute(query, params)
            else:
                self.cur.execute(query)
            self.conn.commit()
            return self.cur.fetchall()
        except Exception as e:
            logging.error(e)
            return None
