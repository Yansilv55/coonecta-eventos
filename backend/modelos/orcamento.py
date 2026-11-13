from banco import ler, salvar, ARQ_ORCAMENTOS

CAMPOS = ["id", "email_cliente", "email_prestador", "id_servico", "data_evento",
          "convidados", "detalhes", "status", "resposta"]

# status possíveis: Pendente, Respondido, Recusado


def todos():
    return ler(ARQ_ORCAMENTOS, CAMPOS)


def guardar(lista):
    salvar(ARQ_ORCAMENTOS, CAMPOS, lista)


def buscar_id(id_orcamento):
    for o in todos():
        if o["id"] == id_orcamento:
            return o
    return None


def do_cliente(email):
    lista = []
    for o in todos():
        if o["email_cliente"] == email:
            lista.append(o)
    return lista


def do_prestador(email):
    lista = []
    for o in todos():
        if o["email_prestador"] == email:
            lista.append(o)
    return lista


def data_valida(data):
    """Aceita datas no formato dd/mm/aaaa."""
    if len(data) != 10 or data[2] != "/" or data[5] != "/":
        return False
    dia = data[0:2]
    mes = data[3:5]
    ano = data[6:10]
    if not (dia.isdigit() and mes.isdigit() and ano.isdigit()):
        return False
    return 1 <= int(dia) <= 31 and 1 <= int(mes) <= 12 and int(ano) >= 2026
