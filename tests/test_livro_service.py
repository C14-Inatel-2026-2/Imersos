import pytest

from services.livro_service import LivroService


@pytest.fixture
def livro_dict():
    return {
        "titulo": "1984",
        "autor": "George Orwell",
        "isbn": "9780451524935",
        "genero": "Distopia",
        "ano": 1949,
        "status_leitura": "lendo",
    }


def test_cadastrar_livro(mocker):
    repo = mocker.Mock()
    repo.carregar.return_value = []

    service = LivroService(repo)
    livro = service.cadastrar_livro(
        "1984", "George Orwell", "9780451524935", "Distopia", 1949, "lendo"
    )

    assert livro.titulo == "1984"
    repo.salvar.assert_called_once()
    livros_salvos = repo.salvar.call_args[0][0]
    assert len(livros_salvos) == 1
    assert livros_salvos[0]["isbn"] == "9780451524935"


def test_cadastrar_livro_isbn_duplicado(mocker, livro_dict):
    repo = mocker.Mock()
    repo.carregar.return_value = [livro_dict]

    service = LivroService(repo)

    with pytest.raises(ValueError):
        service.cadastrar_livro(
            "Outro Titulo", "Outro Autor", "9780451524935", "Genero", 2000, "lendo"
        )


def test_cadastrar_livro_titulo_invalido(mocker):
    repo = mocker.Mock()
    repo.carregar.return_value = []

    service = LivroService(repo)

    with pytest.raises(ValueError):
        service.cadastrar_livro("", "Autor", "1234567890", "Genero", 2000, "lendo")