
# 📚 Imersos — Biblioteca Pessoal

## Descrição

O **Imersos** é um sistema de gerenciamento de biblioteca pessoal que roda no terminal. Ele permite cadastrar livros com título, autor, ISBN, gênero, ano e status de leitura, buscar livros no acervo, acompanhar o progresso de leitura e controlar empréstimos, registrando para quem o livro foi emprestado e até quando deve ser devolvido.

O sistema não tem interface gráfica nem banco de dados: a interação é feita por um menu no terminal (`input()`/`print()`) e os dados ficam salvos em um arquivo JSON local.

### Estrutura do projeto

| Pasta | Responsabilidade |
|---|---|
| `models/` | Classes de domínio (`Livro`, `Emprestimo`) e suas validações |
| `repository/` | Persistência dos dados em arquivo JSON |
| `services/` | Regras de negócio (cadastro, busca, empréstimo) |
| `terminal/` | Menu e interação com o usuário |
| `tests/` | Testes automatizados com pytest |

### Integrantes

| Integrante | Responsabilidade |
|---|---|
| Giuliana Batistella | `services/` |
| Júlia Seixas Souza | `repository/` |
| Camile Brunieri Laraia | CI/CD (Jenkins) e `models/emprestimo.py` |
| Kauan de Abreu Carvalho | `models/livro.py` |
| Luis Otávio Garcia Godoy da Costa | `terminal/` |

## Requisitos funcionais

<!-- Kauan: consolidar aqui (RF01, RF02...). Cada um manda o RF do próprio módulo. -->

## Requisitos não funcionais

RNF01 — Linguagem: A aplicação deve ser desenvolvida utilizando Python.

RNF02 — Modularidade: O código deve possuir uma estrutura modular, separando modelos, repositórios, serviços e interface de terminal.

RNF03 — Testabilidade: As principais funcionalidades devem possuir testes automatizados utilizando Pytest.

RNF04 — Gerenciamento de dependências: O projeto deve utilizar Poetry para gerenciamento de dependências e ambiente virtual.

RNF05 — Integração contínua: O projeto deve utilizar Jenkins para automatizar a execução da build e dos testes.

RNF06 — Versionamento: O código-fonte deve ser versionado utilizando Git e hospedado no GitHub.

RNF07 — Manutenibilidade: O código deve seguir padrões de organização e nomenclatura que facilitem sua compreensão e manutenção.

RNF08 — Compatibilidade: A aplicação deve ser compatível com Python 3.13, versão utilizada no ambiente do projeto.

## Histórias de usuário

<!-- Juh: listar aqui as histórias cadastradas no Jira (título, responsável e link do card). -->

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

O projeto é organizado com **Scrum** no **Jira**, com o backlog dividido em épicos por módulo: *Livros*, *Empréstimos*, *Persistência* e *Interface*. Cada integrante cadastrou ao menos uma história de usuário com critérios de aceitação no formato *Given / When / Then*.

- **Jira:** <!-- colocar o link do board aqui -->
- **Sprint atual:** Sprint 1 – Entrega 5
- **Objetivo da sprint:** organizar o backlog com as histórias do sistema e concluir cadastro, persistência, busca, empréstimo e menu via terminal

<!-- Giu: colocar aqui os prints do backlog e do quadro da sprint -->
