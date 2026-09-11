from models.livro import Livro


class LivroService:
    def __init__(self, repository):
        self.repository = repository

    def _para_dict(self, livro):
        return {
            "titulo": livro.titulo,
            "autor": livro.autor,
            "isbn": livro.isbn,
            "genero": livro.genero,
            "ano": livro.ano,
            "status_leitura": livro.status_leitura,
        }

    def cadastrar_livro(self, titulo, autor, isbn, genero, ano, status_leitura):
        livros = self.repository.carregar()

        if any(item["isbn"] == isbn for item in livros):
            raise ValueError(f"Ja existe um livro cadastrado com o ISBN {isbn}")

        # A validacao dos campos acontece aqui, no __init__ de Livro
        novo_livro = Livro(titulo, autor, isbn, genero, ano, status_leitura)

        livros.append(self._para_dict(novo_livro))
        self.repository.salvar(livros)

        return novo_livro