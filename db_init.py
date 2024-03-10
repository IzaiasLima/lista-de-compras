# Criar a estrutura inicial do banco de dados em SQLite3.

# import sqlite3
import connection


print(f"Script {__name__} executado.")


def tbl_create():
    """Criar as tabelas"""

    # con = sqlite3.connect("compras.db")
    # cur = con.cursor()
    con, cur = connection.get()

    try:
        cur.execute("DROP TABLE itens")
        cur.execute("DROP TABLE users")
    except:
        pass

    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS itens
            (   id integer PRIMARY KEY AUTOINCREMENT,
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
            (   id integer PRIMARY KEY AUTOINCREMENT,
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

    # con = sqlite3.connect("compras.db")
    # cur = con.cursor()
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
        (1, "admin@admin.com", "admin"),
    ]

    cur.execute("DELETE FROM itens")
    cur.execute("DELETE FROM users")

    if connection.DB_TYPE == "psql":
        cur.executemany("INSERT INTO itens VALUES (DEFAULT,%S,%S,%S,%S)", itens)
        cur.executemany("INSERT INTO users VALUES (%S,%S,%S)", users)
    else:
        cur.executemany("INSERT INTO itens VALUES (NULL,?,?,?,?)", itens)
        cur.executemany("INSERT INTO users VALUES (?,?,?)", users)

    con.commit()
    con.close()

    print("Dados iniciais incluídos nas tabelas.")


if __name__ == "__main__":
    tbl_create()
    tables_init()
