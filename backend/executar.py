from rotas.usuarios import cadastrar_usuario, fazer_login

TIPO_CLIENTE = "Cliente"


def exibir_menu():
    print("\n========================")
    print("    CO0NECTA EVENTOS     ")
    print("========================")
    print("1. Entrar (login)")
    print("2. Criar conta")
    print("3. Ver serviços")
    print("4. Sair")


def abrir_area_do_usuario(usuario):
    if usuario["tipo"] == TIPO_CLIENTE:
        print(">> Área do Cliente (em construção)")
    else:
        print(">> Área do Prestador (em construção)")


def entrar():
    usuario = fazer_login()
    if usuario:
        abrir_area_do_usuario(usuario)


def ver_servicos():
    print(">> Lista de serviços (em construção)")


def menu_inicial():
    acoes = {
        "1": entrar,
        "2": cadastrar_usuario,
        "3": ver_servicos,
    }

    while True:
        exibir_menu()
        opcao = input("Escolha: ").strip()

        if opcao == "4":
            print("Até logo!")
            break

        acao = acoes.get(opcao)
        if acao:
            acao()
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_inicial()