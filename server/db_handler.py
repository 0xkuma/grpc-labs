import logging
from psycopg2 import connect, sql
import configparser
import os

environment = os.environ.get('ENVIRONMENT', 'development')
config = configparser.ConfigParser()
config.read('./server/config.ini')
db_name = config[environment]['db_name']
db_user = config[environment]['db_user']
db_password = config[environment]['db_password']
db_host = config[environment]['db_host']
db_port = config[environment]['db_port']


class Database():
    def __init__(self):
        self.conn = connect(f"dbname=%s user=%s password=%s host=%s port=%s" % (
            db_name, db_user, db_password, db_host, db_port))
        self.cur = self.conn.cursor()

    def create_connection(self):
        print("Creating connection")
        self.conn = connect(f"dbname=%s user=%s password=%s host=%s port=%s" % (
            db_name, db_user, db_password, db_host, db_port))
        self.cur = self.conn.cursor()

    def close_connection(self):
        print("Closing connection")
        self.cur.close()
        self.conn.close()

    def rollback(self):
        self.conn.rollback()

    def set_clause(self, keys: list, values: list) -> str:
        identifiers = map(sql.Identifier, keys)
        values = map(sql.Literal, values)
        set_clause = sql.SQL(', ').join(
            sql.SQL("{} = {}").format(k, v) for k, v in zip(identifiers, values))
        return set_clause

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
