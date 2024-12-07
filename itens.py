import csv

def ler_csv(arquivo, user_name):
    lista_final = []
    with open(arquivo, newline='', encoding='utf-8') as csvfile:
        leitor_csv = csv.reader(csvfile)
        for linha in leitor_csv:
            linha.append('cadastrado')
            linha.append(user_name)
            lista_final.append(tuple(linha))
    return lista_final
