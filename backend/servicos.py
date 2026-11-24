# =============================================================
# servicos.py
# Tudo sobre SERVIÇOS: listar, buscar, cadastrar e editar.
# Os serviços ficam salvos em dados/servicos.txt
# =============================================================

from banco import ler, salvar, novo_id, pedir_texto, ARQ_SERVICOS
import usuarios
import avaliacoes
import tela

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
    tela.secao("Categorias")
    for i in range(len(CATEGORIAS)):
        tela.opcao(i + 1, CATEGORIAS[i])
    while True:
        escolha = input("Escolha o número da categoria: ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(CATEGORIAS):
            return CATEGORIAS[int(escolha) - 1]
        tela.erro(f"Categoria inválida! Digite um número de 1 a {len(CATEGORIAS)}.")


def pedir_preco():
    while True:
        preco = pedir_texto("Preço base (ex: 1500,00): ")
        if preco_valido(preco):
            return preco.replace(",", ".")
        tela.erro("Preço inválido. Use só números, com vírgula ou ponto (ex: 1500,00).")


def mostrar(s):
    """Mostra um serviço como um cartão, com as informações alinhadas."""
    tela.cabecalho_cartao(f"[ID {s['id']}]  {s['nome']}")
    tela.campo("Categoria", s["categoria"])
    tela.campo("Descrição", s["descricao"])
    tela.campo("Preço base", tela.dinheiro(s["preco"]))

    dono = usuarios.buscar(s["email_prestador"])
    if dono != None:
        tela.campo("Fornecedor", f"{dono['nome_negocio']} ({dono['nome']})")
        tela.campo("Experiência", f"{dono['anos_experiencia']} ano(s) | {dono['cidade']}")
        tela.campo("Contato", f"{tela.telefone(dono['telefone'])} | {dono['email']}")
        if dono["instagram"] != "":
            tela.campo("Instagram", dono["instagram"])

    nota_media, quantidade = avaliacoes.media(s["email_prestador"])
    if quantidade > 0:
        tela.campo("Avaliação", f"{nota_media:.1f}/5 ({quantidade} avaliação(ões))")
    else:
        tela.campo("Avaliação", "ainda sem avaliações")


def mostrar_lista_curta(lista):
    """Lista resumida (uma linha por serviço), usada para escolher um serviço."""
    print()
    print(f"  {'ID':<4} {'Serviço':<26} {'Categoria':<12} {'Preço':>12}")
    tela.linha()
    for s in lista:
        print(f"  {s['id']:<4} {tela.cortar(s['nome'], 26):<26} "
              f"{tela.cortar(s['categoria'], 12):<12} {tela.dinheiro(s['preco']):>12}")
    tela.linha()


def listar_todos():
    tela.titulo("SERVIÇOS DISPONÍVEIS")
    lista = todos()
    if len(lista) == 0:
        print("  Nenhum serviço cadastrado ainda.")
        return
    tela.subtitulo(f"{len(lista)} serviço(s)")
    for s in lista:
        mostrar(s)
    tela.linha()


def buscar():
    tela.titulo("BUSCAR SERVIÇOS")
    termo = pedir_texto("O que você procura? (ex: buffet, foto, decoração): ")
    encontrados = procurar(termo)
    if len(encontrados) == 0:
        tela.erro(f"Nenhum serviço encontrado para \"{termo}\".")
        return
    tela.subtitulo(f"{len(encontrados)} serviço(s) encontrado(s) para \"{termo}\"")
    for s in encontrados:
        mostrar(s)
    tela.linha()


def cadastrar(prestador):
    tela.titulo("CADASTRAR SERVIÇO")
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
    tela.mensagem(f"Serviço cadastrado! ID: {novo['id']}")


def meus(prestador):
    tela.titulo("MEUS SERVIÇOS")
    lista = do_prestador(prestador["email"])
    if len(lista) == 0:
        print("  Você ainda não cadastrou nenhum serviço.")
        return
    for s in lista:
        mostrar(s)
    tela.linha()


def editar(prestador):
    tela.titulo("EDITAR SERVIÇO")
    lista_do_prestador = do_prestador(prestador["email"])
    if len(lista_do_prestador) == 0:
        print("  Você ainda não cadastrou nenhum serviço.")
        return
    mostrar_lista_curta(lista_do_prestador)

    id_servico = input("ID do serviço que deseja editar (0 para voltar): ").strip()
    if id_servico == "0" or id_servico == "":
        return

    lista = todos()
    servico = None
    for s in lista:
        if s["id"] == id_servico and s["email_prestador"] == prestador["email"]:
            servico = s
    if servico == None:
        tela.erro("Serviço não encontrado entre os seus. Use um ID da lista acima.")
        return

    print("\n  Deixe em branco e aperte Enter para manter o valor atual.")

    novo = input(f"Nome [{servico['nome']}]: ").strip()
    if novo != "":
        servico["nome"] = novo

    novo = input(f"Descrição [{servico['descricao']}]: ").strip()
    if novo != "":
        servico["descricao"] = novo

    novo = input(f"Preço base [{tela.dinheiro(servico['preco'])}]: ").strip()
    if novo != "":
        if preco_valido(novo):
            servico["preco"] = novo.replace(",", ".")
        else:
            tela.erro("Preço inválido. O preço não foi alterado.")

    guardar(lista)
    tela.mensagem("Serviço atualizado!")


def excluir(prestador):
    tela.titulo("EXCLUIR SERVIÇO")
    lista_do_prestador = do_prestador(prestador["email"])
    if len(lista_do_prestador) == 0:
        print("  Você ainda não cadastrou nenhum serviço.")
        return
    mostrar_lista_curta(lista_do_prestador)

    id_servico = input("ID do serviço que deseja excluir (0 para voltar): ").strip()
    if id_servico == "0" or id_servico == "":
        return

    nova_lista = []
    nome = ""
    achou = False
    for s in todos():
        if s["id"] == id_servico and s["email_prestador"] == prestador["email"]:
            achou = True
            nome = s["nome"]
        else:
            nova_lista.append(s)

    if not achou:
        tela.erro("Serviço não encontrado entre os seus. Use um ID da lista acima.")
        return

    confirmar = input(f"Tem certeza que deseja excluir \"{nome}\"? (s/n): ").strip().lower()
    if confirmar != "s":
        print("  Nada foi excluído.")
        return

    guardar(nova_lista)
    tela.mensagem("Serviço excluído!")
