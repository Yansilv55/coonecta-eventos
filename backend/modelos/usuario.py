TIPOS = ["Cliente", "Prestador"]
CATEGORIAS = ["Buffet", "Fotografia", "Decoração", "Música", "Espaço para eventos"]


def criar_usuario(tipo, nome, email, senha, nome_negocio="", categoria=""):
    """Monta um usuário. Cliente não tem nome_negocio nem categoria."""
    return {
        "tipo": tipo,
        "nome": nome,
        "email": email,
        "senha": senha,
        "nome_negocio": nome_negocio,
        "categoria": categoria,
    }