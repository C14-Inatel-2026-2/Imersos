from repository.livro_repository import LivroRepository


def test_salvar_e_carregar_livros(tmp_path):
    arquivo = tmp_path / "livros.json"

    repo = LivroRepository(arquivo)

    livros = [
        {
            "titulo": "1984",
            "autor": "George Orwell",
            "isbn": "9780451524935"
        }
    ]

    repo.salvar(livros)

    resultado = repo.carregar()

    assert resultado == livros


def test_carregar_arquivo_inexistente(tmp_path):
    arquivo = tmp_path / "livros.json"

    repo = LivroRepository(arquivo)

    resultado = repo.carregar()

    assert resultado == []


def test_carregar_json_corrompido(tmp_path):
    arquivo = tmp_path / "livros.json"

    arquivo.write_text(
        "{ isso nao e um json valido",
        encoding="utf-8"
    )

    repo = LivroRepository(arquivo)

    resultado = repo.carregar()

    assert resultado == []