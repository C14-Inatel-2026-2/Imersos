
import json
from pathlib import Path


class EmprestimoRepository:
    """Armazena os empréstimos ativos em um arquivo JSON."""

    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = Path(caminho_arquivo)

    def carregar(self):
        if not self.caminho_arquivo.exists():
            return []

        try:
            with self.caminho_arquivo.open(encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except json.JSONDecodeError:
            return []

    def salvar(self, emprestimos):
        self.caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
        with self.caminho_arquivo.open("w", encoding="utf-8") as arquivo:
            json.dump(emprestimos, arquivo, ensure_ascii=False, indent=4)
