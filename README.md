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

<!-- Mile: escrever aqui (RNF01, RNF02...). -->

## Histórias de usuário

<!-- Juh: listar aqui as histórias cadastradas no Jira (título, responsável e link do card). -->

## Como instalar e executar

<!-- Labubu: escrever aqui (poetry install, como rodar o programa e os testes). -->

## Organização ágil

O projeto é organizado com **Scrum** no **Jira**, com o backlog dividido em épicos por módulo: *Livros*, *Empréstimos*, *Persistência* e *Interface*. Cada integrante cadastrou ao menos uma história de usuário com critérios de aceitação no formato *Given / When / Then*.

- **Jira:** <!-- colocar o link do board aqui -->
- **Sprint atual:** Sprint 1 – Entrega 5
- **Objetivo da sprint:** organizar o backlog com as histórias do sistema e concluir cadastro, persistência, busca, empréstimo e menu via terminal

<!-- Giu: colocar aqui os prints do backlog e do quadro da sprint -->