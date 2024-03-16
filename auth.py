from fastapi import Depends, Request, HTTPException
from fastapi.security import HTTPBearer
from functools import wraps
import jwt

from session import valid

ROLES = {"admin": []}
ADMIN_EMAIL = "admin@admin.com"
SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"


# def create_jwt(username, role):
#     payload = {"sub": username, "role": role}
#     token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
#     return token


# def get_token(req: Request):
#     token = req.headers["Authorization"]
#     return token


# async def get_current_user(token=Depends(HTTPBearer())):
#     try:
#         payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
#         username = payload.get("sub")
#         role = payload.get("role")
#         if role not in ROLES:
#             raise HTTPException(status_code=403, detail="Invalid role")
#         print({"username": username, "role": role})
#         return {"username": username, "role": role}
#     except jwt.PyJWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")


# def authorize(roles):
#     def decorator(func):
#         async def wrapper(current_user=Depends(get_current_user)):
#             if current_user["role"] not in roles:
#                 raise HTTPException(status_code=403, detail="Unauthorized")
#             return await func()

#         return wrapper

#     return decorator


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
