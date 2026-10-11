from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse

import json
import os
import time
import urllib.parse as html
import uvicorn
import static.fragments.html_add as add
import db_api as db
import db_user as user
import db_init
import session
import auth


ERR_MSG = "Todos os campos precisam ser preenchidos!"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMPOS_ITEM = ("nome", "categoria", "status")


app = FastAPI(
    title="Lista de Compras",
    version="1.1.3",
    summary="Lista de compras simples para um usuário.",
)

app.mount(
    "/app",
    StaticFiles(directory=os.path.join(BASE_DIR, "static"), html="True"),
    name="static",
)


async def get_body(request: Request):
    payload = await request.body()
    payload = payload.decode("utf8")
    payload = html.unquote(payload)

    try:
        body = json.loads(payload)
    except:
        try:
            lista = list(payload.split("&"))
            body = dict(l.split("=") for l in lista)
        except:
            body = {}
    return body


@app.get("/", response_class=RedirectResponse)
async def root():
    return "/app/login.html"


@app.get("/api", response_class=RedirectResponse)
async def root():
    return "/app/login.html"


@app.post("/newuser", response_class=HTMLResponse)
async def add_user(request: Request, body: dict = Depends(get_body)):
    username: str = (body.get("user") or "").strip().lower()
    password: str = (body.get("passwd") or "").strip()

    if len(username.strip()) == 0 or len(password) == 0:
        raise HTTPException(status_code=400, detail="Usuário ou senha inválidos.")

    if len(password) < user.MIN_TAM_PWD:
        raise HTTPException(
            status_code=400,
            detail=f"Senha muito curta: mínimo {user.MIN_TAM_PWD} caracteres.",
        )

    if user.exists(username):
        raise HTTPException(status_code=400, detail="Usuário informado já existe.")

    await user.add(username, password)

    # cadastrar lista inicial de produtos
    db_init.init_itens_table(username)

    return await continue_login(username, password, request)


@app.post("/newpwd", response_class=HTMLResponse)
@auth.authenticated
async def new_passwd(request: Request, body: dict = Depends(get_body)):
    username = session.get_user(request)
    oldpwd = (body.get("oldpwd") or "").strip()
    newpwd = (body.get("newpwd") or "").strip()

    allow = await user.is_valid_pwd(username, oldpwd)

    if len(newpwd) < user.MIN_TAM_PWD:
        raise HTTPException(
            status_code=400,
            detail=f"Nova senha inválida: mínimo {user.MIN_TAM_PWD} caracteres.",
        )

    if not allow:
        raise HTTPException(status_code=401, detail="Senha anterior não confere.")

    await user.update_pwd(username, newpwd)

    URL = "<script>window.location.href='/app/home.html'</script>"
    response = HTMLResponse(URL)
    return response


@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, body: dict = Depends(get_body)):
    username = (body.get("user") or "").strip().lower()
    password = (body.get("passwd") or "").strip()
    return await continue_login(username, password, request)


# controle simples de tentativa de login (em memória: vale por processo)
TENTATIVAS_MAX = 5
BLOQUEIO_SEG = 300          # 5 tentativas erradas bloqueiam o e-mail por 5 minutos
_tentativas = {}            # email -> [falhas, desbloqueia_em]


def bloqueado(email):
    dados = _tentativas.get(email)
    return bool(dados and dados[1] > time.time())


def registra_falha(email):
    falhas = _tentativas.get(email, [0, 0])[0] + 1
    desbloqueio = time.time() + BLOQUEIO_SEG if falhas >= TENTATIVAS_MAX else 0
    _tentativas[email] = [falhas, desbloqueio]


def limpa_tentativas(email):
    _tentativas.pop(email, None)


async def continue_login(username, password, request):
    if bloqueado(username):
        raise HTTPException(
            status_code=429,
            detail="Muitas tentativas de acesso. Tente novamente em alguns minutos.",
        )

    allow = await user.is_valid_pwd(username, password)

    if not allow:
        registra_falha(username)
        raise HTTPException(status_code=401, detail="Usuário/senha não confere.")

    limpa_tentativas(username)

    session_id = session.get_random_id()
    await user.set_session(session_id, username)

    URL = "<script>window.location.href='/app/home.html'</script>"

    response = HTMLResponse(URL)
    response.set_cookie(
        key="Authorization",
        value=session_id,
        httponly=True,                     # JS não lê: mitiga roubo de sessão via XSS
        samesite="lax",                    # não segue em requisições de outros sites
        secure=request.url.scheme == "https",
    )

    return response


@app.get("/logout")
async def session_logout(req: Request):
    session_id = req.cookies.get("Authorization")
    await session.remove(session_id)

    URL = "<script>window.location.href='/app/login.html'</script>"
    response = HTMLResponse(URL)
    response.delete_cookie(key="Authorization")

    return response


@app.post("/renewpwd/{username}")
@auth.administrator
async def renew_passwd(username: str, request: Request, body: dict = Depends(get_body)):
    # a senha vai no corpo da requisição, nunca na URL (URLs param no log)
    username = username.strip().lower()
    newpwd = (body.get("newpwd") or "").strip()

    if user.exists(username) == False:
        raise HTTPException(status_code=400, detail="Usuário informado não existe.")

    if len(newpwd) < user.MIN_TAM_PWD:
        raise HTTPException(
            status_code=400,
            detail=f"Nova senha inválida: mínimo {user.MIN_TAM_PWD} caracteres.",
        )

    await user.update_pwd(username, newpwd)

    return HTMLResponse(f"Usuário {username}: senha atualizada com sucesso!")


@app.get("/api/itens", response_class=JSONResponse)
@auth.authenticated
async def get_itens_list(request: Request):
    user_email = session.get_user(request)
    dados = await db.get_itens(user_email)
    return dados


@app.get("/api/session", response_class=JSONResponse)
@auth.authenticated
async def get_session(request: Request):
    """Consulta usada pelo front (o cookie é HttpOnly, o JS não consegue ler)."""
    return JSONResponse(
        {"user": session.get_user(request)}, headers={"Cache-Control": "no-store"}
    )


@app.post("/api/itens", response_class=JSONResponse)
@auth.authenticated
async def add_iten(request: Request, body=Depends(get_body)):
    if is_valid(body):
        email = session.get_user(request)
        db.add_iten({campo: body[campo] for campo in CAMPOS_ITEM}, email)
        dados = await db.get_itens(email)
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.get("/api/compras", response_class=JSONResponse)
@auth.authenticated
async def get_shopping_list(request: Request):
    email = session.get_user(request)
    dados = await db.get_compras(email)
    return dados


@app.get("/api/itens/{id}", response_class=JSONResponse)
@auth.authenticated
async def get_iten(id: int, request: Request):
    email = session.get_user(request)
    dados = await db.get_iten(id, email)
    return dados


@app.patch("/api/compras/{id}/adicionar", response_class=JSONResponse)
@auth.authenticated
async def iten_shopp_cart_add(request: Request, id: int):
    email = session.get_user(request)
    db.patch_status(id, email, "comprado")
    dados = await db.get_compras(email)
    return dados


@app.patch("/api/compras/{id}/remover", response_class=JSONResponse)
@auth.authenticated
async def iten_shopp_cart_remove(request: Request, id: int):
    email = session.get_user(request)
    db.patch_status(id, email, "selecionado")
    dados = await db.get_compras(email)
    return dados


@app.get("/api/lista", response_class=JSONResponse)
@auth.authenticated
async def get_all_itens_list(request: Request):
    email = session.get_user(request)
    return await db.get_lista(email)


@app.get("/api/lista/all/reset", response_class=JSONResponse)
@auth.authenticated
async def shopping_list_reset(request: Request):
    email = session.get_user(request)
    db.patch_status(None, email, "cadastrado")
    return await db.get_lista(email)


@app.patch("/api/lista/{id}/adicionar", response_class=JSONResponse)
@auth.authenticated
async def iten_lista_add(request: Request, id: int):
    email = session.get_user(request)
    db.patch_status(id, email, "selecionado")
    return await db.get_lista(email)


@app.patch("/api/lista/{id}/remover", response_class=JSONResponse)
@auth.authenticated
async def iten_lista_remove(request: Request, id: int):
    email = session.get_user(request)
    db.patch_status(id, email, "cadastrado")
    return await db.get_lista(email)


@app.delete("/api/itens/{id}", response_class=HTMLResponse)
@auth.authenticated
async def del_iten(request: Request, id: int):
    # o filtro por usuário está na camada de dados: id de terceiros não é apagado
    db.del_iten(id, session.get_user(request))
    return ""


# -------------------------------------- #


# retornar template para incluir item
@app.get("/api/itens/new/add", response_class=HTMLResponse)
@auth.authenticated
async def get_add_iten_template(request: Request):
    return add.iten_html()


# --------------------------------------- #


def is_valid(body: dict):
    """Confere se os campos obrigatórios do item foram preenchidos.

    Campos extras no corpo são ignorados (antes geravam 422).
    """
    return all(str(body.get(campo) or "").strip() for campo in CAMPOS_ITEM)


# --------------------------------------- #


# resetar o banco de dados
@app.delete("/reset", response_class=JSONResponse)
@auth.authenticated
async def db_reset(request: Request):
    email = session.get_user(request)
    db_init.init_itens_table(email)
    return


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
