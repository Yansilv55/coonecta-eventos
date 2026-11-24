# =============================================================
# avaliacoes.py
# Tudo sobre AVALIAÇÕES: o cliente dá nota ao prestador,
# o prestador vê suas notas e a média.
# As avaliações ficam salvas em dados/avaliacoes.txt
# =============================================================

from banco import ler, salvar, pedir_texto, ARQ_AVALIACOES
import usuarios
import servicos
import orcamentos
import tela

CAMPOS = ["email_cliente", "email_prestador", "nota", "comentario"]


# ================= DADOS E VALIDAÇÕES =================

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
    """Devolve (média, quantidade de avaliações). Sem avaliações: (0, 0)."""
    soma = 0
    quantidade = 0
    for a in do_prestador(email_prestador):
        soma = soma + int(a["nota"])
        quantidade = quantidade + 1
    if quantidade == 0:
        return 0, 0
    return soma / quantidade, quantidade


# ================= TELAS E AÇÕES =================

def prestadores_do_cliente(cliente):
    """Prestadores que já responderam um orçamento deste cliente."""
    emails = []
    for o in orcamentos.do_cliente(cliente["email"]):
        if o["status"] == orcamentos.RESPONDIDO and o["email_prestador"] not in emails:
            emails.append(o["email_prestador"])

    prestadores = []
    for email in emails:
        p = usuarios.buscar(email)
        if p != None:
            prestadores.append(p)
    return prestadores


def avaliar(cliente):
    tela.titulo("AVALIAR UM PRESTADOR")
    prestadores = prestadores_do_cliente(cliente)
    if len(prestadores) == 0:
        print("  Você só pode avaliar prestadores que responderam um orçamento seu.")
        return

    disponiveis = []
    for p in prestadores:
        if not ja_avaliou(cliente["email"], p["email"]):
            disponiveis.append(p)
    if len(disponiveis) == 0:
        print("  Você já avaliou todos os prestadores que te atenderam.")
        return

    tela.secao("Prestadores que te atenderam")
    for i in range(len(disponiveis)):
        tela.opcao(i + 1, f"{disponiveis[i]['nome_negocio']} ({disponiveis[i]['nome']})")
    posicao = tela.escolher_da_lista(len(disponiveis), "Escolha o prestador (0 para voltar): ")
    if posicao == -1:
        return
    prestador = disponiveis[posicao]

    while True:
        nota = input("Nota (1 a 5): ").strip()
        if nota in ["1", "2", "3", "4", "5"]:
            break
        tela.erro("Nota inválida! Digite um número de 1 a 5.")

    comentario = pedir_texto("Comentário: ")

    lista = todos()
    lista.append({
        "email_cliente": cliente["email"],
        "email_prestador": prestador["email"],
        "nota": nota,
        "comentario": comentario,
    })
    guardar(lista)
    tela.mensagem("Avaliação registrada!")


def estrelas(nota):
    """Ex: 4 vira "★★★★☆"."""
    return "★" * int(nota) + "☆" * (5 - int(nota))


def mostrar_do_prestador(email):
    lista = do_prestador(email)
    if len(lista) == 0:
        print("  Ainda não há avaliações.")
        return
    nota_media, quantidade = media(email)
    tela.subtitulo(f"Média: {nota_media:.1f}/5  ({quantidade} avaliação(ões))")
    for a in lista:
        cliente = usuarios.buscar(a["email_cliente"])
        nome_cliente = "Cliente"
        if cliente != None:
            nome_cliente = cliente["nome"]
        tela.cabecalho_cartao(f"{estrelas(a['nota'])}  {a['nota']}/5  -  {nome_cliente}")
        tela.campo("Comentário", a["comentario"])
    tela.linha()


def minhas(prestador):
    tela.titulo("MINHAS AVALIAÇÕES")
    mostrar_do_prestador(prestador["email"])


def ver_de_um_servico():
    tela.titulo("AVALIAÇÕES DE UM SERVIÇO")
    lista_servicos = servicos.todos()
    if len(lista_servicos) == 0:
        print("  Nenhum serviço cadastrado ainda.")
        return
    servicos.mostrar_lista_curta(lista_servicos)
    id_servico = input("ID do serviço (0 para voltar): ").strip()
    if id_servico == "0" or id_servico == "":
        return
    s = servicos.buscar_id(id_servico)
    if s == None:
        tela.erro("Serviço não encontrado. Use um ID da lista acima.")
        return
    dono = usuarios.buscar(s["email_prestador"])
    if dono != None:
        tela.secao(f"Avaliações de {dono['nome_negocio']}")
    mostrar_do_prestador(s["email_prestador"])
