# =============================================================
# servicos.py
# Tudo sobre SERVIÇOS: listar, buscar, cadastrar e editar.
# Os serviços ficam salvos em dados/servicos.txt
# =============================================================

from banco import ler, salvar, novo_id, pedir_texto, ARQ_SERVICOS
import usuarios
import avaliacoes

CAMPOS = ["id", "email_prestador", "categoria", "nome", "descricao", "preco"]

CATEGORIAS = ["Buffet", "Fotografia", "Decoração", "Música", "Espaço para eventos", "Cerimonial"]


# ================= DADOS E VALIDAÇÕES =================

def todos():
    return ler(ARQ_SERVICOS, CAMPOS)


def guardar(lista):
    salvar(ARQ_SERVICOS, CAMPOS, lista)


def buscar_id(id_servico):
    for s in todos():
        if s["id"] == id_servico:
            return s
    return None


def do_prestador(email):
    lista = []
    for s in todos():
        if s["email_prestador"] == email:
            lista.append(s)
    return lista


def procurar(termo):
    """Procura o termo no nome, categoria, descrição e nome do negócio."""
    termo = termo.lower()
    encontrados = []
    for s in todos():
        dono = usuarios.buscar(s["email_prestador"])
        negocio = ""
        if dono != None:
            negocio = dono["nome_negocio"]
        texto = s["nome"] + " " + s["categoria"] + " " + s["descricao"] + " " + negocio
        if termo in texto.lower():
            encontrados.append(s)
    return encontrados


def preco_valido(texto):
    """Aceita números com vírgula ou ponto. Ex: 1500, 1500,00 ou 1500.50"""
    texto = texto.replace(",", ".")
    if texto.count(".") > 1:
        return False
    sem_ponto = texto.replace(".", "")
    return sem_ponto != "" and sem_ponto.isdigit()


# ================= TELAS E AÇÕES =================

def escolher_categoria():
    print("Categorias:")
    for i in range(len(CATEGORIAS)):
        print(f"{i + 1}. {CATEGORIAS[i]}")
    while True:
        escolha = input("Escolha o número da categoria: ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(CATEGORIAS):
            return CATEGORIAS[int(escolha) - 1]
        print("Categoria inválida!")


def pedir_preco():
    while True:
        preco = pedir_texto("Preço base (ex: 1500,00): ")
        if preco_valido(preco):
            return preco.replace(",", ".")
        print("Preço inválido. Use só números, com vírgula ou ponto.")


def mostrar(s):
    preco = float(s["preco"])
    print(f"\nID: {s['id']}")
    print(f"{s['nome']} ({s['categoria']})")
    print(f"Descrição: {s['descricao']}")
    print(f"Preço base: R$ {preco:.2f}".replace(".", ","))

    dono = usuarios.buscar(s["email_prestador"])
    if dono != None:
        print(f"Negócio: {dono['nome_negocio']} | Responsável: {dono['nome']}")
        print(f"Atua há {dono['anos_experiencia']} ano(s) | {dono['cidade']}")
        print(f"Contato: {dono['telefone']} | {dono['email']}")
        if dono["instagram"] != "":
            print(f"Instagram: {dono['instagram']}")

    nota_media, quantidade = avaliacoes.media(s["email_prestador"])
    if quantidade > 0:
        print(f"Avaliação: {nota_media:.1f}/5 ({quantidade} avaliação(ões))")
    else:
        print("Avaliação: ainda sem avaliações")
    print("-" * 40)


def listar_todos():
    print("\n--- SERVIÇOS DISPONÍVEIS ---")
    lista = todos()
    if len(lista) == 0:
        print("Nenhum serviço cadastrado ainda.")
        return
    for s in lista:
        mostrar(s)


def buscar():
    print("\n--- BUSCAR SERVIÇOS ---")
    termo = pedir_texto("O que você procura? (ex: buffet, foto, decoração): ")
    encontrados = procurar(termo)
    if len(encontrados) == 0:
        print(f"Nenhum serviço encontrado para \"{termo}\".")
        return
    print(f"{len(encontrados)} serviço(s) encontrado(s):")
    for s in encontrados:
        mostrar(s)


def cadastrar(prestador):
    print("\n--- CADASTRAR SERVIÇO ---")
    categoria = escolher_categoria()
    nome = pedir_texto("Nome do serviço: ")
    descricao = pedir_texto("Descrição: ")
    preco = pedir_preco()

    lista = todos()
    novo = {
        "id": novo_id(lista),
        "email_prestador": prestador["email"],
        "categoria": categoria,
        "nome": nome,
        "descricao": descricao,
        "preco": preco,
    }
    lista.append(novo)
    guardar(lista)
    print(f"Serviço cadastrado! ID: {novo['id']}")


def meus(prestador):
    print("\n--- MEUS SERVIÇOS ---")
    lista = do_prestador(prestador["email"])
    if len(lista) == 0:
        print("Você ainda não cadastrou nenhum serviço.")
        return
    for s in lista:
        mostrar(s)


def editar(prestador):
    print("\n--- EDITAR SERVIÇO ---")
    lista_do_prestador = do_prestador(prestador["email"])
    if len(lista_do_prestador) == 0:
        print("Você ainda não cadastrou nenhum serviço.")
        return
    for s in lista_do_prestador:
        print(f"{s['id']} - {s['nome']} ({s['categoria']})")

    id_servico = input("ID do serviço que deseja editar: ").strip()

    lista = todos()
    servico = None
    for s in lista:
        if s["id"] == id_servico and s["email_prestador"] == prestador["email"]:
            servico = s
    if servico == None:
        print("Serviço não encontrado entre os seus.")
        return

    print("Deixe em branco e aperte Enter para manter o valor atual.")

    novo = input(f"Nome [{servico['nome']}]: ").strip()
    if novo != "":
        servico["nome"] = novo

    novo = input(f"Descrição [{servico['descricao']}]: ").strip()
    if novo != "":
        servico["descricao"] = novo

    novo = input(f"Preço base [{servico['preco']}]: ").strip()
    if novo != "":
        if preco_valido(novo):
            servico["preco"] = novo.replace(",", ".")
        else:
            print("Preço inválido. O preço não foi alterado.")

    guardar(lista)
    print("Serviço atualizado!")
