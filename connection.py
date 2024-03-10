import sqlite3

import psycopg2
import psycopg2.extras


TYPE_PSQL = "psql"
TYPE_SQLITE = "sqlite"
TYPE_MYSQL = "msql"

DB_TYPE = TYPE_SQLITE  # TYPE_PSQL


def get():
    ## FIX: Resolver com Strategy, futuramente
    if DB_TYPE == TYPE_PSQL:
        con = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="postgres",
            host="192.168.1.12",
            port="5432",
        )
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


# PGPASSWORD=C8wp31muRvgrYqWh52KCmYsNQ60cztr7 psql -h dpg-cnkul1021fec73d67vk0-a.oregon-postgres.render.com -U izaiaslima clinica_medica_db
# postgres://izaiaslima:C8wp31muRvgrYqWh52KCmYsNQ60cztr7@dpg-cnkul1021fec73d67vk0-a/clinica_medica_db
# postgres://izaiaslima:C8wp31muRvgrYqWh52KCmYsNQ60cztr7@dpg-cnkul1021fec73d67vk0-a.oregon-postgres.render.com/clinica_medica_db
