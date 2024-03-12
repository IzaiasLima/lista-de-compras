from starlette.exceptions import HTTPException

import db_user as db

IS_AUTH: bool = False
IS_ADMIN: bool = False

ADMIN_EMAIL = "admin@admin.com"

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


async def login(email, pwd):
    global IS_AUTH
    global IS_ADMIN

    IS_AUTH = False
    IS_ADMIN = False

    if user_exists(email):
        IS_AUTH = is_valid_pwd(email, pwd)
        IS_ADMIN = IS_AUTH and email == ADMIN_EMAIL
    elif email and pwd:
        await add_user(email, pwd)
        IS_AUTH = True


def logout():
    global IS_AUTH
    global IS_ADMIN

    IS_AUTH = False
    IS_ADMIN = False


async def add_user(email, pwd):
    global CURRENT_USER_ID
    await db.add(email, pwd)
    user = await db.get_user(email)
    CURRENT_USER_ID = user.get("id")


def authenticated(func):
    from functools import wraps

    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not IS_AUTH:
            raise NotAuthorized(status_code=401, detail="Usuário não autenticado.")
        return await func(*args, **kwargs)

    return wrapper


def admin(func):
    from functools import wraps

    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not IS_ADMIN:
            raise NotAuthorized(status_code=403, detail="Usuário sem permissão.")
        return await func(*args, **kwargs)

    return wrapper


class NotAuthorized(HTTPException):
    def __init__(self, status_code, detail):
        super().__init__(status_code, detail)
