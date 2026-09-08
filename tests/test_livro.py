import pytest

from models.livro import Livro


def test_criar_livro():
    livro = Livro(
        "1984",
        "George Orwell",
        "9780451524935",
        "Distopia",
        1949,
        "lendo"
    )

    assert livro.titulo == "1984"
    assert livro.autor == "George Orwell"
    assert livro.isbn == "9780451524935"
    assert livro.genero == "Distopia"
    assert livro.ano == 1949
    assert livro.status_leitura == "lendo"


def test_titulo_vazio():
    with pytest.raises(ValueError):
        Livro(
            "",
            "George Orwell",
            "9780451524935",
            "Distopia",
            1949,
            "lendo"
        )


def test_status_invalido():
    with pytest.raises(ValueError):
        Livro(
            "1984",
            "George Orwell",
            "9780451524935",
            "Distopia",
            1949,
            "abandonado"
        )