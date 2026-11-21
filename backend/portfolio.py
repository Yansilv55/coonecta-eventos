# =============================================================
# portfolio.py
# Tudo sobre o PORTFÓLIO dos prestadores (RF10 / UC05)
# - Prestador cadastra os trabalhos já feitos (título, descrição e link da foto)
# - Cliente vê o portfólio de um fornecedor
# Os trabalhos ficam salvos em dados/portfolio.txt
# =============================================================

from banco import ler, salvar, novo_id, pedir_texto, ARQ_PORTFOLIO
import usuarios

CAMPOS = ["id", "email_prestador", "titulo", "descricao", "foto"]


def todos():
    return ler(ARQ_PORTFOLIO, CAMPOS)


def do_prestador(email):
    return [p for p in todos() if p["email_prestador"] == email]


def mostrar(lista):
    if len(lista) == 0:
        print("Nenhum trabalho no portfólio ainda.")
        return
    for p in lista:
        print(f"\n{p['titulo']}")
        print(f"Descrição: {p['descricao']}")
        if p["foto"] != "":
            print(f"Foto: {p['foto']}")
        print("-" * 40)


def cadastrar(prestador):
    print("\n--- ADICIONAR TRABALHO AO PORTFÓLIO ---")
    lista = todos()
    lista.append({
        "id": novo_id(lista),
        "email_prestador": prestador["email"],
        "titulo": pedir_texto("Título do trabalho: "),
        "descricao": pedir_texto("Descrição: "),
        "foto": input("Link da foto (opcional): ").strip(),
    })
    salvar(ARQ_PORTFOLIO, CAMPOS, lista)
    print("Trabalho adicionado ao portfólio!")


def meu(prestador):
    print("\n--- MEU PORTFÓLIO ---")
    mostrar(do_prestador(prestador["email"]))


def ver_de_um_prestador():
    print("\n--- PORTFÓLIO DE UM FORNECEDOR ---")
    email = pedir_texto("E-mail do prestador: ")
    prestador = usuarios.buscar(email)
    if prestador is None or prestador["tipo"] != usuarios.PRESTADOR:
        print("Prestador não encontrado.")
        return
    print(f"Portfólio de {prestador['nome_negocio']}:")
    mostrar(do_prestador(email))