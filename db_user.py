import hashlib
from db import *


con = DB().con
cur = DB().cur


async def add(email, pwd):
    pwd_crypto = hashlib.sha256(pwd.encode("utf-8")).hexdigest()
    sql = "INSERT INTO users"

    if DB_TYPE == TYPE_PSQL:
        sql += f" VALUES (DEFAULT, '{email}', '{pwd_crypto}', DEFAULT)"
    else:
        sql += f" VALUES (NULL, '{email}', '{pwd_crypto}', NULL)"

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
        return False


async def set_session(session, email):
    sql = f"UPDATE users SET session='{session}' WHERE email='{email}'"
    cur.execute(sql)
    con.commit()

async def del_session(session):
    sql = f"UPDATE users"

    if DB_TYPE == TYPE_PSQL:
        sql += ' SET session=DEFAULT'
    else:
        sql += ' SET session=NULL'

    sql += f" WHERE session='{session}'"

    cur.execute(sql)
    con.commit()

def get_user_by_session(session):
    sql = f"SELECT email FROM users"
    sql += f" WHERE session='{session}'"

    try:
        cur.execute(sql)
        user = cur.fetchone()
        return user[0] if user else None
    except:
        return None

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
