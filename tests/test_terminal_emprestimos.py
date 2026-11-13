
from datetime import date

from terminal.app import (
    realizar_emprestimo,
    listar_emprestimos_atrasados,
)

from terminal.app import (
    realizar_emprestimo,
    realizar_devolucao,
    listar_emprestimos_atrasados,
)


def test_menu_realizar_emprestimo(mocker, capsys):
    service = mocker.Mock()

    mocker.patch(
        "builtins.input",
        side_effect=["123", "Ana", "20-11-2026"]
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
        "emprestado_para": "Ana",
        "data_devolucao_prevista": "20-11-2026",
    }]

    listar_emprestimos_atrasados(service)

    assert "123" in capsys.readouterr().out

def test_menu_realizar_devolucao(mocker, capsys):
    service = mocker.Mock()

    mocker.patch(
        "builtins.input",
        return_value="123"
    )

    realizar_devolucao(service)

    service.realizar_devolucao.assert_called_once_with("123")

    assert "Devolução registrada com sucesso!" in capsys.readouterr().out