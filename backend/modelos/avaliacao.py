from banco import ler, salvar, ARQ_AVALIACOES

CAMPOS = ["email_cliente", "email_prestador", "nota", "comentario"]


def todos():
    return ler(ARQ_AVALIACOES, CAMPOS)


def guardar(lista):
    salvar(ARQ_AVALIACOES, CAMPOS, lista)


def do_prestador(email):
    lista = []
    for a in todos():
        if a["email_prestador"] == email:
            lista.append(a)
    return lista


def ja_avaliou(email_cliente, email_prestador):
    for a in todos():
        if a["email_cliente"] == email_cliente and a["email_prestador"] == email_prestador:
            return True
    return False


def media(email_prestador):
    """Devolve (média, quantidade de avaliações)."""
    soma = 0
    qtd = 0
    for a in do_prestador(email_prestador):
        soma += int(a["nota"])
        qtd += 1
    if qtd == 0:
        return 0, 0
    return soma / qtd, qtd
