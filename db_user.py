import hashlib
from db import *


con = DB().con
cur = DB().cur


async def add(email, pwd):
    pwd_crypto = hashlib.sha256(pwd.encode("utf-8")).hexdigest()
    sql = "INSERT INTO users"

    if DB_TYPE == TYPE_PSQL:
        sql += f" VALUES (DEFAULT, '{email}', '{pwd_crypto}')"
    else:
        sql += f" VALUES (NULL, '{email}', '{pwd_crypto}')"

    cur.execute(sql)
    con.commit()


async def update_pwd(email, newpwd):
    new_pwd_crypto = hashlib.sha256(newpwd.encode("utf-8")).hexdigest()
    sql = f"UPDATE users SET passwd='{new_pwd_crypto}' WHERE email='{email}'"
    cur.execute(sql)
    con.commit()


async def is_valid_pwd(email, pwd):
    pwd_crypto = hashlib.sha256(pwd.encode("utf-8")).hexdigest()

    sql = f"SELECT * FROM users WHERE email = '{email}' AND passwd = '{pwd_crypto}'"

    try:
        cur.execute(sql)
        user = cur.fetchone()
        return True if user else False
    except:
        cur.close()
        return False


def exists(email: str):
    user = None

    if len(email.strip()) > 0:
        sql = f"SELECT * FROM users WHERE email = '{email}'"

        try:
            cur.execute(sql)
            user = cur.fetchone()
            return True if user else False
        except:
            return False
