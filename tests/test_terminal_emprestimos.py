
from datetime import date

from terminal.app import (
    realizar_emprestimo,
    realizar_devolucao,
    listar_emprestimos_atrasados,
)


def test_menu_realizar_emprestimo(mocker, capsys):
    service = mocker.Mock()

    mocker.patch(
        "builtins.input",
        side_effect=[
            "123",
            "Ana",
            "20-11-2026",
            "s"
        ]
    )

    realizar_emprestimo(service)

    service.realizar_emprestimo.assert_called_once_with(
        "123", "Ana", date(2026, 11, 20)
    )

    assert "sucesso" in capsys.readouterr().out


def test_menu_listar_atrasados(mocker, capsys):
    service = mocker.Mock()

    service.listar_atrasados.return_value = [{
        "isbn": "123",
        "titulo": "1984",
        "emprestado_para": "Ana",
        "data_devolucao_prevista": "2026-11-13",
    }]

    listar_emprestimos_atrasados(service)

    saida = capsys.readouterr().out

    assert "1984" in saida
    assert "Ana" in saida
    assert "13-11-2026" in saida


def test_menu_realizar_devolucao(mocker, capsys):
    service = mocker.Mock()

    service.consultar_emprestimo.return_value = {
        "isbn": "123",
        "emprestado_para": "Ana",
        "data_devolucao_prevista": "2026-11-20",
    }

    mocker.patch(
        "builtins.input",
        side_effect=["123", "s"]
    )

    realizar_devolucao(service)

    service.realizar_devolucao.assert_called_once_with(
        "123"
    )

    assert (
        "Devolução registrada com sucesso!"
        in capsys.readouterr().out
    )

def test_cancelar_emprestimo(mocker):
    service = mocker.Mock()

    mocker.patch(
        "builtins.input",
        side_effect=[
            "123",
            "Ana",
            "20-11-2026",
            "n"
        ]
    )

    realizar_emprestimo(service)

    service.realizar_emprestimo.assert_not_called()


def test_cancelar_devolucao(mocker):
    service = mocker.Mock()

    service.consultar_emprestimo.return_value = {
        "isbn": "123",
        "emprestado_para": "Ana",
        "data_devolucao_prevista": "2026-11-20",
    }

    mocker.patch(
        "builtins.input",
        side_effect=["123", "n"]
    )

    realizar_devolucao(service)

    service.realizar_devolucao.assert_not_called()


def test_menu_informa_quando_nao_ha_atrasados(mocker, capsys):
    service = mocker.Mock()
    service.listar_atrasados.return_value = []

    listar_emprestimos_atrasados(service)

    assert (
        "Nenhum empréstimo atrasado."
        in capsys.readouterr().out
    )
