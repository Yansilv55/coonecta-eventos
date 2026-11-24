# =============================================================
# contato.py
# Tudo sobre o CONTATO entre clientes e prestadores (RF06 / UC06)
# - Cliente escolhe um fornecedor e vê os meios de contato dele
#   (telefone/WhatsApp, e-mail e Instagram, que vêm do cadastro do prestador)
# - Se o prestador não tiver contato cadastrado, o sistema avisa
# =============================================================

import usuarios
import tela


# ================= TELAS E AÇÕES =================

def ver_contato():
    tela.titulo("CONTATO DO FORNECEDOR")
    prestador = usuarios.escolher_prestador()
    if prestador == None:
        return

    tela.cabecalho_cartao(f"{prestador['nome_negocio']} ({prestador['nome']})")
    achou = False
    if prestador["telefone"] != "":
        tela.campo("WhatsApp", tela.telefone(prestador["telefone"]))
        achou = True
    if prestador["email"] != "":
        tela.campo("E-mail", prestador["email"])
        achou = True
    if prestador["instagram"] != "":
        tela.campo("Instagram", prestador["instagram"])
        achou = True
    if not achou:
        print("  Este prestador ainda não cadastrou meios de contato.")
    tela.linha()
