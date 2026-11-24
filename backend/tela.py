# =============================================================
# tela.py
# Funções para deixar tudo que aparece no terminal bem formatado
# e com o mesmo visual em todo o sistema.
# Todos os outros arquivos usam estas funções: import tela
# =============================================================

import textwrap

LARGURA = 60   # largura das linhas, títulos e tabelas


def titulo(texto):
    """Título principal, centralizado entre duas linhas de '='."""
    print("\n" + "=" * LARGURA)
    print(f"{texto:^{LARGURA}}")
    print("=" * LARGURA)


def subtitulo(texto):
    """Texto centralizado logo abaixo do título (ex: nome do usuário)."""
    print(f"{texto:^{LARGURA}}")


def secao(nome):
    """Nome de um grupo de opções ou de informações."""
    print(f"\n  -- {nome} --")


def linha():
    print("-" * LARGURA)


def opcao(numero, texto):
    """Uma opção numerada de menu, sempre alinhada (ex: '   1. Ver serviços')."""
    print(f"  {numero:>2}. {texto}")


def campo(rotulo, valor):
    """Uma informação no formato 'Rótulo:  valor', com os valores alinhados.
    Se o valor for grande, ele quebra a linha sem desalinhar."""
    inicio = f"  {rotulo + ':':<14} "
    partes = textwrap.wrap(str(valor), LARGURA - len(inicio))
    if len(partes) == 0:
        partes = ["-"]
    print(inicio + partes[0])
    for parte in partes[1:]:
        print(" " * len(inicio) + parte)


def cabecalho_cartao(texto):
    """Começo de um 'cartão' (um serviço, um pedido, um trabalho...)."""
    print()
    linha()
    print(f"  {texto}")
    linha()


def mensagem(texto):
    """Aviso de sucesso, destacado."""
    print(f"\n  >> {texto}")


def erro(texto):
    """Aviso de erro, destacado."""
    print(f"  !! {texto}")


def cortar(texto, tamanho):
    """Corta textos grandes para caberem numa coluna de tabela."""
    if len(texto) > tamanho:
        return texto[:tamanho - 1] + "…"
    return texto


def dinheiro(valor):
    """Ex: "1600.5" vira "R$ 1.600,50"."""
    texto = f"{float(valor):,.2f}"          # 1,600.50
    texto = texto.replace(",", "#").replace(".", ",").replace("#", ".")
    return "R$ " + texto


def telefone(numero):
    """Ex: "73999991111" vira "(73) 99999-1111"."""
    if len(numero) == 11:
        return f"({numero[0:2]}) {numero[2:7]}-{numero[7:]}"
    if len(numero) == 10:
        return f"({numero[0:2]}) {numero[2:6]}-{numero[6:]}"
    return numero


def cpf(numero):
    """Ex: "52998224725" vira "529.982.247-25"."""
    if len(numero) == 11:
        return f"{numero[0:3]}.{numero[3:6]}.{numero[6:9]}-{numero[9:]}"
    return numero


def escolher_da_lista(quantidade, pergunta="Escolha o número (0 para voltar): "):
    """Pede um número de 1 até 'quantidade'. Devolve a posição (0, 1, 2...)
    ou -1 se a pessoa digitar 0 para voltar."""
    while True:
        escolha = input(pergunta).strip()
        if escolha == "0":
            return -1
        if escolha.isdigit() and 1 <= int(escolha) <= quantidade:
            return int(escolha) - 1
        erro(f"Opção inválida! Digite um número de 1 a {quantidade} (ou 0 para voltar).")
