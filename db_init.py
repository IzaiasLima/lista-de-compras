import os
import uuid

from db import *
from itens import ler_csv

DB_TYPE = os.environ.get("DB_TYPE", TYPE_PSQL)
ADMIN_USR = os.environ.get("ADMIN_USR", "admin@admin.com")
ADMIN_PWD = os.environ.get("ADMIN_PWD", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")

print(f"Script {__name__} executado.")


def drop_tables():
    """Excluir as tabelas"""

    con = DB().con
    cur = DB().cur

    try:
        cur.execute("DROP TABLE itens")
        cur.execute("DROP TABLE users")
    except:
        pass

    con.commit()


def create_tables():
    """Criar as tabelas"""

    con = DB().con
    cur = DB().cur

    PRIMARY_KEY = (
        "id SERIAL PRIMARY KEY"
        if DB_TYPE == TYPE_PSQL
        else "id integer PRIMARY KEY AUTOINCREMENT"
    )

    cur.execute(
        f"""
            CREATE TABLE IF NOT EXISTS itens
            (   {PRIMARY_KEY},
                nome text,
                categoria text,
                status text,
                user_email text
            )
        """
    )

    cur.execute(
        f"""
            CREATE TABLE IF NOT EXISTS users
            (   {PRIMARY_KEY},
                email text,
                passwd text,
                session text
            )
        """
    )

    con.commit()

    print("Tabelas criadas.")


def init_user_table():
    """Incluir dados iniciais de teste na tabela de usuários"""

    con = DB().con
    cur = DB().cur

    users = [
        (f"{ADMIN_USR}", f"{ADMIN_PWD}"),
    ]

    cur.execute("DELETE FROM users")

    if DB_TYPE == TYPE_PSQL:
        cur.executemany("INSERT INTO users VALUES (DEFAULT, %s,%s,DEFAULT)", users)
    else:
        cur.executemany("INSERT INTO users VALUES (NULL,?,?,NULL)", users)

    con.commit()

    print("Usuário inicial incluído na tabela.")


def init_itens_table(user_email):
    """Incluir dados iniciais de teste nas tabelas."""

    con = DB().con
    cur = DB().cur

    itens_iniciais = ler_csv('itens.csv', user_email)

    cur.execute(f"DELETE FROM itens WHERE user_email='{user_email}'")

    if DB_TYPE == TYPE_PSQL:
        cur.executemany("INSERT INTO itens VALUES (DEFAULT,%s,%s,%s,%s)", itens_iniciais)

    else:
        cur.executemany("INSERT INTO itens VALUES (NULL,?,?,?,?)", itens_iniciais)

    con.commit()

    print("Lista de Itens iniciais adicionados à tabela.")


def __db_reset__(user_email):
    drop_tables()
    create_tables()
    init_user_table()
    init_itens_table(user_email)


def get_random_id():
    """Gera um id randômico"""
    return str(uuid.uuid4())


if __name__ == "__main__":
    __db_reset__("admin@admin.com")
