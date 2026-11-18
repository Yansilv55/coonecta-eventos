# =============================================================
# notificacoes.py
# Tudo sobre as NOTIFICAÇÕES dos usuários (RF08 / UC11)
# - Ex: "Você recebeu um pedido de orçamento"
# - Ex: "Seu orçamento foi respondido"
# - As notificações aparecem quando o usuário faz login
# =============================================================

from banco import ler, salvar, novo_id, ARQ_NOTIFICACOES

CAMPOS = ["id", "email_usuario", "mensagem", "lida"]

NAO_LIDA = "nao"
LIDA = "sim"


def todas():
    return ler(ARQ_NOTIFICACOES, CAMPOS)


def guardar(lista):
    salvar(ARQ_NOTIFICACOES, CAMPOS, lista)


def criar(email_usuario, mensagem):
    """Cria uma notificação nova (não lida) para o usuário."""
    lista = todas()
    nova = {
        "id": novo_id(lista),
        "email_usuario": email_usuario,
        "mensagem": mensagem,
        "lida": NAO_LIDA,
    }
    lista.append(nova)
    guardar(lista)


def mostrar_novas(pessoa):
    """Mostra as notificações não lidas e marca como lidas.
    Chamar logo depois do login."""
    lista = todas()
    quantidade = 0
    for n in lista:
        if n["email_usuario"] == pessoa["email"] and n["lida"] == NAO_LIDA:
            if quantidade == 0:
                print("\n--- NOTIFICAÇÕES NOVAS ---")
            print(f"* {n['mensagem']}")
            n["lida"] = LIDA
            quantidade = quantidade + 1
    if quantidade > 0:
        guardar(lista)


def minhas(pessoa):
    """Mostra todas as notificações do usuário (lidas e não lidas)."""
    print("\n--- MINHAS NOTIFICAÇÕES ---")
    lista = todas()
    achou = False
    for n in lista:
        if n["email_usuario"] == pessoa["email"]:
            achou = True
            if n["lida"] == NAO_LIDA:
                print(f"* (nova) {n['mensagem']}")
                n["lida"] = LIDA
            else:
                print(f"* {n['mensagem']}")
    if not achou:
        print("Você não tem notificações.")
        return
    guardar(lista)