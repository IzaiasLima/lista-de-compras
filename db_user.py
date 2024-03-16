from db import *


con = DB().con
cur = DB().cur


async def add(email, pwd):
    sql = "INSERT INTO users"

    if DB.DB_TYPE == DB.TYPE_PSQL:
        sql += f" VALUES (DEFAULT, '{email}', '{pwd}')"
    else:
        sql += f" VALUES (NULL, '{email}', '{pwd}')"

    cur.execute(sql)
    con.commit()


def is_valid_pwd(email, pwd):
    sql = f"SELECT * FROM users WHERE email = '{email}' AND passwd = '{pwd}'"
    cur.execute(sql)
    user = cur.fetchone()
    return True if user else False
