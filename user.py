from starlette.exceptions import HTTPException

import db_user as db

IS_AUTH: bool = False


def logged():
    # global IS_AUTH
    return IS_AUTH


def user_exists(user):
    return db.usr_exists(user)


def is_valid_pwd(user: str, pwd: str):
    return db.is_valid_pwd(user, pwd)


def login(user, pwd):
    global IS_AUTH

    if user_exists(user):
        IS_AUTH = is_valid_pwd(user, pwd)
    elif user and pwd:
        add_user(user, pwd)
        IS_AUTH = True
    else:
        IS_AUTH = False


def logout():
    global IS_AUTH
    IS_AUTH = False


def add_user(user, pwd):

    db.add(user, pwd)


def authenticated(func):
    from functools import wraps

    @wraps(func)
    async def wrapper():
        # global IS_AUTH

        if not IS_AUTH:
            raise NotAuthorized(status_code=401, detail="Usuário não autenticado.")
        return await func()

    return wrapper


class NotAuthorized(HTTPException):
    def __init__(self, status_code, detail):
        super().__init__(status_code, detail)
