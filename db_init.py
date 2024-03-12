# Criar a estrutura inicial do banco de dados em SQLite3.

import os
import connection

ADMIN_USR = os.environ.get("ADMIN_USR", "admin@admin.com")
ADMIN_PWD = os.environ.get("ADMIN_PWD", "admin")

print(f"Script {__name__} executado.")


def drop_tables():
    """Excluir as tabelas"""

    con, cur = connection.get()

    try:
        cur.execute("DROP TABLE itens")
        cur.execute("DROP TABLE users")
    except:
        pass

    con.commit()
    con.close()


def tbl_create():
    """Criar as tabelas"""

    con, cur = connection.get()

    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS itens
            (   id SERIAL NOT NULL PRIMARY KEY,
                nome text,
                categoria text,
                status text,
                user_id integer
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
    con.close()

    print("Tabelas criadas.")


def tables_init():
    """Incluir dados iniciais de teste nas tabelas."""

    con, cur = connection.get()

    itens = [
        ("Carne", "carnes e peixes", "cadastrado", 1),
        ("Sardinha", "enlatados", "cadastrado", 1),
        ("Banana", "frutas e verduras", "cadastrado", 1),
        ("Queijo", "frios", "cadastrado", 1),
        ("Leite", "laticínios", "cadastrado", 1),
        ("Açúcar", "produtos básicos", "cadastrado", 1),
        ("Ovos", "produtos da granja", "cadastrado", 1),
        ("Sabão em pó", "produtos de limpeza", "cadastrado", 1),
        ("Suco", "sucos e bebidas", "cadastrado", 1),
    ]

    users = [
        (1, f"{ADMIN_USR}", f"{ADMIN_PWD}"),
    ]

    cur.execute("DELETE FROM itens")
    cur.execute("DELETE FROM users")

    if connection.DB_TYPE == connection.TYPE_PSQL:
        cur.executemany("INSERT INTO itens VALUES (DEFAULT,%s,%s,%s,%s)", itens)
        cur.executemany("INSERT INTO users VALUES (%s,%s,%s)", users)
    else:
        cur.executemany("INSERT INTO itens VALUES (NULL,?,?,?,?)", itens)
        cur.executemany("INSERT INTO users VALUES (?,?,?)", users)

    con.commit()
    con.close()

    print("Dados iniciais incluídos nas tabelas.")


def db_reset():
    drop_tables()
    tbl_create()
    tables_init()


if __name__ == "__main__":
    db_reset()
