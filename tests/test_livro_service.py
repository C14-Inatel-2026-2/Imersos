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

# ---------- Busca (SCRUM-9) ----------

@pytest.fixture
def acervo():
    return [
        {
            "titulo": "1984",
            "autor": "George Orwell",
            "isbn": "9780451524935",
            "genero": "Distopia",
            "ano": 1949,
            "status_leitura": "lendo",
        },
        {
            "titulo": "A Revolução dos Bichos",
            "autor": "George Orwell",
            "isbn": "9788535909555",
            "genero": "Fábula",
            "ano": 1945,
            "status_leitura": "concluido",
        },
        {
            "titulo": "O Hobbit",
            "autor": "J. R. R. Tolkien",
            "isbn": "9788595084742",
            "genero": "Fantasia",
            "ano": 1937,
            "status_leitura": "nao_iniciado",
        },
    ]


def test_buscar_por_parte_do_titulo(mocker, acervo):
    repo = mocker.Mock()
    repo.carregar.return_value = acervo
    service = LivroService(repo)

    resultado = service.buscar_livros("198", "titulo")

    assert len(resultado) == 1
    assert resultado[0].titulo == "1984"


def test_buscar_por_autor_retorna_todos_correspondentes(mocker, acervo):
    repo = mocker.Mock()
    repo.carregar.return_value = acervo
    service = LivroService(repo)

    resultado = service.buscar_livros("orwell", "autor")

    assert [livro.titulo for livro in resultado] == [
        "1984",
        "A Revolução dos Bichos",
    ]


def test_buscar_por_genero(mocker, acervo):
    repo = mocker.Mock()
    repo.carregar.return_value = acervo
    service = LivroService(repo)

    resultado = service.buscar_livros("Fantasia", "genero")

    assert len(resultado) == 1
    assert resultado[0].titulo == "O Hobbit"


def test_buscar_ignora_maiusculas_e_espacos(mocker, acervo):
    repo = mocker.Mock()
    repo.carregar.return_value = acervo
    service = LivroService(repo)

    resultado = service.buscar_livros("  HOBBIT ", "titulo")

    assert len(resultado) == 1


def test_buscar_retorna_objetos_livro(mocker, acervo):
    repo = mocker.Mock()
    repo.carregar.return_value = acervo
    service = LivroService(repo)

    resultado = service.buscar_livros("1984", "titulo")

    assert isinstance(resultado[0], Livro)


def test_buscar_sem_resultados_retorna_lista_vazia(mocker, acervo):
    repo = mocker.Mock()
    repo.carregar.return_value = acervo
    service = LivroService(repo)

    assert service.buscar_livros("Machado", "autor") == []


def test_buscar_em_acervo_vazio(mocker):
    repo = mocker.Mock()
    repo.carregar.return_value = []
    service = LivroService(repo)

    assert service.buscar_livros("1984", "titulo") == []


def test_buscar_campo_invalido(mocker):
    repo = mocker.Mock()
    service = LivroService(repo)

    with pytest.raises(ValueError, match="Campo"):
        service.buscar_livros("1984", "isbn")

    repo.carregar.assert_not_called()


def test_buscar_termo_vazio(mocker):
    repo = mocker.Mock()
    service = LivroService(repo)

    with pytest.raises(ValueError, match="termo"):
        service.buscar_livros("   ", "titulo")

    repo.carregar.assert_not_called()


def test_buscar_nao_altera_o_arquivo(mocker, acervo):
    repo = mocker.Mock()
    repo.carregar.return_value = acervo
    service = LivroService(repo)

    service.buscar_livros("orwell", "autor")

    repo.salvar.assert_not_called()


def test_buscar_livros_integracao(tmp_path):
    arquivo = tmp_path / "livros.json"
    service = LivroService(LivroRepository(arquivo))

    service.cadastrar_livro(
        "1984", "George Orwell", "9780451524935", "Distopia", 1949, "lendo"
    )
    service.cadastrar_livro(
        "O Hobbit", "J. R. R. Tolkien", "9788595084742", "Fantasia", 1937,
        "nao_iniciado"
    )

    resultado = service.buscar_livros("tolkien", "autor")

    assert len(resultado) == 1
    assert resultado[0].isbn == "9788595084742"


def test_buscar_por_genero_integracao(tmp_path):
    service = LivroService(LivroRepository(tmp_path / "livros.json"))

    service.cadastrar_livro(
        "1984", "George Orwell", "9780451524935", "Distopia", 1949, "lendo"
    )
    service.cadastrar_livro(
        "O Hobbit", "J. R. R. Tolkien", "9788595084742", "Fantasia", 1937,
        "nao_iniciado"
    )

    resultado = service.buscar_livros("fantasia", "genero")

    assert len(resultado) == 1
    assert resultado[0].titulo == "O Hobbit"


def test_buscar_sem_resultados_integracao(tmp_path):
    service = LivroService(LivroRepository(tmp_path / "livros.json"))

    service.cadastrar_livro(
        "1984", "George Orwell", "9780451524935", "Distopia", 1949, "lendo"
    )

    assert service.buscar_livros("Machado", "autor") == []


def test_para_livro_converte_dict():
    service = LivroService(None)
    dados = {
        "titulo": "1984",
        "autor": "George Orwell",
        "isbn": "9780451524935",
        "genero": "Distopia",
        "ano": 1949,
        "status_leitura": "lendo",
    }

    livro = service._para_livro(dados)

    assert isinstance(livro, Livro)
    assert livro.titulo == "1984"
    assert livro.isbn == "9780451524935"


def test_alterar_status_livro(tmp_path):
    repo = LivroRepository(tmp_path / "livros.json")
    service = LivroService(repo)

    service.cadastrar_livro("1984", "George Orwell", "123", "Distopia", 1949, "nao_iniciado")

    service.alterar_status("123", "lendo")

    assert repo.carregar()[0]["status_leitura"] == "lendo"


def test_alterar_status_invalido(tmp_path):
    repo = LivroRepository(tmp_path / "livros.json")
    service = LivroService(repo)

    service.cadastrar_livro("1984", "George Orwell", "123", "Distopia", 1949, "nao_iniciado")

    with pytest.raises(ValueError):
        service.alterar_status("123", "abandonado")

    assert repo.carregar()[0]["status_leitura"] == "nao_iniciado"


def test_alterar_status_livro_inexistente(tmp_path):
    repo = LivroRepository(tmp_path / "livros.json")
    service = LivroService(repo)

    with pytest.raises(ValueError):
        service.alterar_status("123", "lendo")


def test_filtrar_por_status(tmp_path):
    repo = LivroRepository(tmp_path / "livros.json")
    service = LivroService(repo)

    service.cadastrar_livro("1984", "George Orwell", "123", "Distopia", 1949, "lendo")
    service.cadastrar_livro("O Hobbit", "Tolkien", "456", "Fantasia", 1937, "concluido")

    resultado = service.filtrar_por_status("lendo")

    assert len(resultado) == 1
    assert resultado[0].titulo == "1984"


def test_filtrar_status_invalido(tmp_path):
    repo = LivroRepository(tmp_path / "livros.json")
    service = LivroService(repo)

    with pytest.raises(ValueError):
        service.filtrar_por_status("abandonado")

# ---------- Edição e remoção ----------

def test_editar_livro(tmp_path):
    repo = LivroRepository(tmp_path / "livros.json")
    service = LivroService(repo)

    service.cadastrar_livro(
        "1984",
        "George Orwell",
        "123",
        "Distopia",
        1949,
        "nao_iniciado"
    )

    dados_atualizados = {
        "titulo": "1984 - Edição Atualizada",
        "autor": "George Orwell",
        "isbn": "123",
        "genero": "Distopia",
        "ano": 1949,
        "status_leitura": "lendo",
    }

    livro = service.editar_livro("123", dados_atualizados)

    assert livro.titulo == "1984 - Edição Atualizada"
    assert livro.status_leitura == "lendo"
    assert repo.carregar()[0]["titulo"] == "1984 - Edição Atualizada"


def test_editar_livro_isbn_duplicado(tmp_path):
    repo = LivroRepository(tmp_path / "livros.json")
    service = LivroService(repo)

    service.cadastrar_livro(
        "1984", "George Orwell", "123", "Distopia", 1949, "nao_iniciado"
    )

    service.cadastrar_livro(
        "O Hobbit", "Tolkien", "456", "Fantasia", 1937, "concluido"
    )

    dados_atualizados = {
        "titulo": "1984",
        "autor": "George Orwell",
        "isbn": "456",
        "genero": "Distopia",
        "ano": 1949,
        "status_leitura": "lendo",
    }

    with pytest.raises(ValueError, match="ISBN já cadastrado"):
        service.editar_livro("123", dados_atualizados)


def test_editar_livro_inexistente(tmp_path):
    repo = LivroRepository(tmp_path / "livros.json")
    service = LivroService(repo)

    dados = {
        "titulo": "1984",
        "autor": "George Orwell",
        "isbn": "123",
        "genero": "Distopia",
        "ano": 1949,
        "status_leitura": "lendo",
    }

    with pytest.raises(ValueError, match="Livro não encontrado"):
        service.editar_livro("999", dados)


def test_remover_livro(tmp_path):
    repo = LivroRepository(tmp_path / "livros.json")
    service = LivroService(repo)

    service.cadastrar_livro(
        "1984", "George Orwell", "123", "Distopia", 1949, "nao_iniciado"
    )

    service.remover_livro("123")

    assert repo.carregar() == []


def test_remover_livro_inexistente(tmp_path):
    repo = LivroRepository(tmp_path / "livros.json")
    service = LivroService(repo)

    with pytest.raises(ValueError, match="Livro não encontrado"):
        service.remover_livro("999")


def test_alterar_status_livro_inexistente_mensagem_padronizada(tmp_path):
    repo = LivroRepository(tmp_path / "livros.json")
    service = LivroService(repo)

    with pytest.raises(ValueError, match="Livro não encontrado"):
        service.alterar_status("123", "lendo")