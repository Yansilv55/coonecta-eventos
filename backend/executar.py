# =============================================================
# executar.py
# Arquivo que INICIA o sistema. No terminal, dentro da pasta backend:
#   python executar.py      (no Mac: python3 executar.py)
# =============================================================

from banco import criar_arquivos
import usuarios
import servicos
import orcamentos
import avaliacoes


def menu_inicial():
    criar_arquivos()

    while True:
        print("\n" + "=" * 40)
        print("   COONECTA EVENTOS - MENU INICIAL")
        print("=" * 40)
        print("1. Cadastrar")
        print("2. Entrar")
        print("3. Ver serviços")
        print("4. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            usuarios.cadastrar()
        elif opcao == "2":
            pessoa = usuarios.entrar()
            if pessoa != None:
                if pessoa["tipo"] == usuarios.CLIENTE:
                    menu_cliente(pessoa)
                else:
                    menu_prestador(pessoa)
        elif opcao == "3":
            servicos.listar_todos()
        elif opcao == "4":
            print("Até logo!")
            break
        else:
            print("Opção inválida! Escolha entre 1 e 4.")


def menu_cliente(pessoa):
    orcamentos.avisos_cliente(pessoa)

    while True:
        print(f"\n=== ÁREA DO CLIENTE ({pessoa['nome']}) ===")
        print("1. Ver serviços")
        print("2. Buscar serviços")
        print("3. Ver avaliações de um serviço")
        print("4. Pedir orçamento")
        print("5. Meus orçamentos")
        print("6. Avaliar um prestador")
        print("7. Meu perfil")
        print("8. Sair da conta")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            servicos.listar_todos()
        elif opcao == "2":
            servicos.buscar()
        elif opcao == "3":
            avaliacoes.ver_de_um_servico()
        elif opcao == "4":
            orcamentos.pedir(pessoa)
        elif opcao == "5":
            orcamentos.meus_pedidos(pessoa)
        elif opcao == "6":
            avaliacoes.avaliar(pessoa)
        elif opcao == "7":
            pessoa = usuarios.editar_perfil(pessoa)
        elif opcao == "8":
            print("Saindo da conta...")
            break
        else:
            print("Opção inválida!")


def menu_prestador(pessoa):
    orcamentos.avisos_prestador(pessoa)

    while True:
        print(f"\n=== ÁREA DO PRESTADOR ({pessoa['nome_negocio']}) ===")
        print("1. Cadastrar serviço")
        print("2. Meus serviços")
        print("3. Editar serviço")
        print("4. Ver pedidos de orçamento")
        print("5. Responder pedido")
        print("6. Minhas avaliações")
        print("7. Meu perfil")
        print("8. Sair da conta")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            servicos.cadastrar(pessoa)
        elif opcao == "2":
            servicos.meus(pessoa)
        elif opcao == "3":
            servicos.editar(pessoa)
        elif opcao == "4":
            orcamentos.pedidos_recebidos(pessoa)
        elif opcao == "5":
            orcamentos.responder(pessoa)
        elif opcao == "6":
            avaliacoes.minhas(pessoa)
        elif opcao == "7":
            pessoa = usuarios.editar_perfil(pessoa)
        elif opcao == "8":
            print("Saindo da conta...")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu_inicial()
