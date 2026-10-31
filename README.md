
# 📚 Imersos — Biblioteca Pessoal

## Descrição

O **Imersos** é um sistema de gerenciamento de biblioteca pessoal desenvolvido em Python, com o objetivo de facilitar a organização de um acervo de livros.

O projeto busca oferecer funcionalidades como cadastro, busca, listagem, edição e remoção de livros, além do acompanhamento do status de leitura e do controle de empréstimos e devoluções.

A aplicação foi planejada para funcionar por meio de uma interface no terminal, utilizando `input()` e `print()`, sem necessidade de interface gráfica ou banco de dados. Os dados dos livros são armazenados localmente em arquivos JSON.

O sistema está em desenvolvimento, com algumas funcionalidades já implementadas e outras ainda em processo de integração.

O projeto faz parte da disciplina C14 e utiliza conceitos de engenharia de software, testes automatizados, integração contínua e metodologia ágil Scrum.

## Estrutura do projeto

| Pasta | Responsabilidade |
|---|---|
| `models/` | Classes de domínio (`Livro` e `Emprestimo`) e suas validações |
| `repository/` | Persistência dos dados em arquivo JSON |
| `services/` | Regras de negócio e operações sobre os livros |
| `terminal/` | Interface de terminal em desenvolvimento |
| `tests/` | Testes automatizados com Pytest |

## Integrantes

| Integrante | Responsabilidade |
|---|---|
| Giuliana Batistella | Serviços e regras de negócio |
| Júlia Seixas Souza | Persistência dos dados |
| Camile Brunieri Laraia | Modelo de empréstimos e CI/CD |
| Kauan de Abreu Carvalho | Modelo Livro, validações e status de leitura |
| Luis Otávio Garcia Godoy da Costa | Interface de terminal |

## Requisitos funcionais

Os requisitos funcionais descrevem as funcionalidades previstas para o sistema, incluindo aquelas ainda em desenvolvimento.

**RF01 — Cadastro de livros:** O sistema deve permitir cadastrar livros informando título, autor, ISBN, gênero, ano de publicação e status de leitura.

**RF02 — Validação dos dados:** O sistema deve impedir o cadastro de livros com título, autor ou ISBN vazios, ano menor ou igual a zero ou status de leitura inválido.

**RF03 — ISBN único:** O sistema deve impedir o cadastro de dois livros com o mesmo ISBN.

**RF04 — Listagem de livros:** O sistema deve permitir visualizar os livros cadastrados no acervo.

**RF05 — Busca de livros:** O sistema deve permitir buscar livros por título, autor ou gênero.

**RF06 — Edição de livros:** O sistema deve permitir alterar as informações de livros já cadastrados.

**RF07 — Remoção de livros:** O sistema deve permitir remover livros do acervo.

**RF08 — Controle de status de leitura:** O sistema deve permitir definir o status de leitura como "não iniciado", "lendo" ou "concluído", recusando valores inválidos.

**RF09 — Registro de empréstimos:** O sistema deve permitir registrar empréstimos, informando a pessoa responsável, a data do empréstimo e a data prevista de devolução.

**RF10 — Validação de empréstimos:** O sistema deve impedir empréstimos com dados obrigatórios ausentes, datas inconsistentes ou livros indisponíveis.

**RF11 — Devolução de livros:** O sistema deve permitir registrar a devolução de um livro emprestado, atualizando sua disponibilidade.

**RF12 — Empréstimos atrasados:** O sistema deve permitir identificar empréstimos cuja data prevista de devolução já passou.

**RF13 — Persistência dos dados:** O sistema deve salvar e carregar os dados dos livros em arquivos JSON locais.

**RF14 — Tratamento de arquivos:** O sistema deve tratar situações em que o arquivo de dados esteja ausente ou inválido, permitindo iniciar com um acervo vazio.

**RF15 — Interface de terminal:** O sistema deve apresentar um menu textual com as operações disponíveis e informar quando uma opção inválida for selecionada.

## Requisitos não funcionais

**RNF01 — Linguagem:** A aplicação deve ser desenvolvida utilizando Python.

**RNF02 — Modularidade:** O código deve possuir uma estrutura modular, separando modelos, repositórios, serviços e interface de terminal.

**RNF03 — Testabilidade:** As principais funcionalidades devem possuir testes automatizados utilizando Pytest.

**RNF04 — Gerenciamento de dependências:** O projeto deve utilizar Poetry para gerenciamento de dependências e ambiente virtual.

**RNF05 — Integração contínua:** O projeto deve utilizar Jenkins para automatizar o build e a execução dos testes.

**RNF06 — Versionamento:** O código-fonte deve ser versionado utilizando Git e hospedado no GitHub.

**RNF07 — Manutenibilidade:** O código deve seguir padrões de organização e nomenclatura que facilitem sua compreensão e manutenção.

**RNF08 — Compatibilidade:** A aplicação deve ser compatível com Python 3.13 ou superior.

**RNF09 — Usabilidade:** A interface deve apresentar mensagens claras e opções de fácil compreensão.

**RNF10 — Persistência local:** O armazenamento dos dados deve ser realizado em arquivos JSON locais.

**RNF11 — Confiabilidade:** O sistema deve realizar validações para evitar dados inconsistentes.

## Histórias de usuário

As histórias de usuário foram definidas para orientar o desenvolvimento das funcionalidades do sistema e são organizadas no Jira.

### História 1 — Cadastro de livros

**Responsável:** Kauan  
**Épico:** Livros

Como usuário, eu quero cadastrar um livro com título, autor, ISBN, gênero, ano e status de leitura para manter meu acervo organizado.

**Critérios de aceitação:**

- Dados válidos devem permitir o cadastro.
- Título, autor e ISBN não podem estar vazios.
- O ano deve ser maior que zero.
- O sistema deve impedir ISBN duplicado.

### História 2 — Controle de status de leitura

**Responsável:** Kauan  
**Épico:** Livros

Como usuário, eu quero informar se um livro está "não iniciado", "lendo" ou "concluído" para acompanhar meu progresso de leitura.

**Critérios de aceitação:**

- O sistema deve disponibilizar os três status de leitura.
- O status válido deve ser armazenado.
- Status inválidos devem ser recusados.

### História 3 — Persistência dos dados

**Responsável:** Júlia Seixas Souza  
**Épico:** Persistência

Como usuário, eu quero que os dados dos meus livros sejam salvos para recuperá-los posteriormente.

**Critérios de aceitação:**

- Os livros devem ser armazenados em arquivo JSON.
- Os dados devem permanecer disponíveis após o encerramento da aplicação.
- O sistema deve tratar arquivos ausentes ou inválidos.

### História 4 — Controle de empréstimos

**Responsável:** Camile Brunieri Laraia  
**Épico:** Empréstimos

Como usuário, eu quero registrar empréstimos de livros para controlar quem está com cada livro e quando deverá devolvê-lo.

**Critérios de aceitação:**

- O sistema deve registrar o responsável pelo empréstimo.
- A data de empréstimo e a data prevista de devolução devem ser informadas.
- Datas inconsistentes devem ser recusadas.
- O sistema deve permitir identificar empréstimos atrasados.

### História 5 — Interface de terminal

**Responsável:** Luis Otávio Garcia Godoy da Costa  
**Épico:** Interface

Como usuário, eu quero interagir com a biblioteca por meio de um menu no terminal para acessar as funcionalidades disponíveis.

**Critérios de aceitação:**

- O sistema deve apresentar um menu com as operações disponíveis.
- O usuário deve conseguir selecionar as opções pelo terminal.
- Opções inválidas devem apresentar uma mensagem de erro.
- O usuário deve conseguir encerrar a aplicação.

**Situação:** A interface de terminal está em desenvolvimento. A estrutura inicial do menu e a leitura de alguns dados foram criadas, mas a integração completa das operações ainda está pendente.

### História 6 — Busca e gerenciamento de livros

**Responsável:** Giuliana Batistella  
**Épico:** Livros

Como usuário, eu quero consultar e gerenciar os livros cadastrados para manter meu acervo organizado.

**Critérios de aceitação:**

- O sistema deve permitir localizar livros cadastrados.
- O sistema deve permitir consultar as informações dos livros.
- Os dados dos livros devem ser validados pelas regras de negócio.
- As operações devem utilizar a camada de persistência.

## Como instalar e executar

### Pré-requisitos

- Python 3.13 ou superior
- Poetry
- Git

### Clonar o repositório

```bash
git clone https://github.com/C14-Inatel-2026-2/Imersos.git
cd Imersos
```

### Instalar dependências

```bash
poetry install --no-root
```

### Executar os testes

```bash
poetry run python -m pytest tests/ -v
```

### Executar os testes do modelo Livro

```bash
poetry run python -m pytest tests/test_livro.py -v
```

### Executar testes com cobertura

```bash
poetry run python -m pytest tests/ \
    --cov=models \
    --cov=repository \
    --cov=services \
    --cov=terminal \
    --cov-report=term-missing
```

### Executar a aplicação

A interface de terminal está localizada em `terminal/app.py`.

Atualmente, o arquivo contém a estrutura inicial do menu, a leitura de dados dos livros e a conversão do status de leitura.

A execução completa da aplicação depende da implementação e integração das operações do menu com os serviços e repositórios.

## Integração contínua — CI/CD

O projeto utiliza Jenkins para automatizar a execução do build e dos testes.

O arquivo `Jenkinsfile` define as etapas:

1. Build
2. Testes - Emprestimo
3. Testes - Services
4. Testes - Livro
5. Testes - Terminal
6. Testes - Repository
7. Relatorio de Cobertura

Os testes utilizam Pytest, e seus resultados são gerados em relatórios JUnit.

A cobertura é medida com Pytest-Cov, com relatórios em formato HTML e XML.

O ambiente Jenkins é preparado utilizando o arquivo `Dockerfile.jenkins`.

## Organização ágil

O projeto utiliza a metodologia **Scrum**, com planejamento e acompanhamento das atividades no Jira.

As funcionalidades foram organizadas em histórias de usuário, distribuídas entre os integrantes do grupo.

### Épicos

- Livros
- Empréstimos
- Persistência
- Interface

### Sprint 1 — Entrega 5

**Período:** 29/10/2026 a 07/11/2026.

**Objetivo:** organizar o backlog, documentar os requisitos e planejar a implementação das funcionalidades do sistema.

### Fluxo de atividades

O desenvolvimento é acompanhado utilizando os estados:

- A fazer
- Em andamento
- Em análise
- Concluído

As atividades são movimentadas no quadro conforme o progresso real do desenvolvimento.

## Links

**Repositório GitHub:**  
https://github.com/C14-Inatel-2026-2/Imersos

**Jira — Backlog:**  
https://imersos.atlassian.net/jira/software/projects/SCRUM/boards/1/backlog

## Considerações finais

O projeto Imersos aplica conceitos de engenharia de software no desenvolvimento de uma biblioteca pessoal.

A organização modular, os testes automatizados, a integração contínua e o planejamento com Scrum permitem que as funcionalidades sejam desenvolvidas e validadas progressivamente.

O sistema permanece em desenvolvimento, com as responsabilidades distribuídas entre os integrantes do grupo e as histórias acompanhadas pelo Jira.
