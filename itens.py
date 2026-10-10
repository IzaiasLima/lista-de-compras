import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def ler_csv(arquivo, user_name):
    # resolve contra o diretório do módulo: não depende do cwd do processo
    caminho = arquivo if os.path.isabs(arquivo) else os.path.join(BASE_DIR, arquivo)

    lista_final = []
    with open(caminho, newline='', encoding='utf-8') as csvfile:
        leitor_csv = csv.reader(csvfile)
        for linha in leitor_csv:
            linha.append('cadastrado')
            linha.append(user_name)
            lista_final.append(tuple(linha))
    return lista_final
