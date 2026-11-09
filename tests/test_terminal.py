
from terminal.app import ler_opcao, ler_dados_livro, mostrar_menu, converter_status, executar
import pytest

def test_ler_opcao(mocker):
    mocker.patch(
        "builtins.input",
        return_value="1",
    )

    opcao = ler_opcao()

    assert opcao == "1"

def test_ler_dados_livro(mocker):
    mocker.patch(
        "builtins.input",
        side_effect=[
            "1984",
            "George Orwell",
            "9780451524935",
            "Distopia",
            "1949",
            "2",
        ],
    )

    dados = ler_dados_livro()

    assert dados["titulo"] == "1984"
    assert dados["autor"] == "George Orwell"
    assert dados["isbn"] == "9780451524935"
    assert dados["genero"] == "Distopia"
    assert dados["ano"] == 1949
    assert dados["status_leitura"] == "lendo"


def test_mostrar_menu(capsys):
    mostrar_menu()

    saida = capsys.readouterr().out

    assert "Cadastrar livro" in saida
    assert "Buscar livro" in saida
    assert "Realizar empréstimo" in saida

def test_converter_status():
    status = converter_status("2")

    assert status == "lendo"


def test_status_invalido():
    with pytest.raises(
        ValueError,
        match="Status de leitura inválido",
    ):
        converter_status("9")

def test_menu_exibe_todas_opcoes(capsys):
    mostrar_menu()

    saida = capsys.readouterr().out

    opcoes = [
        "1 - Cadastrar livro",
        "2 - Buscar livro",
        "3 - Editar livro",
        "4 - Remover livro",
        "5 - Realizar empréstimo",
        "6 - Realizar devolução",
        "7 - Listar empréstimos atrasados",
        "0 - Sair",
    ]

    for opcao in opcoes:
        assert opcao in saida

def test_opcao_invalida_retorna_menu(mocker, capsys):
    mocker.patch(
        "builtins.input",
        side_effect=["99", "abc", "0"],
    )

    executar()

    saida = capsys.readouterr().out

    assert saida.count("Opção inválida!") == 2

    assert saida.count("=== Biblioteca Imersos ===") == 3

    assert "Encerrando sistema..." in saida
