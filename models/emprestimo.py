from dataclasses import dataclass
from datetime import date


@dataclass
class Emprestimo:
    emprestado: bool = False
    emprestado_para: str | None = None
    data_emprestimo: date | None = None
    data_devolucao_prevista: date | None = None

    def __post_init__(self):
        self._validar()

    def _validar(self):
        if not self.emprestado:
            if any([
                self.emprestado_para,
                self.data_emprestimo,
                self.data_devolucao_prevista
            ]):
                raise ValueError(
                    "Um livro não emprestado não deve possuir dados de empréstimo."
                )

            return

        if not self.emprestado_para or not self.emprestado_para.strip():
            raise ValueError(
                "É necessário informar para quem o livro foi emprestado."
            )

        if self.data_emprestimo is None:
            raise ValueError(
                "A data do empréstimo deve ser informada."
            )

        if self.data_devolucao_prevista is None:
            raise ValueError(
                "A data prevista de devolução deve ser informada."
            )

        if self.data_devolucao_prevista < self.data_emprestimo:
            raise ValueError(
                "A data prevista de devolução não pode ser anterior "
                "à data do empréstimo."
            )