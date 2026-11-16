# =============================================================
# usuarios.py
# =============================================================

from banco import ler, salvar, ARQ_USUARIOS

# Campos do usuário, na ordem em que ficam no .txt
CAMPOS = ["tipo", "nome", "email", "senha", "nome_negocio", "categoria"]

CLIENTE = "Cliente"
PRESTADOR = "Prestador"
CATEGORIAS = ["Buffet", "Fotografia", "Decoração", "Música", "Espaço para eventos"]


# -------------------------------------------------------------
# Ler e salvar
# -------------------------------------------------------------

def todos():
    """Devolve a lista com todos os usuários cadastrados."""
    return ler(ARQ_USUARIOS, CAMPOS)


def guardar(lista):
    """Salva a lista inteira de usuários no .txt."""
    salvar(ARQ_USUARIOS, CAMPOS, lista)


def buscar_por_email(email):
    """Procura um usuário pelo e-mail. Devolve o usuário ou None."""
    for usuario in todos():
        if usuario["email"] == email:
            return usuario
    return None


# -------------------------------------------------------------
# Funções que ajudam a validar o que o usuário digita
# -------------------------------------------------------------

def texto_valido(texto):
    """Não pode ficar vazio e não pode ter ';' (ele separa os campos no .txt)."""
    if texto == "":
        print("Erro: este campo não pode ficar vazio.")
        return False
    if ";" in texto:
        print("Erro: não use o caractere ';'.")
        return False
    return True


def email_valido(email):
    """Confere se o e-mail tem cara de e-mail (tem @ e ponto depois dele)."""
    if "@" not in email or "." not in email.split("@")[-1]:
        print("Erro: e-mail inválido. Exemplo: nome@email.com")
        return False
    return True


def pedir_senha():
    """Pede a senha duas vezes. Devolve a senha ou None se der errado."""
    senha = input("Senha (mínimo 4 caracteres): ").strip()
    if len(senha) < 4:
        print("Erro: a senha precisa ter pelo menos 4 caracteres.")
        return None
    if ";" in senha:
        print("Erro: não use o caractere ';'.")
        return None
    confirmar = input("Confirme a senha: ").strip()
    if senha != confirmar:
        print("Erro: as senhas não são iguais.")
        return None
    return senha


def escolher_categoria():
    """Mostra as categorias e devolve a escolhida, ou None se for inválida."""
    print("Categorias:")
    for i in range(len(CATEGORIAS)):
        print(f"{i + 1}. {CATEGORIAS[i]}")
    escolha = input("Escolha o número: ").strip()
    if not escolha.isdigit() or not (1 <= int(escolha) <= len(CATEGORIAS)):
        print("Erro: categoria inválida.")
        return None
    return CATEGORIAS[int(escolha) - 1]


# -------------------------------------------------------------
# Cadastro
# -------------------------------------------------------------

def cadastrar_usuario(email=""):
    """Pergunta se é Cliente ou Prestador e chama o cadastro certo."""
    print("\n--- CRIAR CONTA ---")
    print("1. Sou Cliente (quero contratar serviços)")
    print("2. Sou Prestador (quero oferecer serviços)")
    opcao = input("Escolha: ").strip()

    if opcao == "1":
        cadastrar(CLIENTE, email)
    elif opcao == "2":
        cadastrar(PRESTADOR, email)
    else:
        print("Opção inválida. Cadastro cancelado.")


def cadastrar(tipo, email=""):
    """Cadastra um Cliente ou um Prestador.
    Se o e-mail já vier do login, não pergunta de novo."""
    print(f"\n--- CADASTRO DE {tipo.upper()} ---")

    nome = input("Nome: ").strip()
    if not texto_valido(nome):
        return

    if email == "":
        email = input("E-mail: ").strip().lower()
    if not texto_valido(email) or not email_valido(email):
        return
    if buscar_por_email(email):
        print("Erro: este e-mail já está cadastrado.")
        return

    senha = pedir_senha()
    if senha is None:
        return

    # Só o prestador tem nome do negócio e categoria
    nome_negocio = ""
    categoria = ""
    if tipo == PRESTADOR:
        nome_negocio = input("Nome do seu negócio: ").strip()
        if not texto_valido(nome_negocio):
            return
        categoria = escolher_categoria()
        if categoria is None:
            return

    novo = {
        "tipo": tipo,
        "nome": nome,
        "email": email,
        "senha": senha,
        "nome_negocio": nome_negocio,
        "categoria": categoria,
    }

    lista = todos()
    lista.append(novo)
    guardar(lista)
    print(f"\n{tipo} cadastrado com sucesso! Agora é só fazer login.")


# -------------------------------------------------------------
# Login
# -------------------------------------------------------------

def fazer_login():
    """Pede e-mail e senha. Devolve o usuário se der certo, ou None."""
    print("\n--- LOGIN ---")
    email = input("E-mail: ").strip().lower()
    usuario = buscar_por_email(email)

    # E-mail não existe: oferece o cadastro
    if usuario is None:
        resposta = input("E-mail não encontrado. Deseja criar uma conta? (s/n): ").strip().lower()
        if resposta == "s":
            cadastrar_usuario(email)
        return None

    # Dá 3 chances para acertar a senha
    for tentativa in range(3):
        senha = input("Senha: ").strip()
        if senha == usuario["senha"]:
            print(f"\nBem-vindo(a), {usuario['nome']}! ({usuario['tipo']})")
            return usuario
        restam = 2 - tentativa
        if restam > 0:
            print(f"Senha incorreta. Você tem mais {restam} tentativa(s).")

    print("Senha incorreta 3 vezes. Voltando ao menu.")
    return None


# -------------------------------------------------------------
# Perfil (ver e editar os próprios dados)
# -------------------------------------------------------------

def ver_perfil(usuario):
    print("\n--- MEU PERFIL ---")
    print(f"Tipo: {usuario['tipo']}")
    print(f"Nome: {usuario['nome']}")
    print(f"E-mail: {usuario['email']}")
    if usuario["tipo"] == PRESTADOR:
        print(f"Negócio: {usuario['nome_negocio']}")
        print(f"Categoria: {usuario['categoria']}")


def editar_perfil(usuario):
    """Deixa o usuário mudar nome, senha e (se for prestador) negócio e categoria.
    O e-mail não muda, porque ele identifica a conta."""
    print("\n--- EDITAR PERFIL ---")
    print("Deixe em branco e aperte Enter para não mudar.")

    novo_nome = input(f"Nome [{usuario['nome']}]: ").strip()
    if novo_nome != "":
        if not texto_valido(novo_nome):
            return
        usuario["nome"] = novo_nome

    if usuario["tipo"] == PRESTADOR:
        novo_negocio = input(f"Nome do negócio [{usuario['nome_negocio']}]: ").strip()
        if novo_negocio != "":
            if not texto_valido(novo_negocio):
                return
            usuario["nome_negocio"] = novo_negocio

        mudar = input(f"Categoria atual: {usuario['categoria']}. Deseja mudar? (s/n): ").strip().lower()
        if mudar == "s":
            categoria = escolher_categoria()
            if categoria is None:
                return
            usuario["categoria"] = categoria

    mudar_senha = input("Deseja mudar a senha? (s/n): ").strip().lower()
    if mudar_senha == "s":
        atual = input("Senha atual: ").strip()
        if atual != usuario["senha"]:
            print("Erro: senha atual incorreta.")
            return
        nova = pedir_senha()
        if nova is None:
            return
        usuario["senha"] = nova

    # Troca o usuário antigo pelo atualizado na lista e salva
    lista = todos()
    for i in range(len(lista)):
        if lista[i]["email"] == usuario["email"]:
            lista[i] = usuario
    guardar(lista)
    print("Perfil atualizado com sucesso!")


def listar_prestadores():
    """Devolve só os usuários que são prestadores (útil para serviços e avaliações)."""
    lista = []
    for usuario in todos():
        if usuario["tipo"] == PRESTADOR:
            lista.append(usuario)
    return lista