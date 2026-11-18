# =============================================================
# orcamentos.py
# Tudo sobre ORÇAMENTOS (RF07 / UC07, UC08, UC12, UC13):
# - Cliente: pede orçamento, acompanha os pedidos e pode cancelar
# - Prestador: vê os pedidos recebidos e responde (envia ou recusa)
# Os orçamentos ficam salvos em dados/orcamentos.txt
# =============================================================

from banco import ler, salvar, novo_id, pedir_texto, ARQ_ORCAMENTOS
import usuarios
import servicos
import notificacoes

# "valor" e "mensagem" ficam no fim da lista, assim os pedidos
# antigos (salvos antes desses campos existirem) continuam funcionando
CAMPOS = ["id", "email_cliente", "email_prestador", "id_servico", "data_evento",
          "convidados", "detalhes", "status", "resposta", "valor", "mensagem"]

PENDENTE = "Pendente"
RESPONDIDO = "Respondido"
RECUSADO = "Recusado"
CANCELADO = "Cancelado"


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


def atualizar(pedido):
    """Troca o pedido antigo pelo atualizado (mesmo id) e salva."""
    lista = todos()
    for i in range(len(lista)):
        if lista[i]["id"] == pedido["id"]:
            lista[i] = pedido
    guardar(lista)


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


def ja_tem_pendente(email_cliente, id_servico):
    """Confere se o cliente já tem um pedido pendente para esse serviço."""
    for o in do_cliente(email_cliente):
        if o["id_servico"] == id_servico and o["status"] == PENDENTE:
            return True
    return False


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


def formatar_valor(valor):
    """Ex: "1400.5" vira "R$ 1400,50"."""
    return f"R$ {float(valor):.2f}".replace(".", ",")


def nome_do_servico(id_servico):
    s = servicos.buscar_id(id_servico)
    if s != None:
        return s["nome"]
    return "(serviço removido)"


# ================= TELAS E AÇÕES =================

def mostrar_resumo(o, quem):
    """Uma linha só, para as listas. quem = "cliente" ou "prestador"."""
    if quem == "prestador":
        outro = usuarios.buscar(o["email_cliente"])
        nome_outro = "Cliente"
        if outro != None:
            nome_outro = outro["nome"]
    else:
        outro = usuarios.buscar(o["email_prestador"])
        nome_outro = "Prestador"
        if outro != None:
            nome_outro = outro["nome_negocio"]
    print(f"  Nº {o['id']} | {nome_do_servico(o['id_servico'])} | {nome_outro} | {o['data_evento']} | {o['status']}")


def mostrar(o, quem):
    """Todos os detalhes de um pedido. quem = "cliente" ou "prestador"."""
    print(f"\nPedido nº {o['id']} | Status: {o['status']}")

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

    if o["status"] == RESPONDIDO:
        print("\n-- Orçamento do prestador --")
        if o["valor"] != "":
            print(f"Valor: {formatar_valor(o['valor'])}")
        print(f"Condições: {o['resposta']}")
        if o["mensagem"] != "":
            print(f"Mensagem: {o['mensagem']}")
    elif o["status"] == RECUSADO:
        print(f"\nMotivo da recusa: {o['resposta']}")
    elif o["status"] == CANCELADO:
        print("\nEste pedido foi cancelado pelo cliente.")
    else:
        print("\nAguardando resposta do prestador.")
    print("-" * 40)


def escolher_pedido(lista):
    """Pede o número de um pedido da lista. Devolve o pedido ou None (0 = voltar)."""
    while True:
        numero = input("\nDigite o nº do pedido para ver os detalhes (0 para voltar): ").strip()
        if numero == "0" or numero == "":
            return None
        for o in lista:
            if o["id"] == numero:
                return o
        print("Pedido não encontrado nesta lista.")


# ---------- Lado do CLIENTE ----------

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
        if s == None:
            print("Serviço não encontrado.")
        elif ja_tem_pendente(cliente["email"], id_servico):
            print("Você já tem um pedido aguardando resposta para este serviço.")
            print("Veja em 'Meus orçamentos'.")
            return
        else:
            break

    print(f"\nPedindo orçamento de: {s['nome']} ({s['categoria']})")

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
        "valor": "",
        "mensagem": "",
    }
    lista.append(novo)
    guardar(lista)

    # Avisa o prestador (UC07: "o sistema encaminha a solicitação ao prestador")
    notificacoes.criar(s["email_prestador"],
                       f"Você recebeu um pedido de orçamento (nº {novo['id']}) de {cliente['nome']} para \"{s['nome']}\".")
    print(f"Pedido de orçamento nº {novo['id']} enviado!")


def meus_pedidos(cliente):
    print("\n--- MEUS ORÇAMENTOS ---")
    lista = do_cliente(cliente["email"])
    if len(lista) == 0:
        print("Você ainda não pediu nenhum orçamento.")
        return

    respondidos = 0
    for o in lista:
        mostrar_resumo(o, "cliente")
        if o["status"] == RESPONDIDO or o["status"] == RECUSADO:
            respondidos = respondidos + 1
    if respondidos == 0:
        print("\nAinda não existem respostas para os seus pedidos.")

    pedido = escolher_pedido(lista)
    if pedido == None:
        return
    mostrar(pedido, "cliente")

    # Enquanto estiver pendente, o cliente pode desistir do pedido
    if pedido["status"] == PENDENTE:
        resposta = input("Deseja cancelar este pedido? (s/n): ").strip().lower()
        if resposta == "s":
            cancelar(cliente, pedido)


def cancelar(cliente, pedido):
    pedido["status"] = CANCELADO
    atualizar(pedido)
    notificacoes.criar(pedido["email_prestador"],
                       f"O pedido de orçamento nº {pedido['id']} foi cancelado por {cliente['nome']}.")
    print("Pedido cancelado.")


# ---------- Lado do PRESTADOR ----------

def pedidos_recebidos(prestador):
    print("\n--- PEDIDOS DE ORÇAMENTO RECEBIDOS ---")
    lista = do_prestador(prestador["email"])
    if len(lista) == 0:
        print("Você ainda não recebeu nenhum pedido de orçamento.")
        return

    pendentes = 0
    for o in lista:
        mostrar_resumo(o, "prestador")
        if o["status"] == PENDENTE:
            pendentes = pendentes + 1
    print(f"\n{pendentes} pedido(s) aguardando sua resposta.")

    pedido = escolher_pedido(lista)
    if pedido == None:
        return
    mostrar(pedido, "prestador")

    # UC12: "o prestador pode responder à solicitação"
    if pedido["status"] == PENDENTE:
        resposta = input("Deseja responder agora? (s/n): ").strip().lower()
        if resposta == "s":
            responder_pedido(prestador, pedido)


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
        mostrar_resumo(o, "prestador")

    pedido = escolher_pedido(pendentes)
    if pedido == None:
        return
    mostrar(pedido, "prestador")
    responder_pedido(prestador, pedido)


def responder_pedido(prestador, pedido):
    """Envia o orçamento (valor, condições e mensagem) ou recusa o pedido."""
    print("1. Enviar orçamento")
    print("2. Recusar pedido")
    print("0. Voltar")
    opcao = input("Escolha: ").strip()

    if opcao == "1":
        while True:
            valor = pedir_texto("Valor do orçamento (ex: 1400,00): ")
            if servicos.preco_valido(valor):
                break
            print("Valor inválido. Use só números, com vírgula ou ponto.")
        pedido["valor"] = valor.replace(",", ".")
        pedido["resposta"] = pedir_texto("Condições (o que inclui, forma de pagamento): ")
        pedido["mensagem"] = input("Mensagem para o cliente (opcional, Enter para pular): ").strip()
        pedido["status"] = RESPONDIDO
        aviso = f"Seu pedido de orçamento nº {pedido['id']} foi respondido por {prestador['nome_negocio']}: {formatar_valor(pedido['valor'])}."
    elif opcao == "2":
        pedido["resposta"] = pedir_texto("Motivo da recusa: ")
        pedido["status"] = RECUSADO
        aviso = f"Seu pedido de orçamento nº {pedido['id']} foi recusado por {prestador['nome_negocio']}."
    elif opcao == "0":
        return
    else:
        print("Opção inválida! Nada foi alterado.")
        return

    atualizar(pedido)
    # Avisa o cliente (UC13: "o sistema disponibiliza o orçamento ao cliente")
    notificacoes.criar(pedido["email_cliente"], aviso + " Veja em 'Meus orçamentos'.")
    print("Resposta enviada!")