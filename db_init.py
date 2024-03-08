# Criar a estrutura inicial do banco de dados em SQLite3.

import sqlite3


print(f"Script {__name__} executado.")


def tbl_create():
    """Criar as tabelas"""

    con = sqlite3.connect("compras.db")
    cur = con.cursor()

    try:
        cur.execute("DROP TABLE itens")
    except:
        pass

    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS itens
            (   id integer PRIMARY KEY AUTOINCREMENT,
                nome text,
                categoria text,
                status text
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
        (None, "Banana", "hortifrutigranjeiros", "cadastrado"),
        (None, "Ovos", "hortifrutigranjeiros", "selecionado"),
        (None, "Leite", "laticínios", "comprado"),
        (None, "Carne", "carnes e peixes", "comprado"),
        (None, "Iogurte", "laticínios", "comprado"),
        (None, "Queijo", "frios", "comprado"),
        (None, "Suco", "sucos e bebidas", "comprado"),
        (None, "Amaciante", "produtos de limpeza", "comprado"),
        (None, "Açúcar mascavo", "produtos básicos", "comprado"),
        (None, "Laranja", "hortifrutigranjeiros", "selecionado"),
        (None, "Sabão em pó", "produtos de limpeza", "selecionado"),
    ]

    cur.execute("DELETE FROM itens")

    cur.executemany("INSERT INTO itens VALUES (?,?,?,?)", itens)

    con.commit()
    con.close()

    print("Dados iniciais incluídos nas tabelas.")


if __name__ == "__main__":
    tbl_create()
    tables_init()
