import pytest

from repository.livro_repository import LivroRepository
from repository.emprestimo_repository import EmprestimoRepository
from services.livro_service import LivroService


@pytest.fixture
def ambiente_web(monkeypatch, tmp_path):
    monkeypatch.setenv("SECRET_KEY", "chave-exclusiva-para-testes")

    import app as modulo_web

    repositorio_livros = LivroRepository(
        tmp_path / "livros.json"
    )
    repositorio_emprestimos = EmprestimoRepository(
        tmp_path / "emprestimos.json"
    )

    servico = LivroService(
        repositorio_livros,
        repositorio_emprestimos
    )

    monkeypatch.setattr(modulo_web, "service", servico)

    modulo_web.app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False
    )

    with modulo_web.app.test_client() as cliente:
        yield cliente, servico, modulo_web.app


def dados_livro():
    return {
        "titulo": "Livro de Teste",
        "autor": "Autor de Teste",
        "isbn": "123456789",
        "genero": "Romance",
        "ano": "2020",
        "status_leitura": "nao_iniciado",
    }


def test_pagina_inicial(ambiente_web):
    cliente, _, _ = ambiente_web

    resposta = cliente.get("/")

    assert resposta.status_code == 200
    assert b"Imersos" in resposta.data


def test_listar_livros(ambiente_web):
    cliente, _, _ = ambiente_web

    resposta = cliente.get("/livros")

    assert resposta.status_code == 200


def test_cadastrar_livro(ambiente_web):
    cliente, servico, _ = ambiente_web

    resposta = cliente.post(
        "/cadastrar",
        data=dados_livro()
    )

    assert resposta.status_code == 302
    assert len(servico.listar_livros()) == 1
    assert servico.listar_livros()[0].titulo == "Livro de Teste"


def test_cadastro_com_ano_invalido(ambiente_web):
    cliente, servico, _ = ambiente_web

    dados = dados_livro()
    dados["ano"] = "abc"

    resposta = cliente.post("/cadastrar", data=dados)

    assert resposta.status_code == 400
    assert servico.listar_livros() == []


def test_editar_livro(ambiente_web):
    cliente, servico, _ = ambiente_web

    servico.cadastrar_livro(
        **{**dados_livro(), "ano": 2020}
    )

    dados = dados_livro()
    dados["titulo"] = "Livro Atualizado"

    resposta = cliente.post(
        "/livros/123456789/editar",
        data=dados
    )

    assert resposta.status_code == 302
    assert servico.listar_livros()[0].titulo == "Livro Atualizado"


def test_remover_livro(ambiente_web):
    cliente, servico, _ = ambiente_web

    servico.cadastrar_livro(
        **{**dados_livro(), "ano": 2020}
    )

    resposta = cliente.post("/livros/123456789/remover")

    assert resposta.status_code == 302
    assert servico.listar_livros() == []


def test_bloquear_remocao_livro_emprestado(ambiente_web):
    cliente, servico, _ = ambiente_web

    servico.cadastrar_livro(
        **{**dados_livro(), "ano": 2020}
    )

    servico.emprestimo_repository.salvar([
        {"isbn": "123456789"}
    ])

    resposta = cliente.post("/livros/123456789/remover")

    assert resposta.status_code == 302
    assert len(servico.listar_livros()) == 1


def test_rejeitar_post_sem_csrf(ambiente_web):
    cliente, servico, aplicacao = ambiente_web

    aplicacao.config["WTF_CSRF_ENABLED"] = True

    resposta = cliente.post(
        "/cadastrar",
        data=dados_livro()
    )

    assert resposta.status_code == 302
    assert servico.listar_livros() == []
