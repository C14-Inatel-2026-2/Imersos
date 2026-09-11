from terminal.app import ler_opcao, ler_dados_livro, mostrar_menu
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


def test_status_invalido(mocker):
    mocker.patch(
        "builtins.input",
        side_effect=[
            "1984",
            "George Orwell",
            "9780451524935",
            "Distopia",
            "1949",
            "9",
        ],
    )

    with pytest.raises(ValueError):
        ler_dados_livro()
