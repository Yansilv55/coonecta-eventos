# =============================================================
# orcamentos.py
# Tudo sobre ORÇAMENTOS: o cliente pede, o prestador responde.
# Os orçamentos ficam salvos em dados/orcamentos.txt
# =============================================================

from banco import ler, salvar, novo_id, pedir_texto, ARQ_ORCAMENTOS
import usuarios
import servicos

CAMPOS = ["id", "email_cliente", "email_prestador", "id_servico", "data_evento",
          "convidados", "detalhes", "status", "resposta"]

PENDENTE = "Pendente"
RESPONDIDO = "Respondido"
RECUSADO = "Recusado"


# ================= DADOS E VALIDAÇÕES =================

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
    """Aceita datas no formato dd/mm/aaaa, com ano a partir de 2026."""
    if len(data) != 10 or data[2] != "/" or data[5] != "/":
        return False
    dia = data[0:2]
    mes = data[3:5]
    ano = data[6:10]
    if not (dia.isdigit() and mes.isdigit() and ano.isdigit()):
        return False
    return 1 <= int(dia) <= 31 and 1 <= int(mes) <= 12 and int(ano) >= 2026


# ================= TELAS E AÇÕES =================

def mostrar(o, quem):
    """quem = "cliente" ou "prestador" (muda os dados de contato mostrados)."""
    print(f"\nPedido nº {o['id']} | {o['status']}")

    s = servicos.buscar_id(o["id_servico"])
    if s != None:
        print(f"Serviço: {s['nome']} ({s['categoria']})")
    else:
        print("Serviço: (serviço removido)")

    if quem == "prestador":
        cliente = usuarios.buscar(o["email_cliente"])
        if cliente != None:
            print(f"Cliente: {cliente['nome']} | Telefone: {cliente['telefone']} | E-mail: {cliente['email']}")
    else:
        prestador = usuarios.buscar(o["email_prestador"])
        if prestador != None:
            print(f"Prestador: {prestador['nome_negocio']} | Telefone: {prestador['telefone']}")

    print(f"Data do evento: {o['data_evento']}")
    print(f"Convidados: {o['convidados']}")
    print(f"Detalhes: {o['detalhes']}")
    if o["resposta"] != "":
        print(f"Resposta: {o['resposta']}")
    print("-" * 40)


def pedir(cliente):
    print("\n--- PEDIR ORÇAMENTO ---")
    if len(servicos.todos()) == 0:
        print("Nenhum serviço disponível no momento.")
        return
    servicos.listar_todos()

    while True:
        id_servico = pedir_texto("ID do serviço (ou 0 para cancelar): ")
        if id_servico == "0":
            print("Pedido cancelado.")
            return
        s = servicos.buscar_id(id_servico)
        if s != None:
            break
        print("Serviço não encontrado.")

    while True:
        data_evento = pedir_texto("Data do evento (dd/mm/aaaa): ")
        if data_valida(data_evento):
            break
        print("Data inválida. Use dd/mm/aaaa, com ano a partir de 2026.")

    while True:
        convidados = pedir_texto("Quantidade de convidados: ")
        if convidados.isdigit() and int(convidados) > 0:
            break
        print("Digite um número maior que zero.")

    detalhes = pedir_texto("Detalhes do evento (local, horário, o que precisa): ")

    lista = todos()
    novo = {
        "id": novo_id(lista),
        "email_cliente": cliente["email"],
        "email_prestador": s["email_prestador"],
        "id_servico": id_servico,
        "data_evento": data_evento,
        "convidados": convidados,
        "detalhes": detalhes,
        "status": PENDENTE,
        "resposta": "",
    }
    lista.append(novo)
    guardar(lista)
    print("Pedido de orçamento enviado!")


def meus_pedidos(cliente):
    print("\n--- MEUS ORÇAMENTOS ---")
    lista = do_cliente(cliente["email"])
    if len(lista) == 0:
        print("Você ainda não pediu nenhum orçamento.")
        return
    for o in lista:
        mostrar(o, "cliente")


def pedidos_recebidos(prestador):
    print("\n--- PEDIDOS DE ORÇAMENTO RECEBIDOS ---")
    lista = do_prestador(prestador["email"])
    if len(lista) == 0:
        print("Você ainda não recebeu nenhum pedido de orçamento.")
        return
    for o in lista:
        mostrar(o, "prestador")


def responder(prestador):
    print("\n--- RESPONDER PEDIDO ---")
    pendentes = []
    for o in do_prestador(prestador["email"]):
        if o["status"] == PENDENTE:
            pendentes.append(o)
    if len(pendentes) == 0:
        print("Nenhum pedido aguardando resposta.")
        return
    for o in pendentes:
        mostrar(o, "prestador")

    id_pedido = pedir_texto("ID do pedido que deseja responder: ")

    lista = todos()
    pedido = None
    for o in lista:
        if o["id"] == id_pedido and o["email_prestador"] == prestador["email"] and o["status"] == PENDENTE:
            pedido = o
    if pedido == None:
        print("Pedido não encontrado entre os pendentes.")
        return

    print("1. Enviar orçamento")
    print("2. Recusar pedido")
    opcao = input("Escolha: ").strip()
    if opcao == "1":
        pedido["resposta"] = pedir_texto("Valor e condições: ")
        pedido["status"] = RESPONDIDO
    elif opcao == "2":
        pedido["resposta"] = pedir_texto("Motivo da recusa: ")
        pedido["status"] = RECUSADO
    else:
        print("Opção inválida! Nada foi alterado.")
        return

    guardar(lista)
    print("Resposta enviada!")


def avisos_cliente(cliente):
    quantidade = 0
    for o in do_cliente(cliente["email"]):
        if o["status"] != PENDENTE:
            quantidade = quantidade + 1
    if quantidade > 0:
        print(f"[Aviso] Você tem {quantidade} orçamento(s) com resposta. Veja em 'Meus orçamentos'.")


def avisos_prestador(prestador):
    quantidade = 0
    for o in do_prestador(prestador["email"]):
        if o["status"] == PENDENTE:
            quantidade = quantidade + 1
    if quantidade > 0:
        print(f"[Aviso] Você tem {quantidade} pedido(s) de orçamento aguardando resposta.")
