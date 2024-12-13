from fastapi import Request, HTTPException
import uuid

import db_user as user


async def remove(session_id):
    await user.del_session(session_id)

async def valid(request: Request):
    """Verifica se há uma sessão válida para o usuário"""

    session_id = request.cookies.get("Authorization")

    if not session_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado.")


def get_user(request: Request):
    session_id = request.cookies.get("Authorization")
    user_email = user.get_user_by_session(session_id)
    return user_email
    

def get_random_id():
    """Gera um id randômico"""
    return str(uuid.uuid4())
