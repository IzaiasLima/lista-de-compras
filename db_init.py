import os
import uuid

from db import *


ADMIN_USR = os.environ.get("ADMIN_USR", "admin@admin.com")
ADMIN_PWD = os.environ.get("ADMIN_PWD", "admin")

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


def tbl_create():
    """Criar as tabelas"""

    con = DB().con
    cur = DB().cur

    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS itens
            (   id SERIAL NOT NULL PRIMARY KEY,
                nome text,
                categoria text,
                status text,
                user_id integer
                user_email text
            )
        """
    )

    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS users
            (   id SERIAL NOT NULL PRIMARY KEY,
                email text,
                passwd text
            )
        """
    )

    con.commit()

    print("Tabelas criadas.")


def tbl_user_init():
    """Incluir dados iniciais de teste na tabela de usuários"""

    con = DB().con
    cur = DB().cur

    users = [
        (1, f"{ADMIN_USR}", f"{ADMIN_PWD}"),
    ]

    cur.execute("DELETE FROM users")

    if DB_TYPE == TYPE_PSQL:
        cur.executemany("INSERT INTO users VALUES (%s,%s,%s)", users)
    else:
        cur.executemany("INSERT INTO users VALUES (?,?,?)", users)

    con.commit()

    print("Usuário inicial incluído na tabela.")


def tables_init(user_email):
    """Incluir dados iniciais de teste nas tabelas."""

    con = DB().con
    cur = DB().cur

    itens = [
        ("Carne", "carnes e peixes", "cadastrado", user_email),
        ("Sardinha", "enlatados", "cadastrado", user_email),
        ("Banana", "frutas e verduras", "cadastrado", user_email),
        ("Queijo", "frios", "cadastrado", user_email),
        ("Leite", "laticínios", "cadastrado", user_email),
        ("Açúcar", "produtos básicos", "cadastrado", user_email),
        ("Ovos", "produtos da granja", "cadastrado", user_email),
        ("Sabão em pó", "produtos de limpeza", "cadastrado", user_email),
        ("Suco", "sucos e bebidas", "cadastrado", user_email),
    ]

    cur.execute(f"DELETE FROM itens WHERE user_email='{user_email}'")

    if DB_TYPE == TYPE_PSQL:
        cur.executemany("INSERT INTO itens VALUES (DEFAULT,%s,%s,%s,%s)", itens)

    else:
        cur.executemany("INSERT INTO itens VALUES (NULL,?,?,?,?)", itens)

    con.commit()

    print("Dados iniciais incluídos nas tabelas.")


def __db_reset__(user_email):
    drop_tables()
    tbl_create()
    tbl_user_init()
    tables_init(user_email)


def get_random_id():
    """Gera um id randômico"""
    return str(uuid.uuid4())


if __name__ == "__main__":
    __db_reset__("admin@admin.com")
