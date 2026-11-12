# Coonecta Eventos

Projeto universitário (ADS). Sistema que conecta **clientes** que vão fazer um evento com **prestadores de serviço** (Buffet, Fotografia, Decoração, Música e Espaço para eventos).

- **Cliente:** consulta e pesquisa serviços, pede orçamento, acompanha seus orçamentos e avalia prestadores.
- **Prestador:** cadastra e edita seus serviços, recebe e responde orçamentos e vê as avaliações que recebeu.

> Os arquivos ainda estão **vazios**. Este documento explica o que cada um vai fazer, para o time saber onde escrever cada parte.

> Os arquivos ainda estão **vazios**. Este documento explica o que cada um vai fazer, para o time saber onde escrever cada parte.carol

Testando 

oi

carlos )!
---

## Estrutura do projeto

```
coonecta-eventos/
├── backend/
│   ├── executar.py
│   ├── banco.py
│   ├── modelos/
│   │   ├── usuario.py
│   │   ├── servico.py
│   │   ├── orcamento.py
│   │   └── avaliacao.py
│   ├── rotas/
│   │   ├── usuarios.py
│   │   ├── servicos.py
│   │   ├── orcamentos.py
│   │   └── avaliacoes.py
│   └── requirements.txt
├── frontend/
└── README.md
```

---

## backend/

É a "parte de trás" do sistema: onde ficam as **regras** (o que pode e o que não pode) e os **dados** (usuários, serviços, orçamentos e avaliações).

### `executar.py`
Arquivo que **inicia o sistema**. É o único que a gente roda no terminal (`python3 executar.py`). Ele junta todas as outras partes e as coloca para funcionar.

### `banco.py`
Faz a **conexão com o banco de dados**, o lugar onde as informações ficam guardadas. Os outros arquivos usam o `banco.py` sempre que precisam salvar ou buscar alguma coisa.

### `requirements.txt`
Lista das **bibliotecas externas** que o projeto usa. Quem baixar o projeto instala todas de uma vez com:
```bash
pip install -r requirements.txt
```

---

## backend/modelos/

Cada arquivo define **como uma informação é guardada**: quais campos ela tem. Pense em cada modelo como uma tabela de planilha.

### `usuario.py`
Guarda as pessoas cadastradas no sistema.
- Campos: tipo (Cliente ou Prestador), nome, e-mail, senha.
- Só para prestador: nome do negócio e categoria principal.

### `servico.py`
Guarda os serviços que os prestadores oferecem.
- Campos: prestador dono do serviço, categoria, nome do serviço, descrição e preço base.
- Categorias permitidas: Buffet, Fotografia, Decoração, Música e Espaço para eventos.

### `orcamento.py`
Guarda os pedidos de orçamento que os clientes fazem.
- Campos: cliente que pediu, serviço escolhido, detalhes do evento (data, local, número de convidados), status e resposta do prestador.
- Status: **Pendente** (aguardando o prestador) ou **Respondido**.

### `avaliacao.py`
Guarda as notas que os clientes dão aos prestadores.
- Campos: cliente que avaliou, prestador avaliado, nota (1 a 5) e comentário.
- Regra: cada cliente avalia o mesmo prestador **uma vez só**.

---

## backend/rotas/

Cada arquivo reúne **as ações** do sistema sobre um assunto. São as opções que aparecem nos menus do Cliente e do Prestador.

### `usuarios.py`
- **Cadastrar usuário:** nome, e-mail e senha, escolhendo entre Cliente ou Prestador. Prestador também informa o nome do negócio e a categoria. Não deixa cadastrar e-mail repetido.
- **Fazer login:** confere e-mail e senha e leva o usuário para a área certa (Cliente ou Prestador).

### `servicos.py`
- **Consultar serviços:** lista todos os serviços com descrição, preço e prestador (qualquer pessoa pode ver).
- **Pesquisar serviços:** busca por categoria ou nome (Cliente).
- **Cadastrar serviço:** adiciona um serviço novo (Prestador).
- **Ver meus serviços:** lista só os serviços do prestador logado.
- **Editar serviço:** muda a descrição ou o preço (somente o dono do serviço).

### `orcamentos.py`
- **Solicitar orçamento:** o cliente escolhe um serviço e descreve o evento.
- **Meus orçamentos:** o cliente acompanha o status e a resposta.
- **Orçamentos recebidos:** o prestador vê os pedidos que chegaram para ele.
- **Responder orçamento:** o prestador informa preço e condições; o status muda para Respondido.

### `avaliacoes.py`
- **Avaliar prestador:** o cliente dá uma nota de 1 a 5 e um comentário.
- **Ver avaliações recebidas:** o prestador vê todas as notas e comentários, com a **média geral**.

---

## Diferença entre modelos e rotas

Jeito fácil de lembrar: **modelo é a ficha, rota é o atendente.**

- **Modelo** = a **ficha em branco**. Diz quais campos uma informação tem (nome, e-mail, senha...). Não pergunta nada e não mostra nada na tela.
- **Rota** = o **atendente**. Conversa com o usuário (`input` e `print`), confere as regras (ex: e-mail repetido) e usa o modelo para preencher a ficha.

### Exemplo: cadastro de usuário

**`modelos/usuario.py`**: só diz como é um usuário.
```python
def criar_usuario(tipo, nome, email, senha):
    return {
        "tipo": tipo,
        "nome": nome,
        "email": email,
        "senha": senha,
    }
```

**`rotas/usuarios.py`**: pergunta, confere e usa o modelo.
```python
from modelos.usuario import criar_usuario

usuarios = []

def cadastrar_usuario():
    nome = input("Nome: ")                 # conversa com o usuário
    email = input("E-mail: ")
    senha = input("Senha: ")

    for u in usuarios:                     # confere a regra
        if u["email"] == email:
            print("E-mail já cadastrado!")
            return

    novo = criar_usuario("Cliente", nome, email, senha)   # preenche a ficha
    usuarios.append(novo)                  # guarda
    print("Cadastrado com sucesso!")
```

### O caminho da informação

```
Usuário digita  →  ROTA (pergunta e confere)  →  MODELO (monta a ficha)  →  guarda
```

### Resumo

| | Modelo | Rota |
|---|---|---|
| Responde à pergunta | O que **é**? | O que **fazer**? |
| Tem `input()` ou `print()`? | ❌ Não | ✅ Sim |
| Tem regras (ex: e-mail repetido)? | ❌ Não | ✅ Sim |
| Exemplo | "Usuário tem nome, e-mail e senha" | "Cadastrar usuário" |

**Regra de ouro:** se o código tem `input()` ou `print()`, ele vai na **rota**. Se só diz quais campos existem, vai no **modelo**.

---

## frontend/

É a "parte da frente": as telas que o usuário vai ver. **Será definida mais adiante.**

---

## Como cada menu do sistema se encaixa

| Menu | Opção | Arquivo |
|---|---|---|
| Inicial | Cadastrar usuário / Fazer login | `rotas/usuarios.py` |
| Inicial | Consultar serviços | `rotas/servicos.py` |
| Cliente | Consultar e pesquisar serviços | `rotas/servicos.py` |
| Cliente | Solicitar orçamento / Meus orçamentos | `rotas/orcamentos.py` |
| Cliente | Avaliar prestador | `rotas/avaliacoes.py` |
| Prestador | Cadastrar, ver e editar serviços | `rotas/servicos.py` |
| Prestador | Ver e responder orçamentos | `rotas/orcamentos.py` |
| Prestador | Ver avaliações e média | `rotas/avaliacoes.py` |

---

## Regras para o time

- Tudo em português. Nomes de arquivo **sem acento, sem ç e sem espaço** (`orcamento.py`, nunca `orçamento.py`).
- Antes de começar a trabalhar: `git pull`.
- Ao terminar: no VS Code, aba **Source Control**, escreva a mensagem e clique em **Commit & Sync**.
- Mensagens de commit: `feat:` (coisa nova), `fix:` (correção), `docs:` (documentação).
