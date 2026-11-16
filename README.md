# Coonecta Eventos

Projeto universitário (ADS). Sistema que conecta **clientes** que vão fazer um evento com **prestadores de serviço** (Buffet, Fotografia, Decoração, Música e Espaço para eventos).

- **Cliente:** consulta e pesquisa serviços, pede orçamento, acompanha seus orçamentos e avalia prestadores.
- **Prestador:** cadastra e edita seus serviços, recebe e responde orçamentos e vê as avaliações que recebeu.

---

## Como rodar

Abra o terminal na pasta do projeto e digite:

```bash
cd backend
python3 executar.py
```

No Windows, use `python executar.py` (ou `py executar.py`).

---

## Estrutura do projeto

```
coonecta-eventos/
├── backend/
│   ├── executar.py
│   ├── banco.py
│   ├── usuarios.py
│   ├── servicos.py
│   ├── orcamentos.py
│   ├── avaliacoes.py
│   ├── portfolio.py
│   ├── notificacoes.py
│   └── requirements.txt
├── frontend/
└── README.md
```

**A regra é simples: cada assunto tem um arquivo, e tudo sobre aquele assunto fica nele.**

---

## Pastas

| Pasta | Responsável por |
|---|---|
| `backend/` | Todo o sistema: o menu, as regras e os dados. É onde a gente trabalha agora. |
| `frontend/` | As telas visuais do sistema. **Vai ser feita mais para frente**, por enquanto fica vazia. |

---

## Arquivos da pasta `backend/`

### `executar.py`
É o arquivo que **liga o sistema**. Mostra o menu inicial (Entrar, Criar conta, Ver serviços, Sair) e chama as funções dos outros arquivos. **É o único que você roda.**

### `banco.py`
**Lê e salva os dados** nos arquivos `.txt` da pasta `BancoDados` (criada sozinha). Os outros arquivos usam as funções `ler()` e `salvar()` daqui.

### `usuarios.py`
Tudo sobre as **pessoas cadastradas**:
- Como é um usuário: tipo (Cliente ou Prestador), nome, e-mail e senha. Prestador também tem nome do negócio e categoria.
- **Cadastrar usuário** (não deixa repetir e-mail).
- **Fazer login** (leva para a área do Cliente ou do Prestador).

### `servicos.py`
Tudo sobre os **serviços que os prestadores oferecem**:
- Como é um serviço: dono, categoria, nome, descrição e preço.
- **Listar** todos os serviços, **pesquisar** por nome ou categoria.
- **Cadastrar**, **ver os meus** e **editar** serviço (só o dono pode editar).

### `orcamentos.py`
Tudo sobre os **pedidos de orçamento**:
- Como é um orçamento: cliente, prestador, serviço, data do evento, convidados, detalhes, status (**Pendente** ou **Respondido**) e resposta.
- Cliente **pede orçamento** e **acompanha** os seus.
- Prestador **vê os pedidos** que recebeu e **responde** com preço e condições.

### `avaliacoes.py`
Tudo sobre as **notas dos clientes**:
- Como é uma avaliação: cliente, prestador, nota de **1 a 5** e comentário.
- Cliente **avalia** o prestador (só uma vez por prestador).
- Prestador **vê suas avaliações** e a **média das notas**.

### `portfolio.py`
Tudo sobre o **portfólio dos prestadores** (é a "vitrine" de cada fornecedor):
- Como é um item do portfólio: prestador dono, título do trabalho, descrição e link da foto.
- Prestador **cadastra** os trabalhos que já fez (ex: "Casamento na praia - decoração completa").
- Cliente **vê o portfólio** de um fornecedor antes de pedir orçamento, para conhecer a qualidade do trabalho.
- Como o sistema ainda é no terminal, a foto entra como **link** (ex: link do Instagram ou do Google Drive).

### `notificacoes.py`
Tudo sobre os **avisos do sistema**, para ninguém perder nada importante:
- Como é uma notificação: para quem é (e-mail), a mensagem e se já foi lida.
- O sistema **cria** um aviso quando algo acontece. Exemplos:
  - Prestador: *"Você recebeu um novo pedido de orçamento."*
  - Cliente: *"Seu orçamento foi respondido."*
  - Prestador: *"Você recebeu uma nova avaliação."*
- As notificações **aparecem logo depois do login**, e o usuário pode vê-las de novo no menu.

### `requirements.txt`
Lista de bibliotecas extras que o projeto usar. Por enquanto fica vazio.

---

## Como um arquivo usa o outro

Você só roda o `executar.py`. Ele **pega emprestadas** as funções dos outros arquivos com o `import`:

```python
from usuarios import cadastrar_usuario, fazer_login
#    ↑ arquivo         ↑ funções que quero usar
```

No `import` não se escreve o `.py`. E sempre rode o programa **de dentro da pasta `backend`** (`cd backend`), senão o Python não encontra os arquivos.

---

## Onde fica cada opção do menu

| Menu | Opção | Arquivo |
|---|---|---|
| Inicial | Criar conta / Entrar | `usuarios.py` |
| Inicial | Ver serviços | `servicos.py` |
| Cliente | Consultar e pesquisar serviços | `servicos.py` |
| Cliente | Solicitar orçamento / Meus orçamentos | `orcamentos.py` |
| Cliente | Avaliar prestador | `avaliacoes.py` |
| Cliente | Ver portfólio de um fornecedor | `portfolio.py` |
| Cliente | Minhas notificações | `notificacoes.py` |
| Prestador | Cadastrar, ver e editar serviços | `servicos.py` |
| Prestador | Ver e responder orçamentos | `orcamentos.py` |
| Prestador | Ver avaliações e média | `avaliacoes.py` |
| Prestador | Cadastrar e ver meu portfólio | `portfolio.py` |
| Prestador | Minhas notificações | `notificacoes.py` |

---

## Relação com o documento do projeto

Cada arquivo atende a requisitos (RF) e casos de uso (UC) do documento oficial do Coonecta Eventos:

| Arquivo | Requisitos | Casos de uso |
|---|---|---|
| `usuarios.py` | RF01 Cadastro, RF02 Login, RF03 Gerenciamento de Perfil, RF06 Contato | UC01, UC02, UC06, UC10 |
| `servicos.py` | RF04 Visualização de Fornecedores e Serviços, RF05 Pesquisa de Serviços | UC03, UC04 |
| `orcamentos.py` | RF07 Consulta de Orçamentos | UC07, UC08, UC12, UC13 |
| `avaliacoes.py` | RF09 Avaliações | UC09, UC14 |
| `portfolio.py` | RF10 Portfólio | UC05 |
| `notificacoes.py` | RF08 Notificações | UC11 |

---

## Regras para o time

- Tudo em português. Nomes de arquivo **sem acento, sem ç e sem espaço** (`orcamentos.py`, nunca `orçamentos.py`).
- Antes de começar a trabalhar: `git pull` (ou **Sync Changes** no VS Code).
- Avise no grupo qual arquivo você vai mexer.
- Ao terminar e testar: no VS Code, aba **Source Control**, escreva a mensagem e clique em **Commit & Sync**.
- Mensagens de commit: `feat:` (coisa nova), `fix:` (correção), `docs:` (documentação).
