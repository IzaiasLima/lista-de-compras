# import connection
import user
from db import DB


# con, cur = connection.get()
db = DB()
con = db.con
cur = db.cur


async def add(email, pwd):
    sql = "INSERT INTO users"

    if DB.DB_TYPE == DB.TYPE_PSQL:
        sql += f" VALUES (DEFAULT, '{email}', '{pwd}')"
    else:
        sql += f" VALUES (NULL, '{email}', '{pwd}')"

    cur.execute(sql)
    con.commit()


async def get_user(email):
    sql = f"SELECT * FROM users WHERE email = '{email}'"
    cur.execute(sql)
    resp = cur.fetchone()
    user = dict(resp) if resp else {}
    return user


def usr_exists(user):
    usr = get_user(user)
    return True if usr else False


def is_valid_pwd(email, pwd):
    sql = f"SELECT * FROM users WHERE email = '{email}' AND passwd = '{pwd}'"
    cur.execute(sql)
    user = cur.fetchone()
    return True if user else False
