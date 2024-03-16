## Borg singleton pattern connection class
import os
import sqlite3
import psycopg2
from psycopg2.extras import DictCursor

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)


TYPE_SQLITE = "sqlite"
TYPE_MYSQL = "msql"
TYPE_PSQL = "psql"

DB_TYPE = TYPE_PSQL


DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgres://postgres:postgres@192.168.1.12/postgres"
)


class DB(object):
    __state = {}

    def __init__(self):
        self.__dict__ = self.__state

        if not hasattr(self, "con"):
            if DB_TYPE == TYPE_PSQL:
                self.con = psycopg2.connect(DATABASE_URL)
                self.cur = self.con.cursor(cursor_factory=DictCursor)

            elif DB_TYPE == TYPE_SQLITE:
                self.con = sqlite3.connect("compras.db")
                self.con.row_factory = sqlite3.Row
                self.cur = self.con.cursor()

            elif DB_TYPE == TYPE_MYSQL:
                raise NotImplementedError("Conexão com o MySql não implementada.")

            else:
                raise NotImplementedError("Tipo de conexão não implementada.")


if __name__ == "__main__":
    db = DB()
    db.cur.execute("select 1=1")
    print(f"Conexão efetuada: {db.cur.fetchone()}")
