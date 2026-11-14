import json

import pytest

from repository.emprestimo_repository import EmprestimoRepository
from repository.livro_repository import LivroRepository
from services.livro_service import LivroService


@pytest.fixture
def ambiente_web(monkeypatch, tmp_path):
    monkeypatch.setenv(
        "SECRET_KEY",
        "chave-exclusiva-para-testes"
    )

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

    monkeypatch.setattr(
        modulo_web,
        "service",
        servico
    )

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


def carregar_json_livros(servico):
    caminho = servico.repository.caminho_arquivo

    if not caminho.exists():
        return []

    with open(
        caminho,
        "r",
        encoding="utf-8"
    ) as arquivo:
        return json.load(arquivo)


def cadastrar(
    servico,
    isbn,
    titulo,
    status="nao_iniciado"
):
    servico.cadastrar_livro(
        titulo=titulo,
        autor="Autor de Teste",
        isbn=isbn,
        genero="Romance",
        ano=2020,
        status_leitura=status,
    )


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

    livros_salvos = carregar_json_livros(servico)

    assert len(livros_salvos) == 1

    assert livros_salvos[0] == {
        "titulo": "Livro de Teste",
        "autor": "Autor de Teste",
        "isbn": "123456789",
        "genero": "Romance",
        "ano": 2020,
        "status_leitura": "nao_iniciado",
    }


def test_cadastro_com_ano_invalido(ambiente_web):
    cliente, servico, _ = ambiente_web

    dados = dados_livro()
    dados["ano"] = "abc"

    resposta = cliente.post(
        "/cadastrar",
        data=dados
    )

    assert resposta.status_code == 400
    assert carregar_json_livros(servico) == []


def test_dados_invalidos_nao_modificam_json(
    ambiente_web
):
    cliente, servico, _ = ambiente_web

    resposta = cliente.post(
        "/cadastrar",
        data=dados_livro()
    )

    assert resposta.status_code == 302

    dados_antes = carregar_json_livros(
        servico
    )

    dados_invalidos = dados_livro()
    dados_invalidos["isbn"] = "999999999"
    dados_invalidos["titulo"] = ""

    resposta = cliente.post(
        "/cadastrar",
        data=dados_invalidos
    )

    dados_depois = carregar_json_livros(
        servico
    )

    assert resposta.status_code == 400
    assert dados_depois == dados_antes


def test_editar_livro(ambiente_web):
    cliente, servico, _ = ambiente_web

    servico.cadastrar_livro(
        **{
            **dados_livro(),
            "ano": 2020
        }
    )

    dados = dados_livro()
    dados["titulo"] = "Livro Atualizado"

    resposta = cliente.post(
        "/livros/123456789/editar",
        data=dados
    )

    assert resposta.status_code == 302

    livros_salvos = carregar_json_livros(
        servico
    )

    assert (
        livros_salvos[0]["titulo"]
        == "Livro Atualizado"
    )


def test_edicao_parcial_preserva_campos(
    ambiente_web
):
    cliente, servico, _ = ambiente_web

    cliente.post(
        "/cadastrar",
        data=dados_livro()
    )

    resposta = cliente.post(
        "/livros/123456789/editar",
        data={
            "titulo": "Livro Atualizado"
        }
    )

    assert resposta.status_code == 302

    livros_salvos = carregar_json_livros(
        servico
    )

    assert len(livros_salvos) == 1

    livro = livros_salvos[0]

    assert livro["titulo"] == "Livro Atualizado"
    assert livro["autor"] == "Autor de Teste"
    assert livro["isbn"] == "123456789"
    assert livro["genero"] == "Romance"
    assert livro["ano"] == 2020
    assert (
        livro["status_leitura"]
        == "nao_iniciado"
    )


def test_remover_livro(ambiente_web):
    cliente, servico, _ = ambiente_web

    cliente.post(
        "/cadastrar",
        data=dados_livro()
    )

    assert len(
        carregar_json_livros(servico)
    ) == 1

    resposta = cliente.post(
        "/livros/123456789/remover"
    )

    assert resposta.status_code == 302
    assert carregar_json_livros(servico) == []


def test_bloquear_remocao_livro_emprestado(
    ambiente_web
):
    cliente, servico, _ = ambiente_web

    servico.cadastrar_livro(
        **{
            **dados_livro(),
            "ano": 2020
        }
    )

    servico.emprestimo_repository.salvar([
        {
            "isbn": "123456789"
        }
    ])

    resposta = cliente.post(
        "/livros/123456789/remover"
    )

    assert resposta.status_code == 302
    assert len(
        servico.listar_livros()
    ) == 1


def test_rejeitar_post_sem_csrf(
    ambiente_web
):
    cliente, servico, aplicacao = ambiente_web

    aplicacao.config[
        "WTF_CSRF_ENABLED"
    ] = True

    resposta = cliente.post(
        "/cadastrar",
        data=dados_livro()
    )

    assert resposta.status_code == 302
    assert servico.listar_livros() == []


def test_alterar_status_livro(
    ambiente_web
):
    cliente, servico, _ = ambiente_web

    cadastrar(
        servico,
        "111",
        "Livro A"
    )

    resposta = cliente.post(
        "/livros/111/status",
        data={
            "status_leitura": "lendo"
        }
    )

    assert resposta.status_code == 302

    assert (
        servico
        .listar_livros()[0]
        .status_leitura
        == "lendo"
    )


def test_alterar_status_invalido_nao_altera_livro(
    ambiente_web
):
    cliente, servico, _ = ambiente_web

    cadastrar(
        servico,
        "111",
        "Livro A"
    )

    resposta = cliente.post(
        "/livros/111/status",
        data={
            "status_leitura": "abandonado"
        },
        follow_redirects=True
    )

    assert (
        "Status de leitura invalido"
        in resposta.get_data(as_text=True)
    )

    assert (
        servico
        .listar_livros()[0]
        .status_leitura
        == "nao_iniciado"
    )


def test_alterar_status_livro_inexistente(
    ambiente_web
):
    cliente, _, _ = ambiente_web

    resposta = cliente.post(
        "/livros/999/status",
        data={
            "status_leitura": "lendo"
        },
        follow_redirects=True
    )

    assert (
        "Livro não encontrado"
        in resposta.get_data(as_text=True)
    )


def test_filtrar_por_status(ambiente_web):
    cliente, servico, _ = ambiente_web

    cadastrar(
        servico,
        "111",
        "Livro A",
        "lendo"
    )

    cadastrar(
        servico,
        "222",
        "Livro B",
        "concluido"
    )

    resposta = cliente.get(
        "/livros?status=lendo"
    )

    html = resposta.get_data(
        as_text=True
    )

    assert resposta.status_code == 200
    assert "Livro A" in html
    assert "Livro B" not in html


def test_filtrar_por_status_invalido(
    ambiente_web
):
    cliente, servico, _ = ambiente_web

    cadastrar(
        servico,
        "111",
        "Livro A"
    )

    resposta = cliente.get(
        "/livros?status=abandonado"
    )

    html = resposta.get_data(
        as_text=True
    )

    assert (
        "Status de leitura invalido"
        in html
    )

    assert "Livro A" not in html


def test_busca_combinada_com_filtro_de_status(
    ambiente_web
):
    cliente, servico, _ = ambiente_web

    cadastrar(
        servico,
        "111",
        "Duna",
        "lendo"
    )

    cadastrar(
        servico,
        "222",
        "Duna Messias",
        "concluido"
    )

    cadastrar(
        servico,
        "333",
        "Outro",
        "lendo"
    )

    resposta = cliente.get(
        "/livros"
        "?termo=duna"
        "&campo=titulo"
        "&status=lendo"
    )

    html = resposta.get_data(
        as_text=True
    )

    assert "Duna" in html
    assert "Duna Messias" not in html
    assert "Outro" not in html


def test_buscar_livros_por_titulo(
    ambiente_web
):
    cliente, servico, _ = ambiente_web

    cadastrar(
        servico,
        "111",
        "Livro A"
    )

    cadastrar(
        servico,
        "222",
        "Outro"
    )

    resposta = cliente.get(
        "/livros?termo=livro&campo=titulo"
    )

    html = resposta.get_data(
        as_text=True
    )

    assert "Livro A" in html
    assert "Outro" not in html


def test_busca_com_termo_vazio(
    ambiente_web
):
    cliente, _, _ = ambiente_web

    resposta = cliente.get(
        "/livros?termo=&campo=titulo"
    )

    assert (
        "Informe um termo"
        in resposta.get_data(as_text=True)
    )


def test_busca_com_campo_invalido(
    ambiente_web
):
    cliente, _, _ = ambiente_web

    resposta = cliente.get(
        "/livros?termo=x&campo=isbn"
    )

    assert (
        "Campo de busca invalido"
        in resposta.get_data(as_text=True)
    )


def test_health(ambiente_web):
    cliente, _, _ = ambiente_web

    resposta = cliente.get("/health")

    assert resposta.status_code == 200
    assert resposta.json["status"] == "online"


def test_edicao_sem_dados_nao_altera_livro(
    ambiente_web
):
    cliente, servico, _ = ambiente_web

    cliente.post(
        "/cadastrar",
        data=dados_livro()
    )

    dados_antes = carregar_json_livros(
        servico
    )

    resposta = cliente.post(
        "/livros/123456789/editar",
        data={}
    )

    dados_depois = carregar_json_livros(
        servico
    )

    assert resposta.status_code == 400
    assert dados_depois == dados_antes
    assert (
        "Nenhum dado informado para edição."
        in resposta.get_data(as_text=True)
    )

def test_abrir_formulario_edicao(ambiente_web):
    cliente, servico, _ = ambiente_web

    cadastrar(servico, "123", "Duna")

    resposta = cliente.get("/livros/123/editar")

    assert resposta.status_code == 200
    assert "Duna" in resposta.get_data(as_text=True)