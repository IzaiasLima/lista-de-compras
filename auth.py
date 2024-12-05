import os
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from functools import wraps

from session import valid

ROLES = {"admin": []}
ADMIN_EMAIL = os.environ.get("ADMIN_USR", "admin@admin.com")
SECRET_KEY = os.environ.get("ADMIN_PWD", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")

def authenticated(func):
    @wraps(func)
    async def wrap_func(*args, request, **kwargs):
        valid(request)
        return await func(*args, request, **kwargs)

    return wrap_func


def administrator(func):
    from functools import wraps

    @wraps(func)
    async def wrapper(email, *args, **kwargs):
        if not email == ADMIN_EMAIL:
            raise NotAuthorized(status_code=403, detail="Usuário sem permissão.")
        return await func(*args, **kwargs)

    return wrapper


class NotAuthorized(HTTPException):
    def __init__(self, status_code, detail):
        super().__init__(status_code, detail)
