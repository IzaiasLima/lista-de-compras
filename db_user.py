# import sqlite3 as s
import connection

# con = s.connect("compras.db")
# con.row_factory = s.Row
# cur = con.cursor()

con, cur = connection.get()


def add(email, pwd):
    sql = "INSERT INTO users"

    if connection.DB_TYPE == connection.TYPE_PSQL:
        sql += f" VALUES (DEFAULT, '{email}', '{pwd}')"
    else:
        sql += f" VALUES (NULL, '{email}', '{pwd}')"

    cur.execute(sql)
    con.commit()


def get_user(email):
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
