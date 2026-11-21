

from banco import criar_arquivos
import usuarios
import servicos
import orcamentos
import avaliacoes
import notificacoes
import portfolio


def mostrar_titulo(texto):
    """Mostra um título centralizado entre duas linhas de '='."""
    print("\n" + "=" * 40)
    print(f"{texto:^40}")
    print("=" * 40)


def mostrar_secao(nome):
    """Mostra o nome de um grupo de opções dentro do menu."""
    print(f"\n  -- {nome} --")


def abrir_area(pessoa):
    """Leva o usuário para a tela principal certa, de acordo com o tipo."""
    if pessoa["tipo"] == usuarios.CLIENTE:
        menu_cliente(pessoa)
    elif pessoa["tipo"] == usuarios.PRESTADOR:
        menu_prestador(pessoa)
    else:
        print("Tipo de usuário desconhecido. Fale com o suporte.")


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
            pessoa = usuarios.cadastrar()
            if pessoa != None:
                abrir_area(pessoa)
        elif opcao == "2":
            pessoa = usuarios.entrar()
            if pessoa != None:
                abrir_area(pessoa)
        elif opcao == "3":
            servicos.listar_todos()
        elif opcao == "4":
            print("Até logo!")
            break
        else:
            print("Opção inválida! Escolha entre 1 e 4.")


def menu_cliente(pessoa):
    notificacoes.mostrar_novas(pessoa)

    while True:
        mostrar_titulo("ÁREA DO CLIENTE")
        print(f"{'Olá, ' + pessoa['nome'] + '!':^40}")
        mostrar_secao("Serviços")
        print("   1. Ver serviços")
        print("   2. Buscar serviços")
        print("   3. Ver avaliações de um serviço")
        print("   4. Ver portfólio de um fornecedor")
        mostrar_secao("Orçamentos")
        print("   5. Pedir orçamento")
        print("   6. Meus orçamentos")
        mostrar_secao("Avaliações e avisos")
        print("   7. Avaliar um prestador")
        print("   8. Minhas notificações")
        mostrar_secao("Minha conta")
        print("   9. Meu perfil")
        print("  10. Sair da conta")
        print("-" * 40)
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            servicos.listar_todos()
        elif opcao == "2":
            servicos.buscar()
        elif opcao == "3":
            avaliacoes.ver_de_um_servico()
        elif opcao == "4":
            portfolio.ver_de_um_prestador()
        elif opcao == "5":
            orcamentos.pedir(pessoa)
        elif opcao == "6":
            orcamentos.meus_pedidos(pessoa)
        elif opcao == "7":
            avaliacoes.avaliar(pessoa)
        elif opcao == "8":
            notificacoes.minhas(pessoa)
        elif opcao == "9":
            pessoa = usuarios.editar_perfil(pessoa)
        elif opcao == "10":
            print("Saindo da conta...")
            break
        else:
            print("Opção inválida!")


def menu_prestador(pessoa):
    notificacoes.mostrar_novas(pessoa)

    while True:
        mostrar_titulo("ÁREA DO PRESTADOR")
        print(f"{'Negócio: ' + pessoa['nome_negocio']:^40}")
        mostrar_secao("Serviços")
        print("   1. Cadastrar serviço")
        print("   2. Meus serviços")
        print("   3. Editar serviço")
        print("   4. Excluir serviço")
        mostrar_secao("Portfólio")
        print("   5. Adicionar trabalho ao portfólio")
        print("   6. Meu portfólio")
        mostrar_secao("Orçamentos")
        print("   7. Ver pedidos de orçamento")
        print("   8. Responder pedido")
        mostrar_secao("Avaliações e avisos")
        print("   9. Minhas avaliações")
        print("  10. Minhas notificações")
        mostrar_secao("Minha conta")
        print("  11. Meu perfil")
        print("  12. Sair da conta")
        print("-" * 40)
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            servicos.cadastrar(pessoa)
        elif opcao == "2":
            servicos.meus(pessoa)
        elif opcao == "3":
            servicos.editar(pessoa)
        elif opcao == "4":
            servicos.excluir(pessoa)
        elif opcao == "5":
            portfolio.cadastrar(pessoa)
        elif opcao == "6":
            portfolio.meu(pessoa)
        elif opcao == "7":
            orcamentos.pedidos_recebidos(pessoa)
        elif opcao == "8":
            orcamentos.responder(pessoa)
        elif opcao == "9":
            avaliacoes.minhas(pessoa)
        elif opcao == "10":
            notificacoes.minhas(pessoa)
        elif opcao == "11":
            pessoa = usuarios.editar_perfil(pessoa)
        elif opcao == "12":
            print("Saindo da conta...")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu_inicial()