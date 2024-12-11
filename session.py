from fastapi import Request, HTTPException
import uuid


SESSION_DB = {}


def add(id, username):
    """Salva a sessão no banco de dados de sessões"""
    SESSION_DB[id] = username


def remove(session_id):
    SESSION_DB.pop(session_id, None)


async def valid(request: Request):
    """Verifica se há uma sessão válida para o usuário"""

    session_id = request.cookies.get("Authorization")

    if not session_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado.")

    if session_id not in SESSION_DB:
        raise HTTPException(status_code=403, detail="Favor se logar novamente.")


def get_user(request: Request):
    session_id = request.cookies.get("Authorization")
    return SESSION_DB[session_id]


def get_session(username):
    """Se já existir uma sessão válida para o usuário, retorna o ID"""
    session_id = get_random_id()

    try:
        session_id = list(SESSION_DB.keys())[list(SESSION_DB.values()).index(username)]
    except:
        pass

    return session_id


def get_random_id():
    """Gera um id randômico"""
    return str(uuid.uuid4())
