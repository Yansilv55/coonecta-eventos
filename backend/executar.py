from rotas.usuarios import cadastrar_usuario, fazer_login


def menu_inicial():
    while True:
        print("\n========================")
        print("    COONECTA EVENTOS    ")
        print("========================")
        print("1. Entrar (login)")
        print("2. Criar conta")
        print("3. Ver serviços")
        print("4. Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            usuario = fazer_login()
            if usuario:  
                if usuario["tipo"] == "Cliente":
                    print(">> Área do Cliente (em construção)")
                else:
                    print(">> Área do Prestador (em construção)")
        elif opcao == "2":
            cadastrar_usuario()
        elif opcao == "3":
            print(">> Lista de serviços (em construção)")
        elif opcao == "4":
            print("Até logo!")
            break
        else:
            print("Opção inválida.")
            print("Tente novamente.")
            print("Carlos")


if __name__ == "__main__":
    menu_inicial()