# Lista de Compras

## Apresentação
Lista de Compras simplificada para poucos usuários, desenvolvida em Python (FastApi) no _backend_. O _frontend_ foi feito em HTML e CSS puros, apenas adicionando um pouco de reatividade com o uso do [HTMX](htmx.org). A intenção é mostrar o uso dessas linguagens, sem ocultar ou mascarar o seu funcionamento pela adoção de _frameworks_, dando un caráter quase didático para o projeto.

## Banco de dados
Da mesma forma, o acesso a banco de dados foi feito "na unha", intencionalmente, para exemplificar o uso de SQL, podendo ser testado localmente com SQlite e PostgreSql. O deploy provavelmente só será possível usando o PostgreSql.

## Autenticação
Incluímos também um sistema de _login_ simplicíssimo, só para permitir o acesso por mais de um usuário, mas sem a pretensão de ser eficiente, nem seguro.

## Execução
Para testar localmente:
- faça o clone do projeto
- execute ```pip install -r requirements.txt``` para atualizar as dependências
- crie o banco de dados, executando ```python db_init.py```
- execute no servidor web local: ```uvicorn main:app --reload```

## Deploy na web, para acesso público
O protótipo desta aplicação está disponível para acesso público no seguinte endereço [fazercompras.vercel.app](https://fazercompras.vercel.app), onde pode ser testado livremente, mediante o cadastro rápido de um e-mail e senha, podendo ser um e-mail fictício.