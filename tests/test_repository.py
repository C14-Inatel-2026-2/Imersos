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

def test_salvar_cria_diretorio_pai(tmp_path):
    arquivo = tmp_path / "data" / "livros.json"

    repo = LivroRepository(arquivo)

    livros = [
        {
            "titulo": "O Hobbit",
            "autor": "J. R. R. Tolkien",
            "isbn": "9788595084742"
        }
    ]

    repo.salvar(livros)

    assert arquivo.exists()
    assert repo.carregar() == livros

def test_salvar_e_carregar_multiplos_livros(tmp_path):
    arquivo = tmp_path / "livros.json"

    repo = LivroRepository(arquivo)

    livros = [
        {
            "titulo": "1984",
            "autor": "George Orwell",
            "isbn": "9780451524935"
        },
        {
            "titulo": "O Hobbit",
            "autor": "J. R. R. Tolkien",
            "isbn": "9788595084742"
        },
    ]

    repo.salvar(livros)

    resultado = repo.carregar()

    assert resultado == livros
    assert len(resultado) == 2

def test_carregar_arquivo_vazio_retorna_lista_vazia(tmp_path):
    arquivo = tmp_path / "livros.json"

    arquivo.write_text("", encoding="utf-8")

    repo = LivroRepository(arquivo)

    resultado = repo.carregar()

    assert resultado == []

def test_salvar_com_mock(mocker):
    repo = LivroRepository("dados/livros.json")

    livros = [
        {
            "titulo": "1984",
            "autor": "George Orwell",
            "isbn": "9780451524935"
        },
    ]

    mkdir_mock = mocker.patch(
        "repository.livro_repository.Path.mkdir"
    )

    open_mock = mocker.patch(
        "builtins.open",
        mocker.mock_open()
    )

    dump_mock = mocker.patch(
        "repository.livro_repository.json.dump"
    )

    repo.salvar(livros)

    mkdir_mock.assert_called_once_with(
        parents=True,
        exist_ok=True
    )

    open_mock.assert_called_once_with(
        repo.caminho_arquivo,
        "w",
        encoding="utf-8"
    )

    dump_mock.assert_called_once()

    assert dump_mock.call_args.args[0] == livros
    assert dump_mock.call_args.kwargs["ensure_ascii"] is False
    assert dump_mock.call_args.kwargs["indent"] == 4

def test_carregar_com_mock(mocker):
    repo = LivroRepository("livros.json")

    livros_esperados = [
        {
            "titulo": "1984",
            "autor": "George Orwell",
            "isbn": "9780451524935"
        }
    ]

    exists_mock = mocker.patch(
        "repository.livro_repository.Path.exists",
        return_value=True
    )

    open_mock = mocker.patch(
        "builtins.open",
        mocker.mock_open()
    )

    load_mock = mocker.patch(
        "repository.livro_repository.json.load",
        return_value=livros_esperados
    )

    resultado = repo.carregar()

    exists_mock.assert_called_once()

    open_mock.assert_called_once_with(
        repo.caminho_arquivo,
        "r",
        encoding="utf-8"
    )

    load_mock.assert_called_once()

    assert resultado == livros_esperados