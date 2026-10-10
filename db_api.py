from db import *


con = DB().con
cur = DB().cur


async def get_itens(user_email):
    return await get_dados("itens", user_email)


async def get_iten(id, user_email):
    return await get_dados("itens", user_email, id)


def add_iten(new_iten, user_email):
    add("itens", user_email, new_iten)


def del_iten(id):
    delete("itens", id)


async def get_lista(user_email):
    selecionados = await get_filtrado("itens", user_email, "selecionado")
    comprados = await get_filtrado("itens", user_email, "comprado")
    cadastrados = await get_filtrado("itens", user_email, "cadastrado")

    lista = {"selecionados": selecionados, "comprados": comprados, "cadastrados": cadastrados}

    return lista


async def get_compras(user_email):
    selecionados = await get_filtrado("itens", user_email, "selecionado")
    comprados = await get_filtrado("itens", user_email, "comprado")

    lista = {"selecionados": selecionados, "comprados": comprados}
    return lista


async def get_dados(tbl, user_email, id=None):
    sql = f"SELECT * FROM {tbl}"
    sql += f" WHERE user_email='{user_email}'"
    sql += f" AND id={id}" if id else ""
    sql += " ORDER BY 3,2;"

    try:
        cur.execute(sql)
        rows = cur.fetchall()
        dados = [dict(row) for row in rows]
        return dados
    except:
        cur.close()
        return []


async def get_filtrado(tbl, user_email, filtro=None):
    sql = f"SELECT * FROM {tbl}"
    sql += f" WHERE user_email='{user_email}'"
    sql += f" AND status='{filtro}'" if filtro else ""
    sql += " ORDER BY 3,2;"

    try:
        cur.execute(sql)
        rows = cur.fetchall()
        dados = [dict(row) for row in rows]
        return dados
    except:
        cur.close()
        return []


COLUNAS_ITENS = ("nome", "categoria", "status")


def add(table, user_email, dados: dict):
    """Insere um registro usando apenas as colunas conhecidas da tabela.

    Os valores são passados como parâmetros da query, para que textos
    com aspas (ex.: "Farinha d'água") não quebrem o SQL.
    """
    colunas = [c for c in COLUNAS_ITENS if c in dados]
    if not colunas:
        return

    marcador = "%s" if DB_TYPE == TYPE_PSQL else "?"
    valores = [dados[c] for c in colunas] + [user_email]

    sql = f"INSERT INTO {table} ({', '.join(colunas)}, user_email)"
    sql += f" VALUES ({', '.join([marcador] * len(valores))})"

    cur.execute(sql, valores)
    con.commit()


def patch_status(id, user_email, status):
    sql = f"UPDATE itens SET status='{status}'"
    sql += f" WHERE user_email='{user_email}'"
    sql += f" AND id={id}" if id else ""
    cur.execute(sql)
    con.commit()


def delete(tbl, id):
    sql = f"DELETE FROM {tbl} WHERE id={id}"
    cur.execute(sql)
    con.commit()
