from starlette.exceptions import HTTPException

import db_user as db

IS_AUTH: bool = False
CURRENT_USER_ID = None


def logged():
    return IS_AUTH


def user_exists(email):
    global CURRENT_USER_ID

    user = db.get_user(email)
    CURRENT_USER_ID = user.get("id") if user else 0
    return CURRENT_USER_ID > 0


def is_valid_pwd(email: str, pwd: str):
    return db.is_valid_pwd(email, pwd)


def login(email, pwd):
    global IS_AUTH

    if user_exists(email):
        IS_AUTH = is_valid_pwd(email, pwd)
    elif email and pwd:
        add_user(email, pwd)
        IS_AUTH = True
    else:
        IS_AUTH = False


def logout():
    global IS_AUTH
    IS_AUTH = False


def add_user(email, pwd):
    global CURRENT_USER_ID
    db.add(email, pwd)
    user = db.get_user(email)
    CURRENT_USER_ID = user.get("id")


def authenticated(func):
    from functools import wraps

    @wraps(func)
    async def wrapper():
        if not IS_AUTH:
            raise NotAuthorized(status_code=401, detail="Usuário não autenticado.")
        return await func()

    return wrapper


class NotAuthorized(HTTPException):
    def __init__(self, status_code, detail):
        super().__init__(status_code, detail)
