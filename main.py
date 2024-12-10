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


@app.post("/cadastrar", response_class=HTMLResponse)
async def add_user(request:Request, body: dict = Depends(get_body)):
    username: str = body.get("user")
    password: str = body.get("passwd")

    if len(username.strip()) == 0 or len(password.strip()) == 0:
        raise HTTPException(status_code=400, detail="Usuário ou senha inválidos.")

    if user.exists(username):
        raise HTTPException(status_code=400, detail="Usuário informado já existe.")

    await user.add(username, password)
    
    # cadastrar lista inicial de produtos
    db_init.init_itens_table(username)

    return continue_login(username, password)


@app.post("/newpwd", response_class=HTMLResponse)
@auth.authenticated
async def new_passwd(request: Request, body: dict = Depends(get_body)):
    username = session.get_user(request)
    oldpwd = body.get("oldpwd")
    newpwd = body.get("newpwd")

    allow = user.is_valid_pwd(username, oldpwd)

    if len(newpwd.strip()) == 0:
        raise HTTPException(status_code=400, detail="Nova senha inválida.")

    if not allow:
        raise HTTPException(status_code=401, detail="Senha anterior não confere.")

    await user.update_pwd(username, newpwd)

    URL = "<script>window.location.href='/app/home.html'</script>"
    response = HTMLResponse(URL)
    return response


@app.post("/login", response_class=HTMLResponse)
async def login(body: dict = Depends(get_body)):
    username = body.get("user")
    password = body.get("passwd")
    return continue_login(username, password)


def continue_login(username, password):
    allow = user.is_valid_pwd(username, password)

    if not allow:
        raise HTTPException(status_code=401, detail="Usuário/senha não confere.")

    session_id = session.get_session(username)

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
async def psalm_of_day():
    res = {"capitulo": sort_chapter()}
    return res


@app.get("/api/itens", response_class=JSONResponse)
@auth.authenticated
async def get_itens_list(request: Request):
    dados = await db.get_itens(session.get_user(request))
    return dados


@app.get("/api/itens/{id}", response_class=JSONResponse)
@auth.authenticated
async def get_iten(id, request: Request):
    dados = await db.get_iten(id, session.get_user(request))
    return dados


@app.post("/api/itens", response_class=JSONResponse)
@auth.authenticated
async def add_iten(request: Request, body=Depends(get_body)):
    if is_valid(body, 3):
        email = session.get_user(request)
        db.add_iten(body, email)
        dados = await db.get_itens(email)
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.get("/api/compras", response_class=JSONResponse)
@auth.authenticated
async def get_shopping_list(request: Request):
    dados = await db.get_compras(session.get_user(request))
    return dados


@app.patch("/api/compras/{id}/adicionar", response_class=JSONResponse)
@auth.authenticated
async def iten_car_add(request: Request, id):
    email = session.get_user(request)
    db.patch_status(id, email, "comprado")
    dados = await db.get_compras(email)
    return dados


@app.patch("/api/compras/{id}/remover", response_class=JSONResponse)
@auth.authenticated
async def iten_car_remove(request: Request, id):
    email = session.get_user(request)
    db.patch_status(id, email, "selecionado")
    dados = await db.get_compras(email)
    return dados


@app.get("/api/lista", response_class=JSONResponse)
@auth.authenticated
async def get_all_itens_list(request: Request):
    return await db.get_lista(session.get_user(request))


@app.get("/api/lista/all/reset", response_class=JSONResponse)
@auth.authenticated
async def shopping_list_reset(request: Request):
    email = session.get_user(request)
    db.patch_status(None, email, "cadastrado")
    return await db.get_lista(email)


@app.patch("/api/lista/{id}/adicionar", response_class=JSONResponse)
@auth.authenticated
async def iten_lista_add(request: Request, id):
    email = session.get_user(request)
    db.patch_status(id, email, "selecionado")
    return await db.get_lista(email)


@app.patch("/api/lista/{id}/remover", response_class=JSONResponse)
@auth.authenticated
async def iten_lista_remove(request: Request, id):
    email = session.get_user(request)
    db.patch_status(id, email, "cadastrado")
    return await db.get_lista(email)


@app.delete("/api/itens/{id}", response_class=HTMLResponse)
@auth.authenticated
async def del_iten(request: Request, id):
    db.del_iten(id)
    return ""


# -------------------------------------- #


# retornar template para incluir item
@app.get("/api/itens/new/add", response_class=HTMLResponse)
@auth.authenticated
async def get_add_iten_template(request: Request):
    return add.iten_html()


# --------------------------------------- #


def is_valid(body: dict, qtd: int):
    return sum([1 if v else 0 for _, v in body.items()]) == qtd


def sort_chapter():
    import random as r

    chapter = [1, 2, 14, 15, 19, 23, 24, 37, 51, 84, 91, 100, 133, 139, 150][r.randint(0, 14)]
    return chapter


# --------------------------------------- #


# resetar o banco de dados
@app.delete("/reset", response_class=JSONResponse)
@auth.authenticated
async def db_reset(request: Request):
    db_init.init_itens_table(session.get_user(request))
    return
