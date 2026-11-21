# =============================================================
# contato.py
# Tudo sobre o CONTATO entre clientes e prestadores (RF06 / UC06)
# - Cliente escolhe um fornecedor e vê os meios de contato dele
#   (telefone/WhatsApp, e-mail e Instagram, que vêm do cadastro do prestador)
# - Se o prestador não tiver contato cadastrado, o sistema avisa
# =============================================================

from banco import pedir_texto
import usuarios


def ver_contato():
    print("\n--- CONTATO DO FORNECEDOR ---")
    email = pedir_texto("E-mail do prestador: ")
    prestador = usuarios.buscar(email)
    if prestador is None or prestador["tipo"] != usuarios.PRESTADOR:
        print("Prestador não encontrado.")
        return

    contatos = []
    if prestador["telefone"] != "":
        contatos.append(f"Telefone/WhatsApp: {prestador['telefone']}")
    if prestador["email"] != "":
        contatos.append(f"E-mail: {prestador['email']}")
    if prestador["instagram"] != "":
        contatos.append(f"Instagram: {prestador['instagram']}")

    print(f"\nContato de {prestador['nome_negocio']}:")
    if len(contatos) == 0:
        print("Este prestador ainda não cadastrou meios de contato.")
    for contato in contatos:
        print(contato)
# =============================================================

