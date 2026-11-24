# =============================================================
# usuarios.py
# Tudo sobre USUÁRIOS: cadastro (cliente e prestador), login,
# recuperação de senha e perfil.
# Os usuários ficam salvos em dados/usuarios.txt
# =============================================================

from banco import ler, salvar, pedir_texto, ARQ_USUARIOS
import servicos
import notificacoes
import tela

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


def atualizar(pessoa):
    """Troca o usuário antigo pelo atualizado (mesmo e-mail) e salva."""
    lista = todos()
    for i in range(len(lista)):
        if lista[i]["email"] == pessoa["email"]:
            lista[i] = pessoa
    guardar(lista)


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
    if cpf == cpf[0] * 11:  
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

def pedir_senha():
    """Pede a senha (mínimo 6) e a repetição. Só sai quando as duas forem iguais.
    É usada no cadastro, na recuperação de senha e na edição do perfil."""
    while True:
        senha = pedir_texto("Senha (mínimo 6 caracteres): ")
        if len(senha) < 6:
            tela.erro("A senha precisa ter pelo menos 6 caracteres.")
            continue
        repetir = input("Repita a senha: ").strip()
        if repetir != senha:
            tela.erro("As senhas não são iguais. Tente de novo.")
        else:
            return senha


def cadastrar():
    """Cadastra um Cliente ou um Prestador.
    Devolve o usuário criado, para ele já entrar na conta."""
    tela.titulo("CADASTRO")
    tela.secao("Tipo de conta")
    tela.opcao(1, "Cliente (quero contratar serviços)")
    tela.opcao(2, "Prestador de serviço (quero oferecer serviços)")
    while True:
        opcao = input("Você é: ").strip()
        if opcao == "1":
            tipo = CLIENTE
            break
        elif opcao == "2":
            tipo = PRESTADOR
            break
        tela.erro("Opção inválida! Digite 1 ou 2.")

    nome = pedir_texto("Nome completo: ")

    while True:
        email = pedir_texto("E-mail: ").lower()
        if not email_valido(email):
            tela.erro("E-mail inválido. Exemplo: nome@email.com")
        elif buscar(email) != None:
            tela.erro("Este e-mail já está cadastrado.")
        else:
            break

    senha = pedir_senha()

    while True:
        telefone = so_numeros(pedir_texto("Telefone com DDD (só números): "))
        if telefone_valido(telefone):
            break
        tela.erro("Telefone inválido. Digite o DDD + número (10 ou 11 números).")

    while True:
        cpf = so_numeros(pedir_texto("CPF (só números): "))
        if not cpf_valido(cpf):
            tela.erro("CPF inválido. Confira os números.")
        elif cpf_existe(cpf):
            tela.erro("Este CPF já está cadastrado.")
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
        tela.secao("Dados do negócio")
        nome_negocio = pedir_texto("Nome do negócio: ")
        categoria = servicos.escolher_categoria()

        while True:
            anos_experiencia = pedir_texto("Anos de experiência: ")
            if anos_experiencia.isdigit():
                break
            tela.erro("Digite só números.")

        while True:
            cnpj = input("CNPJ (opcional, aperte Enter para pular): ").strip()
            if cnpj == "":
                break
            cnpj = so_numeros(cnpj)
            if cnpj_valido(cnpj):
                break
            tela.erro("CNPJ inválido. Ele precisa ter 14 números.")

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

    # Notificação de boas-vindas (aparece logo ao entrar na área principal)
    if tipo == PRESTADOR:
        notificacoes.criar(email, "Bem-vindo(a) ao Coonecta Eventos! Comece cadastrando seu primeiro serviço.")
    else:
        notificacoes.criar(email, "Bem-vindo(a) ao Coonecta Eventos! Veja os serviços e peça seu primeiro orçamento.")

    tela.mensagem("Cadastro realizado com sucesso!")
    print(f"     Bem-vindo(a), {nome}!")
    return novo


def entrar():
    """Pede e-mail e senha. Devolve o usuário se der certo, ou None.
    Se errar, oferece a recuperação de senha."""
    tela.titulo("ENTRAR")
    email = input("E-mail: ").strip().lower()
    senha = input("Senha: ").strip()
    usuario = verificar_login(email, senha)
    if usuario == None:
        tela.erro("E-mail ou senha incorretos.")
        resposta = input("Esqueceu sua senha? (s/n): ").strip().lower()
        if resposta == "s":
            recuperar_senha()
        return None
    tela.mensagem(f"Bem-vindo(a), {usuario['nome']}!")
    return usuario


def recuperar_senha():
    """Cria uma senha nova depois de confirmar e-mail, CPF e telefone."""
    tela.titulo("RECUPERAR SENHA")
    tela.subtitulo("Para sua segurança, confirme os dados do cadastro")
    email = pedir_texto("E-mail: ").lower()
    cpf = so_numeros(pedir_texto("CPF: "))
    telefone = so_numeros(pedir_texto("Telefone com DDD: "))

    usuario = buscar(email)
    if usuario == None or usuario["cpf"] != cpf or usuario["telefone"] != telefone:
        tela.erro("Os dados não conferem com nenhum cadastro.")
        return

    tela.mensagem("Dados confirmados! Crie sua nova senha.")
    usuario["senha"] = pedir_senha()
    atualizar(usuario)
    notificacoes.criar(email, "Sua senha foi alterada. Se não foi você, recupere a senha de novo.")
    tela.mensagem("Senha alterada! Agora você já pode entrar com a nova senha.")


def mostrar_perfil(pessoa):
    tela.titulo("MEU PERFIL")
    tela.secao("Dados pessoais")
    tela.campo("Tipo", pessoa["tipo"])
    tela.campo("Nome", pessoa["nome"])
    tela.campo("E-mail", pessoa["email"])
    tela.campo("Telefone", tela.telefone(pessoa["telefone"]))
    tela.campo("CPF", tela.cpf(pessoa["cpf"]))
    tela.campo("Cidade", f"{pessoa['cidade']} - {pessoa['bairro']}")
    if pessoa["tipo"] == PRESTADOR:
        tela.secao("Dados do negócio")
        tela.campo("Negócio", pessoa["nome_negocio"])
        tela.campo("Categoria", pessoa["categoria"])
        tela.campo("Experiência", f"{pessoa['anos_experiencia']} ano(s)")
        if pessoa["cnpj"] != "":
            tela.campo("CNPJ", pessoa["cnpj"])
        if pessoa["instagram"] != "":
            tela.campo("Instagram", pessoa["instagram"])
        tela.campo("Sobre", pessoa["descricao"])
    tela.linha()


def lista_de_prestadores():
    """Todos os usuários que são prestadores."""
    lista = []
    for u in todos():
        if u["tipo"] == PRESTADOR:
            lista.append(u)
    return lista


def escolher_prestador():
    """Mostra os fornecedores numerados e devolve o escolhido (ou None para voltar).
    Assim o cliente não precisa saber o e-mail do prestador."""
    lista = lista_de_prestadores()
    if len(lista) == 0:
        print("  Nenhum fornecedor cadastrado ainda.")
        return None
    print()
    print(f"  {'Nº':>3}  {'Fornecedor':<20} {'Categoria':<12} {'Cidade':<12}")
    tela.linha()
    for i in range(len(lista)):
        p = lista[i]
        print(f"  {i + 1:>3}  {tela.cortar(p['nome_negocio'], 20):<20} "
              f"{tela.cortar(p['categoria'], 12):<12} {tela.cortar(p['cidade'], 12):<12}")
    tela.linha()
    posicao = tela.escolher_da_lista(len(lista), "Escolha o fornecedor (0 para voltar): ")
    if posicao == -1:
        return None
    return lista[posicao]


def editar_perfil(pessoa):
    """Mostra o perfil e deixa editar. Devolve o usuário (atualizado ou não)."""
    mostrar_perfil(pessoa)

    resposta = input("\nDeseja editar seu perfil? (s/n): ").strip().lower()
    if resposta != "s":
        return pessoa

    tela.secao("Editar perfil")
    print("  Deixe em branco e aperte Enter para manter o valor atual.")
    print("  (E-mail e CPF não podem ser alterados.)")

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
        tela.erro("Telefone inválido. Digite o DDD + número (10 ou 11 números).")

    novo = input(f"Cidade [{pessoa['cidade']}]: ").strip()
    if novo != "":
        pessoa["cidade"] = novo

    novo = input(f"Bairro [{pessoa['bairro']}]: ").strip()
    if novo != "":
        pessoa["bairro"] = novo

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
            tela.erro("Digite só números.")

        novo = input(f"Instagram [{pessoa['instagram']}]: ").strip()
        if novo != "":
            pessoa["instagram"] = novo

        novo = input(f"Sobre o trabalho [{pessoa['descricao']}]: ").strip()
        if novo != "":
            pessoa["descricao"] = novo

    # Para trocar a senha, precisa confirmar a senha atual
    resposta = input("Deseja mudar a senha? (s/n): ").strip().lower()
    if resposta == "s":
        atual = input("Senha atual: ").strip()
        if atual == pessoa["senha"]:
            pessoa["senha"] = pedir_senha()
        else:
            tela.erro("Senha atual incorreta. A senha não foi alterada.")

    atualizar(pessoa)
    tela.mensagem("Perfil atualizado!")
    return pessoa