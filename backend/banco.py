# =============================================================
# banco.py
# Lê e salva os dados nos arquivos .txt da pasta "dados".
# Cada linha do .txt é um registro, com os campos separados por ";".
# =============================================================

import os

# A pasta "dados" fica ao lado deste arquivo (dentro de backend)
PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados")

ARQ_USUARIOS = os.path.join(PASTA, "usuarios.txt")
ARQ_SERVICOS = os.path.join(PASTA, "servicos.txt")
ARQ_ORCAMENTOS = os.path.join(PASTA, "orcamentos.txt")
ARQ_AVALIACOES = os.path.join(PASTA, "avaliacoes.txt")
ARQ_NOTIFICACOES = os.path.join(PASTA, "notificacoes.txt")


def criar_arquivos():
    """Cria a pasta dados e os 4 arquivos vazios, se ainda não existirem."""
    if not os.path.exists(PASTA):
        os.makedirs(PASTA)
    for arquivo in [ARQ_USUARIOS, ARQ_SERVICOS, ARQ_ORCAMENTOS, ARQ_AVALIACOES, ARQ_NOTIFICACOES]:
        if not os.path.exists(arquivo):
            f = open(arquivo, "w", encoding="utf-8")
            f.close()


def ler(arquivo, campos):
    """Lê o arquivo e devolve uma lista de dicionários.
    Os valores de cada linha seguem a ordem da lista campos."""
    lista = []
    if not os.path.exists(arquivo):
        return lista
    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.rstrip("\r\n")
            if linha.strip() == "":
                continue
            partes = linha.split(";")
            item = {}
            for i in range(len(campos)):
                if i < len(partes):
                    item[campos[i]] = partes[i]
                else:
                    item[campos[i]] = ""
            lista.append(item)
    return lista


def salvar(arquivo, campos, lista):
    """Apaga o conteúdo do arquivo e escreve a lista inteira de novo.
    Troca ";" por "," dentro dos valores para não bagunçar as colunas."""
    with open(arquivo, "w", encoding="utf-8") as f:
        for item in lista:
            valores = []
            for campo in campos:
                valor = str(item.get(campo, ""))
                valor = valor.replace(";", ",").replace("\n", " ")
                valores.append(valor)
            f.write(";".join(valores) + "\n")


def novo_id(lista):
    """Devolve o próximo id: o maior id da lista + 1 (como texto)."""
    maior = 0
    for item in lista:
        valor = item.get("id", "")
        if valor.isdigit() and int(valor) > maior:
            maior = int(valor)
    return str(maior + 1)


def pedir_texto(pergunta):
    """Pergunta até a pessoa digitar alguma coisa."""
    while True:
        texto = input(pergunta).strip()
        if texto != "":
            return texto
        print("Este campo é obrigatório.")
