# Roteiro de testes — Coonecta Eventos

Este roteiro passa por **todas as funcionalidades** do sistema, na ordem em que uma pessoa usaria de verdade.
Para cada passo, ele mostra **o que escolher, o que digitar em cada campo e o que o sistema deve responder**.

As respostas abaixo foram tiradas de uma execução real do sistema. Se aparecer algo diferente, anote o passo: é sinal de que algo mudou ou quebrou.

> Os passos marcados com ⚠️ são **testes de erro**: digitamos algo errado de propósito para mostrar que o sistema não aceita.
> Na tela, as mensagens de sucesso começam com `>>` e as de erro com `!!`.

---

## Antes de começar

1. Para começar com o sistema **vazio** (e os números deste roteiro baterem), apague a pasta `backend/dados`. O sistema cria de novo sozinho.
2. Abra o terminal na pasta do projeto e rode:

```bash
cd backend
python3 executar.py        # no Windows: python executar.py
```

3. Deve aparecer o menu inicial:

```
============================================================
              COONECTA EVENTOS - MENU INICIAL
============================================================
             Clientes e fornecedores de eventos

   1. Cadastrar
   2. Entrar
   3. Ver serviços
   4. Sair
------------------------------------------------------------
```

### Menus usados no roteiro

**Área do Prestador:** 1 Cadastrar serviço · 2 Meus serviços · 3 Editar serviço · 4 Excluir serviço · 5 Adicionar trabalho ao portfólio · 6 Meu portfólio · 7 Ver pedidos de orçamento · 8 Responder pedido · 9 Minhas avaliações · 10 Minhas notificações · 11 Meu perfil · 12 Sair da conta

**Área do Cliente:** 1 Ver serviços · 2 Buscar serviços · 3 Ver avaliações de um serviço · 4 Ver portfólio de um fornecedor · 5 Ver contato de um fornecedor · 6 Pedir orçamento · 7 Meus orçamentos · 8 Avaliar um prestador · 9 Minhas notificações · 10 Meu perfil · 11 Sair da conta

### Pessoas usadas no teste

| | Prestadora | Cliente |
|---|---|---|
| Nome | Ana Souza | Bruno Lima |
| E-mail | `ana@festas.com` | `bruno@email.com` |
| Senha | `festa123` | `bruno123` |
| Telefone | `73999991111` | `73988887777` |
| CPF | `529.982.247-25` | `111.444.777-35` |
| Cidade / Bairro | Eunápolis / Centro | Porto Seguro / Taperapuan |
| Negócio | Ana Festas (Buffet, 10 anos, @anafestas) | — |

> Os CPFs acima são números **válidos para teste** (passam no cálculo dos dígitos verificadores). Não são de pessoas reais.

---

## Parte 1 — Cadastro da prestadora (RF01)

| Passo | O sistema pergunta | Digite | O sistema responde |
|---|---|---|---|
| 1 | Escolha uma opção | `1` (Cadastrar) | Título **CADASTRO** e "Tipo de conta": 1. Cliente / 2. Prestador de serviço |
| 2 | Você é | `2` | — |
| 3 | Nome completo | `Ana Souza` | — |
| 4 ⚠️ | E-mail | `ana@festas` | **!! E-mail inválido. Exemplo: nome@email.com** |
| 5 | E-mail | `ana@festas.com` | — |
| 6 | Senha (mínimo 6 caracteres) | `festa123` | — |
| 7 | Repita a senha | `festa123` | — |
| 8 | Telefone com DDD | `73999991111` | — |
| 9 ⚠️ | CPF | `111.111.111-11` | **!! CPF inválido. Confira os números.** |
| 10 | CPF | `529.982.247-25` | — |
| 11 | Cidade | `Eunápolis` | — |
| 12 | Bairro | `Centro` | `-- Dados do negócio --` |
| 13 | Nome do negócio | `Ana Festas` | `-- Categorias --` (1. Buffet ... 6. Cerimonial) |
| 14 | Escolha o número da categoria | `1` (Buffet) | — |
| 15 | Anos de experiência | `10` | — |
| 16 | CNPJ (opcional) | *(só aperte Enter)* | — |
| 17 | Instagram (opcional) | `@anafestas` | — |
| 18 | Fale um pouco sobre o seu trabalho | `Buffet completo para casamentos e aniversários` | **>> Cadastro realizado com sucesso!** / Bem-vindo(a), Ana Souza! |

**Resultado esperado:** o sistema entra **direto** na Área do Prestador, mostrando antes:

```
============================================================
                     NOTIFICAÇÕES NOVAS
============================================================
  * Bem-vindo(a) ao Coonecta Eventos! Comece cadastrando seu primeiro serviço.
```

---

## Parte 2 — Serviços e portfólio da prestadora (RF04, RF10)

### 2.1 Cadastrar o primeiro serviço

| Passo | O sistema pergunta | Digite | O sistema responde |
|---|---|---|---|
| 1 | Escolha uma opção | `1` | Título **CADASTRAR SERVIÇO** e a lista de categorias |
| 2 | Escolha o número da categoria | `1` (Buffet) | — |
| 3 | Nome do serviço | `Buffet Casamento Completo` | — |
| 4 | Descrição | `Buffet para 100 pessoas com garçons` | — |
| 5 ⚠️ | Preço base | `1.500,00` | **!! Preço inválido. Use só números, com vírgula ou ponto (ex: 1500,00).** |
| 6 | Preço base | `1500,00` | **>> Serviço cadastrado! ID: 1** |

### 2.2 Cadastrar um segundo serviço (para testar a exclusão)

| Passo | O sistema pergunta | Digite | O sistema responde |
|---|---|---|---|
| 1 | Escolha uma opção | `1` | — |
| 2 | Categoria | `2` (Fotografia) | — |
| 3 | Nome do serviço | `Cobertura Fotográfica` | — |
| 4 | Descrição | `Fotos do evento inteiro` | — |
| 5 | Preço base | `800` | **>> Serviço cadastrado! ID: 2** |

### 2.3 Ver os meus serviços

Digite `2`. Cada serviço aparece como um cartão:

```
------------------------------------------------------------
  [ID 1]  Buffet Casamento Completo
------------------------------------------------------------
  Categoria:     Buffet
  Descrição:     Buffet para 100 pessoas com garçons
  Preço base:    R$ 1.500,00
  Fornecedor:    Ana Festas (Ana Souza)
  Experiência:   10 ano(s) | Eunápolis
  Contato:       (73) 99999-1111 | ana@festas.com
  Instagram:     @anafestas
  Avaliação:     ainda sem avaliações
```

### 2.4 Editar o preço do serviço 1

| Passo | O sistema pergunta | Digite | O sistema responde |
|---|---|---|---|
| 1 | Escolha uma opção | `3` | Tabela com ID, Serviço, Categoria e Preço dos 2 serviços |
| 2 | ID do serviço que deseja editar (0 para voltar) | `1` | Deixe em branco e aperte Enter para manter o valor atual. |
| 3 | Nome [Buffet Casamento Completo] | *(Enter)* | — |
| 4 | Descrição [...] | *(Enter)* | — |
| 5 | Preço base [R$ 1.500,00] | `1600` | **>> Serviço atualizado!** |

### 2.5 Excluir o serviço 2

| Passo | O sistema pergunta | Digite | O sistema responde |
|---|---|---|---|
| 1 | Escolha uma opção | `4` | Tabela dos serviços |
| 2 | ID do serviço que deseja excluir (0 para voltar) | `2` | Tem certeza que deseja excluir "Cobertura Fotográfica"? |
| 3 | (s/n) | `s` | **>> Serviço excluído!** |

### 2.6 Portfólio

| Passo | O sistema pergunta | Digite | O sistema responde |
|---|---|---|---|
| 1 | Escolha uma opção | `5` | Título **ADICIONAR TRABALHO AO PORTFÓLIO** |
| 2 | Título do trabalho | `Casamento na praia 2025` | — |
| 3 | Descrição | `Buffet para 150 convidados em Porto Seguro` | — |
| 4 | Link da foto (opcional) | `instagram.com/p/exemplo` | **>> Trabalho adicionado ao portfólio!** |
| 5 | Escolha uma opção | `6` | Título **MEU PORTFÓLIO**, "1 trabalho(s)" e o cartão do trabalho com descrição e foto |
| 6 | Escolha uma opção | `12` | **>> Saindo da conta...** |

---

## Parte 3 — Cadastro do cliente (RF01)

| Passo | O sistema pergunta | Digite | O sistema responde |
|---|---|---|---|
| 1 | Escolha uma opção | `1` | — |
| 2 | Você é | `1` (Cliente) | — |
| 3 | Nome completo | `Bruno Lima` | — |
| 4 | E-mail | `bruno@email.com` | — |
| 5 | Senha | `bruno123` | — |
| 6 | Repita a senha | `bruno123` | — |
| 7 | Telefone com DDD | `73988887777` | — |
| 8 | CPF | `111.444.777-35` | — |
| 9 | Cidade | `Porto Seguro` | — |
| 10 | Bairro | `Taperapuan` | **>> Cadastro realizado com sucesso!** / Bem-vindo(a), Bruno Lima! |

**Resultado esperado:** o cliente **não** responde perguntas do negócio, entra **direto** na Área do Cliente e vê:

```
  * Bem-vindo(a) ao Coonecta Eventos! Veja os serviços e peça seu primeiro orçamento.
```

---

## Parte 4 — Cliente procura e pede orçamento (RF04, RF05, RF06, RF07, RF10)

| Passo | O sistema pergunta | Digite | O sistema responde |
|---|---|---|---|
| 1 | Escolha uma opção | `1` | Título **SERVIÇOS DISPONÍVEIS**, "1 serviço(s)" e o cartão do serviço **ID 1**, agora com **R$ 1.600,00** |
| 2 | Escolha uma opção | `2` | Título **BUSCAR SERVIÇOS** |
| 3 | O que você procura? | `buffet` | **1 serviço(s) encontrado(s) para "buffet"** e o cartão do serviço |
| 4 | Escolha uma opção | `4` | Título **PORTFÓLIO DE UM FORNECEDOR** e a tabela: `1  Ana Festas  Buffet  Eunápolis` |
| 5 | Escolha o fornecedor (0 para voltar) | `1` | `-- Portfólio de Ana Festas --` e o cartão "Casamento na praia 2025" |
| 6 | Escolha uma opção | `5` | Título **CONTATO DO FORNECEDOR** e a mesma tabela de fornecedores |
| 7 | Escolha o fornecedor (0 para voltar) | `1` | Cartão **Ana Festas (Ana Souza)** com WhatsApp: (73) 99999-1111 / E-mail: ana@festas.com / Instagram: @anafestas |
| 8 ⚠️ | Escolha uma opção | `8` (Avaliar) | **Você só pode avaliar prestadores que responderam um orçamento seu.** |
| 9 | Escolha uma opção | `6` | Título **PEDIR ORÇAMENTO** e a tabela de serviços |
| 10 | ID do serviço (0 para voltar) | `1` | `-- Pedido para: Buffet Casamento Completo (Buffet) --` |
| 11 ⚠️ | Data do evento (ex: 20122026 ou 20/12/2026) | `31022027` | **!! Data inválida. Use dia, mês e ano (ex: 20122026) e uma data que ainda não passou.** (31 de fevereiro não existe) |
| 12 | Data do evento | `20122026` *(só números)* | **Data registrada: 20/12/2026** |
| 13 ⚠️ | Quantidade de convidados | `0` | **!! Digite um número maior que zero.** |
| 14 | Quantidade de convidados | `120` | — |
| 15 | Detalhes do evento | `Casamento na praia às 17h` | **>> Pedido de orçamento nº 1 enviado!** |
| 16 ⚠️ | Escolha uma opção | `6` e depois ID `1` | **!! Você já tem um pedido aguardando resposta para este serviço.** |
| 17 | Escolha uma opção | `7` | Tabela: `1  Buffet Casament…  Ana Festas  20/12/2026  Pendente` / Ainda não existem respostas para os seus pedidos. |
| 18 | Digite o nº do pedido | `1` | Cartão **Pedido nº 1 \| Status: Pendente** e "Aguardando resposta do prestador." |
| 19 | Deseja cancelar este pedido? | `n` | — |
| 20 | Escolha uma opção | `11` | **>> Saindo da conta...** |

> Datas que já passaram também são recusadas. A data também pode ser digitada como `20/12/2026`, `20-12-2026` ou `20.12.2026`.

---

## Parte 5 — Login com senha errada (RF02) ⚠️

| Passo | O sistema pergunta | Digite | O sistema responde |
|---|---|---|---|
| 1 | Escolha uma opção | `2` (Entrar) | Título **ENTRAR** |
| 2 | E-mail | `bruno@email.com` | — |
| 3 | Senha | `senhaerrada` | **!! E-mail ou senha incorretos.** |
| 4 | Esqueceu sua senha? (s/n) | `n` | Volta ao menu inicial |

---

## Parte 6 — Prestadora responde o orçamento (RF07, RF08)

| Passo | O sistema pergunta | Digite | O sistema responde |
|---|---|---|---|
| 1 | Escolha uma opção | `2` | — |
| 2 | E-mail / Senha | `ana@festas.com` / `festa123` | **>> Bem-vindo(a), Ana Souza!** e a notificação: **Você recebeu um pedido de orçamento (nº 1) de Bruno Lima para "Buffet Casamento Completo".** |
| 3 | Escolha uma opção | `7` | Tabela: `1  Buffet Casament…  Bruno Lima  20/12/2026  Pendente` / 1 pedido(s) aguardando sua resposta. |
| 4 | Digite o nº do pedido | `1` | Cartão do pedido, com o contato do cliente: (73) 98888-7777 \| bruno@email.com |
| 5 | Deseja responder agora? | `s` | `-- O que deseja fazer? --` 1. Enviar orçamento / 2. Recusar pedido / 0. Voltar |
| 6 | Escolha | `1` | — |
| 7 | Valor do orçamento | `1400,00` | — |
| 8 | Condições | `Inclui garçons e decoração da mesa. 50% na reserva.` | — |
| 9 | Mensagem para o cliente (opcional) | `Obrigada pelo contato!` | **>> Resposta enviada!** |
| 10 | Escolha uma opção | `12` | **>> Saindo da conta...** |

---

## Parte 7 — Cliente vê a resposta, avalia e edita o perfil (RF03, RF07, RF08, RF09)

| Passo | O sistema pergunta | Digite | O sistema responde |
|---|---|---|---|
| 1 | Entrar | `2` → `bruno@email.com` → `bruno123` | Notificação: **Seu pedido de orçamento nº 1 foi respondido por Ana Festas: R$ 1.400,00. Veja em 'Meus orçamentos'.** |
| 2 | Escolha uma opção | `7` | Tabela com o pedido 1 **Respondido** |
| 3 | Digite o nº do pedido | `1` | Cartão com `-- Orçamento do prestador --`: **Valor: R$ 1.400,00** / Condições / Mensagem |
| 4 | Escolha uma opção | `8` | `-- Prestadores que te atenderam --` 1. Ana Festas (Ana Souza) |
| 5 | Escolha o prestador (0 para voltar) | `1` | — |
| 6 | Nota (1 a 5) | `5` | — |
| 7 | Comentário | `Comida maravilhosa e equipe atenciosa!` | **>> Avaliação registrada!** |
| 8 | Escolha uma opção | `3` | Tabela de serviços |
| 9 | ID do serviço (0 para voltar) | `1` | `-- Avaliações de Ana Festas --` / **Média: 5.0/5 (1 avaliação(ões))** / `★★★★★  5/5  -  Bruno Lima` e o comentário |
| 10 | Escolha uma opção | `9` | **MINHAS NOTIFICAÇÕES**: boas-vindas e resposta do orçamento |
| 11 | Escolha uma opção | `10` | **MEU PERFIL** com telefone `(73) 98888-7777` e CPF `111.444.777-35` formatados |
| 12 | Deseja editar seu perfil? | `s` | `-- Editar perfil --` (E-mail e CPF não podem ser alterados.) |
| 13 | Nome [Bruno Lima] | `Bruno Lima Santos` | — |
| 14 | Telefone / Cidade / Bairro | *(Enter nos três)* | — |
| 15 | Deseja mudar a senha? | `n` | **>> Perfil atualizado!** |
| 16 | Escolha uma opção | `11` | **>> Saindo da conta...** |

---

## Parte 8 — Recuperar a senha (RF02 / UC02)

| Passo | O sistema pergunta | Digite | O sistema responde |
|---|---|---|---|
| 1 | Entrar | `2` → `bruno@email.com` → `errada` | **!! E-mail ou senha incorretos.** |
| 2 | Esqueceu sua senha? | `s` | Título **RECUPERAR SENHA** / Para sua segurança, confirme os dados do cadastro |
| 3 | E-mail | `bruno@email.com` | — |
| 4 | CPF | `11144477735` | — |
| 5 | Telefone com DDD | `73988887777` | **>> Dados confirmados! Crie sua nova senha.** |
| 6 | Senha / Repita a senha | `novasenha1` / `novasenha1` | **>> Senha alterada! Agora você já pode entrar com a nova senha.** |
| 7 | Entrar | `2` → `bruno@email.com` → `novasenha1` | **>> Bem-vindo(a), Bruno Lima Santos!** (com o nome novo) e a notificação **Sua senha foi alterada.** |

---

## Parte 9 — Cliente cancela um pedido e faz outro

*(continua logado como Bruno, com a senha `novasenha1`)*

| Passo | O sistema pergunta | Digite | O sistema responde |
|---|---|---|---|
| 1 | Escolha uma opção | `6` → ID `1` | — |
| 2 | Data / Convidados / Detalhes | `15/01/2027` / `50` / `Aniversário de 30 anos` | Data registrada: 15/01/2027 / **>> Pedido de orçamento nº 2 enviado!** |
| 3 | Escolha uma opção | `7` | Tabela: pedido 1 **Respondido** e pedido 2 **Pendente** |
| 4 | Digite o nº do pedido | `2` | Cartão do pedido 2 |
| 5 | Deseja cancelar este pedido? | `s` | **>> Pedido cancelado.** |
| 6 | Escolha uma opção | `6` → `1` / `10.02.2027` / `80` / `Formatura` | Data registrada: 10/02/2027 / **>> Pedido de orçamento nº 3 enviado!** |
| 7 | Escolha uma opção | `11` | **>> Saindo da conta...** |

---

## Parte 10 — Prestadora recusa um pedido e vê suas avaliações (RF07, RF08, RF09)

| Passo | O sistema pergunta | Digite | O sistema responde |
|---|---|---|---|
| 1 | Entrar | `2` → `ana@festas.com` → `festa123` | 3 notificações: pedido nº 2 recebido · **pedido nº 2 cancelado por Bruno Lima Santos** · pedido nº 3 recebido |
| 2 | Escolha uma opção | `8` (Responder pedido) | Tabela só com o **Nº 3** (o 2 foi cancelado e o 1 já foi respondido) |
| 3 | Digite o nº do pedido | `3` | Cartão do pedido 3 e as opções 1. Enviar / 2. Recusar / 0. Voltar |
| 4 | Escolha | `2` (Recusar pedido) | — |
| 5 | Motivo da recusa | `Já tenho outro evento nessa data` | **>> Resposta enviada!** |
| 6 | Escolha uma opção | `9` | **MINHAS AVALIAÇÕES**: Média: 5.0/5 (1 avaliação(ões)) / `★★★★★  5/5  -  Bruno Lima Santos` |
| 7 | Escolha uma opção | `10` | Todas as 5 notificações da prestadora |
| 8 | Escolha uma opção | `12` | **>> Saindo da conta...** |
| 9 | Escolha uma opção | `4` | **>> Até logo!** |

---

## Conferindo os dados salvos

Abra a pasta `backend/dados`. Ao final do roteiro, ela deve ter:

| Arquivo | O que deve ter |
|---|---|
| `usuarios.txt` | 2 linhas: Ana (Prestador) e Bruno (Cliente, com nome "Bruno Lima Santos") |
| `servicos.txt` | 1 linha: Buffet Casamento Completo, preço 1600 |
| `orcamentos.txt` | 3 linhas: nº 1 **Respondido**, nº 2 **Cancelado**, nº 3 **Recusado** |
| `avaliacoes.txt` | 1 linha: nota 5 |
| `portfolio.txt` | 1 linha: Casamento na praia 2025 |
| `notificacoes.txt` | As notificações dos dois usuários |

---

## Requisitos cobertos por este roteiro

| Requisito | Onde é testado |
|---|---|
| RF01 Cadastro | Partes 1 e 3 |
| RF02 Login (e recuperar senha) | Partes 5 e 8 |
| RF03 Gerenciamento de perfil | Parte 7 |
| RF04 Visualização de fornecedores e serviços | Partes 2 e 4 |
| RF05 Pesquisa de serviços | Parte 4 |
| RF06 Contato | Parte 4 |
| RF07 Orçamentos | Partes 4, 6, 7, 9 e 10 |
| RF08 Notificações | Partes 1, 3, 6, 7, 8 e 10 |
| RF09 Avaliações | Partes 7 e 10 |
| RF10 Portfólio | Partes 2 e 4 |
