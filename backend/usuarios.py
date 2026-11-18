# =============================================================
# usuarios.py
# Tudo sobre USUÁRIOS: cadastro (cliente e prestador), login e perfil.
# Os usuários ficam salvos em dados/usuarios.txt
# =============================================================

from banco import ler, salvar, pedir_texto, ARQ_USUARIOS
import servicos

CAMPOS = ["tipo", "nome", "email", "senha", "telefone", "cpf", "cidade", "bairro",
          "nome_negocio", "categoria", "anos_experiencia", "cnpj", "instagram", "descricao"]

CLIENTE = "Cliente"
PRESTADOR = "Prestador"


# ================= DADOS E VALIDAÇÕES =================

def todos():
    return ler(ARQ_USUARIOS, CAMPOS)


def guardar(lista):
    salvar(ARQ_USUARIOS, CAMPOS, lista)


def buscar(email):
    """Procura um usuário pelo e-mail. Devolve o usuário ou None."""
    for u in todos():
        if u["email"] == email:
            return u
    return None


def cpf_existe(cpf):
    for u in todos():
        if u["cpf"] == cpf:
            return True
    return False


def verificar_login(email, senha):
    """Devolve o usuário se e-mail e senha estiverem certos, senão None."""
    u = buscar(email)
    if u != None and u["senha"] == senha:
        return u
    return None


def so_numeros(texto):
    """Tira tudo que não é número. Ex: "123.456.789-09" vira "12345678909"."""
    resultado = ""
    for letra in texto:
        if letra.isdigit():
            resultado = resultado + letra
    return resultado


def email_valido(email):
    if " " in email or email.count("@") != 1:
        return False
    partes = email.split("@")
    antes = partes[0]
    dominio = partes[1]
    if antes == "":
        return False
    if "." not in dominio:
        return False
    if dominio.startswith(".") or dominio.endswith("."):
        return False
    return True


def telefone_valido(telefone):
    return telefone.isdigit() and (len(telefone) == 10 or len(telefone) == 11)


def cpf_valido(cpf):
    """Confere o CPF pelo cálculo oficial dos dois dígitos verificadores."""
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    if cpf == cpf[0] * 11:  # ex: 11111111111
        return False

    # Primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma = soma + int(cpf[i]) * (10 - i)
    digito1 = (soma * 10) % 11
    if digito1 == 10:
        digito1 = 0
    if digito1 != int(cpf[9]):
        return False

    # Segundo dígito verificador
    soma = 0
    for i in range(10):
        soma = soma + int(cpf[i]) * (11 - i)
    digito2 = (soma * 10) % 11
    if digito2 == 10:
        digito2 = 0
    return digito2 == int(cpf[10])


def cnpj_valido(cnpj):
    return len(cnpj) == 14 and cnpj.isdigit()


# ================= TELAS E AÇÕES =================

def cadastrar():
    print("\n--- CADASTRO ---")
    print("1. Cliente")
    print("2. Prestador de serviço")
    while True:
        opcao = input("Você é: ").strip()
        if opcao == "1":
            tipo = CLIENTE
            break
        elif opcao == "2":
            tipo = PRESTADOR
            break
        print("Opção inválida! Digite 1 ou 2.")

    nome = pedir_texto("Nome completo: ")

    while True:
        email = pedir_texto("E-mail: ").lower()
        if not email_valido(email):
            print("E-mail inválido. Exemplo: nome@email.com")
        elif buscar(email) != None:
            print("Este e-mail já está cadastrado.")
        else:
            break

    while True:
        senha = pedir_texto("Senha (mínimo 6 caracteres): ")
        if len(senha) < 6:
            print("A senha precisa ter pelo menos 6 caracteres.")
            continue
        repetir = input("Repita a senha: ").strip()
        if repetir != senha:
            print("As senhas não são iguais. Tente de novo.")
        else:
            break

    while True:
        telefone = so_numeros(pedir_texto("Telefone com DDD (só números): "))
        if telefone_valido(telefone):
            break
        print("Telefone inválido. Digite o DDD + número (10 ou 11 números).")

    while True:
        cpf = so_numeros(pedir_texto("CPF (só números): "))
        if not cpf_valido(cpf):
            print("CPF inválido.")
        elif cpf_existe(cpf):
            print("Este CPF já está cadastrado.")
        else:
            break

    cidade = pedir_texto("Cidade: ")
    bairro = pedir_texto("Bairro: ")

    # Campos do negócio (ficam vazios para o cliente)
    nome_negocio = ""
    categoria = ""
    anos_experiencia = ""
    cnpj = ""
    instagram = ""
    descricao = ""

    if tipo == PRESTADOR:
        print("\n-- Dados do negócio --")
        nome_negocio = pedir_texto("Nome do negócio: ")
        categoria = servicos.escolher_categoria()

        while True:
            anos_experiencia = pedir_texto("Anos de experiência: ")
            if anos_experiencia.isdigit():
                break
            print("Digite só números.")

        while True:
            cnpj = input("CNPJ (opcional, aperte Enter para pular): ").strip()
            if cnpj == "":
                break
            cnpj = so_numeros(cnpj)
            if cnpj_valido(cnpj):
                break
            print("CNPJ inválido. Ele precisa ter 14 números.")

        instagram = input("Instagram (opcional, aperte Enter para pular): ").strip()
        descricao = pedir_texto("Fale um pouco sobre o seu trabalho: ")

    novo = {
        "tipo": tipo,
        "nome": nome,
        "email": email,
        "senha": senha,
        "telefone": telefone,
        "cpf": cpf,
        "cidade": cidade,
        "bairro": bairro,
        "nome_negocio": nome_negocio,
        "categoria": categoria,
        "anos_experiencia": anos_experiencia,
        "cnpj": cnpj,
        "instagram": instagram,
        "descricao": descricao,
    }

    lista = todos()
    lista.append(novo)
    guardar(lista)
    print("Cadastro realizado com sucesso!")


def entrar():
    print("\n--- ENTRAR ---")
    email = input("E-mail: ").strip().lower()
    senha = input("Senha: ").strip()
    usuario = verificar_login(email, senha)
    if usuario == None:
        print("E-mail ou senha incorretos.")
        return None
    print(f"Bem-vindo(a), {usuario['nome']}!")
    return usuario


def mostrar_perfil(pessoa):
    print("\n--- MEU PERFIL ---")
    print(f"Tipo: {pessoa['tipo']}")
    print(f"Nome: {pessoa['nome']}")
    print(f"E-mail: {pessoa['email']}")
    print(f"Telefone: {pessoa['telefone']}")
    print(f"CPF: {pessoa['cpf']}")
    print(f"Cidade: {pessoa['cidade']} | Bairro: {pessoa['bairro']}")
    if pessoa["tipo"] == PRESTADOR:
        print(f"Negócio: {pessoa['nome_negocio']}")
        print(f"Categoria: {pessoa['categoria']}")
        print(f"Anos de experiência: {pessoa['anos_experiencia']}")
        if pessoa["cnpj"] != "":
            print(f"CNPJ: {pessoa['cnpj']}")
        if pessoa["instagram"] != "":
            print(f"Instagram: {pessoa['instagram']}")
        print(f"Sobre o trabalho: {pessoa['descricao']}")


def editar_perfil(pessoa):
    """Mostra o perfil e deixa editar. Devolve o usuário (atualizado ou não)."""
    mostrar_perfil(pessoa)

    resposta = input("\nDeseja editar seu perfil? (s/n): ").strip().lower()
    if resposta != "s":
        return pessoa

    print("\nDeixe em branco e aperte Enter para manter o valor atual.")
    print("(E-mail e CPF não podem ser alterados.)")

    novo = input(f"Nome [{pessoa['nome']}]: ").strip()
    if novo != "":
        pessoa["nome"] = novo

    while True:
        novo = input(f"Telefone [{pessoa['telefone']}]: ").strip()
        if novo == "":
            break
        novo = so_numeros(novo)
        if telefone_valido(novo):
            pessoa["telefone"] = novo
            break
        print("Telefone inválido. Digite o DDD + número (10 ou 11 números).")

    novo = input(f"Cidade [{pessoa['cidade']}]: ").strip()
    if novo != "":
        pessoa["cidade"] = novo

    novo = input(f"Bairro [{pessoa['bairro']}]: ").strip()
    if novo != "":
        pessoa["bairro"] = novo

    while True:
        novo = input("Nova senha (Enter para manter): ").strip()
        if novo == "":
            break
        if len(novo) >= 6:
            pessoa["senha"] = novo
            break
        print("A senha precisa ter pelo menos 6 caracteres.")

    if pessoa["tipo"] == PRESTADOR:
        novo = input(f"Nome do negócio [{pessoa['nome_negocio']}]: ").strip()
        if novo != "":
            pessoa["nome_negocio"] = novo

        while True:
            novo = input(f"Anos de experiência [{pessoa['anos_experiencia']}]: ").strip()
            if novo == "":
                break
            if novo.isdigit():
                pessoa["anos_experiencia"] = novo
                break
            print("Digite só números.")

        novo = input(f"Instagram [{pessoa['instagram']}]: ").strip()
        if novo != "":
            pessoa["instagram"] = novo

        novo = input(f"Sobre o trabalho [{pessoa['descricao']}]: ").strip()
        if novo != "":
            pessoa["descricao"] = novo

    # Troca o usuário antigo pelo atualizado e salva
    lista = todos()
    for i in range(len(lista)):
        if lista[i]["email"] == pessoa["email"]:
            lista[i] = pessoa
    guardar(lista)
    print("Perfil atualizado!")
    return pessoa
