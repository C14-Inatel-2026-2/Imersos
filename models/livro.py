class Livro:
    STATUS_VALIDOS = ["nao_iniciado", "lendo", "concluido"]

    def __init__(self, titulo, autor, isbn, genero, ano, status_leitura):
        if not titulo:
            raise ValueError("O titulo nao pode estar vazio")

        if not autor:
            raise ValueError("O autor nao pode estar vazio")

        if not isbn:
            raise ValueError("O ISBN nao pode estar vazio")

        if ano <= 0:
            raise ValueError("O ano deve ser valido")

        if status_leitura not in self.STATUS_VALIDOS:
            raise ValueError("Status de leitura invalido")

        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.genero = genero
        self.ano = ano
        self.status_leitura = status_leitura