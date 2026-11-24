# =============================================================
# portfolio.py
# Tudo sobre o PORTFÓLIO dos prestadores (RF10 / UC05)
# - Prestador cadastra os trabalhos já feitos (título, descrição e link da foto)
# - Cliente vê o portfólio de um fornecedor
# Os trabalhos ficam salvos em dados/portfolio.txt
# =============================================================

from banco import ler, salvar, novo_id, pedir_texto, ARQ_PORTFOLIO
import usuarios
import tela

CAMPOS = ["id", "email_prestador", "titulo", "descricao", "foto"]


# ================= DADOS E VALIDAÇÕES =================

def todos():
    return ler(ARQ_PORTFOLIO, CAMPOS)


def guardar(lista):
    salvar(ARQ_PORTFOLIO, CAMPOS, lista)


def do_prestador(email):
    lista = []
    for p in todos():
        if p["email_prestador"] == email:
            lista.append(p)
    return lista


# ================= TELAS E AÇÕES =================

def mostrar(lista):
    """Mostra cada trabalho do portfólio como um cartão."""
    if len(lista) == 0:
        print("  Nenhum trabalho no portfólio ainda.")
        return
    tela.subtitulo(f"{len(lista)} trabalho(s)")
    for p in lista:
        tela.cabecalho_cartao(p["titulo"])
        tela.campo("Descrição", p["descricao"])
        if p["foto"] != "":
            tela.campo("Foto", p["foto"])
    tela.linha()


def cadastrar(prestador):
    tela.titulo("ADICIONAR TRABALHO AO PORTFÓLIO")
    titulo = pedir_texto("Título do trabalho (ex: Casamento na praia 2025): ")
    descricao = pedir_texto("Descrição: ")
    foto = input("Link da foto (opcional, Enter para pular): ").strip()

    lista = todos()
    lista.append({
        "id": novo_id(lista),
        "email_prestador": prestador["email"],
        "titulo": titulo,
        "descricao": descricao,
        "foto": foto,
    })
    guardar(lista)
    tela.mensagem("Trabalho adicionado ao portfólio!")


def meu(prestador):
    tela.titulo("MEU PORTFÓLIO")
    mostrar(do_prestador(prestador["email"]))


def ver_de_um_prestador():
    tela.titulo("PORTFÓLIO DE UM FORNECEDOR")
    prestador = usuarios.escolher_prestador()
    if prestador == None:
        return
    tela.secao(f"Portfólio de {prestador['nome_negocio']}")
    mostrar(do_prestador(prestador["email"]))
