# Criar a estrutura inicial do banco de dados em SQLite3.

import sqlite3


print(f"Script {__name__} executado.")


def tbl_create():
    """Criar as tabelas"""

    con = sqlite3.connect("compras.db")
    cur = con.cursor()

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

    con = sqlite3.connect("compras.db")
    cur = con.cursor()

    itens = [
        (None, "Banana", "hortifrutigranjeiros", "cadastrado", 1),
        (None, "Ovos", "hortifrutigranjeiros", "selecionado", 1),
        (None, "Leite", "laticínios", "comprado", 1),
        (None, "Carne", "carnes e peixes", "comprado", 1),
        (None, "Iogurte", "laticínios", "comprado", 1),
        (None, "Queijo", "frios", "comprado", 1),
        (None, "Suco", "sucos e bebidas", "comprado", 1),
        (None, "Amaciante", "produtos de limpeza", "comprado", 1),
        (None, "Açúcar mascavo", "produtos básicos", "comprado", 1),
        (None, "Laranja", "hortifrutigranjeiros", "selecionado", 1),
        (None, "Sabão em pó", "produtos de limpeza", "selecionado", 1),
    ]

    users = [
        (None, "admin@admin.com", "admin"),
    ]

    cur.execute("DELETE FROM itens")
    cur.execute("DELETE FROM users")

    cur.executemany("INSERT INTO itens VALUES (?,?,?,?,?)", itens)
    cur.executemany("INSERT INTO users VALUES (?,?,?)", users)

    con.commit()
    con.close()

    print("Dados iniciais incluídos nas tabelas.")


if __name__ == "__main__":
    tbl_create()
    tables_init()
