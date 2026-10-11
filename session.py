from fastapi import Request, HTTPException
import time
import uuid

import db_user as user


async def remove(session_id):
    await user.del_session(session_id)


async def valid(request: Request):
    """Verifica se há uma sessão válida (existente e não expirada) no banco"""

    session_id = request.cookies.get("Authorization")

    if not session_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado.")

    user_email = user.get_user_by_session(session_id)

    if not user_email:
        raise HTTPException(status_code=401, detail="Sessão inválida ou expirada.")

    # guarda o resultado para os endpoints não precisarem consultar de novo
    request.state.user = user_email


def get_user(request: Request):
    """E-mail do usuário da requisição (já resolvido por `valid`, quando há)."""
    user_email = getattr(request.state, "user", None)

    if user_email is None:
        user_email = user.get_user_by_session(request.cookies.get("Authorization"))

    return user_email


def get_random_id():
    """Gera o valor do cookie de sessão: id aleatório + prazo de validade"""
    expira = int(time.time()) + user.TTL_SESSAO_SEG
    return f"{uuid.uuid4()}|{expira}"
