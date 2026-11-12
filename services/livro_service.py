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

    def _buscar_indice_por_isbn(self, livros, isbn):
        for i, item in enumerate(livros):
            if item["isbn"] == isbn:
                return i

        return None

    def _obter_indice_existente(self, livros, isbn):
        indice = self._buscar_indice_por_isbn(livros, isbn)

        if indice is None:
            raise ValueError("Livro não encontrado")

        return indice

    def cadastrar_livro(
        self,
        titulo,
        autor,
        isbn,
        genero,
        ano,
        status_leitura
    ):
        novo_livro = Livro(
            titulo,
            autor,
            isbn,
            genero,
            ano,
            status_leitura
        )

        livros = self.repository.carregar()

        self._validar_isbn_unico(
            livros,
            isbn,
            mensagem=f"Ja existe um livro cadastrado com o ISBN {isbn}"
        )

        livros.append(self._para_dict(novo_livro))
        self.repository.salvar(livros)

        return novo_livro

    def buscar_livros(self, termo, campo):
        if campo not in self.CAMPOS_BUSCA:
            raise ValueError(
                f"Campo de busca invalido: {campo}"
            )

        if not termo or not termo.strip():
            raise ValueError(
                "O termo de busca nao pode estar vazio"
            )

        termo = termo.strip().lower()
        livros = self.repository.carregar()

        return [
            self._para_livro(item)
            for item in livros
            if termo in (item.get(campo) or "").lower()
        ]

    def alterar_status(self, isbn, novo_status):
        livros = self.repository.carregar()

        indice = self._obter_indice_existente(livros, isbn)

        livro = self._para_livro(livros[indice])
        livro.alterar_status(novo_status)

        livros[indice]["status_leitura"] = livro.status_leitura
        self.repository.salvar(livros)

        return livro

    def filtrar_por_status(self, status):
        if status not in Livro.STATUS_VALIDOS:
            raise ValueError(
                "Status de leitura invalido"
            )

        livros = self.repository.carregar()

        return [
            self._para_livro(item)
            for item in livros
            if item["status_leitura"] == status
        ]

    def listar_livros(self):
        return [
            self._para_livro(item)
            for item in self.repository.carregar()
        ]

    def editar_livro(self, isbn, dados):
        livros = self.repository.carregar()

        indice = self._obter_indice_existente(livros, isbn)

        livro = Livro(**dados)

        if livro.isbn != isbn:
            self._validar_isbn_unico(
                livros,
                livro.isbn,
                indice_ignorado=indice
            )

        livros[indice] = self._para_dict(livro)
        self.repository.salvar(livros)

        return livro

    def remover_livro(self, isbn):
        livros = self.repository.carregar()

        indice = self._obter_indice_existente(livros, isbn)

        livros.pop(indice)
        self.repository.salvar(livros)


    def _validar_isbn_unico(
        self,
        livros,
        isbn,
        indice_ignorado=None,
        mensagem="ISBN já cadastrado"
    ):
        for i, item in enumerate(livros):
            if i != indice_ignorado and item["isbn"] == isbn:
                raise ValueError(mensagem)