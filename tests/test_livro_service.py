import pytest
from models.livro import Livro
from repository.livro_repository import LivroRepository
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

    repo.salvar.assert_not_called()


def test_cadastrar_livro_titulo_invalido(mocker):
    repo = mocker.Mock()
    repo.carregar.return_value = []

    service = LivroService(repo)

    with pytest.raises(ValueError):
        service.cadastrar_livro("", "Autor", "1234567890", "Genero", 2000, "lendo")

    repo.salvar.assert_not_called()


def test_carregar_repositorio_ao_cadastrar(mocker):
    repo = mocker.Mock()
    repo.carregar.return_value = []

    service = LivroService(repo)

    service.cadastrar_livro(
        "1984",
        "George Orwell",
        "9780451524935",
        "Distopia",
        1949,
        "lendo"
    )

    repo.carregar.assert_called_once()


def test_cadastrar_livro_mantem_livros_existentes(mocker):
    repo = mocker.Mock()

    repo.carregar.return_value = [
        {
            "titulo": "1984",
            "autor": "George Orwell",
            "isbn": "9780451524935",
            "genero": "Distopia",
            "ano": 1949,
            "status_leitura": "lendo",
        }
    ]

    service = LivroService(repo)

    service.cadastrar_livro(
        "O Hobbit",
        "J. R. R. Tolkien",
        "9788595084742",
        "Fantasia",
        1937,
        "nao_iniciado"
    )

    livros_salvos = repo.salvar.call_args[0][0]

    assert len(livros_salvos) == 2
    assert livros_salvos[0]["titulo"] == "1984"
    assert livros_salvos[1]["titulo"] == "O Hobbit"

def test_cadastrar_livro_titulo_vazio_sem_repositorio():
        service = LivroService(None)

        with pytest.raises(ValueError, match="titulo"):
            service.cadastrar_livro(
                "", "George Orwell", "9780451524935", "Distopia", 1949, "lendo"
            )


def test_para_dict_converte_livro():
    service = LivroService(None)
    livro = Livro(
        "1984", "George Orwell", "9780451524935", "Distopia", 1949, "lendo"
    )

    resultado = service._para_dict(livro)

    assert resultado == {
        "titulo": "1984",
        "autor": "George Orwell",
        "isbn": "9780451524935",
        "genero": "Distopia",
        "ano": 1949,
        "status_leitura": "lendo",
    }


def test_cadastrar_livro_persiste_no_arquivo(tmp_path):
    arquivo = tmp_path / "livros.json"
    service = LivroService(LivroRepository(arquivo))

    service.cadastrar_livro(
        "1984", "George Orwell", "9780451524935", "Distopia", 1949, "lendo"
    )

    livros = LivroRepository(arquivo).carregar()

    assert len(livros) == 1
    assert livros[0]["titulo"] == "1984"
    assert livros[0]["isbn"] == "9780451524935"

def test_cadastrar_livro_isbn_duplicado_integracao(tmp_path):
    arquivo = tmp_path / "livros.json"
    repo = LivroRepository(arquivo)
    service = LivroService(repo)

    service.cadastrar_livro(
        "1984", "George Orwell", "9780451524935", "Distopia", 1949, "lendo"
    )

    with pytest.raises(ValueError):
        service.cadastrar_livro(
            "Outro Titulo", "Outro Autor", "9780451524935", "Genero", 2000, "lendo"
        )

    assert len(repo.carregar()) == 1

def test_cadastrar_livro_titulo_invalido_integracao(tmp_path):
    arquivo = tmp_path / "livros.json"
    repo = LivroRepository(arquivo)
    service = LivroService(repo)

    with pytest.raises(ValueError):
        service.cadastrar_livro("", "Autor", "1234567890", "Genero", 2000, "lendo")

    assert repo.carregar() == []