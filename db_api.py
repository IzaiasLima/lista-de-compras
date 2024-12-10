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
    cadastrados = await get_filtrado("itens", user_email, "cadastrado")

    lista = {"selecionados": selecionados, "cadastrados": cadastrados}

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
    cur.execute(sql)
    rows = cur.fetchall()
    dados = [dict(row) for row in rows]
    return dados


async def get_filtrado(tbl, user_email, filtro=None):
    sql = f"SELECT * FROM {tbl}"
    sql += f" WHERE user_email='{user_email}'"
    sql += f" AND status='{filtro}'" if filtro else ""
    sql += " ORDER BY 3,2;"
    cur.execute(sql)
    rows = cur.fetchall()
    dados = [dict(row) for row in rows]
    return dados


def add(table, user_email, dados: dict):
    if dados:
        values = [f"'{v}'" for _, v in dados.items()]
        all_values = ",".join(values)

        sql = f"INSERT INTO {table}"

        if DB_TYPE == TYPE_PSQL:
            sql += f" VALUES (DEFAULT, {all_values}, '{user_email}')"
        else:
            sql += f" VALUES (NULL, {all_values}, '{user_email}')"

        cur.execute(sql)
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
