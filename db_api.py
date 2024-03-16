from db import *


con = DB().con
cur = DB().cur


def get_itens(user_email):
    return get_dados("itens", user_email)


def get_item(id, user_email):
    return get_dados("itens", user_email, id)


def add_item(new_item, user_email):
    add("itens", user_email, new_item)


def del_item(id):
    delete("itens", id)


def get_lista(user_email):
    selecionados = get_filtrado("itens", user_email, "selecionado")
    cadastrados = get_filtrado("itens", user_email, "cadastrado")

    lista = {"selecionados": selecionados, "cadastrados": cadastrados}

    return lista


def get_compras(user_email):
    selecionados = get_filtrado("itens", user_email, "selecionado")
    comprados = get_filtrado("itens", user_email, "comprado")

    lista = {"selecionados": selecionados, "comprados": comprados}

    return lista


def get_dados(tbl, user_email, id=None):
    sql = f"SELECT * FROM {tbl}"
    # sql += f" WHERE user_id={user.CURRENT_USER_ID}"
    sql += f" WHERE user_email='{user_email}'"
    sql += f" AND id={id}" if id else ""
    sql += " ORDER BY 3,2;"
    cur.execute(sql)
    rows = cur.fetchall()
    dados = [dict(row) for row in rows]
    return dados


def get_filtrado(tbl, user_email, filtro=None):
    sql = f"SELECT * FROM {tbl}"
    # sql += f" WHERE user_id={user.CURRENT_USER_ID}"
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
    # sql += f" WHERE user_id={user.CURRENT_USER_ID}"
    sql += f" WHERE user_email='{user_email}'"
    sql += f" AND id={id}" if id else ""
    cur.execute(sql)
    con.commit()


def delete(tbl, id):
    sql = f"DELETE FROM {tbl} WHERE id={id}"
    cur.execute(sql)
    con.commit()
