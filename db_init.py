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


def tbl_user_init():
    """Incluir dados iniciais de teste na tabela de usuarios"""
    con, cur = connection.get()

    users = [
        (1, f"{ADMIN_USR}", f"{ADMIN_PWD}"),
    ]

    cur.execute("DELETE FROM users")

    if connection.DB_TYPE == connection.TYPE_PSQL:
        cur.executemany("INSERT INTO users VALUES (%s,%s,%s)", users)
    else:
        cur.executemany("INSERT INTO users VALUES (?,?,?)", users)

    con.commit()
    con.close()

    print("Usuário inicial incluído na tabela.")


def tables_init():
    """Incluir dados iniciais de teste nas tabelas."""
    import user

    con, cur = connection.get()

    itens = [
        ("Carne", "carnes e peixes", "cadastrado", user.CURRENT_USER_ID),
        ("Sardinha", "enlatados", "cadastrado", user.CURRENT_USER_ID),
        ("Banana", "frutas e verduras", "cadastrado", user.CURRENT_USER_ID),
        ("Queijo", "frios", "cadastrado", user.CURRENT_USER_ID),
        ("Leite", "laticínios", "cadastrado", user.CURRENT_USER_ID),
        ("Açúcar", "produtos básicos", "cadastrado", user.CURRENT_USER_ID),
        ("Ovos", "produtos da granja", "cadastrado", user.CURRENT_USER_ID),
        ("Sabão em pó", "produtos de limpeza", "cadastrado", user.CURRENT_USER_ID),
        ("Suco", "sucos e bebidas", "cadastrado", user.CURRENT_USER_ID),
    ]

    cur.execute(f"DELETE FROM itens WHERE user_id={user.CURRENT_USER_ID}")

    if connection.DB_TYPE == connection.TYPE_PSQL:
        cur.executemany("INSERT INTO itens VALUES (DEFAULT,%s,%s,%s,%s)", itens)

    else:
        cur.executemany("INSERT INTO itens VALUES (NULL,?,?,?,?)", itens)

    con.commit()
    con.close()

    print("Dados iniciais incluídos nas tabelas.")


def db_reset():
    drop_tables()
    tbl_create()
    tbl_user_init()
    tables_init()


if __name__ == "__main__":
    db_reset()
