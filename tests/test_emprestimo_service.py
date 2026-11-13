
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

def test_devolucao_remove_emprestimo_ativo(service):
    service.realizar_emprestimo(
        "123",
        "Ana",
        date(2026, 11, 20),
        date(2026, 11, 13)
    )

    devolvido = service.realizar_devolucao("123")

    assert devolvido["isbn"] == "123"
    assert devolvido["emprestado_para"] == "Ana"
    assert service.consultar_emprestimo("123") is None
    assert service.emprestimo_repository.carregar() == []


def test_devolucao_livro_nao_emprestado_nao_altera_dados(service):
    dados_anteriores = service.emprestimo_repository.carregar()

    with pytest.raises(
        ValueError,
        match="Livro não está emprestado"
    ):
        service.realizar_devolucao("123")

    assert service.emprestimo_repository.carregar() == dados_anteriores


def test_devolucao_isbn_inexistente_nao_altera_dados(service):
    dados_anteriores = service.emprestimo_repository.carregar()

    with pytest.raises(
        ValueError,
        match="Livro não encontrado"
    ):
        service.realizar_devolucao("999")

    assert service.emprestimo_repository.carregar() == dados_anteriores


def test_permite_emprestar_novamente_apos_devolucao(service):
    service.realizar_emprestimo(
        "123",
        "Ana",
        date(2026, 11, 20),
        date(2026, 11, 13)
    )

    service.realizar_devolucao("123")

    novo_emprestimo = service.realizar_emprestimo(
        "123",
        "Bia",
        date(2026, 11, 30),
        date(2026, 11, 21)
    )

    assert novo_emprestimo["isbn"] == "123"
    assert novo_emprestimo["emprestado_para"] == "Bia"
    assert service.consultar_emprestimo("123") == novo_emprestimo

def test_permite_remover_livro_apos_devolucao(service):
    service.realizar_emprestimo(
        "123",
        "Ana",
        date(2026, 11, 20),
        date(2026, 11, 13)
    )

    service.realizar_devolucao("123")

    livro_service = LivroService(
        service.livro_repository,
        service.emprestimo_repository
    )

    livro_service.remover_livro("123")

    assert service.livro_repository.carregar() == []    