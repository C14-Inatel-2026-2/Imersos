
# 📚 Imersos — Biblioteca Pessoal

## Descrição

O **Imersos** é um sistema de gerenciamento de biblioteca pessoal desenvolvido em Python, com o objetivo de facilitar a organização de um acervo de livros.

O sistema foi projetado para permitir o cadastro, a busca, a listagem, a edição e a remoção de livros, além do acompanhamento do status de leitura e do controle de empréstimos e devoluções.

A aplicação utiliza uma interface via terminal, sem interface gráfica ou banco de dados. A interação ocorre por meio de `input()` e `print()`, enquanto a persistência dos dados é realizada em arquivos JSON locais.

O projeto foi desenvolvido como parte da disciplina C14, utilizando práticas de engenharia de software, testes automatizados, integração contínua e metodologia ágil Scrum.

## Estrutura do projeto

| Pasta | Responsabilidade |
|---|---|
| `models/` | Classes de domínio (`Livro` e `Emprestimo`) e validações |
| `repository/` | Persistência dos dados em arquivo JSON |
| `services/` | Regras de negócio e operações sobre os livros |
| `terminal/` | Menu e interação com o usuário |
| `tests/` | Testes automatizados com Pytest |

## Integrantes

| Integrante | Responsabilidade |
|---|---|
| Giuliana Batistella | `services/` |
| Júlia Seixas Souza | `repository/` |
| Camile Brunieri Laraia | CI/CD (Jenkins) e `models/emprestimo.py` |
| Kauan de Abreu Carvalho | `models/livro.py` |
| Luis Otávio Garcia Godoy da Costa | `terminal/` |

## Requisitos funcionais

Os requisitos funcionais descrevem as funcionalidades que o sistema deve oferecer aos usuários.

**RF01 — Cadastro de livros:** O sistema deve permitir cadastrar livros informando título, autor, ISBN, gênero, ano de publicação e status de leitura.

**RF02 — Validação dos dados:** O sistema deve impedir o cadastro de livros com título, autor ou ISBN vazios, ano menor ou igual a zero ou status de leitura inválido.

**RF03 — ISBN único:** O sistema deve impedir o cadastro de dois livros com o mesmo ISBN.

**RF04 — Listagem de livros:** O sistema deve permitir visualizar todos os livros cadastrados no acervo.

**RF05 — Busca de livros:** O sistema deve permitir buscar livros por título, autor ou gênero.

**RF06 — Edição de livros:** O sistema deve permitir alterar as informações de um livro já cadastrado.

**RF07 — Remoção de livros:** O sistema deve permitir remover livros do acervo.

**RF08 — Controle de status de leitura:** O sistema deve permitir definir o status de leitura de um livro como "não iniciado", "lendo" ou "concluído", recusando valores inválidos.

**RF09 — Registro de empréstimos:** O sistema deve permitir registrar empréstimos de livros, informando a pessoa responsável, a data do empréstimo e a data prevista para devolução.

**RF10 — Validação de empréstimos:** O sistema deve impedir empréstimos sem identificação do responsável, sem datas obrigatórias, com data de devolução anterior à data do empréstimo ou de livros já emprestados.

**RF11 — Devolução de livros:** O sistema deve permitir registrar a devolução de um livro emprestado, atualizando sua disponibilidade.

**RF12 — Empréstimos atrasados:** O sistema deve permitir identificar livros emprestados cuja data prevista de devolução já passou.

**RF13 — Persistência dos dados:** O sistema deve salvar os dados dos livros em arquivos JSON locais, permitindo recuperá-los posteriormente.

**RF14 — Tratamento de arquivos:** O sistema deve tratar arquivos de dados ausentes ou inválidos, permitindo iniciar um acervo vazio sem interromper a aplicação.

**RF15 — Interface de terminal:** O sistema deve apresentar um menu textual com as operações disponíveis e informar ao usuário quando uma opção inválida for selecionada.

## Requisitos não funcionais

Os requisitos não funcionais descrevem características técnicas e de qualidade que o sistema deve atender.

**RNF01 — Linguagem:** A aplicação deve ser desenvolvida utilizando Python.

**RNF02 — Modularidade:** O código deve possuir uma estrutura modular, separando modelos, repositórios, serviços e interface de terminal.

**RNF03 — Testabilidade:** As principais funcionalidades devem possuir testes automatizados utilizando Pytest.

**RNF04 — Gerenciamento de dependências:** O projeto deve utilizar Poetry para gerenciamento de dependências e ambiente virtual.

**RNF05 — Integração contínua:** O projeto deve utilizar Jenkins para automatizar a execução do build e dos testes.

**RNF06 — Versionamento:** O código-fonte deve ser versionado utilizando Git e hospedado no GitHub.

**RNF07 — Manutenibilidade:** O código deve seguir padrões de organização e nomenclatura que facilitem sua compreensão e manutenção.

**RNF08 — Compatibilidade:** A aplicação deve ser compatível com Python 3.13, versão utilizada no ambiente do projeto.

**RNF09 — Usabilidade:** A aplicação deve apresentar mensagens claras ao usuário e permitir a interação por meio de um menu no terminal.

**RNF10 — Persistência local:** Os dados devem ser armazenados em arquivos JSON locais, sem necessidade de um servidor de banco de dados.

**RNF11 — Confiabilidade:** A aplicação deve validar os dados recebidos e tratar situações inválidas para evitar inconsistências no acervo.

## Histórias de usuário

As histórias de usuário representam funcionalidades do sistema sob a perspectiva de quem utiliza a aplicação.

### História 1 — Cadastro de livros

**Responsável:** Kauan  
**Épico:** Livros

Como usuário, eu quero cadastrar um livro com título, autor, ISBN, gênero, ano e status de leitura para manter meu acervo organizado.

**Critérios de aceitação:**

- Dados válidos devem permitir o cadastro do livro.
- Título, autor e ISBN não podem estar vazios.
- O ano de publicação deve ser maior que zero.
- Livros com ISBN duplicado não devem ser cadastrados.

### História 2 — Persistência dos dados

**Responsável:** Juh  
**Épico:** Persistência

Como usuário, eu quero que meus livros sejam salvos em arquivo para não perder meus dados ao fechar o programa.

**Critérios de aceitação:**

- Os livros cadastrados devem continuar disponíveis ao reabrir a aplicação.
- Caso o arquivo não exista, o sistema deve iniciar com um acervo vazio.
- Arquivos inválidos devem ser tratados sem interromper a aplicação.
- O diretório de armazenamento deve ser criado quando necessário.

### História 3 — Controle de empréstimos

**Responsável:** Mile  
**Épico:** Empréstimos

Como usuário, eu quero registrar quando um livro foi emprestado, para quem e até quando deve ser devolvido, para controlar meus empréstimos.

**Critérios de aceitação:**

- Um livro disponível deve poder ser emprestado.
- Um livro já emprestado não deve ser emprestado novamente.
- A data prevista de devolução deve ser registrada.
- Empréstimos atrasados devem ser identificados.
- A devolução deve atualizar a disponibilidade do livro.

### História 4 — Interface via terminal

**Responsável:** Labubu  
**Épico:** Interface

Como usuário, eu quero interagir com o sistema por um menu simples no terminal para acessar as funcionalidades da biblioteca.

**Critérios de aceitação:**

- O menu deve apresentar as operações disponíveis.
- O usuário deve selecionar opções numéricas.
- Opções inválidas devem apresentar uma mensagem de erro.
- O usuário deve poder encerrar a aplicação.

### História 5 — Controle de status de leitura

**Responsável:** Kauan  
**Épico:** Livros

Como usuário, eu quero informar se um livro está "não iniciado", "lendo" ou "concluído" para acompanhar meu progresso de leitura.

**Critérios de aceitação:**

- O sistema deve apresentar as três opções de status disponíveis.
- A escolha de um status válido deve ser aceita e armazenada.
- Status inválidos devem ser recusados com uma mensagem de erro.

As histórias e demais atividades são organizadas no Jira, com seus respectivos responsáveis, prioridades e estados de desenvolvimento.

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

### Instalar as dependências

```bash
poetry install --no-root
```

### Executar a aplicação

A interface principal está localizada em `terminal/app.py`. A execução interativa completa depende da integração das operações do menu com as funcionalidades do sistema.

### Executar os testes

Para executar todos os testes automatizados:

```bash
poetry run python -m pytest tests/ -v
```

Para executar somente os testes do modelo Livro:

```bash
poetry run python -m pytest tests/test_livro.py -v
```

### Executar testes com cobertura

```bash
poetry run python -m pytest tests/ --cov=models --cov=repository --cov=services --cov=terminal --cov-report=term-missing
```

## Integração contínua — CI/CD

O projeto utiliza Jenkins como ferramenta de integração contínua.

O arquivo `Jenkinsfile` define os estágios responsáveis por verificar o código, executar os testes automatizados e gerar relatórios.

### Estágios do pipeline

1. **Build:** verifica o ambiente, instala as dependências e compila os arquivos Python.
2. **Testes - Emprestimo:** executa os testes do modelo de empréstimos.
3. **Testes - Services:** executa os testes dos serviços.
4. **Testes - Livro:** executa os testes do modelo Livro.
5. **Testes - Terminal:** executa os testes da interface de terminal.
6. **Testes - Repository:** executa os testes da camada de persistência.
7. **Relatorio de Cobertura:** executa os testes e gera relatórios de cobertura.

Os resultados dos testes são publicados no Jenkins utilizando relatórios JUnit, enquanto a cobertura é gerada com Pytest-Cov.

O ambiente Jenkins é preparado por meio do arquivo `Dockerfile.jenkins`.

## Organização ágil

O projeto utiliza a metodologia **Scrum**, com atividades organizadas no Jira.

O planejamento é dividido em épicos, histórias de usuário e sprints, permitindo acompanhar o andamento do desenvolvimento.

### Épicos

- **Livros:** cadastro, consulta e controle de leitura.
- **Empréstimos:** registro, devolução e controle de atrasos.
- **Persistência:** armazenamento e recuperação dos dados.
- **Interface:** interação com o usuário pelo terminal.

### Sprint 1 — Entrega 5

**Período:** 29/10/2026 a 07/11/2026.

**Objetivo:** organizar o backlog, documentar os requisitos do sistema e acompanhar o desenvolvimento das funcionalidades da biblioteca.

### Quadro Scrum

O quadro utiliza os seguintes estados:

- **A fazer:** atividades que ainda não foram iniciadas.
- **Em andamento:** atividades em desenvolvimento.
- **Em análise:** atividades aguardando revisão ou validação.
- **Concluído:** atividades finalizadas.

### Links do projeto

- **GitHub:** https://github.com/C14-Inatel-2026-2/Imersos
- **Jira:** https://imersos.atlassian.net/jira/software/projects/SCRUM/boards/1/backlog

## Considerações finais

O projeto Imersos busca aplicar conceitos de engenharia de software no desenvolvimento de um sistema de biblioteca pessoal.

A separação em módulos, os testes automatizados, a integração contínua e a organização com Scrum contribuem para um desenvolvimento mais organizado, colaborativo e de fácil manutenção.

As funcionalidades são implementadas progressivamente, seguindo as histórias de usuário e os critérios de aceitação definidos pelo grupo.
