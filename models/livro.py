class Livro:
    STATUS_VALIDOS = ["nao_iniciado", "lendo", "concluido"]

    def __init__(self, titulo, autor, isbn, genero, ano, status_leitura):
        self._validar_dados(titulo, autor, isbn, ano, status_leitura)

        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.genero = genero
        self.ano = ano
        self.status_leitura = status_leitura

    def _validar_dados(self, titulo, autor, isbn, ano, status_leitura):
        if not titulo:
            raise ValueError("O titulo nao pode estar vazio")

        if not autor:
            raise ValueError("O autor nao pode estar vazio")

        if not isbn:
            raise ValueError("O ISBN nao pode estar vazio")

        if ano <= 0:
            raise ValueError("O ano deve ser valido")

        self._validar_status(status_leitura)

    def _validar_status(self, status):
        if status not in self.STATUS_VALIDOS:
            raise ValueError("Status de leitura invalido")

    def alterar_status(self, novo_status):
        self._validar_status(novo_status)
        self.status_leitura = novo_status
