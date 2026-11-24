# =============================================================
# executar.py
# Arquivo que INICIA o sistema. No terminal, dentro da pasta backend:
#   python3 executar.py      (no Windows: python executar.py)
# =============================================================

from banco import criar_arquivos
import usuarios
import servicos
import orcamentos
import avaliacoes
import notificacoes
import portfolio
import contato
import tela


def abrir_area(pessoa):
    """Leva o usuário para a tela principal certa, de acordo com o tipo."""
    if pessoa["tipo"] == usuarios.CLIENTE:
        menu_cliente(pessoa)
    elif pessoa["tipo"] == usuarios.PRESTADOR:
        menu_prestador(pessoa)
    else:
        tela.erro("Tipo de usuário desconhecido. Fale com o suporte.")


def menu_inicial():
    criar_arquivos()

    while True:
        tela.titulo("COONECTA EVENTOS - MENU INICIAL")
        tela.subtitulo("Clientes e fornecedores de eventos")
        print()
        tela.opcao(1, "Cadastrar")
        tela.opcao(2, "Entrar")
        tela.opcao(3, "Ver serviços")
        tela.opcao(4, "Sair")
        tela.linha()
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
            tela.mensagem("Até logo!")
            break
        else:
            tela.erro("Opção inválida! Escolha entre 1 e 4.")


def menu_cliente(pessoa):
    notificacoes.mostrar_novas(pessoa)

    while True:
        tela.titulo("ÁREA DO CLIENTE")
        tela.subtitulo(f"Olá, {pessoa['nome']}!")
        tela.secao("Fornecedores e serviços")
        tela.opcao(1, "Ver serviços")
        tela.opcao(2, "Buscar serviços")
        tela.opcao(3, "Ver avaliações de um serviço")
        tela.opcao(4, "Ver portfólio de um fornecedor")
        tela.opcao(5, "Ver contato de um fornecedor")
        tela.secao("Orçamentos")
        tela.opcao(6, "Pedir orçamento")
        tela.opcao(7, "Meus orçamentos")
        tela.secao("Avaliações e avisos")
        tela.opcao(8, "Avaliar um prestador")
        tela.opcao(9, "Minhas notificações")
        tela.secao("Minha conta")
        tela.opcao(10, "Meu perfil")
        tela.opcao(11, "Sair da conta")
        tela.linha()
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
            contato.ver_contato()
        elif opcao == "6":
            orcamentos.pedir(pessoa)
        elif opcao == "7":
            orcamentos.meus_pedidos(pessoa)
        elif opcao == "8":
            avaliacoes.avaliar(pessoa)
        elif opcao == "9":
            notificacoes.minhas(pessoa)
        elif opcao == "10":
            pessoa = usuarios.editar_perfil(pessoa)
        elif opcao == "11":
            tela.mensagem("Saindo da conta...")
            break
        else:
            tela.erro("Opção inválida! Escolha entre 1 e 11.")


def menu_prestador(pessoa):
    notificacoes.mostrar_novas(pessoa)

    while True:
        tela.titulo("ÁREA DO PRESTADOR")
        tela.subtitulo(f"Negócio: {pessoa['nome_negocio']}")
        tela.secao("Serviços")
        tela.opcao(1, "Cadastrar serviço")
        tela.opcao(2, "Meus serviços")
        tela.opcao(3, "Editar serviço")
        tela.opcao(4, "Excluir serviço")
        tela.secao("Portfólio")
        tela.opcao(5, "Adicionar trabalho ao portfólio")
        tela.opcao(6, "Meu portfólio")
        tela.secao("Orçamentos")
        tela.opcao(7, "Ver pedidos de orçamento")
        tela.opcao(8, "Responder pedido")
        tela.secao("Avaliações e avisos")
        tela.opcao(9, "Minhas avaliações")
        tela.opcao(10, "Minhas notificações")
        tela.secao("Minha conta")
        tela.opcao(11, "Meu perfil")
        tela.opcao(12, "Sair da conta")
        tela.linha()
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
            tela.mensagem("Saindo da conta...")
            break
        else:
            tela.erro("Opção inválida! Escolha entre 1 e 12.")


if __name__ == "__main__":
    menu_inicial()
