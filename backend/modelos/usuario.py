TIPOS = ["Cliente", "Prestador"]
CATEGORIAS = ["Buffet e alimentação", "Fotografia e filmagem", "Decoração", "Música e entretenimento", "Espaço para eventos", "Outros serviços"]


def criar_usuario(tipo, nome, email, senha, nome_negocio="", categoria="", data_nascimento="", confirmar_senha=""):
    """Monta um usuário. Cliente não tem nome_negocio nem categoria."""
    return {
        "tipo": tipo,
        "nome": nome,
        "email": email,
        "senha": senha,
        "nome_negocio": nome_negocio,
        "categoria": categoria,
        "data_nascimento": data_nascimento,
        "confirmar_senha": confirmar_senha,
    }