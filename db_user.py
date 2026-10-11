import hashlib
import hmac
import os
import time

from db import *


con = DB().con
cur = DB().cur


# ------------------------------- senhas ---------------------------------
# Formato guardado: pbkdf2_sha256$<iterações>$<sal_hex>$<resumo_hex>
# O sal é aleatório por usuário (senhas iguais geram resumos diferentes) e o
# PBKDF2 com 600 mil iterações torna o ataque de força bruta caro.
# Tudo com a biblioteca padrão do Python, sem dependência nova.
SCHEMA_PWD = "pbkdf2_sha256"
ITERACOES = 600_000
MIN_TAM_PWD = 6                       # política mínima de senha
TTL_SESSAO_SEG = 7 * 24 * 60 * 60     # validade da sessão (cookie e banco)


def hash_pwd(pwd: str) -> str:
    """Gera o resumo da senha com sal aleatório."""
    sal = os.urandom(16)
    resumo = hashlib.pbkdf2_hmac("sha256", pwd.encode("utf-8"), sal, ITERACOES)
    return f"{SCHEMA_PWD}${ITERACOES}${sal.hex()}${resumo.hex()}"


def verify_pwd(pwd: str, guardado: str) -> bool:
    """Compara a senha informada com o valor guardado no banco."""
    if not guardado:
        return False

    if guardado.startswith(f"{SCHEMA_PWD}$"):
        _, iteracoes, sal, resumo = guardado.split("$")
        teste = hashlib.pbkdf2_hmac(
            "sha256", pwd.encode("utf-8"), bytes.fromhex(sal), int(iteracoes)
        )
        return hmac.compare_digest(teste.hex(), resumo)

    # compatibilidade com o formato antigo: sha256 sem sal, senha em minúsculas
    antigo = hashlib.sha256(pwd.strip().lower().encode("utf-8")).hexdigest()
    return hmac.compare_digest(antigo, guardado)


# ------------------------------- usuários --------------------------------

async def add(email, pwd):
    if DB_TYPE == TYPE_PSQL:
        sql = f"INSERT INTO users VALUES (DEFAULT, {placeholders(2)}, DEFAULT)"
    else:
        sql = f"INSERT INTO users VALUES (NULL, {placeholders(2)}, NULL)"

    cur.execute(sql, (email, hash_pwd(pwd)))
    con.commit()


async def update_pwd(email, newpwd):
    sql = f"UPDATE users SET passwd={placeholders(1)} WHERE email={placeholders(1)}"
    cur.execute(sql, (hash_pwd(newpwd), email))
    con.commit()


async def is_valid_pwd(email, pwd):
    """True se a senha confere. Resumos no formato antigo são atualizados
    para o formato novo (sal + PBKDF2) na primeira entrada válida."""
    sql = f"SELECT passwd FROM users WHERE email={placeholders(1)}"

    try:
        cur.execute(sql, (email,))
        linha = cur.fetchone()
    except Exception:
        return False

    if not linha:
        return False

    guardado = linha[0]

    if not verify_pwd(pwd, guardado):
        return False

    if not str(guardado).startswith(f"{SCHEMA_PWD}$"):
        await update_pwd(email, pwd)

    return True


async def set_session(dado, email):
    """Grava o valor do cookie (id | prazo de validade) na sessão do usuário."""
    sql = f"UPDATE users SET session={placeholders(1)} WHERE email={placeholders(1)}"
    cur.execute(sql, (dado, email))
    con.commit()


async def del_session(session):
    if not session:
        return

    valor_nulo = "DEFAULT" if DB_TYPE == TYPE_PSQL else "NULL"
    sql = f"UPDATE users SET session={valor_nulo} WHERE session={placeholders(1)}"
    cur.execute(sql, (session,))
    con.commit()


def get_user_by_session(session):
    """E-mail dono da sessão; None se não existir, estiver malformada ou expirada."""
    if not session:
        return None

    _, separador, expira = str(session).partition("|")

    if not separador or not expira.isdigit():
        return None        # formato antigo (só o uuid) ou inválido: faça login de novo

    if int(expira) < time.time():
        return None        # sessão expirada

    sql = f"SELECT email FROM users WHERE session={placeholders(1)}"

    try:
        cur.execute(sql, (session,))
        linha = cur.fetchone()
        return linha[0] if linha else None
    except Exception:
        return None


def exists(email: str):
    if not email or not len(email.strip()) > 0:
        return False

    sql = f"SELECT 1 FROM users WHERE email={placeholders(1)}"

    try:
        cur.execute(sql, (email,))
        return cur.fetchone() is not None
    except Exception:
        return False
