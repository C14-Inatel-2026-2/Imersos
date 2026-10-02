from datetime import date

import pytest

from models.emprestimo import Emprestimo


def test_emprestimo_deve_iniciar_como_nao_emprestado():
    emprestimo = Emprestimo()

    assert emprestimo.emprestado is False
    assert emprestimo.emprestado_para is None
    assert emprestimo.data_emprestimo is None
    assert emprestimo.data_devolucao_prevista is None


def test_deve_criar_emprestimo_valido():
    emprestimo = Emprestimo(
        emprestado=True,
        emprestado_para="Camile",
        data_emprestimo=date(2026, 9, 10),
        data_devolucao_prevista=date(2026, 9, 20),
    )

    assert emprestimo.emprestado is True
    assert emprestimo.emprestado_para == "Camile"
    assert emprestimo.data_emprestimo == date(2026, 9, 10)
    assert emprestimo.data_devolucao_prevista == date(2026, 9, 20)


def test_emprestimo_deve_exigir_nome_da_pessoa():
    with pytest.raises(ValueError, match="É necessário informar"):
        Emprestimo(
            emprestado=True,
            emprestado_para="",
            data_emprestimo=date(2026, 9, 10),
            data_devolucao_prevista=date(2026, 9, 20),
        )


def test_emprestimo_deve_exigir_data_de_emprestimo():
    with pytest.raises(
        ValueError,
        match="A data do empréstimo deve ser informada",
    ):
        Emprestimo(
            emprestado=True,
            emprestado_para="Camile",
            data_emprestimo=None,
            data_devolucao_prevista=date(2026, 9, 20),
        )


def test_emprestimo_deve_exigir_data_de_devolucao():
    with pytest.raises(
        ValueError,
        match="A data prevista de devolução deve ser informada",
    ):
        Emprestimo(
            emprestado=True,
            emprestado_para="Camile",
            data_emprestimo=date(2026, 9, 10),
            data_devolucao_prevista=None,
        )


def test_devolucao_nao_pode_ser_anterior_ao_emprestimo():
    with pytest.raises(ValueError, match="não pode ser anterior"):
        Emprestimo(
            emprestado=True,
            emprestado_para="Camile",
            data_emprestimo=date(2026, 9, 20),
            data_devolucao_prevista=date(2026, 9, 10),
        )


def test_livro_nao_emprestado_nao_deve_ter_dados_de_emprestimo():
    with pytest.raises(ValueError, match="não emprestado"):
        Emprestimo(
            emprestado=False,
            emprestado_para="Camile",
            data_emprestimo=date(2026, 9, 10),
            data_devolucao_prevista=date(2026, 9, 20),
        )