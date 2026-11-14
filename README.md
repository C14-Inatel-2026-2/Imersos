
# 📚 Imersos — Biblioteca Pessoal

## Descrição

O **Imersos** é um sistema de gerenciamento de biblioteca pessoal que roda no terminal. Ele permite cadastrar livros com título, autor, ISBN, gênero, ano e status de leitura, buscar livros no acervo, acompanhar o progresso de leitura e controlar empréstimos, registrando para quem o livro foi emprestado e até quando deve ser devolvido.

O sistema não tem interface gráfica nem banco de dados: a interação é feita por um menu no terminal (`input()`/`print()`) e os dados ficam salvos em um arquivo JSON local.

### Estrutura do projeto

| Pasta | Responsabilidade |

| `models/` | Classes de domínio (`Livro`, `Emprestimo`) e suas validações |

| `repository/` | Persistência dos dados em arquivo JSON |

| `services/` | Regras de negócio (cadastro, busca, empréstimo) |

| `terminal/` | Menu e interação com o usuário |

| `tests/` | Testes automatizados com Pytest |

### Integrantes

| Integrante | Responsabilidade |

| Giuliana Batistella | `services/` |

| Júlia Seixas Souza | `repository/` |

| Camile Brunieri Laraia | CI/CD (Jenkins) e `models/emprestimo.py` |

| Kauan de Abreu Carvalho | `models/livro.py` |

| Luis Otávio Garcia Godoy da Costa | `terminal/` |

## Requisitos funcionais

### Módulo Livro — Kauan

**RF01 — Cadastro de livros:** O sistema deve permitir cadastrar livros com título, autor, ISBN, gênero, ano de publicação e status de leitura.

**RF02 — Validação dos dados:** O sistema deve impedir a criação de livros com título, autor ou ISBN vazios e ano de publicação menor ou igual a zero.

**RF03 — Controle de status de leitura:** O sistema deve permitir definir o status de leitura de um livro como "não iniciado", "lendo" ou "concluído".

**RF04 — Validação do status de leitura:** O sistema deve rejeitar qualquer status de leitura diferente das três opções permitidas.

### Módulo Repository — Juh

**RF05 — Persistência dos dados:** O sistema deve permitir salvar os dados dos livros em um arquivo JSON local.

**RF06 — Recuperação dos dados:** O sistema deve permitir carregar os livros previamente salvos no arquivo JSON.

**RF07 — Tratamento de arquivo inexistente:** Caso o arquivo de dados ainda não exista, o sistema deve iniciar com o acervo vazio sem interromper a execução.

**RF08 — Tratamento de arquivo inválido:** Caso o arquivo JSON esteja corrompido ou inválido, o sistema deve retornar um acervo vazio sem interromper a execução.

**RF09 — Criação do diretório de armazenamento:** Caso a pasta destinada ao arquivo de dados não exista, o sistema deve criá-la automaticamente ao salvar os livros.

## Requisitos não funcionais

**RNF01 — Linguagem:** A aplicação deve ser desenvolvida utilizando Python.

**RNF02 — Modularidade:** O código deve possuir uma estrutura modular, separando modelos, repositórios, serviços e interface de terminal.

**RNF03 — Testabilidade:** As principais funcionalidades devem possuir testes automatizados utilizando Pytest.

**RNF04 — Gerenciamento de dependências:** O projeto deve utilizar Poetry para gerenciamento de dependências e ambiente virtual.

**RNF05 — Integração contínua:** O projeto deve utilizar Jenkins para automatizar a execução da build e dos testes.

**RNF06 — Versionamento:** O código-fonte deve ser versionado utilizando Git e hospedado no GitHub.

**RNF07 — Manutenibilidade:** O código deve seguir padrões de organização e nomenclatura que facilitem sua compreensão e manutenção.

**RNF08 — Compatibilidade:** A aplicação deve ser compatível com Python 3.13, versão utilizada no ambiente do projeto.

## Histórias de usuário

As histórias estão cadastradas no Jira, com critérios de aceitação no formato *Given / When / Then*.

| # | História | Responsável | Épico | Status | Card |

| 1 | Cadastrar livro no acervo | Kauan | Livros | A fazer | [SCRUM-12](https://imersos.atlassian.net/browse/SCRUM-12) |

| 2 | Persistência dos dados | Júlia | Persistência | A fazer | [SCRUM-15](https://imersos.atlassian.net/browse/SCRUM-15) |

| 3 | Buscar livros por título, autor ou gênero | Giuliana | Livros | A fazer | [SCRUM-9](https://imersos.atlassian.net/browse/SCRUM-9) |

| 4 | Interface via Terminal | Luis Otavio | Interface | A fazer | [SCRUM-14](https://imersos.atlassian.net/browse/SCRUM-14) |

| 5 | Controlar status de leitura dos livros | Kauan | Livros | A fazer | [SCRUM-13](https://imersos.atlassian.net/browse/SCRUM-13) |

| 6 | Registrar empréstimo de livro | Camile | Empréstimos | A fazer | [SCRUM-10](https://imersos.atlassian.net/browse/SCRUM-10) |

O backlog também possui histórias planejadas para as próximas sprints, incluindo listar, editar e remover livros, filtrar por status, registrar devoluções e listar empréstimos atrasados.

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

7. **Relatório de Cobertura:** executa os testes e gera relatórios de cobertura.

Os resultados dos testes são publicados no Jenkins utilizando relatórios JUnit, enquanto a cobertura é gerada com Pytest-Cov.

O ambiente Jenkins é preparado por meio do arquivo `Dockerfile.jenkins`.

8. **Deploy - Docker Hub:** após a aprovação dos testes, o Jenkins constrói uma imagem Docker da aplicação e publica no repositório `milelaraia/imersos`, utilizando uma tag com o número da execução e a tag `latest`.

9. **Deploy - Render:** após a publicação da imagem, o Jenkins utiliza um Deploy Hook para solicitar automaticamente uma nova implantação no Render.

### Fluxo de CI/CD

O processo de integração e implantação contínua segue o fluxo:

**GitHub (`main`) → Jenkins (build e testes) → Docker Hub (publicação da imagem) → Deploy Hook → Render (aplicação web)**

Os estágios de deploy são executados somente para a branch `main`. As credenciais do Docker Hub e o Deploy Hook são armazenados de forma segura nas credenciais do Jenkins.

### Evidências do deploy

A execução do pipeline pode ser verificada por meio dos seguintes recursos:

- **Aplicação web:** https://imersos-c14.onrender.com/
- **Health Check:** https://imersos-c14.onrender.com/health
- **Imagem Docker:** https://hub.docker.com/r/milelaraia/imersos

A aplicação foi acessada no Render, sendo confirmado o carregamento da interface web e o funcionamento das operações de cadastro, listagem, busca, edição, alteração do status de leitura e remoção de livros.

**Execução validada no Jenkins:**

- **Build:** #29
- **Resultado:** SUCCESS
- **Testes aprovados:** 124
- **Cobertura de código:** 87%
- **Publicação no Docker Hub:** confirmada
- **Imagem publicada:** `milelaraia/imersos:29`
- **Tag `latest`:** atualizada com sucesso
- **Deploy no Render:** solicitação aceita pelo Deploy Hook
- **Validação da aplicação:** interface web acessível e funcionalidades testadas com sucesso pela URL pública

A execução #29 utilizou a branch `main`, incluindo as correções da interface web incorporadas pela PR #49. O pipeline concluiu todas as etapas sem falhas.

A publicação da imagem e o acionamento do Deploy Hook foram confirmados pelos logs do Jenkins. O funcionamento da interface web hospedada no Render foi verificado manualmente pelo navegador.

### Aplicação web — Deploy no Render

A Biblioteca Imersos está disponível publicamente por meio do Render, com deploy automatizado utilizando Jenkins e Docker Hub.

**Acesse a aplicação:** https://imersos-c14.onrender.com/

**Health Check:** https://imersos-c14.onrender.com/health

A interface web foi desenvolvida com Flask e permite cadastrar, listar, buscar, editar e remover livros, além de gerenciar seus status de leitura.

## Organização ágil

O projeto é organizado com **Scrum** no **Jira**, com o backlog dividido em épicos por módulo: *Livros*, *Empréstimos*, *Persistência* e *Interface*. Cada integrante cadastrou ao menos uma história de usuário com critérios de aceitação no formato *Given / When / Then*.

- **Jira:** https://imersos.atlassian.net/jira/software/projects/SCRUM/boards/1/backlog

- **Sprint atual:** Sprint 1 – Entrega 5

- **Objetivo da sprint:** organizar o backlog com as histórias do sistema e concluir cadastro, persistência, busca, empréstimo e menu via terminal.

## Refactorings

### Modelo Livro — Kauan

#### Refactoring 1 — Extração da validação de status

**Code smell:** Duplicated Code

**Técnica:** Extract Method

**Problema:** A validação do status de leitura estava repetida no construtor `__init__()` e no método `alterar_status()`.

**Solução:** Foi criado o método `_validar_status()`, que centraliza a verificação dos status permitidos e é utilizado pelos dois métodos.

**Justificativa:** Eliminar a duplicação de código, facilitar a manutenção e evitar que a mesma regra precise ser alterada em diferentes lugares.

#### Refactoring 2 — Extração das validações do construtor

**Code smell:** Multiple Responsibilities

**Técnica:** Extract Method

**Problema:** O construtor `__init__()` era responsável por validar os dados recebidos e inicializar os atributos do livro.

**Solução:** Foi criado o método `_validar_dados()`, que reúne as validações de título, autor, ISBN, ano e status de leitura.

**Justificativa:** O Extract Method foi utilizado para separar a responsabilidade de validação da inicialização dos atributos. Isso deixa o construtor mais simples e organizado, facilitando a leitura e manutenção do código sem alterar seu comportamento.

**Pull Request:** [#28 — Refactoring do modelo Livro](https://github.com/C14-Inatel-2026-2/Imersos/pull/28)

### Livro Service — Júlia

#### Refactoring 1 — Extração da busca de livro por ISBN

**Code smell:** Duplicated Code

**Técnica:** Extract Method

**Problema:** A lógica responsável por localizar um livro pelo ISBN estava repetida nos métodos `alterar_status()`, `editar_livro()` e `remover_livro()`.

**Solução:** Foi criado o método auxiliar `_buscar_indice_por_isbn()`, responsável por localizar o índice de um livro a partir do ISBN informado.

**Justificativa:** Centralizar a busca por ISBN elimina código duplicado, facilita a manutenção e evita que alterações na lógica de localização precisem ser realizadas em vários métodos.

#### Refactoring 2 — Extração da validação de ISBN duplicado

**Code smell:** Duplicated Code

**Técnica:** Extract Method

**Problema:** A verificação de ISBN duplicado era realizada separadamente nos métodos `cadastrar_livro()` e `editar_livro()`.

**Solução:** Foi criado o método auxiliar `_validar_isbn_unico()`, que centraliza a regra de validação da unicidade do ISBN.

**Justificativa:** A centralização da regra reduz duplicação de código, melhora a legibilidade e garante que a mesma regra de negócio seja utilizada tanto no cadastro quanto na edição de livros.

**Pull Request:** [#31 — Refactoring do LivroService](https://github.com/C14-Inatel-2026-2/Imersos/pull/31)

### Livro Service — Giuliana

#### Refactoring 1 — Extração da verificação de livro existente

**Code smell:** Duplicated Code

**Técnica:** Extract Method

**Problema:** Os métodos `alterar_status()`, `editar_livro()` e `remover_livro()` repetiam o bloco que verifica se o livro foi encontrado e lança o erro caso não exista. Além disso, a mensagem estava inconsistente: `"Livro nao encontrado"` em um método e `"Livro não encontrado"` nos outros.

**Solução:** Foi criado o método auxiliar `_obter_indice_existente()`, que busca o índice pelo ISBN e lança `ValueError("Livro não encontrado")` quando o livro não existe. Os três métodos passaram a utilizá-lo. Também foi adicionado um teste garantindo a mensagem padronizada.

**Justificativa:** A regra de que o livro precisa existir fica centralizada em um único lugar, os métodos ficam mais curtos e a mensagem de erro passa a ser a mesma em todas as operações.

#### Refactoring 2 — Extração da filtragem de livros

**Code smell:** Duplicated Code

**Técnica:** Extract Method

**Problema:** Os métodos `buscar_livros()`, `filtrar_por_status()` e `listar_livros()` repetiam a mesma estrutura: carregar os dados do repositório, percorrer a lista e converter cada item em `Livro`, mudando apenas a condição de filtro.

**Solução:** Foi criado o método auxiliar `_filtrar_livros()`, que recebe uma condição opcional e retorna os livros que a satisfazem. Cada método passou a informar apenas a sua condição.

**Justificativa:** Elimina a duplicação, deixa explícito o que diferencia cada consulta e concentra em um só ponto a conversão dos dados do repositório em objetos `Livro`.

**Pull Request:** [#34 — Refactoring do LivroService (Giuliana)](https://github.com/C14-Inatel-2026-2/Imersos/pull/34)

### Empréstimo Service — Camile

#### Refactoring 1 — Reutilização da consulta de empréstimos ativos

**Code smell:** Duplicated Code

**Técnica:** Replace Inline Code with Function Call

**Problema:** O método `verificar_disponibilidade()` realizava uma busca própria por empréstimos ativos, apesar de `consultar_emprestimo()` já implementar a mesma lógica de localização por ISBN.

**Solução:** A busca duplicada foi substituída por uma chamada ao método `consultar_emprestimo()`.

**Justificativa:** Centralizar a consulta evita duplicação de código, facilita a manutenção e garante que a verificação de disponibilidade utilize a mesma lógica da consulta de empréstimos, sem alterar o comportamento existente.

#### Refactoring 2 — Extração da montagem do registro de empréstimo

**Code smell:** Multiple Responsibilities

**Técnica:** Extract Method

**Problema:** O método `realizar_emprestimo()` era responsável tanto por validar e registrar um empréstimo quanto por montar o dicionário utilizado na persistência JSON.

**Solução:** Foi criado o método `_montar_registro_emprestimo()`, responsável pela conversão dos dados do empréstimo para o formato persistido.

**Justificativa:** A extração separa responsabilidades, melhora a legibilidade e facilita futuras alterações no formato de persistência, preservando o comportamento original.

**Testes:** A suíte de testes foi executada antes e depois dos refactorings, incluindo novos testes de regressão para disponibilidade e persistência.

**Pull Request:** **Pull Request:** [#42 — Refactoring do EmprestimoService (Camile)](https://github.com/C14-Inatel-2026-2/Imersos/pull/42)

## Uso de IA

Durante o desenvolvimento do Imersos, ferramentas de inteligência artificial foram utilizadas como apoio em diferentes etapas do projeto. As sugestões foram analisadas pelos integrantes antes de serem aplicadas, respeitando os requisitos definidos para o trabalho.

**Ferramentas utilizadas:** ChatGPT (OpenAI), Claude (Anthropic).

**Finalidades:** 
- **Geração e revisão de código.**
- **Testes:** sugestões de casos de teste com pytest e pytest-mock.
- **Refatoração:** identificação de code smells e sugestão de extrações de métodos, documentadas na seção *Refactorings*.
- **Debugging e ambiente:** entendimento de erros na execução da suíte de testes e na configuração do Docker e do pipeline.
- **Revisão e documentação:** revisão de Pull Requests, conferência do que já estava implementado no repositório e escrita do README.

**Exemplos reais de prompts:**
1. **Prompt:** "Confere no repositório se o método remover livro por ISBN já foi feito"
   **Resultado:** A IA identificou o método `remover_livro` no `LivroService`, a opção 4 do menu no terminal e os testes correspondentes. A informação foi conferida pelo grupo no código.
2. **Prompt:** "Analisa a pr da Giuliana e confere se está tudo de cordo para seguir para o merge"<br>
   **Resultado:** A análise auxiliou na identificação de uma inconsistência na documentação do README e na conferência dos refactorings realizados, contribuindo para a revisão do código antes do merge.
3. **Prompt:** "Como posso testar nossa aplicação?"<br>
   **Resultado:**  A IA orientou a execução dos testes automatizados com Pytest e o teste manual da aplicação pelo terminal. Durante o teste foi identificado um problema de importação, e a forma de execução foi ajustada para poetry run python -m terminal.app. Os comandos foram executados e conferidos pelo grupo.

**Dinâmica de uso:** A IA foi utilizada individualmente para esclarecer dúvidas, revisar implementações e sugerir melhorias. As respostas foram avaliadas e adaptadas conforme as necessidades do projeto.

**Atividades realizadas manualmente:** Execução dos testes, organização dos commits, abertura das Pull Requests, validação das funcionalidades e testes práticos da aplicação no Docker.
