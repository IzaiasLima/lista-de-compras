import os
import re
import sqlite3
import psycopg2 as psql
from psycopg2.extras import DictCursor

from dotenv import load_dotenv

load_dotenv()


TYPE_SQLITE = "sqlite"
TYPE_MYSQL = "msql"
TYPE_PSQL = "psql"

LOCAL_DB_URL = "postgres://postgres:postgres@127.0.0.1/postgres"

DB_TYPE = os.environ.get("DB_TYPE", TYPE_PSQL)
DATABASE_URL = os.environ.get("DATABASE_URL", LOCAL_DB_URL)


def placeholders(n: int) -> str:
    """Marcadores de parâmetros do driver ativo: %s (PostgreSQL) ou ? (SQLite).

    Valores vindos do usuário entram sempre por aqui e viajam separados em
    `cur.execute(sql, valores)`; a query nunca é montada com f-string,
    é isso que impede injeção de SQL.
    """
    return ", ".join(["%s" if DB_TYPE == TYPE_PSQL else "?"] * n)


## Borg singleton pattern connection class
class DB(object):
    __state = {}

    def __init__(self):
        self.__dict__ = self.__state

        if not hasattr(self, "con"):
            if DB_TYPE == TYPE_PSQL:
                self.con = psql.connect(DATABASE_URL)
                self.cur = self.con.cursor(cursor_factory=DictCursor)

            elif DB_TYPE == TYPE_SQLITE:
                self.con = sqlite3.connect(DATABASE_URL)
                self.con.row_factory = sqlite3.Row
                self.cur = self.con.cursor()

            elif DB_TYPE == TYPE_MYSQL:
                raise NotImplementedError("Conexão com o MySql não implementada.")

            else:
                raise NotImplementedError("Tipo de conexão não implementada.")

            # nunca imprimir o URL completo: ele pode conter usuário e senha
            url_segura = re.sub(r"://[^@/]+@", "://***@", DATABASE_URL)
            print(f"Sistema conectado à base de dados: {url_segura} ({DB_TYPE}).")


if __name__ == "__main__":
    db = DB()
    db.cur.execute("select 1=1")
    print(f"Conexão efetuada: {db.cur.fetchone()}")
