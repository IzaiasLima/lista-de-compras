from db import *


con = DB().con
cur = DB().cur


async def get_itens(user_email):
    return await get_dados("itens", user_email)


async def get_iten(id, user_email):
    return await get_dados("itens", user_email, id)


def add_iten(new_iten, user_email):
    add("itens", user_email, new_iten)


def del_iten(id, user_email):
    delete("itens", id, user_email)


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
    sql = f"SELECT * FROM {tbl} WHERE user_email={placeholders(1)}"
    valores = [user_email]

    if id is not None:
        sql += f" AND id={placeholders(1)}"
        valores.append(id)

    sql += " ORDER BY 3,2;"

    try:
        cur.execute(sql, valores)
        rows = cur.fetchall()
        dados = [dict(row) for row in rows]
        return dados
    except Exception:
        cur.close()
        return []


async def get_filtrado(tbl, user_email, filtro=None):
    sql = f"SELECT * FROM {tbl} WHERE user_email={placeholders(1)}"
    valores = [user_email]

    if filtro:
        sql += f" AND status={placeholders(1)}"
        valores.append(filtro)

    sql += " ORDER BY 3,2;"

    try:
        cur.execute(sql, valores)
        rows = cur.fetchall()
        dados = [dict(row) for row in rows]
        return dados
    except Exception:
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
    sql = f"UPDATE itens SET status={placeholders(1)} WHERE user_email={placeholders(1)}"
    valores = [status, user_email]

    if id is not None:
        sql += f" AND id={placeholders(1)}"
        valores.append(id)

    cur.execute(sql, valores)
    con.commit()


def delete(tbl, id, user_email):
    """Exclui apenas itens do próprio usuário — id de terceiros é ignorado."""
    sql = f"DELETE FROM {tbl} WHERE id={placeholders(1)} AND user_email={placeholders(1)}"
    cur.execute(sql, (id, user_email))
    con.commit()
