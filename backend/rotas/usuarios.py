# =============================================================
# rotas/usuarios.py
# Ações de usuário: cadastro e login
# =============================================================

from modelos.usuario import criar_usuario, CATEGORIAS

# Lista onde os usuários ficam guardados enquanto o programa está aberto.
# Quando o programa fecha, a lista é apagada (ainda não temos banco de dados).
usuarios = []


def buscar_por_email(email):
    """Procura um usuário pelo e-mail. Devolve o usuário ou None."""
    for usuario in usuarios:
        if usuario["email"] == email:
            return usuario
    return None


def cadastrar_usuario(email=""):
    """Cadastra um novo usuário. Se já vier um e-mail (do login), não pergunta de novo."""
    print("\n--- CADASTRO ---")
    nome = input("Nome: ").strip()
    if not email:
        email = input("E-mail: ").strip()
    senha = input("Senha: ").strip()

    # Regra 1: nenhum campo pode ficar vazio
    if not nome or not email or not senha:
        print("Erro: preencha todos os campos.")
        return

    # Regra 2: não pode usar ";" (vai separar os campos quando tivermos o .txt)
    if ";" in nome + email + senha:
        print("Erro: não use o caractere ';'.")
        return

    # Regra 3: e-mail não pode repetir
    if buscar_por_email(email):
        print("Erro: este e-mail já está cadastrado.")
        return

    print("Tipo de conta:")
    print("1. Cliente")
    print("2. Prestador de serviço")
    opcao = input("Escolha: ").strip()

    if opcao == "1":
        novo = criar_usuario("Cliente", nome, email, senha)
    elif opcao == "2":
        nome_negocio = input("Nome do seu negócio: ").strip()
        print("Categoria principal:")
        for i in range(len(CATEGORIAS)):
            print(f"{i + 1}. {CATEGORIAS[i]}")
        escolha = input("Escolha: ").strip()
        if not escolha.isdigit() or not (1 <= int(escolha) <= len(CATEGORIAS)):
            print("Categoria inválida. Cadastro cancelado.")
            return
        categoria = CATEGORIAS[int(escolha) - 1]
        novo = criar_usuario("Prestador", nome, email, senha, nome_negocio, categoria)
    else:
        print("Opção inválida. Cadastro cancelado.")
        return

    usuarios.append(novo)
    print("Cadastro realizado com sucesso! Agora é só fazer login.")


def fazer_login():
    """Pede e-mail e senha. Devolve o usuário se der certo, ou None se não der."""
    print("\n--- LOGIN ---")
    email = input("E-mail: ").strip()
    usuario = buscar_por_email(email)

    # E-mail não existe: oferece o cadastro
    if usuario is None:
        resposta = input("E-mail não encontrado. Deseja se cadastrar? (s/n): ").strip().lower()
        if resposta == "s":
            cadastrar_usuario(email)
        return None

    senha = input("Senha: ").strip()
    if senha != usuario["senha"]:
        print("Senha incorreta.")
        return None

    print(f"\nBem-vindo(a), {usuario['nome']}!")
    return usuario