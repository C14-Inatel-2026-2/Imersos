from pathlib import Path

from repository.livro_repository import LivroRepository
from services.livro_service import LivroService

def mostrar_menu():
    print("\n=== Biblioteca Imersos ===")
    print("1 - Cadastrar livro")
    print("2 - Buscar livro")
    print("3 - Editar livro")
    print("4 - Remover livro")
    print("5 - Realizar empréstimo")
    print("6 - Realizar devolução")
    print("7 - Listar empréstimos atrasados")
    print("8 - Listar todos os livros")
    print("0 - Sair")


def ler_opcao():
    return input("Escolha uma opção: ")

def converter_status(opcao_status):
    status = {
        "1": "nao_iniciado",
        "2": "lendo",
        "3": "concluido",
    }.get(opcao_status)

    if status is None:
        raise ValueError("Status de leitura inválido")

    return status

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
    status = converter_status(opcao_status)

    return {
        "titulo": titulo,
        "autor": autor,
        "isbn": isbn,
        "genero": genero,
        "ano": ano,
        "status_leitura": status,
    }

def exibir_livro(livro):
    print(f"\nTítulo: {livro.titulo}")
    print(f"Autor: {livro.autor}")
    print(f"ISBN: {livro.isbn}")
    print(f"Gênero: {livro.genero}")
    print(f"Ano: {livro.ano}")
    print(f"Status: {livro.status_leitura}")


def cadastrar_livro(service):
    dados = ler_dados_livro()
    service.cadastrar_livro(**dados)
    print("Livro cadastrado com sucesso!")


def buscar_livro(service):
    campo = input("Buscar por (titulo/autor/genero): ").strip().lower()
    termo = input("Digite o termo de busca: ")

    livros = service.buscar_livros(termo, campo)

    if not livros:
        print("Nenhum livro encontrado.")
        return

    for livro in livros:
        exibir_livro(livro)


def listar_livros(service):
    livros = service.listar_livros()

    if not livros:
        print("Nenhum livro cadastrado.")
        return

    for livro in livros:
        exibir_livro(livro)


def editar_livro(service):
    isbn = input("ISBN do livro que deseja editar: ").strip()
    print("Informe os novos dados:")
    dados = ler_dados_livro()

    service.editar_livro(isbn, dados)
    print("Livro atualizado com sucesso!")


def remover_livro(service):
    isbn = input("ISBN do livro que deseja remover: ").strip()

    service.remover_livro(isbn)
    print("Livro removido com sucesso!")

def executar():

    caminho = Path(__file__).resolve().parents[1] / "dados" / "livros.json"

    repository = LivroRepository(caminho)
    service = LivroService(repository)

    while True:
        mostrar_menu()

        opcao = ler_opcao()

        try:
            if opcao == "1":
                cadastrar_livro(service)
            elif opcao == "2":
                buscar_livro(service)
            elif opcao == "3":
                editar_livro(service)
            elif opcao == "4":
                remover_livro(service)
            elif opcao in ("5", "6", "7"):
                print("Funcionalidade de empréstimos ainda não integrada.")
            elif opcao == "8":
                listar_livros(service)
            elif opcao == "0":
                print("Encerrando sistema...")
                break
            else:
                print("Opção inválida! Tente novamente.")

        except ValueError as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    executar()
