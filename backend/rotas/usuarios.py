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

    print("Tipo de conta:")
    print("1. Cliente")
    print("2. Prestador de serviço")
    opcao = input("Escolha: ").strip()

    if opcao != "1" and opcao != "2":
        print("Opção inválida. Cadastro cancelado.")
        return

    nome = input("Nome: ").strip()
    data_nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()
    if not email:
        email = input("E-mail: ").strip()
    senha = input("Senha: ").strip()
    confirmar_senha = input("Confirme a senha: ").strip()

    if not senha:
        print("Erro: a senha não pode ficar vazia.")
        return

    if senha != confirmar_senha:
        print("Erro: as senhas não coincidem.")
        return

    # Regra 1: nenhum campo pode ficar vazio
    if not nome or not email or not senha:
        print("Erro: preencha todos os campos.")
        return

    # Regra 2: não pode usar ";" (vai separar os campos quando tivermos o .txt)
    if ";" in nome + data_nascimento + email + senha:
        print("Erro: não use o caractere ';'.")
        return

    # Regra 3: e-mail não pode repetir
    if buscar_por_email(email):
        print("Erro: este e-mail já está cadastrado.")
        return

    if opcao == "1":
        novo = criar_usuario("Cliente", nome, email, senha, data_nascimento=data_nascimento)
        usuarios.append(novo)
        print("Cadastro realizado com sucesso! Bem-vindo(a) ao Coonecta Eventos,", nome, "!")
    elif opcao == "2":
        print("\n--- DADOS DA EMPRESA ---")
        nome_negocio = input("Nome fantasia: ").strip()
        razao_social = input("Razão social: ").strip()
        cpf_cnpj = input("CPF/CNPJ: ").strip()
        cidade = input("Cidade: ").strip()
        estado = input("Estado: ").strip()

        if not nome_negocio or not cpf_cnpj or not cidade or not estado:
            print("Erro: preencha todos os dados da empresa.")
            return

        print("\nCategoria principal:")
        for i in range(len(CATEGORIAS)):
            print(f"{i + 1}. {CATEGORIAS[i]}")
        escolha = input("Escolha: ").strip()
        if not escolha.isdigit() or not (1 <= int(escolha) <= len(CATEGORIAS)):
            print("Categoria inválida. Cadastro cancelado.")
            return
        categoria = CATEGORIAS[int(escolha) - 1]

        instagram = input("Instagram comercial (opcional): ").strip()
        site = input("Site da empresa (opcional): ").strip()

        novo = criar_usuario(
            "Prestador de serviço",
            nome,
            email,
            senha,
            data_nascimento=data_nascimento,
        )
        novo.update({
            "nome_negocio": nome_negocio,
            "razao_social": razao_social,
            "cpf_cnpj": cpf_cnpj,
            "cidade": cidade,
            "estado": estado,
            "categoria": categoria,
            "instagram": instagram,
            "site": site,
        })
        usuarios.append(novo)

        print("Cadastro realizado com sucesso! Bem-vindo(a),", nome_negocio, "!")
        # enviar o usuário para a página inicial
    else:
        print("Opção inválida. Cadastro cancelado.")
        return

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
    #encaminhar o usuário para a página inicial
    return usuario