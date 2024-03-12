import connection
import user


con, cur = connection.get()


def get_itens():
    return get_dados("itens")


def get_item(id):
    return get_dados("itens", id)


def add_item(new_item):
    add("itens", new_item)


def del_item(id):
    delete("itens", id)


def get_lista():
    selecionados = get_filtrado("itens", "selecionado")
    cadastrados = get_filtrado("itens", "cadastrado")

    lista = {"selecionados": selecionados, "cadastrados": cadastrados}

    return lista


def get_compras():
    selecionados = get_filtrado("itens", "selecionado")
    comprados = get_filtrado("itens", "comprado")

    lista = {"selecionados": selecionados, "comprados": comprados}

    return lista


def get_dados(tbl, id=None):
    sql = f"SELECT * FROM {tbl}"
    sql += f" WHERE user_id={user.CURRENT_USER_ID}"
    sql += f" AND id={id}" if id else ""
    sql += " ORDER BY 3,2;"
    cur.execute(sql)
    rows = cur.fetchall()
    dados = [dict(row) for row in rows]
    return dados


def get_filtrado(tbl, filtro=None):
    sql = f"SELECT * FROM {tbl}"
    sql += f" WHERE user_id={user.CURRENT_USER_ID}"
    sql += f" AND status='{filtro}'" if filtro else ""
    sql += " ORDER BY 3,2;"
    cur.execute(sql)
    rows = cur.fetchall()
    dados = [dict(row) for row in rows]
    return dados


def add(table, dados: dict):
    import user

    if dados:
        values = [f"'{v}'" for _, v in dados.items()]
        all_values = ",".join(values)

        sql = f"INSERT INTO {table}"

        if connection.DB_TYPE == connection.TYPE_PSQL:
            sql += f" VALUES (DEFAULT, {all_values}, {user.CURRENT_USER_ID})"
        else:
            sql += f" VALUES (NULL, {all_values}, {user.CURRENT_USER_ID})"

        cur.execute(sql)
        con.commit()


def patch_status(id, status):
    sql = f"UPDATE itens SET status='{status}'"
    sql += f" WHERE user_id={user.CURRENT_USER_ID}"
    sql += f" AND id={id}" if id else ""
    cur.execute(sql)
    con.commit()


def delete(tbl, id):
    sql = f"DELETE FROM {tbl} WHERE id={id}"
    cur.execute(sql)
    con.commit()
