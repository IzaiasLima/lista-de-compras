import sqlite3 as s

con = s.connect("compras.db")
# con.row_factory = s.Row
cur = con.cursor()


def add(user, pwd):
    sql = f"INSERT INTO users VALUES (NULL, '{user}', '{pwd}')"
    cur.execute(sql)
    con.commit()


def get(user):
    sql = f"SELECT * FROM users WHERE user = '{user}'"
    cur.execute(sql)
    user = cur.fetchone()
    return user


def usr_exists(user):
    usr = get(user)
    return True if usr else False


def is_valid_pwd(user, pwd):
    sql = f"SELECT * FROM users WHERE user = '{user}' AND passwd = '{pwd}'"
    cur.execute(sql)
    user = cur.fetchone()
    return True if user else False
