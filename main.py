from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse

import json
import urllib.parse as html

import static.fragments.html_add as add
import db_api as db
import db_user as user
import db_init
import session
import auth


ERR_MSG = "Todos os campos precisam ser preenchidos!"


app = FastAPI(
    title="Lista de Compras",
    version="0.0.1",
    summary="Lista de compras simples para um usuário.",
)

app.mount("/app", StaticFiles(directory="static", html="True"), name="static")


async def get_body(req: Request):
    payload = await req.body()
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


@app.post("/cadastrar", response_class=HTMLResponse)
async def login(body: dict = Depends(get_body)):
    username = body.get("user")
    password = body.get("passwd")

    if len(username) == 0:
        raise HTTPException(status_code=400, detail="Usuário inválido.")

    if user.exists(username):
        raise HTTPException(status_code=400, detail="Usuário informado já existe.")

    await user.add(username, password)
    return continue_login(username, password)


@app.post("/login", response_class=HTMLResponse)
async def login(body: dict = Depends(get_body)):
    username = body.get("user")
    password = body.get("passwd")
    return continue_login(username, password)


def continue_login(username, password):

    allow = user.is_valid_pwd(username, password)

    if not allow:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválida.")

    session_id = session.get_id(username)

    if not session_id:
        session_id = session.get_random_id()

    session.add(session_id, username)

    URL = "<script>window.location.href='/app/home.html'</script>"

    response = HTMLResponse(URL)
    response.set_cookie(key="Authorization", value=session_id)

    return response


@app.get("/logout")
async def session_logout(req: Request):
    session_id = req.cookies.get("Authorization")
    session.remove(session_id)

    URL = "<script>window.location.href='/app/login.html'</script>"
    response = HTMLResponse(URL)
    response.delete_cookie(key="Authorization")

    return response


@app.get("/api/capitulo", response_class=JSONResponse)
# @authorize(["xxx"])
async def salmos():
    res = {"capitulo": sort_chapter()}
    return res


@app.get("/api/itens", response_class=JSONResponse)
@auth.authenticated
async def get_itens(request: Request):
    dados = db.get_itens(session.get_user(request))
    return dados


@app.get("/api/itens/{id}", response_class=JSONResponse)
@auth.authenticated
async def get_item(id, request: Request):
    dados = db.get_item(id, session.get_user(request))
    return dados


@app.post("/api/itens", response_class=JSONResponse)
@auth.authenticated
async def add_item(request: Request, body=Depends(get_body)):
    if is_valid(body, 3):
        email = session.get_user(request)
        db.add_item(body, email)
        dados = db.get_itens(email)
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.get("/api/compras", response_class=JSONResponse)
@auth.authenticated
async def get_compras(request: Request):
    dados = db.get_compras(session.get_user(request))
    return dados


@app.patch("/api/compras/{id}/adicionar", response_class=JSONResponse)
@auth.authenticated
async def item_select(request: Request, id):
    email = session.get_user(request)
    db.patch_status(id, email, "comprado")
    dados = db.get_compras(email)
    return dados


@app.patch("/api/compras/{id}/remover", response_class=JSONResponse)
@auth.authenticated
async def item_remove(request: Request, id):
    email = session.get_user(request)
    db.patch_status(id, email, "selecionado")
    dados = db.get_compras(email)
    return dados


@app.get("/api/lista", response_class=JSONResponse)
@auth.authenticated
async def get_lista(request: Request):
    return db.get_lista(session.get_user(request))


@app.get("/api/lista/all/reset", response_class=JSONResponse)
@auth.authenticated
async def list_reset(request: Request):
    email = session.get_user(request)
    db.patch_status(None, email, "cadastrado")
    return db.get_lista(email)
    # return "/app/lista.html"


@app.patch("/api/lista/{id}/adicionar", response_class=JSONResponse)
@auth.authenticated
async def item_lista_add(request: Request, id):
    email = session.get_user(request)
    db.patch_status(id, email, "selecionado")
    return db.get_lista(email)


@app.patch("/api/lista/{id}/remover", response_class=JSONResponse)
@auth.authenticated
async def item_lista_remove(request: Request, id):
    email = session.get_user(request)
    db.patch_status(id, email, "cadastrado")
    return db.get_lista(email)


@app.delete("/api/itens/{id}", response_class=HTMLResponse)
@auth.authenticated
async def del_item(request: Request, id):
    db.del_item(id)
    return ""


# -------------------------------------- #


# retornar template para incluir item
@app.get("/api/itens/new/add", response_class=HTMLResponse)
@auth.authenticated
async def add_item(request: Request):
    return add.item_html()


# --------------------------------------- #


def is_valid(body: dict, qtd: int):
    return sum([1 if v else 0 for _, v in body.items()]) == qtd


def sort_chapter():
    import random as r

    chapter = [1, 2, 14, 15, 23, 24, 91, 100, 133, 150][r.randint(0, 9)]
    return chapter


# --------------------------------------- #


# resetar o banco de dados
@app.get("/reset", response_class=RedirectResponse)
@auth.authenticated
async def db_reset(request: Request):
    db_init.tables_init(session.get_user(request))
    return "/app/home.html"
