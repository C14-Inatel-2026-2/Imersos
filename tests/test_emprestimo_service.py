
from datetime import date

import pytest

from repository.emprestimo_repository import EmprestimoRepository
from repository.livro_repository import LivroRepository
from services.emprestimo_service import EmprestimoService
from services.livro_service import LivroService


@pytest.fixture
def service(tmp_path):
    livros = LivroRepository(tmp_path / "livros.json")

    livros.salvar([{
        "titulo": "1984",
        "autor": "George Orwell",
        "isbn": "123",
        "genero": "Distopia",
        "ano": 1949,
        "status_leitura": "lendo",
    }])

    emprestimos = EmprestimoRepository(tmp_path / "emprestimos.json")
    return EmprestimoService(livros, emprestimos)


def test_registra_emprestimo_e_persiste(service):
    registro = service.realizar_emprestimo(
        "123", "Ana", date(2026, 11, 20), date(2026, 11, 12)
    )

    assert registro["isbn"] == "123"
    assert registro["emprestado_para"] == "Ana"
    assert service.emprestimo_repository.carregar() == [registro]


def test_rejeita_livro_inexistente(service):
    with pytest.raises(ValueError, match="Livro não encontrado"):
        service.realizar_emprestimo("999", "Ana", date(2026, 11, 20))


def test_rejeita_emprestimo_duplicado(service):
    service.realizar_emprestimo("123", "Ana", date(2026, 11, 20))

    with pytest.raises(ValueError, match="já está emprestado"):
        service.realizar_emprestimo("123", "Bia", date(2026, 11, 22))


def test_rejeita_data_anterior(service):
    with pytest.raises(ValueError, match="não pode ser anterior"):
        service.realizar_emprestimo(
            "123", "Ana", date(2026, 11, 10), date(2026, 11, 12)
        )


def test_lista_somente_atrasados(service):
    service.realizar_emprestimo(
        "123", "Ana", date(2026, 11, 13), date(2026, 11, 10)
    )

    assert len(service.listar_atrasados(date(2026, 11, 14))) == 1
    assert service.listar_atrasados(date(2026, 11, 13)) == []


def test_nao_permite_remover_livro_emprestado(service):
    service.realizar_emprestimo(
        "123", "Ana", date(2026, 11, 20), date(2026, 11, 10)
    )

    livro_service = LivroService(
        service.livro_repository,
        service.emprestimo_repository
    )

    with pytest.raises(ValueError, match="livro emprestado"):
        livro_service.remover_livro("123")

    assert len(service.livro_repository.carregar()) == 1


def test_nao_permite_alterar_isbn_de_livro_emprestado(service):
    service.realizar_emprestimo(
        "123", "Ana", date(2026, 11, 20), date(2026, 11, 10)
    )

    livro_service = LivroService(
        service.livro_repository,
        service.emprestimo_repository
    )

    dados = service.livro_repository.carregar()[0].copy()
    dados["isbn"] = "456"

    with pytest.raises(ValueError, match="ISBN de um livro emprestado"):
        livro_service.editar_livro("123", dados)

    assert service.livro_repository.carregar()[0]["isbn"] == "123"


def test_permite_editar_titulo_de_livro_emprestado(service):
    service.realizar_emprestimo(
        "123", "Ana", date(2026, 11, 20), date(2026, 11, 10)
    )

    livro_service = LivroService(
        service.livro_repository,
        service.emprestimo_repository
    )

    dados = service.livro_repository.carregar()[0].copy()
    dados["titulo"] = "1984 - Nova Edição"

    livro_service.editar_livro("123", dados)

    assert (
        service.livro_repository.carregar()[0]["titulo"]
        == "1984 - Nova Edição"
    )


def test_consultar_emprestimo_persistido(service):
    registro = service.realizar_emprestimo(
        "123",
        "Ana",
        date(2026, 11, 20),
        date(2026, 11, 13)
    )

    outro_repositorio = EmprestimoRepository(
        service.emprestimo_repository.caminho_arquivo
    )

    outro_service = EmprestimoService(
        service.livro_repository,
        outro_repositorio
    )

    assert outro_service.consultar_emprestimo("123") == registro
    assert outro_service.consultar_emprestimo("999") is None


def test_disponibilidade_antes_e_depois_do_emprestimo(service):
    assert service.verificar_disponibilidade(" 123 ") is True

    service.realizar_emprestimo(
        "123",
        "Ana",
        date(2026, 11, 20),
        date(2026, 11, 13)
    )

    with pytest.raises(ValueError, match="já está emprestado"):
        service.verificar_disponibilidade(" 123 ")


def test_registro_emprestimo_preserva_formato_json(service):
    registro = service.realizar_emprestimo(
        "123",
        "Ana",
        date(2026, 11, 20),
        date(2026, 11, 13)
    )

    assert registro == {
        "isbn": "123",
        "emprestado_para": "Ana",
        "data_emprestimo": "2026-11-13",
        "data_devolucao_prevista": "2026-11-20",
    }

    assert service.emprestimo_repository.carregar() == [registro]
