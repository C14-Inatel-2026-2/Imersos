
from datetime import date

from models.emprestimo import Emprestimo


class EmprestimoService:
    """Gerencia empréstimos ativos, devoluções e atrasos por ISBN."""

    def __init__(self, livro_repository, emprestimo_repository):
        self.livro_repository = livro_repository
        self.emprestimo_repository = emprestimo_repository

    
    def _montar_registro_emprestimo(self, isbn, emprestimo):
        return {
            "isbn": isbn,
            "emprestado_para": emprestimo.emprestado_para,
            "data_emprestimo": emprestimo.data_emprestimo.isoformat(),
            "data_devolucao_prevista": emprestimo.data_devolucao_prevista.isoformat(),
        }


    def realizar_emprestimo(self, isbn, pessoa, data_prevista, data_emprestimo=None):
        isbn = isbn.strip()

        self.verificar_disponibilidade(isbn)

        ativos = self.emprestimo_repository.carregar()

        emprestimo = Emprestimo(
            emprestado=True,
            emprestado_para=pessoa,
            data_emprestimo=data_emprestimo or date.today(),
            data_devolucao_prevista=data_prevista,
        )

        registro = self._montar_registro_emprestimo(
            isbn, emprestimo
        )

        ativos.append(registro)
        self.emprestimo_repository.salvar(ativos)

        return registro


    def listar_atrasados(self, hoje=None):
        hoje = hoje or date.today()
        return [
            registro
            for registro in self.emprestimo_repository.carregar()
            if date.fromisoformat(registro["data_devolucao_prevista"]) < hoje
        ]

    
    def verificar_disponibilidade(self, isbn):
        isbn = isbn.strip()

        livros = self.livro_repository.carregar()

        if not any(livro["isbn"] == isbn for livro in livros):
            raise ValueError("Livro não encontrado")

        if self.consultar_emprestimo(isbn) is not None:
            raise ValueError("Este livro já está emprestado")

        return True


    def consultar_emprestimo(self, isbn):
        isbn = isbn.strip()

        emprestimos = self.emprestimo_repository.carregar()

        for registro in emprestimos:
            if registro["isbn"] == isbn:
                return registro

        return None
