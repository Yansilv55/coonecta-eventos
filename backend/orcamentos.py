# =============================================================
# orcamentos.py
# Tudo sobre ORÇAMENTOS (RF07 / UC07, UC08, UC12, UC13):
# - Cliente: pede orçamento, acompanha os pedidos e pode cancelar
# - Prestador: vê os pedidos recebidos e responde (envia ou recusa)
# Os orçamentos ficam salvos em dados/orcamentos.txt
# =============================================================

import datetime
from banco import ler, salvar, novo_id, pedir_texto, ARQ_ORCAMENTOS
import usuarios
import servicos
import notificacoes
import tela

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


def arrumar_data(texto):
    """Coloca as barras sozinho: "20122026", "20-12-2026" ou "20.12.2026"
    viram "20/12/2026"."""
    numeros = ""
    for letra in texto:
        if letra.isdigit():
            numeros = numeros + letra
    if len(numeros) == 8:
        return numeros[0:2] + "/" + numeros[2:4] + "/" + numeros[4:8]
    return texto


def data_valida(data):
    """Aceita datas dd/mm/aaaa que existam de verdade (31/02 não existe)
    e que não estejam no passado."""
    if len(data) != 10 or data[2] != "/" or data[5] != "/":
        return False
    dia = data[0:2]
    mes = data[3:5]
    ano = data[6:10]
    if not (dia.isdigit() and mes.isdigit() and ano.isdigit()):
        return False
    try:
        data_evento = datetime.date(int(ano), int(mes), int(dia))
    except ValueError:
        return False   # data que não existe, como 31/02/2027
    return data_evento >= datetime.date.today()


def formatar_valor(valor):
    """Ex: "1400.5" vira "R$ 1.400,50"."""
    return tela.dinheiro(valor)


def nome_do_servico(id_servico):
    s = servicos.buscar_id(id_servico)
    if s != None:
        return s["nome"]
    return "(serviço removido)"


# ================= TELAS E AÇÕES =================

def mostrar_tabela(lista, quem):
    """Mostra os pedidos como uma tabela, um por linha, com colunas alinhadas.
    quem = "cliente" (mostra o fornecedor) ou "prestador" (mostra o cliente)."""
    if quem == "prestador":
        coluna = "Cliente"
    else:
        coluna = "Fornecedor"
    print()
    print(f"  {'Nº':<4} {'Serviço':<16} {coluna:<13} {'Data':<11} {'Status':<10}")
    tela.linha()
    for o in lista:
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
        print(f"  {o['id']:<4} {tela.cortar(nome_do_servico(o['id_servico']), 16):<16} "
              f"{tela.cortar(nome_outro, 13):<13} {o['data_evento']:<11} {o['status']:<10}")
    tela.linha()


def mostrar(o, quem):
    """Todos os detalhes de um pedido, como um cartão.
    quem = "cliente" ou "prestador" (muda os dados de contato mostrados)."""
    tela.cabecalho_cartao(f"Pedido nº {o['id']}  |  Status: {o['status']}")

    s = servicos.buscar_id(o["id_servico"])
    if s != None:
        tela.campo("Serviço", f"{s['nome']} ({s['categoria']})")
    else:
        tela.campo("Serviço", "(serviço removido)")

    if quem == "prestador":
        cliente = usuarios.buscar(o["email_cliente"])
        if cliente != None:
            tela.campo("Cliente", cliente["nome"])
            tela.campo("Contato", f"{tela.telefone(cliente['telefone'])} | {cliente['email']}")
    else:
        prestador = usuarios.buscar(o["email_prestador"])
        if prestador != None:
            tela.campo("Fornecedor", prestador["nome_negocio"])
            tela.campo("Contato", tela.telefone(prestador["telefone"]))

    tela.campo("Data", o["data_evento"])
    tela.campo("Convidados", o["convidados"])
    tela.campo("Detalhes", o["detalhes"])

    if o["status"] == RESPONDIDO:
        tela.secao("Orçamento do prestador")
        if o["valor"] != "":
            tela.campo("Valor", formatar_valor(o["valor"]))
        tela.campo("Condições", o["resposta"])
        if o["mensagem"] != "":
            tela.campo("Mensagem", o["mensagem"])
    elif o["status"] == RECUSADO:
        tela.secao("Pedido recusado")
        tela.campo("Motivo", o["resposta"])
    elif o["status"] == CANCELADO:
        print("\n  Este pedido foi cancelado pelo cliente.")
    else:
        print("\n  Aguardando resposta do prestador.")
    tela.linha()


def escolher_pedido(lista):
    """Pede o número de um pedido da lista. Devolve o pedido ou None (0 = voltar)."""
    while True:
        numero = input("\nDigite o nº do pedido para ver os detalhes (0 para voltar): ").strip()
        if numero == "0" or numero == "":
            return None
        for o in lista:
            if o["id"] == numero:
                return o
        tela.erro("Pedido não encontrado nesta lista. Use um número da coluna Nº.")


def pedir_data():
    """Pede a data do evento. A pessoa pode digitar só os números (20122026)
    que o sistema coloca as barras sozinho."""
    while True:
        data_evento = arrumar_data(pedir_texto("Data do evento (ex: 20122026 ou 20/12/2026): "))
        if data_valida(data_evento):
            print(f"  Data registrada: {data_evento}")
            return data_evento
        tela.erro("Data inválida. Use dia, mês e ano (ex: 20122026) e uma data que ainda não passou.")


# ---------- Lado do CLIENTE ----------

def pedir(cliente):
    tela.titulo("PEDIR ORÇAMENTO")
    lista_servicos = servicos.todos()
    if len(lista_servicos) == 0:
        print("  Nenhum serviço disponível no momento.")
        return
    servicos.mostrar_lista_curta(lista_servicos)

    while True:
        id_servico = pedir_texto("ID do serviço (0 para voltar): ")
        if id_servico == "0":
            print("  Pedido cancelado.")
            return
        s = servicos.buscar_id(id_servico)
        if s == None:
            tela.erro("Serviço não encontrado. Use um ID da lista acima.")
        elif ja_tem_pendente(cliente["email"], id_servico):
            tela.erro("Você já tem um pedido aguardando resposta para este serviço.")
            print("     Veja em 'Meus orçamentos'.")
            return
        else:
            break

    tela.secao(f"Pedido para: {s['nome']} ({s['categoria']})")
    data_evento = pedir_data()

    while True:
        convidados = pedir_texto("Quantidade de convidados: ")
        if convidados.isdigit() and int(convidados) > 0:
            break
        tela.erro("Digite um número maior que zero.")

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
    tela.mensagem(f"Pedido de orçamento nº {novo['id']} enviado!")


def meus_pedidos(cliente):
    tela.titulo("MEUS ORÇAMENTOS")
    lista = do_cliente(cliente["email"])
    if len(lista) == 0:
        print("  Você ainda não pediu nenhum orçamento.")
        return

    mostrar_tabela(lista, "cliente")

    respondidos = 0
    for o in lista:
        if o["status"] == RESPONDIDO or o["status"] == RECUSADO:
            respondidos = respondidos + 1
    if respondidos == 0:
        print("  Ainda não existem respostas para os seus pedidos.")

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
    tela.mensagem("Pedido cancelado.")


# ---------- Lado do PRESTADOR ----------

def pedidos_recebidos(prestador):
    tela.titulo("PEDIDOS DE ORÇAMENTO RECEBIDOS")
    lista = do_prestador(prestador["email"])
    if len(lista) == 0:
        print("  Você ainda não recebeu nenhum pedido de orçamento.")
        return

    mostrar_tabela(lista, "prestador")

    pendentes = 0
    for o in lista:
        if o["status"] == PENDENTE:
            pendentes = pendentes + 1
    print(f"  {pendentes} pedido(s) aguardando sua resposta.")

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
    tela.titulo("RESPONDER PEDIDO")
    pendentes = []
    for o in do_prestador(prestador["email"]):
        if o["status"] == PENDENTE:
            pendentes.append(o)
    if len(pendentes) == 0:
        print("  Nenhum pedido aguardando resposta.")
        return

    mostrar_tabela(pendentes, "prestador")

    pedido = escolher_pedido(pendentes)
    if pedido == None:
        return
    mostrar(pedido, "prestador")
    responder_pedido(prestador, pedido)


def responder_pedido(prestador, pedido):
    """Envia o orçamento (valor, condições e mensagem) ou recusa o pedido."""
    tela.secao("O que deseja fazer?")
    tela.opcao(1, "Enviar orçamento")
    tela.opcao(2, "Recusar pedido")
    tela.opcao(0, "Voltar")
    opcao = input("Escolha: ").strip()

    if opcao == "1":
        while True:
            valor = pedir_texto("Valor do orçamento (ex: 1400,00): ")
            if servicos.preco_valido(valor):
                break
            tela.erro("Valor inválido. Use só números, com vírgula ou ponto (ex: 1400,00).")
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
        tela.erro("Opção inválida! Nada foi alterado.")
        return

    atualizar(pedido)
    # Avisa o cliente (UC13: "o sistema disponibiliza o orçamento ao cliente")
    notificacoes.criar(pedido["email_cliente"], aviso + " Veja em 'Meus orçamentos'.")
    tela.mensagem("Resposta enviada!")
