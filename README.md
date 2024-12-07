# Lista de Compras

Lista de Compras simplificada, desenvolvida em Python (FastApi) no _backend_ e em HTML e CSS puros no _frontend_, apenas adicionando um pouco de reatividade com o uso do [HTMX](htmx.org). A intenção foi mostrar o uso dessas linguagens, sem ocultar ou ofuscar como elas funcionam, o que ocorre, geralmente, quando adotamos um _frameworks_. Essa abordagem dá um caráter quase didático ao projeto.

## Banco de dados
Da mesma forma, o acesso a banco de dados foi feito "na unha", intencionalmente, para exemplificar o uso de SQL, podendo ser testado localmente com SQlite e PostgreSQL. O deploy na WEB, provavelmente, só será possível usando o PostgreSQL. Pelo menos, assim foi mais fácil para mim.

## Autenticação
Incluímos também um sistema de _login_ simplicíssimo, só para permitir o acesso por mais de um usuário, mas sem a mínima pretensão de ser eficiente, nem seguro.

## Execução
Para testar localmente:
- faça o clone do projeto
- execute ```pip install -r requirements.txt``` para atualizar as dependências
- crie o banco de dados, executando ```python db_init.py```
- execute no servidor web local: ```uvicorn main:app --reload```

## Deploy
O protótipo da aplicação está disponível para acesso público no seguinte endereço [fazercompras.vercel.app](https://fazercompras.vercel.app), onde pode ser testado livremente, mediante o cadastro rápido de um e-mail e senha, podendo ser um e-mail fictício.