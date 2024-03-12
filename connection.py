import sqlite3
import os

import psycopg2
import psycopg2.extras


TYPE_SQLITE = "sqlite"
TYPE_MYSQL = "msql"
TYPE_PSQL = "psql"

DB_TYPE = TYPE_PSQL


DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgres://postgres:postgres@192.168.1.12/postgres"
)


def get():
    ## FIX: Resolver com Strategy, futuramente
    if DB_TYPE == TYPE_PSQL:
        con = psycopg2.connect(DATABASE_URL)
        cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return con, cur

    elif DB_TYPE == TYPE_SQLITE:
        con = sqlite3.connect("compras.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        return con, cur

    elif DB_TYPE == TYPE_MYSQL:
        raise NotImplementedError("Conexão com o MySql não implementada.")

    else:
        raise NotImplementedError("Tipo de conexão não implementada.")
