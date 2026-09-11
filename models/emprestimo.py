from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Emprestimo:
    livro_titulo: str
    pessoa: str
    data_emprestimo: date
    data_devolucao_prevista: date

    def __post_init__(self):
        if not self.pessoa:
            raise ValueError("O nome da pessoa nao pode estar vazio!")
        if self.data_devolucao_prevista < self.data_emprestimo:
            raise ValueError("Data de devolucao nao pode ser anterior a data de emprestimo!")