import hashlib
from db import *


con = DB().con
cur = DB().cur


async def add(email, pwd):
    sql = "INSERT INTO users"

    pwd_crypto = hashlib.sha256(pwd.encode("utf-8")).hexdigest()

    if DB_TYPE == TYPE_PSQL:
        sql += f" VALUES (DEFAULT, '{email}', '{pwd_crypto}')"
    else:
        sql += f" VALUES (NULL, '{email}', '{pwd_crypto}')"

    cur.execute(sql)
    con.commit()


def is_valid_pwd(email, pwd):
    pwd_crypto = hashlib.sha256(pwd.encode("utf-8")).hexdigest()

    sql = f"SELECT * FROM users WHERE email = '{email}' AND passwd = '{pwd_crypto}'"
    cur.execute(sql)
    user = cur.fetchone()
    return True if user else False


def exists(email: str):
    user = None

    if len(email.strip()) > 0:
        sql = f"SELECT * FROM users WHERE email = '{email}'"
        cur.execute(sql)
        user = cur.fetchone()

    return True if user else False
