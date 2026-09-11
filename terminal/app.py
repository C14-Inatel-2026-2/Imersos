def mostrar_menu():
    print("\n=== Biblioteca Imersos ===")
    print("1 - Cadastrar livro")
    print("2 - Buscar livro")
    print("3 - Editar livro")
    print("4 - Remover livro")
    print("5 - Realizar empréstimo")
    print("6 - Realizar devolução")
    print("7 - Listar empréstimos atrasados")
    print("0 - Sair")


def ler_opcao():
    return input("Escolha uma opção: ")

def ler_dados_livro():
    titulo = input("Título: ")
    autor = input("Autor: ")
    isbn = input("ISBN: ")
    genero = input("Gênero: ")
    ano = int(input("Ano: "))

    print("\nStatus de leitura:")
    print("1 - Não iniciado")
    print("2 - Lendo")
    print("3 - Concluído")

    opcao_status = input("Status: ")

    status = {
        "1": "nao_iniciado",
        "2": "lendo",
        "3": "concluido",
    }.get(opcao_status)

    if status is None:
        raise ValueError("Status de leitura inválido")

    return {
        "titulo": titulo,
        "autor": autor,
        "isbn": isbn,
        "genero": genero,
        "ano": ano,
        "status_leitura": status,
    }


def executar():
    while True:
        mostrar_menu()

        opcao = ler_opcao()

        if opcao == "1":
            cadastrar_livro()
        elif opcao == "2":
            buscar_livro()
        elif opcao == "3":
            editar_livro()
        elif opcao == "4":
            remover_livro()
        elif opcao == "5":
            realizar_emprestimo()
        elif opcao == "6":
            realizar_devolucao()
        elif opcao == "7":
            listar_atrasados()
        elif opcao == "0":
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida.")
