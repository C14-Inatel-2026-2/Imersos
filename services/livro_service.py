from models.livro import Livro


class LivroService:
    CAMPOS_BUSCA = ["titulo", "autor", "genero"]

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

    def _para_livro(self, dados):
        return Livro(
            dados["titulo"],
            dados["autor"],
            dados["isbn"],
            dados["genero"],
            dados["ano"],
            dados["status_leitura"],
        )

    def cadastrar_livro(self, titulo, autor, isbn, genero, ano, status_leitura):
        novo_livro = Livro(titulo, autor, isbn, genero, ano, status_leitura)

        livros = self.repository.carregar()

        if any(item["isbn"] == isbn for item in livros):
            raise ValueError(f"Ja existe um livro cadastrado com o ISBN {isbn}")

        livros.append(self._para_dict(novo_livro))
        self.repository.salvar(livros)

        return novo_livro

    def buscar_livros(self, termo, campo):
        if campo not in self.CAMPOS_BUSCA:
            raise ValueError(f"Campo de busca invalido: {campo}")

        if not termo or not termo.strip():
            raise ValueError("O termo de busca nao pode estar vazio")

        termo = termo.strip().lower()
        livros = self.repository.carregar()

        return [
            self._para_livro(item)
            for item in livros
            if termo in (item.get(campo) or "").lower()
        ]


    def alterar_status(self, isbn, novo_status):
        livros = self.repository.carregar()

        for item in livros:
            if item["isbn"] == isbn:
                livro = self._para_livro(item)
                livro.alterar_status(novo_status)
                item["status_leitura"] = livro.status_leitura
                self.repository.salvar(livros)
                return livro

        raise ValueError("Livro nao encontrado")


    
    def filtrar_por_status(self, status):
        if status not in Livro.STATUS_VALIDOS:
            raise ValueError("Status de leitura invalido")

        livros = self.repository.carregar()

        return [
            self._para_livro(item)
            for item in livros
            if item["status_leitura"] == status
        ]


