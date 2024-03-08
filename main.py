#! env/bin/python
# -*- coding: UTF-8 -*-

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse

import json
import time
import urllib.parse as html
import uvicorn

import db
import db_init

import static.fragments.html_add as add

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
        lista = list(payload.split("&"))
        body = dict(l.split("=") for l in lista)

    return body


@app.get("/", response_class=RedirectResponse)
async def root():
    return "/app/home.html"


@app.get("/api", response_class=RedirectResponse)
async def root():
    return "/app/home.html"


@app.get("/api/capitulo", response_class=JSONResponse)
async def root():
    return {"capitulo": sort_chapter()}


@app.get("/api/itens")
async def itens():
    # time.sleep(0.5)
    dados = db.get_itens()
    return JSONResponse(dados)


@app.get("/api/itens/{id}")
async def item(id: int):
    dados = db.get_item(id)
    return JSONResponse(dados)


@app.post("/api/itens", response_class=JSONResponse)
async def add_item(body=Depends(get_body)):
    if is_valid(body, 3):
        db.add_item(body)
        dados = db.get_itens()
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.get("/api/compras")
async def get_compras():
    dados = db.get_compras()
    return JSONResponse(dados)


@app.patch("/api/compras/{id}/adicionar", response_class=JSONResponse)
async def item_select(id: int):
    db.patch_status(id, "comprado")
    dados = db.get_compras()
    return dados


@app.patch("/api/compras/{id}/remover", response_class=JSONResponse)
async def item_select(id: int):
    db.patch_status(id, "selecionado")
    dados = db.get_compras()
    return dados


@app.get("/api/lista")
async def get_lista():
    dados = db.get_lista()
    return JSONResponse(dados)


@app.get("/api/lista/all/reset", response_class=RedirectResponse)
async def list_reset():
    db.patch_status(None, "cadastrado")
    return "/app/lista.html"


@app.patch("/api/lista/{id}/adicionar", response_class=JSONResponse)
async def item_select(id: int):
    db.patch_status(id, "selecionado")
    dados = db.get_lista()
    return dados


@app.patch("/api/lista/{id}/remover", response_class=JSONResponse)
async def item_remove(id: int):
    db.patch_status(id, "cadastrado")
    dados = db.get_lista()
    return dados


@app.delete("/api/itens/{id}", response_class=HTMLResponse)
async def del_item(id: int):
    db.del_item(id)
    return ""


# -------------------------------------- #


# retornar template para incluir item
@app.get("/api/itens/new/add", response_class=HTMLResponse)
async def add_item():
    return add.item_html()


# retornar template para editar item
# @app.get("/api/itens/{id}/edit", response_class=HTMLResponse)
# async def edit_item(id: int):
#     item = db.get_item(id)

#     if item:
#         dados = item[0]
#         return edit.item_html(dados)
#     else:
#         raise HTTPException(status_code=404)


# --------------------------------------- #


# resetar o banco de dados
@app.get("/reset", response_class=RedirectResponse)
def db_reset():
    db_init.tables_init()
    return "/app/home.html"


def is_valid(body: dict, qtd: int):
    return sum([1 if v else 0 for _, v in body.items()]) == qtd


def sort_chapter():
    import random as r

    chapter = [1, 2, 14, 15, 23, 24, 91, 100, 133, 150][r.randint(0, 9)]
    return chapter


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
