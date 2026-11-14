# =============================================================
# banco.py
# Lê e salva os dados nos arquivos .txt da pasta BancoDados
# Cada linha do .txt é um registro, com os campos separados por ";"
# =============================================================

import os

# A pasta BancoDados fica dentro de backend (é criada sozinha)
PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "BancoDados")

ARQ_USUARIOS = os.path.join(PASTA, "usuarios.txt")
ARQ_SERVICOS = os.path.join(PASTA, "servicos.txt")
ARQ_ORCAMENTOS = os.path.join(PASTA, "orcamentos.txt")
ARQ_AVALIACOES = os.path.join(PASTA, "avaliacoes.txt")


def ler(arquivo, campos):
    """Lê o arquivo e devolve uma lista de dicionários com os campos informados."""
    if not os.path.exists(arquivo):
        return []
    dados = []
    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if linha:
                partes = linha.split(";")
                registro = {}
                for i in range(len(campos)):
                    if i < len(partes):
                        registro[campos[i]] = partes[i]
                    else:
                        registro[campos[i]] = ""
                dados.append(registro)
    return dados


def salvar(arquivo, campos, lista):
    """Apaga o conteúdo do arquivo e escreve a lista inteira de novo."""
    if not os.path.exists(PASTA):
        os.makedirs(PASTA)
    with open(arquivo, "w", encoding="utf-8") as f:
        for registro in lista:
            valores = []
            for campo in campos:
                valores.append(str(registro.get(campo, "")))
            f.write(";".join(valores) + "\n")
