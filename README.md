# Coonecta Eventos

Projeto Integrador do curso de **Análise e Desenvolvimento de Sistemas (ADS)**.

O **Coonecta Eventos** é um sistema de terminal, feito em **Python**, que conecta **clientes** que vão organizar um evento a **prestadores de serviço** (Buffet, Fotografia, Decoração, Música, Espaço para eventos e Cerimonial).

- **Cliente:** vê e pesquisa serviços, vê o portfólio e o contato dos fornecedores, pede orçamentos, acompanha as respostas e avalia os prestadores.
- **Prestador:** cadastra, edita e exclui serviços, monta o portfólio, recebe e responde pedidos de orçamento e vê as avaliações que recebeu.

---

## Como rodar

**Requisito:** Python 3.9 ou mais novo. O projeto usa **só a biblioteca padrão** do Python, então não é preciso instalar nada.

Abra o terminal na pasta do projeto e digite:

```bash
cd backend
python3 executar.py
```

No Windows, use `python executar.py` (ou `py executar.py`).

Sempre rode **de dentro da pasta `backend`**, senão o Python não encontra os outros arquivos.

Para testar o sistema passo a passo, siga o arquivo **[ROTEIRO_DE_TESTES.md](ROTEIRO_DE_TESTES.md)**.

---

## Funcionalidades

### Menu inicial (sem login)
1. **Cadastrar** como Cliente ou Prestador (depois do cadastro, a pessoa já entra na conta)
2. **Entrar** (se errar a senha, o sistema oferece a recuperação de senha)
3. **Ver serviços** (qualquer pessoa pode ver, mesmo sem conta)
4. **Sair**

### Área do Cliente
| Grupo | Opções |
|---|---|
| Fornecedores e serviços | 1 Ver serviços · 2 Buscar serviços · 3 Ver avaliações de um serviço · 4 Ver portfólio de um fornecedor · 5 Ver contato de um fornecedor |
| Orçamentos | 6 Pedir orçamento · 7 Meus orçamentos (com detalhes e opção de cancelar) |
| Avaliações e avisos | 8 Avaliar um prestador · 9 Minhas notificações |
| Minha conta | 10 Meu perfil (ver e editar) · 11 Sair da conta |

### Área do Prestador
| Grupo | Opções |
|---|---|
| Serviços | 1 Cadastrar · 2 Meus serviços · 3 Editar · 4 Excluir |
| Portfólio | 5 Adicionar trabalho · 6 Meu portfólio |
| Orçamentos | 7 Ver pedidos recebidos · 8 Responder pedido (enviar valor ou recusar) |
| Avaliações e avisos | 9 Minhas avaliações (com média) · 10 Minhas notificações |
| Minha conta | 11 Meu perfil (ver e editar) · 12 Sair da conta |

---

## Estrutura do projeto

```
coonecta-eventos/
├── backend/
│   ├── executar.py        ← o arquivo que você roda (menus)
│   ├── tela.py            ← formatação das telas (títulos, tabelas, cartões)
│   ├── banco.py           ← ler e salvar os dados
│   ├── usuarios.py
│   ├── servicos.py
│   ├── orcamentos.py
│   ├── avaliacoes.py
│   ├── portfolio.py
│   ├── notificacoes.py
│   ├── contato.py
│   ├── requirements.txt
│   └── dados/             ← criada sozinha (não vai para o GitHub)
├── frontend/              ← protótipo de tela (HTML), para uma próxima etapa
├── .gitignore
├── README.md
└── ROTEIRO_DE_TESTES.md   ← passo a passo para testar todas as funções
```

**Regra do projeto:** cada assunto tem um arquivo, e tudo sobre aquele assunto fica nele.
Dentro de cada arquivo, a parte de cima (`DADOS E VALIDAÇÕES`) lê, salva e confere os dados, e a parte de baixo (`TELAS E AÇÕES`) conversa com o usuário (`input` e `print`).

---

## Arquivos da pasta `backend/`

### `executar.py`
**Liga o sistema.** Mostra o menu inicial, a Área do Cliente e a Área do Prestador, e chama as funções dos outros arquivos. A função `abrir_area()` leva cada pessoa para o menu certo, de acordo com o tipo de conta. **É o único arquivo que você roda.**

### `tela.py`
Deixa **tudo o que aparece no terminal com o mesmo visual**. Todos os outros arquivos usam estas funções:
- `titulo()`, `subtitulo()`, `secao()` e `linha()`: títulos centralizados e divisões.
- `opcao()`: opções de menu numeradas e alinhadas.
- `cabecalho_cartao()` e `campo()`: mostram um serviço, um pedido ou um perfil como um "cartão", com os rótulos alinhados.
- `mensagem()` e `erro()`: avisos de sucesso (`>>`) e de erro (`!!`).
- `dinheiro()`, `telefone()` e `cpf()`: formatam valores (ex: `R$ 1.500,00`, `(73) 99999-1111`, `529.982.247-25`).
- `escolher_da_lista()`: pede um número de uma lista, com a opção 0 para voltar.

Para mudar o visual do sistema inteiro (por exemplo, a largura das linhas), basta mexer neste arquivo.

### `banco.py`
**Lê e salva os dados** nos arquivos `.txt` da pasta `dados`. Cada linha do arquivo é um registro, com os campos separados por `;`.
- `criar_arquivos()`: cria a pasta e os arquivos, se não existirem.
- `ler()` e `salvar()`: transformam as linhas em dicionários e vice-versa.
- `novo_id()`: gera o próximo número de identificação.
- `pedir_texto()`: repete a pergunta até a pessoa digitar alguma coisa.

### `usuarios.py`
Tudo sobre as **pessoas cadastradas**.
- **Dados de todo usuário:** tipo (Cliente ou Prestador), nome, e-mail, senha, telefone, CPF, cidade e bairro.
- **Só do prestador:** nome do negócio, categoria, anos de experiência, CNPJ (opcional), Instagram (opcional) e descrição do trabalho.
- **Cadastrar**, **entrar**, **recuperar a senha** (confirmando e-mail, CPF e telefone), **ver e editar o perfil** (e-mail e CPF não mudam; para trocar a senha é preciso informar a senha atual).
- `escolher_prestador()`: mostra a lista numerada de fornecedores para o cliente escolher, sem precisar saber o e-mail de ninguém.

### `servicos.py`
Tudo sobre os **serviços** que os prestadores oferecem.
- **Dados:** dono, categoria, nome, descrição e preço base.
- **Listar** e **buscar** (por nome, categoria, descrição ou nome do negócio).
- **Cadastrar**, **ver os meus**, **editar** e **excluir** (só o dono pode editar ou excluir).
- Cada serviço aparece como um cartão, com o contato do prestador e a **média das avaliações**. Para escolher um serviço, aparece uma tabela resumida (ID, nome, categoria e preço).

### `orcamentos.py`
Tudo sobre os **pedidos de orçamento**.
- **Dados:** cliente, prestador, serviço, data do evento, convidados, detalhes, status, valor, condições e mensagem.
- **Status:** `Pendente` → `Respondido` ou `Recusado` (pelo prestador) ou `Cancelado` (pelo cliente).
- **Cliente:** pede orçamento, vê a tabela dos pedidos e os detalhes de cada um, e pode cancelar enquanto estiver pendente.
- **Prestador:** vê os pedidos recebidos e responde com **valor, condições e mensagem**, ou recusa informando o motivo.
- **Data do evento:** pode ser digitada só com números (`20122026`); o sistema coloca as barras e mostra "Data registrada: 20/12/2026".

### `avaliacoes.py`
Tudo sobre as **notas dos clientes**.
- **Dados:** cliente, prestador, nota de **1 a 5** e comentário.
- O cliente só pode avaliar um prestador que **respondeu um orçamento** dele, e **uma vez só**.
- O prestador vê as avaliações (com estrelas, ex: ★★★★★) e a **média**. O cliente vê as avaliações de um serviço antes de contratar.

### `portfolio.py`
A **vitrine** de cada prestador: trabalhos que ele já fez.
- **Dados:** prestador, título, descrição e link da foto.
- O prestador **adiciona** trabalhos e vê o **seu portfólio**. O cliente escolhe um fornecedor na lista e vê o **portfólio** dele.
- Como o sistema é no terminal, a foto entra como **link** (Instagram, Google Drive etc.).

### `notificacoes.py`
Os **avisos** do sistema.
- **Dados:** para quem é, a mensagem e se já foi lida.
- As novas aparecem **logo depois do login**, e todas podem ser vistas em "Minhas notificações".
- **Avisos que o sistema envia:**
  - Boas-vindas ao se cadastrar
  - Prestador: novo pedido de orçamento e pedido cancelado
  - Cliente: orçamento respondido ou recusado
  - Senha alterada (aviso de segurança)

### `contato.py`
O cliente escolhe um fornecedor na lista e vê os **meios de contato** dele (WhatsApp/telefone, e-mail e Instagram), usando os dados do cadastro do prestador. Se o prestador não tiver contato cadastrado, o sistema avisa.

### `requirements.txt`
Fica **vazio** de propósito: o projeto usa só a biblioteca padrão do Python.

---

## Onde ficam os dados

Tudo é salvo em arquivos de texto na pasta **`backend/dados/`**:

| Arquivo | Guarda |
|---|---|
| `usuarios.txt` | Clientes e prestadores |
| `servicos.txt` | Serviços |
| `orcamentos.txt` | Pedidos de orçamento e respostas |
| `avaliacoes.txt` | Notas e comentários |
| `portfolio.txt` | Trabalhos do portfólio |
| `notificacoes.txt` | Avisos dos usuários |

A pasta `dados/` está no `.gitignore` e **não vai para o GitHub**, porque guarda senhas e CPFs. Cada pessoa tem os próprios dados de teste. Para começar do zero, é só apagar a pasta: o sistema cria de novo.

---

## Tratamento de erros e validações

O sistema não aceita dados errados e explica o problema (com `!!`) para a pessoa digitar de novo:

| Onde | O que é conferido |
|---|---|
| Campos obrigatórios | Não aceita campo vazio ("Este campo é obrigatório.") |
| E-mail | Formato válido (tem `@` e domínio com ponto) e não pode repetir |
| Senha | Mínimo de 6 caracteres e confirmação igual |
| Telefone | Só números, com DDD (10 ou 11 dígitos) |
| CPF | Cálculo oficial dos dígitos verificadores, sem números repetidos, e não pode repetir |
| CNPJ | 14 números (opcional) |
| Preço e valor | Número com vírgula ou ponto |
| Data do evento | Aceita `20122026`, `20/12/2026`, `20-12-2026` ou `20.12.2026`; a data precisa existir (31/02 não existe) e não pode já ter passado |
| Convidados e nota | Número dentro do limite (convidados > 0, nota de 1 a 5) |
| Opções de menu e listas | Opção inexistente mostra "Opção inválida!" e diz quais números são aceitos; 0 volta |
| Permissões | Só o dono edita/exclui o serviço; só avalia quem teve orçamento respondido; não repete pedido pendente para o mesmo serviço |
| Arquivo de dados | O caractere `;` digitado pelo usuário é trocado por `,` para não quebrar as colunas |

---

## Relação com o documento do projeto

| Arquivo | Requisitos | Casos de uso |
|---|---|---|
| `usuarios.py` | RF01 Cadastro · RF02 Login · RF03 Gerenciamento de Perfil | UC01, UC02, UC10 |
| `servicos.py` | RF04 Visualização de Fornecedores e Serviços · RF05 Pesquisa de Serviços | UC03, UC04 |
| `contato.py` | RF06 Contato | UC06 |
| `orcamentos.py` | RF07 Consulta de Orçamentos | UC07, UC08, UC12, UC13 |
| `notificacoes.py` | RF08 Notificações | UC11 |
| `avaliacoes.py` | RF09 Avaliações | UC09, UC14 |
| `portfolio.py` | RF10 Portfólio | UC05 |

### Além do escopo original
- Excluir serviço
- Cancelar pedido de orçamento
- Bloqueio de pedido repetido para o mesmo serviço
- Validação real de CPF e de datas (data que existe e que ainda não passou)
- Data digitada só com números, formatada automaticamente
- Escolha de fornecedor por lista numerada (sem precisar do e-mail)
- Telas padronizadas: tabelas, cartões, valores em reais e telefone/CPF formatados
- Notificações de boas-vindas e de senha alterada

---

## Equipe

| Integrante | Responsável por |
|---|---|
| Yan Silva | `usuarios.py`, `orcamentos.py`, menus do `executar.py`, `tela.py`, coordenação |
| Carlos Eduardo | `servicos.py`, `portfolio.py`, `contato.py`, protótipo do `frontend` |
| Julia Eliza | `avaliacoes.py`, `notificacoes.py`, exclusão de serviço |
| Ana Carolina | Documentação (README) e testes |

---

## Como a equipe trabalha (Git)

- Antes de começar: **Sync Changes** (ou `git pull`).
- Avisar no grupo qual arquivo vai ser alterado.
- Depois de testar: no VS Code, aba **Source Control**, escrever a mensagem e clicar em **Commit & Sync**.
- Mensagens de commit: `feat:` (coisa nova), `fix:` (correção), `docs:` (documentação), `style:` (aparência).
- Nomes de arquivo **sem acento, sem ç e sem espaço** (`orcamentos.py`, nunca `orçamentos.py`).
